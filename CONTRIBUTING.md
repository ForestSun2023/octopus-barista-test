# 投稿你自己的结果

## 必须附上的信息

1. 模型名称与版本（例如 `DeepSeek-V4.1-Flash`）
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

## 预览图怎么来

```bash
node scripts/render.mjs results/your-agent.svg
```

输出与 SVG 同尺寸的 PNG。想省体积就再转成 WebP（仓库里用的是这条）：

```bash
python -c "from PIL import Image; Image.open('results/your-agent.png').convert('RGB').save('results/your-agent.webp','WEBP',quality=88,method=6)"
```

宽度不要超过 1400px。

## 文件放哪

| 内容 | 路径 |
| --- | --- |
| 作品 | `results/<agent-tool>.svg`，文件名用小写连字符 |
| 预览图 | `results/<agent-tool>.webp`（或 `.png`），宽度 ≤ 1400px |
| 运行信息 | 追加到 [results/MANIFEST.md](results/MANIFEST.md) 的表里 |

预览图在 README 的「作品预览」表里加一格。

## 评分

按 README 的[评分标准](README.md#评分标准)逐项判，**先看结构，再看美观**。把 SVG 实际渲染出来再检查，不要只看模型的文字说明。

## 多轮跑更好

同一个 Agent 跑 3 次，比较平均分和最低分。单次结果说明不了稳定性。
