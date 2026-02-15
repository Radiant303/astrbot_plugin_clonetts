# 🎙️ 克隆语音 — AstrBot CloneTTS 插件

<p align="center">
  基于 <strong>火山引擎音色克隆 (ICL)</strong> 的 AstrBot 文本转语音插件，使用自定义克隆音色让你的聊天机器人开口"说话"。
</p>

<p align="center">
  <a href="https://github.com/Radiant303/astrbot_plugin_clonetts"><img src="https://img.shields.io/badge/version-v1.0.0-blue" alt="version" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-AGPL--3.0-green" alt="license" /></a>
  <a href="https://docs.astrbot.app/dev/star/plugin-new.html"><img src="https://img.shields.io/badge/docs-AstrBot-orange" alt="docs" /></a>
</p>

---

## ✨ 功能特性

| 特性           | 说明                                               |
| -------------- | -------------------------------------------------- |
| 🗣️ 音色克隆     | 接入火山引擎音色克隆 (ICL) API，使用自定义克隆音色 |
| 🎛️ 音频参数可调 | 支持调节语速、音量、音调                           |
| 🎲 概率触发     | 可配置 0–100% 的回复概率，不是每条都转语音         |
| 📏 长度限制     | 超出设定字数的回复自动跳过，保留文字输出           |
| 🔌 即插即用     | 安装后通过 AstrBot 面板配置即可使用，无需额外代码  |
| 🛡️ 防御性设计   | 完善的配置校验、异常捕获与日志，稳定运行不崩溃     |

---

## 📋 前置要求

1. **AstrBot** ≥ v4.5.0 已安装并正常运行
2. **火山引擎账号**，并开通 [语音合成服务](https://www.volcengine.com/product/tts)
3. 在火山引擎控制台创建 **音色克隆** 音色，获取以下凭证信息：
   - `appid` — 应用 AppID
   - `access_token` — API 访问令牌
   - `voice_type` — 克隆音色 ID

---

## 🚀 安装

### 方式一：通过 AstrBot 插件市场安装（推荐）

在 AstrBot 管理面板中搜索 **克隆语音** 或 `astrbot_plugin_clonetts`，点击安装即可。

### 方式二：手动安装

将本仓库克隆到 AstrBot 的插件目录：

```bash
cd <AstrBot 根目录>/data/plugins
git clone https://github.com/Radiant303/astrbot_plugin_clonetts.git
```

重启 AstrBot 后插件将自动加载。

---

## ⚙️ 配置说明

安装后在 AstrBot 管理面板的 **插件配置** 中找到 `克隆语音`，填写以下参数：

| 参数              | 类型     | 默认值            | 说明                                                |
| ----------------- | -------- | ----------------- | --------------------------------------------------- |
| `enable_tts`      | `bool`   | `true`            | 是否启用该插件                                      |
| `appid`           | `string` | `""`              | 火山引擎应用 AppID **（必填）**                     |
| `access_token`    | `string` | `""`              | 火山引擎 Access Token **（必填）**                  |
| `cluster`         | `string` | `volcano_icl`     | 集群名称（`volcano_icl` 表示音色克隆）              |
| `voice_type`      | `string` | `""`              | 克隆音色 ID **（必填）**                            |
| `uid`             | `string` | `388808087185088` | 用户 ID（用于火山引擎侧标识）                       |
| `speed_ratio`     | `float`  | `1.0`             | 语速（0.5–2.0，1.0 为正常速度）                     |
| `volume_ratio`    | `float`  | `1.0`             | 音量（0.5–2.0，1.0 为正常音量）                     |
| `pitch_ratio`     | `float`  | `1.0`             | 音调（0.5–2.0，1.0 为正常音调）                     |
| `tts_probability` | `int`    | `50`              | TTS 回复概率（0–100），0 = 永不触发，100 = 必定触发 |
| `max_length`      | `int`    | `50`              | TTS 最大处理字数，超出时保持文字回复                |
| `min_length`      | `int`    | `5`               | TTS 最小处理字数，低于时跳过语音                    |

---

## 📖 使用方式

插件采用 **被动触发** 模式，无需任何命令。工作流程如下：

```
用户发送消息 → LLM 生成文字回复 → 插件以设定概率拦截
                                       │
                              ┌────────┴────────┐
                              │ 概率命中 & 文本   │
                              │ 长度在范围内      │
                              └────────┬────────┘
                                       │
                          调用火山引擎克隆语音 API
                                       │
                              ┌────────┴────────┐
                              │ 合成成功          │
                              └────────┬────────┘
                                       │
                           将文字回复替换为语音消息
```

- 当概率未命中或文本超长/过短时，原始文字回复不受影响。
- 当 TTS 合成失败时，插件会记录错误日志并静默降级为文字回复，**不会影响正常聊天**。

---

## 🏗️ 项目结构

```
astrbot_plugin_clonetts/
├── main.py              # 插件主逻辑
├── metadata.yaml        # 插件元信息（名称、版本、作者等）
├── _conf_schema.json    # 配置项 JSON Schema
├── README.md            # 本文档
├── LICENSE              # AGPL-3.0 许可证
└── .gitignore           # Git 忽略规则
```

---

## 🔧 常见问题排查

### 插件已启用但没有语音回复

1. 确认 `enable_tts` 设置为 `true`
2. 检查 `tts_probability` 是否过低（建议测试时设为 `100`）
3. 检查 `max_length` 和 `min_length` 设置是否导致大多数回复被跳过
4. 查看 AstrBot 日志中是否有 `CloneTTS 以下必要配置为空` 的警告

### 日志中出现 `CloneTTS HTTP 错误`

- 确认 `appid`、`access_token`、`voice_type` 填写正确
- 确认火山引擎账号已开通语音合成服务且余额充足
- 检查 `cluster` 是否为正确的集群名称

### 日志中出现 `CloneTTS 请求失败`

- 检查服务器网络是否能正常访问 `openspeech.bytedance.com`
- 请求超时默认为 30 秒，若网络环境较差可能需要检查连通性

---

## 🔗 相关链接

- 📘 [AstrBot 插件开发文档](https://docs.astrbot.app/dev/star/plugin-new.html)
- 🌋 [火山引擎语音合成](https://www.volcengine.com/product/tts)
- 🔊 [音色克隆文档](https://www.volcengine.com/docs/6561/1234)
- 🐙 [本插件 GitHub 仓库](https://github.com/Radiant303/astrbot_plugin_clonetts)

---

## 📄 许可证

本项目基于 [GNU Affero General Public License v3.0](LICENSE) 开源。

Copyright © 2026 Radiant303
