# 投稿你自己的结果

## 必须附上的信息

1. 模型名称与版本（例如 `DeepSeek-V4.1-Flash`），以及推理档位
2. Agent 工具名称与版本
3. 运行日期
4. 用的是哪个版本的提示词：[prompt.md](prompt.md)（v2）还是 [prompts/v1.md](prompts/v1.md)；有改动就把改动贴出来
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

见 [rubric/v2.md](rubric/v2.md)：11 项，每项 1 分，满分 11，含写死的距离阈值。**先看结构，再看美观**。人工项要对着渲染出来的图找证据，不接受模型的文字说明。

## 盲评复核

现在的排名不是盲评——评审者知道每份作品属于哪个 Agent，容易受品牌影响。想检验评分本身是否可靠，做一遍盲评：

1. 把 `results/*.svg` 复制到一个**仓库之外**的目录，重命名成 `A.svg` `B.svg` `C.svg`…，顺序随机
2. 把映射关系写在**另一个文件**里，不要放进作品目录
3. 把作品目录和 [rubric/v2.md](rubric/v2.md) 交给一个不知道映射的评审者（另一个模型，或者人），要求它按那张表逐项打分。rubric 里没有结果也没有 Agent 名称，可以安全交出去
4. 拿盲评结果和已发布分数对比；排名差得多，说明原评分不可靠

两条硬要求：评审者必须真的把 SVG 渲染出来看；作品目录里不能有任何能泄露来源的元数据。

## 多轮跑更好

同一个 Agent 跑 3 次，比较平均分和最低分。单次结果说明不了稳定性。
