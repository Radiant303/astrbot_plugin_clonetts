# 更新日志

<p align="center">
  <img src="https://count.getloli.com/@astrbotpluginclonetts?name=astrbotpluginclonetts&theme=miku&padding=7&offset=0&align=center&scale=0.3&pixelated=1&darkmode=auto" alt="visitor count" />
</p>

## v2.2.0 (2026-03-27)

- 🚀新增可调节LLM是否受到字数限制控制的选项

## v2.1.6 (2026-03-24)

- 🐞修复文本长度小于下限时候错误的问题

## v2.1.5 (2026-03-19)

- 📝 优化了语气指令提示词

## v2.0.4 (2026-03-19)

- 🚀 新增语气增强模式,可以自定义模型识别转语音时的语气

## v2.0.3 (2026-03-12)

- 📝 上传音色时候(请注意要选择"我要复刻中文音色",其他语种火山引擎V3接口暂不支持,但是实际声音效果相同,所以如果需要复刻其他语种的音色也可以选择这个选项)

## v2.0.2 (2026-03-11)

- 🐞 增加错误日志debug信息。
- 🐞 修复当 `enable_llm_response` 关闭时模型继续回复用户的bug。
- ⚙️ 使LLM工具调用的语音回复也受 `tts_probability` 和长度限制的控制，避免过度触发。

## v2.0.0 (2026-03-10)

- 🚀 **新增 LLM 工具支持**：允许 AI 主动调用 `clone_tts` 工具进行语音回复。
- ⚡ **流式合成优化**：切换至 SSE (Server-Sent Events) 流式接口，显著提升响应速度
- 🎙️ **音色克隆升级**：基于火山引擎 ICL 2.0 协议重构，支持最新的音色克隆技术。
- ⚙️ **配置系统重构**：
  - 新增 `sample_rate` (采样率) 调节。
  - 新增 `enable_llm_tool` 开关。
  - 移除了 `cluster`, `uid`, `pitch_ratio` 等不再需要的繁琐配置。
- 🛡️ **稳定性增强**：增加了完善的防御性校验逻辑，防止因配置错误导致的插件崩溃，优化了错误日志信息。
- 📝 **文档大修**：重写 README.md，包含详细的火山引擎凭证获取图文教程及联系方式。

## v1.0.0 (2026-02-15)

- 初始版本发布：支持火山引擎音色复刻API
