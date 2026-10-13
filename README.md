# 章鱼咖啡师测试 · Octopus Barista Test

一个单提示词测试，用来观察 AI 编码 Agent 的**空间推理、多约束执行和代码生成**能力。灵感来自鹈鹕测试（Pelican Test：让模型画一只骑自行车的鹈鹕）。

> 同一款模型、同一份提示词，换不同的 Agent 工具，看谁真的把八条触手的活都干完了。

## 它比鹈鹕测试难在哪

鹈鹕测试主要看能不能把「鸟 + 自行车」两个物体摆对。章鱼咖啡师测试把压力集中在四点上：

| 考察点 | 具体表现 |
| --- | --- |
| 视觉结构构建 | 能否同时表示八条触手和多个独立物体 |
| 空间推理 | 接触、支撑、方向、遮挡关系是否说得通 |
| 多约束执行 | 能否遵循全部要求，而不是只完成最显眼的部分 |
| 程序生成 | 能否生成合法、可渲染的自包含 SVG 代码 |

画八条触手并不难，难的是**让每条触手完成不同的任务，同时保证整幅图在空间关系上说得通**。

## 测试指令

完整提示词见 [prompt.md](prompt.md)。直接整段复制粘贴给 Agent 即可，不需要任何额外工具说明。

## 评分标准（10 分制，每项 1 分）

| 测试项目 | 通过标准 |
| --- | --- |
| 肢体数量 | 八条触手数量准确，彼此可区分 |
| 物体抓取 | 触手与手柄的接触关系合理 |
| 液体流向 | 牛奶连续流入杯内，而非悬空或流到杯外 |
| 按钮交互 | 触手确实接触咖啡机按钮 |
| 指向关系 | 触手方向明确指向挂钟 |
| 杯子与秤 | 杯子直接放在电子秤上 |
| 场景支撑 | 咖啡机和电子秤均落在台面上 |
| 肢体连接 | 剩余四条触手清晰可见且连接正确 |
| 空间关系 | 前后遮挡合理，物体没有明显穿插 |
| 代码质量 | SVG 合法、自包含，能正常渲染 |

**判分原则**：不因为画得漂亮就给高分。画面精美但只有六条触手、牛奶流在杯子外面，照样扣分。最好把生成的 SVG 实际渲染出来再检查结构，而不是只看模型给出的文字解释。

## 本轮结果

同一款模型 **DeepSeek-V4.1-Flash**，通过 5 个不同的 Agent 工具，使用同一份提示词，各生成一次。

| 排名 | Agent 工具 | 作品 | 得分 | 一句话点评 |
| --- | --- | --- | --- | --- |
| 1 | ZCode | [zcode.svg](results/zcode.svg) | **9.5** | 细节丰富，空间结构完整，八条触手职责区分明确 |
| 2 | ChatGPT | [chatgpt.svg](results/chatgpt.svg) | **9.4** | 画面均衡，前后层次自然，任务完成度高 |
| 3 | WorkBuddy | [workbuddy.svg](results/workbuddy.svg) | **9.2** | 指令执行优秀，动作关系清楚，但偏示意图风格 |
| 4 | DeepSeek Harness | [deepseek-harness.svg](results/deepseek-harness.svg) | **8.3** | 主要结构完整，但部分触手交叠，空间层次稍弱 |
| 5 | Claude | [claude.svg](results/claude.svg) | **7.8** | 构图清爽，但奶壶与触手之间缺少明确的抓握关系 |

### 作品预览

| **#1 ZCode · 9.5** | **#2 ChatGPT · 9.4** |
| --- | --- |
| ![ZCode](results/zcode.webp) | ![ChatGPT](results/chatgpt.webp) |
| **#3 WorkBuddy · 9.2** | **#4 DeepSeek Harness · 8.3** |
| ![WorkBuddy](results/workbuddy.webp) | ![DeepSeek Harness](results/deepseek-harness.webp) |
| **#5 Claude · 7.8** | |
| ![Claude](results/claude.webp) | |

完整点评与各分项依据见 [results/SCORES.md](results/SCORES.md)。

画廊预览：用浏览器打开 [index.html](index.html) 即可，纯静态、无需构建，也可以直接开 GitHub Pages。

## 仓库结构

```
prompt.md                测试提示词，复制即用
CONTRIBUTING.md          投稿要求
README.en.md             English
results/*.svg            各 Agent 的最终作品（也是唯一被评分的产物）
results/SCORES.md        本轮评分依据与逐份点评
results/MANIFEST.md      运行记录：环境与产物规模
scripts/check-svg.mjs    自包含性校验，CI 与投稿前都跑它
scripts/render.mjs       SVG 渲染成 PNG，做预览图用
scripts/<agent>/         各 Agent 生成作品时留下的脚本，仅供参考
index.html               作品画廊
```

## 自己跑一遍

1. 新开一个 Agent 会话，把 [prompt.md](prompt.md) 里的提示词整段贴进去。
2. 把返回的 SVG 存成文件并渲染，逐项对照上面的评分标准检查——**先看结构，再看美观**。
3. 建议每个 Agent 独立运行 3 次，比较平均分与最低分，而不是只看一次结果。

## 说明

- 本仓库只收录 5 个 Agent 工具的结果。
- 一次结果不能代表某个 Agent 工具或模型的整体水平，也不能据此判断 API 是否「降智」。模型输出本身有随机性，提示词、推理档位和运行环境都会影响结果。
- `scripts/` 里的脚本是各 Agent 在生成过程中留下的，风格、质量差异很大，不代表测试要求，也不参与评分。

## 许可

MIT，见 [LICENSE](LICENSE)。作者：[@ForestSun2023](https://github.com/ForestSun2023)。
