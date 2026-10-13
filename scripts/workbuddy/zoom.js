const { Resvg } = require('@resvg/resvg-js');
const fs = require('fs');
// usage: node zoom.js in.svg out.png "x y w h"
const svg = fs.readFileSync(process.argv[2], 'utf8');
const [x, y, w, h] = process.argv[4].split(/\s+/).map(Number);
const zoomed = svg.replace(/viewBox="[^"]*"/, `viewBox="${x} ${y} ${w} ${h}"`)
                  .replace(/width="1200" height="800"/, `width="${Math.round(w * 1000 / h)}" height="1000"`);
const r = new Resvg(zoomed, { fitTo: { mode: 'height', value: 1000 }, background: '#ffffff' });
fs.writeFileSync(process.argv[3], r.render().asPng());
console.log('ok', process.argv[3]);
