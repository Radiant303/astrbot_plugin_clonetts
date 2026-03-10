import base64
import json
import uuid

import aiohttp

from astrbot.api import logger

# python version: ==3.11


async def tts_http_stream(self, text):
    headers = {
        "X-Api-App-Id": self.appid,
        "X-Api-Access-Key": self.access_token,
        "X-Api-Resource-Id": "seed-icl-2.0",
        "Content-Type": "application/json",
        "Connection": "keep-alive",
    }

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
            "additions": '{"explicit_language":"zh-cn","disable_markdown_filter":true, "enable_latex_tn":true}',
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
                async for line in response.content:
                    if line:
                        line_str = line.decode("utf-8").strip()
                        if not line_str or not line_str.startswith("data:"):
                            continue

                        try:
                            data_str = line_str[5:].strip()  # 安全截取并去空
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
                    logger.warning("流结束但未收到任何音频数据")
                    return None

                try:
                    base64_audio_data = base64.b64encode(audio_data).decode("utf-8")
                    return base64_audio_data
                except Exception as e:
                    logger.error(f"Base64 encoding failed: {e}")

        except Exception as e:
            logger.error(f"Request failed: {e}")
