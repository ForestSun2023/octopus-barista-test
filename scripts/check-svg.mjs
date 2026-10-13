#!/usr/bin/env node
// 校验 results/*.svg 是否合法、自包含、可渲染。
// 零依赖。用法：node scripts/check-svg.mjs [文件...]   默认扫描 results/*.svg
//
// 检查项对应评分表里「代码质量」那一分（唯一可自动判定的一项）：
//   1. XML 标签配对、根元素是 <svg>
//   2. 有合法 viewBox（4 个数字，宽高为正）
//   3. 自包含：无 <image>、无 base64、无 <script>、无 <foreignObject>、无外部 URL 引用

import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const FORBIDDEN = [
  [/<\s*image\b/i, '<image> 位图元素'],
  [/base64/i, 'base64 数据'],
  [/<\s*script\b/i, '<script> 元素'],
  [/<\s*foreignObject\b/i, '<foreignObject> 元素'],
  [/(?:xlink:)?href\s*=\s*["'](?!#)/i, 'href 不是内部引用（应为 #id）'],
  [/url\(\s*["']?(?:https?:)?\/\//i, 'CSS 里的外部引用'],
];

function check(file) {
  let text;
  try {
    text = readFileSync(file, 'utf8').replace(/^\uFEFF/, '');
  } catch (e) {
    return ['读不到文件：' + e.message];
  }
  const errors = [];

  for (const [re, label] of FORBIDDEN) {
    if (re.test(text)) errors.push('含' + label);
  }

  // 去掉注释、PI、CDATA、DOCTYPE 后再看结构
  const body = text
    .replace(/<\?[\s\S]*?\?>/g, '')
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/<!\[CDATA\[[\s\S]*?\]\]>/g, '')
    .replace(/<!DOCTYPE[^>]*>/gi, '');

  const root = body.match(/<\s*([A-Za-z_][\w.:-]*)/);
  if (!root || root[1] !== 'svg') errors.push('根元素不是 <svg>');

  const vb = text.match(/viewBox\s*=\s*["']\s*([^"']+)["']/);
  const nums = vb ? vb[1].trim().split(/[\s,]+/).map(Number) : [];
  if (nums.length !== 4 || nums.some((n) => !Number.isFinite(n)) || nums[2] <= 0 || nums[3] <= 0) {
    errors.push('viewBox 缺失或非法（需要 4 个数字，宽高为正）');
  }

  const tagRe = /<(\/?)([A-Za-z_][\w.:-]*)((?:"[^"]*"|'[^']*'|[^>"'])*?)(\/?)>/g;
  const stack = [];
  let m;
  while ((m = tagRe.exec(body))) {
    const name = m[2];
    const selfClosing = m[4] === '/' || /\/\s*$/.test(m[3]);
    if (m[1] === '/') {
      const open = stack.pop();
      if (open !== name) {
        errors.push('标签不配对：</' + name + '> 对应 <' + (open ?? '无') + '>');
        break;
      }
    } else if (!selfClosing) {
      stack.push(name);
    }
  }
  if (stack.length) errors.push('未闭合标签：<' + stack.join('>, <') + '>');

  return errors;
}

const args = process.argv.slice(2);
const files = args.length
  ? args
  : readdirSync('results').filter((f) => f.endsWith('.svg')).sort().map((f) => join('results', f));

let failed = 0;
for (const f of files) {
  const errors = check(f);
  if (errors.length) {
    failed++;
    console.log('FAIL  ' + f);
    for (const e of errors) console.log('        - ' + e);
  } else {
    console.log('OK    ' + f);
  }
}
console.log('');
console.log(files.length - failed + '/' + files.length + ' 通过');
process.exit(failed ? 1 : 0);
