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

The full prompt is in [prompt.md](prompt.md). Paste it verbatim; no extra tool instructions are needed.

## Scoring

Ten items, one point each. Only "SVG engineering" can be judged automatically; the rest are human judgement, and must be judged **on the rendered image**, not on the model's own description.

| # | Item | Passes when |
| --- | --- | --- |
| 1 | Tentacle count | Exactly eight, clearly distinguishable |
| 2 | Object grip | Tentacle-to-portafilter-handle contact is plausible |
| 3 | Liquid flow | Milk flows continuously into the cup, not into mid-air or outside |
| 4 | Button interaction | A tentacle actually touches the espresso machine button |
| 5 | Pointing | A tentacle clearly points at the wall clock |
| 6 | Cup and scale | The cup sits directly on the digital scale |
| 7 | Scene support | Machine and scale both rest on the countertop |
| 8 | Limb connection | The remaining four tentacles are visible and connected to the body |
| 9 | Spatial relations | Occlusion is consistent, objects do not visibly interpenetrate |
| 10 | SVG engineering | Valid, self-contained SVG that renders correctly |

Item 10 is enforced by CI on every push. Run it locally before submitting (see [CONTRIBUTING.md](CONTRIBUTING.md)):

```bash
node scripts/check-svg.mjs
```

**Principle**: a pretty drawing does not earn points. Gorgeous artwork with only six tentacles, or milk pouring outside the cup, still loses points.
Model **DeepSeek-V4.1-Flash**, five different agent tools, one generation each, same prompt.

| Rank | Agent tool | Work | Score | One-line note |
| --- | --- | --- | --- | --- |
| 1 | ZCode | [zcode.svg](results/zcode.svg) | **9.5** | Richest detail, complete spatial structure, eight tentacles clearly differentiated |
| 2 | ChatGPT | [chatgpt.svg](results/chatgpt.svg) | **9.4** | Balanced composition, natural depth, high task completion |
| 3 | WorkBuddy | [workbuddy.svg](results/workbuddy.svg) | **9.2** | Excellent instruction following, clear action relationships, but diagram-like |
| 4 | DeepSeek Harness | [deepseek-harness.svg](results/deepseek-harness.svg) | **8.3** | Main structure complete, but some tentacles overlap and depth is weak |
| 5 | Claude | [claude.svg](results/claude.svg) | **7.8** | Clean composition, but no clear grip between the milk pitcher and the tentacle |

Full commentary: [results/SCORES.md](results/SCORES.md).
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
prompt.md                The prompt — copy and paste
CONTRIBUTING.md          Submission requirements
README.en.md             English
results/*.svg            Each agent tool's output (the only artefact that is scored)
results/SCORES.md        Scoring basis and per-work commentary
results/MANIFEST.md      Run record: environment and artefact sizes
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
