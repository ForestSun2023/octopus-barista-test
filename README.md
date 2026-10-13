# 章鱼咖啡师测试 · Octopus Barista Test

[中文](README.md) · [English](README.en.md)

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

完整提示词见 [prompt.md](prompt.md)（当前 v2）。直接整段复制粘贴给 Agent 即可，不需要任何额外工具说明。

本仓库收录的 2026-10-13 轮次用的是 [prompts/v1.md](prompts/v1.md)，v2 只多了一条禁止用标注代替绘图的约束。

## 评分标准

分两步：先按下表的 **4 类加权**算总分，再用 **10 项检查清单**逐项找证据。

| 评分项目 | 满分 | 覆盖的检查项 |
| --- | --- | --- |
| 指令完成度 | 5 | 八条触手、四项指定动作、其余肢体是否齐全 |
| 空间与交互关系 | 2 | 抓握、倒奶、按钮接触、杯子和秤的关系 |
| 构图与视觉表达 | 2 | 遮挡、透视、比例、可辨识度及细节 |
| SVG 工程质量 | 1 | XML 有效性、自包含性、能否正常渲染 |

> 总分不是 10 项直接相加——二值检查只能出整数，而本轮的 9.5 / 8.3 / 7.8 来自上面的加权。
> 清单和加权口径不一致的地方、以及清单漏掉的判据，都记在 [results/EVIDENCE.md](results/EVIDENCE.md)。

### 10 项检查清单

10 项里只有「代码质量」能自动判定，其余 9 项靠人工。人工项也要对着**渲染出来的图**找证据，不接受模型的文字说明。

| # | 测试项目 | 判定 | 通过标准 |
| --- | --- | --- | --- |
| 1 | 代码质量 | 🤖 自动 | SVG 合法、有 viewBox、自包含，无位图 / base64 / 外部资源 |
| 2 | 肢体数量 | 👁 人工 | 八条触手数量准确，彼此可区分 |
| 3 | 物体抓取 | 👁 人工 | 触手与手柄的接触关系合理 |
| 4 | 液体流向 | 👁 人工 | 牛奶连续流入杯内，而非悬空或流到杯外 |
| 5 | 按钮交互 | 👁 人工 | 触手确实接触咖啡机按钮 |
| 6 | 指向关系 | 👁 人工 | 触手方向明确指向挂钟 |
| 7 | 杯子与秤 | 👁 人工 | 杯子直接放在电子秤上 |
| 8 | 场景支撑 | 👁 人工 | 咖啡机和电子秤均落在台面上 |
| 9 | 肢体连接 | 👁 人工 | 剩余四条触手清晰可见且连接正确 |
| 10 | 空间关系 | 👁 人工 | 前后遮挡合理，物体没有明显穿插 |

第 1 项由 CI 每次 push 强制。投稿前先本地跑一遍（见 [CONTRIBUTING.md](CONTRIBUTING.md)）：

```bash
node scripts/check-svg.mjs
```

### 人工项的判定证据

9 项人工判断都要在渲染图上逐条找证据，「看起来差不多」不算：

| 项目 | 怎么算过 |
| --- | --- |
| 肢体数量 | 从身体出发把 8 条触手逐个编号，编号时不能出现「这里算一条还是两条」的犹豫 |
| 物体抓取 | 手柄图形与触手末端贴合；「靠近」不算 |
| 液体流向 | 奶流是一条连续路径，终点落在杯口内；中段断开或落到杯外都算不过 |
| 按钮交互 | 触手末端压在按钮图形上，而不是停在按钮旁边 |
| 指向关系 | 触手的轴线延长线穿过钟面 |
| 杯子与秤 | 杯底与秤台面贴合，中间看不到台面 |
| 场景支撑 | 咖啡机、秤的底边与台面线重合 |
| 肢体连接 | 四条剩余触手的起点在身体上，不是从画面外伸进来 |
| 空间关系 | 遮挡前后一致：同一条触手不能既在机器前又在机器后 |

**判分原则**：不因为画得漂亮就给高分。画面精美但只有六条触手、牛奶流在杯子外面，照样扣分。

本轮逐项复核的证据和两处口径问题见 [results/EVIDENCE.md](results/EVIDENCE.md)。

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

完整点评与各分项依据见 [results/SCORES.md](results/SCORES.md)；运行环境、产物规模与已知缺口见 [results/MANIFEST.md](results/MANIFEST.md)。

画廊预览：用浏览器打开 [index.html](index.html) 即可，纯静态、无需构建，也可以直接开 GitHub Pages。

## 仓库结构

```
prompt.md                测试提示词 v2，复制即用
prompts/v1.md            冻结的 v1，本轮结果用的就是它
README.en.md             English
CONTRIBUTING.md          投稿要求与盲评复核方法
results/*.svg            各 Agent 的最终作品（也是唯一被评分的产物）
results/MANIFEST.md      运行记录：环境、产物规模、已知缺口
results/SCORES.md        本轮评分依据与逐份点评
results/EVIDENCE.md      逐项判定证据与复核发现
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
- 每次 push 都会跑 `node scripts/check-svg.mjs`，任何不合法或含位图的 SVG 会让 CI 失败。
- 一次结果不能代表某个 Agent 工具或模型的整体水平，也不能据此判断 API 是否「降智」。模型输出本身有随机性，提示词、推理档位和运行环境都会影响结果。
- `scripts/<agent>/` 里的脚本是各 Agent 在生成过程中留下的，风格、质量差异很大，不代表测试要求，也不参与评分；`scripts/check-svg.mjs` 例外，它是评分表第 1 项的检查器。

## 许可

MIT，见 [LICENSE](LICENSE)。作者：[@ForestSun2023](https://github.com/ForestSun2023)。
