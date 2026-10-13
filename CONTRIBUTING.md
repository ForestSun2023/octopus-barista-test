# 投稿你自己的结果

## 必须附上的信息

1. 模型名称与版本（例如 `DeepSeek-V4.1-Flash`），以及推理档位
2. Agent 工具名称与版本
3. 运行日期
4. 是否逐字使用 [prompt.md](prompt.md)；有改动就把改动贴出来
5. 生成耗时、token 用量（拿得到就给，拿不到写 `unknown`）

`unknown` 可以接受，编造不可以。

## 提交前自检

```bash
node scripts/check-svg.mjs results/your-agent.svg
```

必须输出 `OK`。这一项对应评分表里「代码质量」的 1 分，过不了就不必提。CI 会在 push 时跑同一份检查。

## 文件放哪

| 内容 | 路径 |
| --- | --- |
| 作品 | `results/<agent-tool>.svg`，文件名用小写连字符 |
| 预览图 | `results/<agent-tool>.webp`，宽度 ≤ 1400px |
| 运行信息 | 追加到 [results/MANIFEST.md](results/MANIFEST.md) 的表里 |

预览图在 README 的「作品预览」表里加一格。

## 评分

按 README 的评分表逐项判，**先看结构，再看美观**。画得漂亮但只有六条触手、牛奶流在杯子外面，照样扣分。人工项要对着渲染出来的图找证据，不接受模型的文字说明。

## 多轮跑更好

同一个 Agent 跑 3 次，比较平均分和最低分。单次结果说明不了稳定性。
