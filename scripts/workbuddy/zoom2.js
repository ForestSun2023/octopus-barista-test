const { Resvg } = require('@resvg/resvg-js');
const fs = require('fs');
// usage: node zoom2.js in.svg out.png "x y w h"   (wraps content in a transform group)
let svg = fs.readFileSync(process.argv[2], 'utf8');
const [x, y, w, h] = process.argv[4].split(/\s+/).map(Number);
const k = Math.min(1200 / w, 800 / h);
const tx = -x * k + (1200 - w * k) / 2, ty = -y * k + (800 - h * k) / 2;
svg = svg.replace(/(<svg[^>]*>)/, `$1<g transform="translate(${tx.toFixed(2)},${ty.toFixed(2)}) scale(${k.toFixed(3)})">`)
         .replace('</svg>', '</g></svg>');
const r = new Resvg(svg, { fitTo: { mode: 'width', value: 1200 }, background: '#ffffff' });
fs.writeFileSync(process.argv[3], r.render().asPng());
console.log('ok', process.argv[3]);
