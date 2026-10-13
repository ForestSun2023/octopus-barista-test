# 运行记录 / Run manifest

## 环境

| 项 | 值 |
| --- | --- |
| 模型 | DeepSeek-V4.1-Flash |
| 提示词 | [prompt.md](../prompt.md)，逐字使用，未追加任何说明 |
| 生成方式 | 每个 Agent 工具新开一个会话，一次生成，无重试、无人工修改 |
| 日期 | 2026-10-13 |
| 评审 | 由 ChatGPT 依据本仓库评分表逐项检查，一次评审，无第二人复核 |
| Agent 工具版本 | unknown（当时未记录） |
| 推理档位 / 生成耗时 / token 用量 | unknown（当时未记录） |

## 产物

| 产物 | Agent 工具 | 字节 | 行数 | viewBox | `<path>` | `<text>` | image/base64 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [zcode.svg](zcode.svg) | ZCode | 39 045 | 299 | 1600×1100 | 35 | 2 | 0 |
| [workbuddy.svg](workbuddy.svg) | WorkBuddy | 23 659 | 254 | 1200×800 | 43 | 0 | 0 |
| [chatgpt.svg](chatgpt.svg) | ChatGPT | 20 471 | 211 | 1200×800 | 35 | 2 | 0 |
| [claude.svg](claude.svg) | Claude | 22 385 | 138 | 1200×900 | 25 | 1 | 0 |
| [deepseek-harness.svg](deepseek-harness.svg) | DeepSeek Harness | 16 880 | 92 | 1000×750 | 31 | 1 | 0 |

`image/base64` 全部为 0：五份都满足「只用矢量元素、不含位图」的约束，所以**「代码质量」那一分没有拉开差距**，区分度全部来自 9 项人工判断。

行数从 92 到 299，差 3.2 倍。但**它和排名不是单调关系**（第 4 名的 DeepSeek Harness 文件最小，第 5 名的 Claude 倒数第二），所以代码量只能当参考列，不能当分数。

## 已知缺口

- Agent 工具版本、推理档位、生成耗时、token 用量都没有记录，无法核对。
- 每个 Agent 只跑了 1 次，没有多轮数据，因此不能比较稳定性与最低分。
- 评审是单人一次，没有第二人复核。

补齐这些缺口的要求见 [../CONTRIBUTING.md](../CONTRIBUTING.md)。
