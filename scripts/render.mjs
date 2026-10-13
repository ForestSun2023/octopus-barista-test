#!/usr/bin/env node
// 把一个 SVG 渲染成 PNG。零依赖，用系统已装的 Chrome / Edge 无头模式。
// 用法：node scripts/render.mjs results/zcode.svg [出来.png]
//
// 浏览器把独立 SVG 文档按固有尺寸 1:1 显示，所以窗口必须正好等于 viewBox 的宽高，否则会留白或被裁切。

import { readFileSync, existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { resolve } from 'node:path';

const [svgPath, outArg] = process.argv.slice(2);
if (!svgPath) {
  console.error('用法: node scripts/render.mjs <svg> [out.png]');
  process.exit(1);
}

const svg = readFileSync(svgPath, 'utf8');
const vb = svg.match(/viewBox\s*=\s*["']\s*([-\d.eE]+)[\s,]+([-\d.eE]+)[\s,]+([-\d.eE]+)[\s,]+([-\d.eE]+)/);
if (!vb) {
  console.error('这个 SVG 没有 viewBox，无法确定窗口尺寸');
  process.exit(1);
}
const w = Math.round(Number(vb[3]));
const h = Math.round(Number(vb[4]));

const CANDIDATES = [
  process.env.CHROME_PATH,
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
  '/usr/bin/chromium-browser',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
].filter(Boolean);
const browser = CANDIDATES.find((p) => existsSync(p));
if (!browser) {
  console.error('找不到 Chrome / Edge，用 CHROME_PATH 环境变量指定可执行文件');
  process.exit(1);
}

const out = resolve(outArg || svgPath.replace(/\.svg$/i, '') + '.png');
const url = 'file:///' + resolve(svgPath).replace(/\\/g, '/');

execFileSync(browser, [
  '--headless=new',
  '--disable-gpu',
  '--hide-scrollbars',
  '--force-device-scale-factor=1',
  `--window-size=${w},${h}`,
  `--screenshot=${out}`,
  url,
], { stdio: 'inherit' });

console.log(`rendered ${out} (${w}x${h})`);
