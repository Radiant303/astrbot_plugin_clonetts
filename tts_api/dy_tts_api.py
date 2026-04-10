import base64
import json
import uuid

import aiohttp

from astrbot.api import logger

from ..utils.mp3_base64_to_wav_base64 import mp3_base64_to_wav_base64
# python version: ==3.11


async def tts_http_stream(self, text,context_texts):
    headers = {
        "X-Api-App-Id": self.appid,
        "X-Api-Access-Key": self.access_token,
        "X-Api-Resource-Id": "seed-icl-2.0",
        "Content-Type": "application/json",
        "Connection": "keep-alive",
    }
    ctx_list = []
    if context_texts:
        if isinstance(context_texts, str):
            ctx_list = [context_texts]
        elif isinstance(context_texts, list):
            ctx_list = context_texts
        else:
            logger.warning(f"Invalid context_texts type: {type(context_texts)}, expected str or list.")

    additions_payload = {
            "explicit_language": "zh-cn",
            "disable_markdown_filter": True,
            "enable_latex_tn": True,
        }
    if ctx_list:
        additions_payload["context_texts"] = ctx_list
    additions_json_str = json.dumps(additions_payload, ensure_ascii=False)
    params = {
        "user": {
            "uid": f"{uuid.uuid4()}",
        },
        "req_params": {
            "text": text,
            "speaker": self.voice_type,
            "audio_params": {
                "format": "mp3",
                "sample_rate": self.sample_rate,
                "enable_timestamp": True,
                "speech_rate": self.speed_ratio,
                "loudness_rate": self.loudness_rate,
            },
            "additions":additions_json_str,
        },
    }

    async with aiohttp.ClientSession() as session:
        url = "https://openspeech.bytedance.com/api/v3/tts/unidirectional/sse"
        try:
            async with session.post(url, headers=headers, json=params) as response:
                if response.status != 200:
                    resp_text = await response.text()
                    logger.error(f"获取TTS失败: {response.status}, 详情: {resp_text}")
                    return None

                # 处理 SSE stream
                audio_data = bytearray()
                debug_count = 0 # 用于限制日志数量，防止刷屏
                async for line in response.content:
                    if debug_count < 5:
                        logger.debug(f"Raw SSE Line: {repr(line)}")
                        debug_count += 1
                    if line:
                        line_str = line.decode("utf-8").strip()
                        if not line_str or not line_str.startswith("data:"):
                            continue

                        try:
                            data_str = line_str[len("data: "):]
                            if data_str:
                                data = json.loads(data_str)
                                if (
                                    data.get("code") == 0
                                    and "data" in data
                                    and data["data"]
                                ):
                                    chunk_audio = base64.b64decode(data["data"])
                                    audio_data.extend(chunk_audio)
                                elif data.get("code", 0) == 20000000:
                                    logger.info("语音合成完毕")
                                    break
                        except json.JSONDecodeError:
                            logger.error(
                                f"JSON decoding error in SSE response: {line_str}"
                            )
                            continue

                # 返回base64编码数据
                if not audio_data:
                    logger.warning(f"流结束但未收到任何音频数据:{audio_data}")
                    return None

                try:
                    base64_audio_data = base64.b64encode(audio_data).decode("utf-8")
                    base64_audio_data_wav = mp3_base64_to_wav_base64(base64_audio_data)
                    return base64_audio_data_wav
                except Exception as e:
                    logger.error(f"Base64 encoding failed: {e}")

        except Exception as e:
            logger.error(f"Request failed: {e}")
