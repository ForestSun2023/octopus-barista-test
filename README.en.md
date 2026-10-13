# Octopus Barista Test

[中文](README.md) · [English](README.en.md)

A single-prompt benchmark that probes an AI coding agent's **spatial reasoning, multi-constraint execution and code generation**. Inspired by the Pelican Test (asking a model to draw a pelican riding a bicycle).

> Same model, same prompt, different agent tools — see who actually gets all eight tentacles to do their job.

## What makes it harder than the Pelican Test

The Pelican Test mainly checks whether two objects (bird, bicycle) are put together correctly. This one concentrates the pressure on four things:

| Aspect | What it probes |
| --- | --- |
| Visual structure | Can it represent eight tentacles and several independent objects at once? |
| Spatial reasoning | Do contact, support, direction and occlusion actually make sense? |
| Multi-constraint execution | Does it satisfy every requirement, not just the most obvious one? |
| Code generation | Is the output valid, self-contained, renderable SVG? |

Drawing eight tentacles is not the hard part. The hard part is **giving every tentacle a different job while keeping the whole scene spatially coherent**.

## The prompt

The full prompt is in [prompt.md](prompt.md) (currently v2). Paste it verbatim; no extra tool instructions are needed.

The 2026-10-13 run in this repository used [prompts/v1.md](prompts/v1.md). v2 only adds a constraint forbidding labels or arrows in place of actual drawing.

## Scoring

**Checklist v2: 11 items, 1 point each, 11 points total.** Only "SVG engineering" can be judged automatically; the other 10 are human judgement and must be backed by evidence found **in the rendered image**, not by the model's own description.

For a blind review, hand [rubric/v2.md](rubric/v2.md) to the evaluator — it contains no results and no agent names, so it cannot leak the origin of a work.

| # | Item | Judged | Passes when |
| --- | --- | --- | --- |
| 1 | SVG engineering | 🤖 auto | Valid, has a viewBox, self-contained, no raster/base64/external assets |
| 2 | Tentacle count | 👁 human | Eight tentacles, numbered from the body with no hesitation over whether something is one tentacle or two |
| 3a | Portafilter grip | 👁 human | The tentacle tip is on or inside the handle shape; tolerance below |
| 3b | Pitcher grip | 👁 human | The pitcher has a definite contact point with a tentacle, not floating; same tolerance |
| 4 | Liquid flow | 👁 human | The milk stream is one continuous path ending inside the cup rim; a break, or landing outside, fails |
| 5 | Button interaction | 👁 human | The tentacle tip is on the button shape, not beside it; tolerance below |
| 6 | Pointing | 👁 human | The tentacle's extended axis passes through the clock face and the tip is within tolerance of it; **dashed lines, arrows or labels may not bridge that gap** |
| 7 | Cup and scale | 👁 human | The cup base meets the scale platform with no countertop visible between them; tolerance below |
| 8 | Scene support | 👁 human | The bottom edges of the machine and scale coincide with the countertop line |
| 9 | Limb connection | 👁 human | The four remaining tentacles start at the body, not from off-screen |
| 10 | Spatial relations | 👁 human | ① Occlusion is consistent; ② the outline overlap of any two tentacles is at most **1/3** of the shorter one's visible length; ③ no three or more limbs piled up near the body beyond the point where each outline can still be traced |

Item 1 is enforced by CI on every push. Run it locally before submitting (see [CONTRIBUTING.md](CONTRIBUTING.md)):

```bash
node scripts/check-svg.mjs
```

### Distance tolerances

Tolerances are a **percentage of the canvas short side**, not absolute pixels — canvases in this run range from 1000×750 to 1600×1100, so a fixed pixel budget would be unfair across sizes.

| Kind | Tolerance | 1200×800 | 1200×900 | 1600×1100 |
| --- | --- | --- | --- | --- |
| Contact: 3a handle / 3b pitcher / 5 button / 7 cup & scale | short side **1%** | 8 px | 9 px | 11 px |
| Pointing: 6 clock | short side **5%** | 40 px | 45 px | 55 px |

Contact keeps only 1% for line width and antialiasing — touching means touching, a 10 px gap is not touching. Pointing is looser because the clock hangs on the wall and the tentacle crosses the whole frame; whether the direction is right matters more here than whether it is touching.

Calibrated on the contested values measured in the previous run (raw measurements in [results/BLIND.md](results/BLIND.md)):

| Measured | Canvas | Tip to clock face | Tolerance | Verdict |
| --- | --- | --- | --- | --- |
| ZCode | 1600×1100 | 45 px (axis off by 1.8 px) | 55 px | pass |
| WorkBuddy | 1200×800 | 40 px, bridged by a purple dashed line | 40 px | **fail** — distance just fits, but it violates item 6's prohibition |
| Claude | 1200×900 | 80 px | 45 px | fail |

### Rubric versions

| Version | Items | Basis |
| --- | --- | --- |
| [v1](rubric/v1.md) | 10 | The published scores use a 4-category weighting (5 + 2 + 2 + 1), **not** the checklist sum; the checklist also missed pitcher grip and tentacle overlap |
| **v2 (current)** | 11 | 1 point per item, 11 total; tolerances are fixed numbers |

The published 9.5 / 9.4 / 9.2 / 8.3 / 7.8 were scored with **v1** and cannot be reproduced with v2. Comparing across versions requires re-scoring with v2.

**Principle**: a pretty drawing does not earn points. Gorgeous artwork with only six tentacles, or milk pouring outside the cup, still loses points.

## Results of this run

Model **DeepSeek-V4.1-Flash**, five different agent tools, one generation each, same prompt.

| Rank | Agent tool | Work | Score | One-line note |
| --- | --- | --- | --- | --- |
| 1 | ZCode | [zcode.svg](results/zcode.svg) | **9.5** | Richest detail, complete spatial structure, eight tentacles clearly differentiated |
| 2 | ChatGPT | [chatgpt.svg](results/chatgpt.svg) | **9.4** | Balanced composition, natural depth, high task completion |
| 3 | WorkBuddy | [workbuddy.svg](results/workbuddy.svg) | **9.2** | Excellent instruction following, clear action relationships, but diagram-like |
| 4 | DeepSeek Harness | [deepseek-harness.svg](results/deepseek-harness.svg) | **8.3** | Main structure complete, but some tentacles overlap and depth is weak |
| 5 | Claude | [claude.svg](results/claude.svg) | **7.8** | Clean composition, but no clear grip between the milk pitcher and the tentacle |

Blind review (works anonymised A–E, the evaluator did not know the mapping): [results/BLIND.md](results/BLIND.md) — **all five scored 10/10**, so this checklist is saturated on this batch and cannot rank them.

Full commentary and per-item evidence: [results/SCORES.md](results/SCORES.md) and [results/EVIDENCE.md](results/EVIDENCE.md).
Run environment and artefact sizes: [results/MANIFEST.md](results/MANIFEST.md).

### Preview

| **#1 ZCode · 9.5** | **#2 ChatGPT · 9.4** |
| --- | --- |
| ![ZCode](results/zcode.webp) | ![ChatGPT](results/chatgpt.webp) |
| **#3 WorkBuddy · 9.2** | **#4 DeepSeek Harness · 8.3** |
| ![WorkBuddy](results/workbuddy.webp) | ![DeepSeek Harness](results/deepseek-harness.webp) |
| **#5 Claude · 7.8** | |
| ![Claude](results/claude.webp) | |

Open [index.html](index.html) in a browser for the gallery — static, no build step, works as-is on GitHub Pages.

## Repository layout

```
prompt.md                The prompt, v2 — copy and paste
prompts/v1.md            Frozen v1, the version this run used
rubric/v1.md             Frozen rubric v1, what the published scores used
rubric/v2.md             Current rubric v2 (11 items), hand this to a blind evaluator
README.en.md             English
CONTRIBUTING.md          Submission requirements and blind review method
results/*.svg            Each agent tool's output (the only artefact that is scored)
results/MANIFEST.md      Run record: environment, artefact sizes, known gaps
results/SCORES.md        Scoring basis and per-work commentary
results/EVIDENCE.md      Per-item evidence and review findings
results/BLIND.md         Blind review result and rank comparison
scripts/check-svg.mjs    Self-containment check, run by CI and before submitting
scripts/render.mjs       SVG to PNG, for previews
scripts/<agent>/         Scripts the agents left behind; reference only
index.html               Gallery
```

## Running it yourself

1. Start a fresh agent session and paste the prompt from [prompt.md](prompt.md) verbatim.
2. Save the returned SVG, render it, and check it item by item against the checklist above — **structure first, beauty second**.
3. Prefer three independent runs per agent tool and compare the mean and minimum, not a single result.

## Notes

- This repository includes results from five agent tools only.
- A single run does not represent the overall ability of an agent tool or a model, and cannot be used to conclude that an API has been "nerfed". Model output is stochastic; prompt, reasoning effort and runtime all matter.
- CI runs `node scripts/check-svg.mjs` on every push; any invalid SVG, or one containing raster data, fails the build.
- The scripts under `scripts/<agent>/` were left behind during generation. Their style and quality vary widely; they are not part of the test and are not scored. `scripts/check-svg.mjs` and `scripts/render.mjs` are the exception — they are tooling, not outputs.

## License

MIT — see [LICENSE](LICENSE). Author: [@ForestSun2023](https://github.com/ForestSun2023).
