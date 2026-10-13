const { Resvg } = require('@resvg/resvg-js');
const fs = require('fs');
const svg = fs.readFileSync(process.argv[2], 'utf8');
const r = new Resvg(svg, { fitTo: { mode: 'width', value: 1200 }, background: '#ffffff' });
const png = r.render().asPng();
fs.writeFileSync(process.argv[3], png);
console.log('rendered', process.argv[3], png.length, 'bytes');
