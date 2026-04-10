# 🎙️ 克隆语音 — AstrBot CloneTTS 插件

<p align="center">
  基于 <strong>火山引擎音色克隆 (ICL)</strong> 的 AstrBot 文本转语音插件，使用自定义克隆音色让你的聊天机器人开口"说话"。
</p>

<p align="center">
  <a href="https://github.com/Radiant303/astrbot_plugin_clonetts"><img src="https://img.shields.io/badge/version-v2.3.0-blue" alt="version" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-AGPL--3.0-green" alt="license" /></a>
  <a href="https://docs.astrbot.app/dev/star/plugin-new.html"><img src="https://img.shields.io/badge/docs-AstrBot-orange" alt="docs" /></a>
</p>
<p align="center">
  <img src="https://count.getloli.com/@astrbotpluginclonetts?name=astrbotpluginclonetts&theme=miku&padding=7&offset=0&align=center&scale=0.3&pixelated=1&darkmode=auto" alt="visitor count" />
</p>

---

## 如果你觉得教程太繁琐或者有问题 可以提交issu或者联系我提供技术支持

#### qq 3511078185 (申请好友时备注插件名😊,记得点star!)

## 本插件不依赖AstrBot的TTS功能,所以你不需要额外配置AstrBot的tts,只需要按照以下教程获取火山引擎的凭证并配置到插件里就可以了

## 📋 前置要求

1. **AstrBot** ≥ v4.5.0 已安装并正常运行
2. **火山引擎账号**，并开通 [语音合成服务](https://console.volcengine.com/speech/new/overview?projectName=default)
3. 在火山引擎控制台创建 **音色克隆** 音色，获取以下凭证：
   - `appid` — 应用 AppID
   - `access_token` — API 访问令牌 (Access Key)
   - `voice_type` — 克隆音色 ID (Speaker ID)

## 📖 凭证获取教程

### 1. 点击打开火山引擎 https://console.volcengine.com/speech/new/overview?projectName=default 登录并实名认证

### 2. 回到刚刚的[火山引擎](https://console.volcengine.com/speech/new/overview?projectName=default)

### 3. ![1773151167896.png](https://free.picui.cn/free/2026/03/11/69b0f7fc9339c.png)

### 4. ![1773151183200.png](https://free.picui.cn/free/2026/03/11/69b0f7fc9937c.png)

### 5. 上传音色(请注意要选择"我要复刻中文音色",其他语种火山引擎V3接口暂不支持,但是实际声音效果相同,所以如果需要复刻其他语种的音色也可以选择这个选项)

### ![1773151195702.png](https://free.picui.cn/free/2026/03/11/69b0f7fcce286.png)

### 6. 成功后返回这个页面 并切换到旧版

### ![1773151225265.png](https://free.picui.cn/free/2026/03/11/69b0f7fcb8ba4.png)

### 7. ![1773151231623.png](https://free.picui.cn/free/2026/03/11/69b0f7fe6eb1e.png)

### 8. 划到底部

### 9. ![1773151245322.png](https://free.picui.cn/free/2026/03/11/69b0f7fea5d20.png)

---

## ⚙️ 配置说明

安装后在 AstrBot 管理面板的 **插件配置** 中找到 `克隆语音`，填写以下参数：

| 参数                  | 类型     | 默认值  | 说明                                             |
| --------------------- | -------- | ------- | ------------------------------------------------ |
| `enable_tts`          | `bool`   | `true`  | 是否启用该插件                                   |
| `appid`               | `string` | `""`    | 火山引擎应用 AppID **（必填）**                  |
| `access_token`        | `string` | `""`    | 火山引擎 Access Token **（必填）**               |
| `voice_type`          | `string` | `""`    | 克隆音色 ID **（必填）**                         |
| `speed_ratio`         | `int`    | `0`     | 语速 (-50 到 100，0 为正常，100 为 2 倍)         |
| `loudness_rate`       | `int`    | `0`     | 音量 (-50 到 100，0 为正常，100 为 2 倍)         |
| `sample_rate`         | `int`    | `24000` | 采样率 (推荐 24000)                              |
| `tts_probability`     | `int`    | `80`    | 被动回复概率 (0–100)，0 = 永不触发               |
| `max_length`          | `int`    | `50`    | 被动 TTS 最大处理字数                            |
| `min_length`          | `int`    | `5`     | 被动 TTS 最小处理字数                            |
| `enable_llm_tool`     | `bool`   | `true`  | 是否启用 LLM 工具，允许 AI 主动调用语音合成      |
| `enable_llm_response` | `bool`   | `false` | ![1773150294051.png](https://free.picui.cn/free/2026/03/11/69b0f7fc468c3.png) |

---

## 📖 使用方式

### 1. 被动模式（自动转换）

插件会根据 `tts_probability` 的概率自动将 LLM 的文字回复转换为语音。如果回复字数不在 `min_length` 到 `max_length` 之间，则跳过转换。

### 2. 工具模式（AI 主动触发）

当 `enable_llm_tool` 开启时，AI 可以在对话中意识到自己具有 `clone_tts` 工具。它会根据语境主动决定是否使用语音回复。

---

## ✨ 功能特性

| 特性            | 说明                                               |
| --------------- | -------------------------------------------------- |
| 🗣️ 音色克隆     | 接入火山引擎音色克隆 (ICL) v3 API，音质逼真        |
| 🛠️ LLM 工具支持 | 允许 LLM 主动调用 `clone_tts` 工具进行语音回复     |
| 🎛️ 音频参数可调 | 支持调节语速、音量、采样率                         |
| 🎲 概率触发     | 可配置 0–100% 的被动回复概率，灵活控制语音频率     |
| 📏 长度限制     | 被动模式下可设置字数上下限，避免长文本或短语转语音 |
| ⚡ 流式合成     | 使用 SSE 流式接口获取音频，响应更迅速              |
| 🛡️ 防御性设计   | 完善的配置校验、异常捕获与日志，运行稳定           |

---

## 🏗️ 项目结构

```
astrbot_plugin_clonetts/
├── main.py              # 插件主逻辑与工具定义
├── tts_api/
│   └── dy_tts_api.py    # 封装火山引擎 SSE 接口
├── metadata.yaml        # 插件元信息
├── _conf_schema.json    # 配置项定义
├── README.md            # 本文档
└── requirements.txt     # 依赖 (aiohttp)
```

---

## 🔧 常见问题排查

### 插件已启用但没有语音回复

1. 确认 `appid`、`access_token`、`voice_type` 已正确配置。
2. 检查 `tts_probability` 是否过低，或回复字数超出了限制。
3. 查看 AstrBot 运行日志，寻找以 `CloneTTS` 开头的错误提示。

### 语音合成失败

- 确认火山引擎账号欠费或服务已过期。
- 确认网络能访问 `openspeech.bytedance.com`。
- 如果使用的是旧版音色，请确认其支持 `seed-icl-2.0`（本插件使用此 Resource ID）。

---

## 🔗 相关链接

- 📘 [AstrBot 插件开发文档](https://docs.astrbot.app/dev/star/plugin-new.html)
- 🌋 [火山引擎音色克隆 ICL](https://www.volcengine.com/product/tts)
- 🐙 [本插件 GitHub 仓库](https://github.com/Radiant303/astrbot_plugin_clonetts)

---


## ⭐ Star History

> [!TIP]
> 如果本项目对您的生活 / 工作产生了帮助，或者您关注本项目的未来发展，请给项目 Star，这是我们维护这个开源项目的动力 <3

<div align="center">

[![Star History Chart](https://api.star-history.com/image?repos=Radiant303/astrbot_plugin_clonetts&type=date&legend=top-left)](https://www.star-history.com/?repos=Radiant303%2Fastrbot_plugin_clonetts&type=date&legend=top-left)

</div>


