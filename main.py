import base64
import json
import random
import uuid

import requests

import astrbot.api.message_components as Comp
from astrbot.api import logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star, register
from astrbot.core.config import AstrBotConfig


@register(
    "astrbot_plugin_clonetts",
    "Radiant303",
    "基于火山引擎音色克隆(ICL)的文本转语音插件",
    "1.0.0",
)
class CloneTTSPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)

        # --- 配置读取与防御性校验 ---
        self.enable_tts = bool(config.get("enable_tts", False))

        # 概率 & 长度：强制转为数值并限制在合理范围
        try:
            self.tts_probability = max(
                0, min(100, float(config.get("tts_probability", 100)))
            )
        except (TypeError, ValueError):
            logger.warning("tts_probability 配置值无效，已使用默认值 100")
            self.tts_probability = 100

        try:
            self.max_length = max(1, int(config.get("max_length", 50)))
        except (TypeError, ValueError):
            logger.warning("max_length 配置值无效，已使用默认值 50")
            self.max_length = 50

        try:
            self.min_length = max(1, int(config.get("min_length", 5)))
        except (TypeError, ValueError):
            logger.warning("min_length 配置值无效，已使用默认值 5")
            self.min_length = 5

        # 凭证类字段：确保为非空字符串
        self.appid = str(config.get("appid") or "")
        self.access_token = str(config.get("access_token") or "")
        self.cluster = str(config.get("cluster") or "volcano_icl")
        self.voice_type = str(config.get("voice_type") or "")
        self.uid = str(config.get("uid") or "388808087185088")

        # 音频参数
        try:
            self.speed_ratio = max(0.5, min(2.0, float(config.get("speed_ratio", 1.0))))
        except (TypeError, ValueError):
            self.speed_ratio = 1.0

        try:
            self.volume_ratio = max(
                0.5, min(2.0, float(config.get("volume_ratio", 1.0)))
            )
        except (TypeError, ValueError):
            self.volume_ratio = 1.0

        try:
            self.pitch_ratio = max(0.5, min(2.0, float(config.get("pitch_ratio", 1.0))))
        except (TypeError, ValueError):
            self.pitch_ratio = 1.0

        # API 相关
        self.api_url = str(
            config.get("url") or "https://openspeech.bytedance.com/api/v1/tts"
        )

        # 启动时预检关键配置
        missing = [
            name
            for name, val in [
                ("appid", self.appid),
                ("access_token", self.access_token),
                ("voice_type", self.voice_type),
            ]
            if not val
        ]
        if missing and self.enable_tts:
            logger.warning(
                f"CloneTTS 以下必要配置为空，语音合成可能失败: {', '.join(missing)}"
            )

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
        logger.info("CloneTTS plugin 已经启用")

    @filter.on_decorating_result()
    async def on_decorating_result(self, event: AstrMessageEvent):
        try:
            if not self.enable_tts:
                return

            if not self.probability(self.tts_probability):
                logger.debug("本次消息未命中 TTS 概率，跳过语音合成")
                return

            result = event.get_result()
            if not result or not result.chain:
                return

            text_parts = []
            for component in result.chain:
                if hasattr(component, "text"):
                    text_parts.append(component.text)

            if not text_parts:
                return

            llm_text = "".join(text_parts).strip()

            if len(llm_text) < 1:
                logger.debug("LLM 文本为空，跳过语音合成")
                return

            if len(llm_text) > self.max_length:
                logger.debug(
                    f"LLM 文本长度 {len(llm_text)} 超过上限 {self.max_length}，跳过语音合成"
                )
                return

            if len(llm_text) < self.min_length:
                logger.debug(
                    f"LLM 文本长度 {len(llm_text)} 小于下限 {self.min_length}，跳过语音合成"
                )
                return

            logger.info(f"正在合成克隆语音: {llm_text}")
            audio_b64 = await self.tts_synthesize(llm_text)

            if not audio_b64:
                logger.warning("语音合成返回空数据，跳过本次语音回复")
                return

            result = event.get_result()
            if result is None:
                logger.warning("合成完成但 event result 已失效，跳过")
                return
            result.chain = [Comp.Record.fromBase64(audio_b64)]
        except Exception as e:
            logger.error(f"Error in on_decorating_result: {e}")

    def probability(self, percent) -> bool:
        """以给定百分比概率返回 True（0 = 永不触发，100 = 必定触发）。"""
        try:
            p = float(percent)
        except (TypeError, ValueError):
            return False
        p = max(0.0, min(100.0, p))
        return random.random() < (p / 100)

    async def tts_synthesize(self, text: str) -> str:
        """
        使用火山引擎 v1 音色克隆 API 进行文本转语音合成。

        Args:
            text: 要合成的文本内容

        Returns:
            str: 合成的音频 base64 编码字符串，失败时返回空字符串
        """
        # 输入文本校验
        if not isinstance(text, str) or not text.strip():
            logger.warning("tts_synthesize 收到无效文本，已跳过")
            return ""

        # 运行时凭证校验
        required_fields = {
            "appid": self.appid,
            "access_token": self.access_token,
            "voice_type": self.voice_type,
        }
        missing = [k for k, v in required_fields.items() if not v]
        if missing:
            raise RuntimeError(f"CloneTTS 缺少必要配置项: {', '.join(missing)}")

        header = {"Authorization": f"Bearer;{self.access_token}"}

        request_json = {
            "app": {
                "appid": self.appid,
                "token": "access_token",
                "cluster": self.cluster,
            },
            "user": {"uid": self.uid},
            "audio": {
                "voice_type": self.voice_type,
                "encoding": "mp3",
                "speed_ratio": self.speed_ratio,
                "volume_ratio": self.volume_ratio,
                "pitch_ratio": self.pitch_ratio,
            },
            "request": {
                "reqid": str(uuid.uuid4()),
                "text": text,
                "text_type": "plain",
                "operation": "query",
                "with_frontend": 1,
                "frontend_type": "unitTson",
            },
        }

        try:
            resp = requests.post(
                self.api_url, json.dumps(request_json), headers=header, timeout=30
            )

            resp_json = resp.json()
            logger.debug(f"CloneTTS API 响应状态码: {resp.status_code}")

            if resp.status_code != 200:
                raise RuntimeError(
                    f"CloneTTS HTTP 错误: status={resp.status_code}, body={resp_json}"
                )

            # 检查业务状态码
            code = resp_json.get("code", -1)
            if code != 3000:
                message = resp_json.get("message", "未知错误")
                raise RuntimeError(
                    f"CloneTTS 服务返回错误: code={code}, message={message}"
                )

            data = resp_json.get("data")
            if not data:
                logger.warning("CloneTTS 响应中无音频数据")
                return ""

            # 验证 base64 数据有效性
            try:
                base64.b64decode(data)
            except Exception:
                logger.warning("CloneTTS 返回的 base64 数据无效")
                return ""

            return data

        except requests.RequestException as e:
            raise RuntimeError(f"CloneTTS 请求失败: {e}") from e
        except json.JSONDecodeError as e:
            raise RuntimeError(f"CloneTTS 响应 JSON 解析失败: {e}") from e

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
        logger.info("CloneTTS plugin 已经停用/卸载")
