/* Generates a self-contained SVG: an octopus barista in a coffee shop.
   Oblique three-quarter projection: front + top + right faces visible.
   depth per unit z = (+0.46, -0.40);  ground plane y = 855 at z = 0. */
const fs = require('fs');
const r = (n) => Math.round(n);
const P = (xf, z, h) => [xf + 0.46 * z, 855 - 0.40 * z - h];

/* ---------------------------------------------------------------- helpers */
function catmullRom(pts, per) {
  const p = [pts[0], ...pts, pts[pts.length - 1]], out = [];
  for (let i = 1; i < p.length - 2; i++) {
    const [x0, y0] = p[i - 1], [x1, y1] = p[i], [x2, y2] = p[i + 1], [x3, y3] = p[i + 2];
    for (let j = 0; j < per; j++) {
      const t = j / per, t2 = t * t, t3 = t2 * t;
      out.push([
        0.5 * (2 * x1 + (-x0 + x2) * t + (2 * x0 - 5 * x1 + 4 * x2 - x3) * t2 + (-x0 + 3 * x1 - 3 * x2 + x3) * t3),
        0.5 * (2 * y1 + (-y0 + y2) * t + (2 * y0 - 5 * y1 + 4 * y2 - y3) * t2 + (-y0 + 3 * y1 - 3 * y2 + y3) * t3),
      ]);
    }
  }
  out.push(pts[pts.length - 1].slice());
  return out;
}
/* Tapered arm: closed fill path (no stroke, cap hidden inside the body) plus an
   OPEN outline path so no dark line is drawn across the arm's base. */
function buildArm(pts, wBase, wTip, per = 8) {
  const sp = catmullRom(pts, per), n = sp.length, N = [];
  for (let i = 0; i < n; i++) {
    const a = sp[Math.max(0, i - 1)], b = sp[Math.min(n - 1, i + 1)];
    let tx = b[0] - a[0], ty = b[1] - a[1];
    const L = Math.hypot(tx, ty) || 1;
    N.push([-ty / L, tx / L]);
  }
  const hw = (t) => (wTip + (wBase - wTip) * Math.pow(1 - t, 1.15)) / 2;
  let side = 0;
  for (let i = 0; i < n; i++) side += Math.sign(N[i][1]) * hw(i / (n - 1));
  const sgn = side >= 0 ? 1 : -1;
  const Ls = [], Rs = [], arc = [0];
  for (let i = 1; i < n; i++) arc.push(arc[i - 1] + Math.hypot(sp[i][0] - sp[i - 1][0], sp[i][1] - sp[i - 1][1]));
  for (let i = 0; i < n; i++) {
    const h = hw(i / (n - 1));
    Ls.push([sp[i][0] + N[i][0] * h, sp[i][1] + N[i][1] * h]);
    Rs.push([sp[i][0] - N[i][0] * h, sp[i][1] - N[i][1] * h]);
  }
  const seg = (arr) => arr.map(q => r(q[0]) + ' ' + r(q[1])).join('L');
  const fill = 'M' + seg(Ls) + 'L' + seg(Rs.slice().reverse()) + 'Z';
  const outline = 'M' + seg(Ls) + 'L' + seg(Rs.slice().reverse());
  const total = arc[n - 1], suckers = [];
  let next = total * 0.26;
  for (let i = 0; i < n; i++) {
    if (arc[i] >= next && arc[i] < total * 0.94) {
      const t = i / (n - 1), h = hw(t);
      suckers.push([sp[i][0] + N[i][0] * sgn * h * 0.5, sp[i][1] + N[i][1] * sgn * h * 0.5, Math.min(7.4, Math.max(3, h * 0.5))]);
      next += 31;
    }
  }
  return { fill, outline, suckers };
}

/* ---------------------------------------------------------------- geometry */
const CX = -80, CW = 520, MZ0 = 40, MZ1 = 280, MH = 360;
const mFBL = P(CX, MZ0, 0), mFBR = P(CX + CW, MZ0, 0);
const mBBL = P(CX, MZ1, 0), mBBR = P(CX + CW, MZ1, 0);
const MX0 = mFBL[0], MX1 = mFBR[0], MYT = mFBL[1] - MH;
const MYB = mFBL[1], MBX = mBBR[0], MBY = mBBR[1], MBYT = MBY - MH;

const SC = [800, 60], SCD = 180, SH = 54, SW = 180;
const sFBL = P(SC[0], SC[1], 0), sFBR = P(SC[0] + SW, SC[1], 0);
const sBBL = P(SC[0], SC[1] + SCD, 0), sBBR = P(SC[0] + SW, SC[1] + SCD, 0);

const SCM = [SC[0] + SW / 2, SC[1] + SCD / 2];
const cupP = P(SCM[0], SCM[1], SH + 4);
const CBX = cupP[0], CBY = cupP[1];
const CRIM = CBY - 137;                     // cup rim centre y
const PC = [CBX + 95.4, CRIM - 101];        // pitcher centre (tilted -50 deg)
const SPX = PC[0] - 95.4, SPY = PC[1] + 4.8; // spout tip

const ARMS = [
  { id: 'CT', role: 'tentacle 1 - points at the wall clock', w: [42, 6],
    pts: [[1150, 600], [1188, 516], [1226, 432], [1264, 348], [1300, 272]] },
  { id: 'BT', role: 'tentacle 2 - presses the espresso machine button', w: [44, 8],
    pts: [[862, 572], [776, 548], [676, 536], [572, 534], [470, 540], [362, 540]] },
  { id: 'X2', role: 'tentacle 3 - free, raised and curled', w: [44, 6],
    pts: [[834, 652], [752, 588], [690, 508], [654, 420], [652, 342], [686, 294], [732, 300], [754, 342], [736, 384], [698, 392], [672, 366]] },
  { id: 'X3', role: 'tentacle 4 - free, resting along the counter', w: [42, 7],
    pts: [[1192, 700], [1276, 744], [1356, 754], [1430, 736], [1464, 704], [1450, 680], [1416, 686]] },
  { id: 'MT', role: 'tentacle 5 - holds the pitcher and pours milk', w: [43, 7],
    pts: [[1104, 708], [1140, 650], [1132, 600], [1110, 562], [1088, 545], [1074, 558]] },
  { id: 'PT', role: 'tentacle 6 - holds the portafilter', w: [44, 13],
    pts: [[838, 690], [754, 706], [666, 710], [580, 706], [504, 712], [462, 728], [420, 752], [390, 730], [398, 706]] },
  { id: 'X1', role: 'tentacle 7 - free, drapes over the counter edge', w: [42, 7],
    pts: [[892, 720], [812, 786], [744, 852], [722, 922], [752, 988], [800, 1006]] },
  { id: 'X4', role: 'tentacle 8 - free, drapes over the counter edge', w: [42, 7],
    pts: [[1064, 726], [1130, 796], [1206, 882], [1286, 956], [1348, 998], [1400, 990]] },
];
const DRAW_ORDER = ['CT', 'BT', 'X2', 'X3', 'MT', 'PT', 'X1', 'X4'];

const SKIN = '#e8734a', SKIN_LINE = '#a83d18', SUCKER = '#ffd9c4', SUCKER_LINE = '#c2703f';

/* ---------------------------------------------------------------- emit */
const s = [];
s.push('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1100" width="1600" height="1100">');
s.push('<title>Octopus barista at an espresso machine</title>');
s.push(`<desc>Front three-quarter view of a coral octopus working behind a wooden coffee-shop counter. All eight tentacles are separate and visible: one grips the portafilter below the espresso machine, one holds a milk pitcher and pours a continuous stream into a cup standing on a digital scale on the countertop, one presses a button on the machine panel, one extends straight out to point at the wall clock, and four more drape over the counter and curl in the air.</desc>`);
s.push(`<defs>
 <linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7ead8"/><stop offset="0.6" stop-color="#efdfc7"/><stop offset="1" stop-color="#e3cfb2"/></linearGradient>
 <linearGradient id="tile" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d3e3dd"/><stop offset="1" stop-color="#b7cec7"/></linearGradient>
 <radialGradient id="wallShade" cx="0.5" cy="0.46" r="0.66"><stop offset="0.5" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#6b4a2c" stop-opacity="0.24"/></radialGradient>
 <linearGradient id="woodTop" x1="0" y1="0" x2="0.3" y2="1"><stop offset="0" stop-color="#a06a44"/><stop offset="1" stop-color="#7f5031"/></linearGradient>
 <linearGradient id="woodFront" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6f4728"/><stop offset="1" stop-color="#4f301a"/></linearGradient>
 <linearGradient id="steelF" x1="0" y1="0" x2="0.7" y2="1"><stop offset="0" stop-color="#5a646f"/><stop offset="0.45" stop-color="#454e58"/><stop offset="1" stop-color="#333b44"/></linearGradient>
 <linearGradient id="steelT" x1="0" y1="0" x2="0.35" y2="1"><stop offset="0" stop-color="#8b959f"/><stop offset="1" stop-color="#69737d"/></linearGradient>
 <linearGradient id="steelR" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#39414a"/><stop offset="1" stop-color="#262c33"/></linearGradient>
 <linearGradient id="chrome" x1="0" y1="0" x2="1" y2="0.2"><stop offset="0" stop-color="#7d8894"/><stop offset="0.3" stop-color="#eef4f9"/><stop offset="0.6" stop-color="#aeb9c3"/><stop offset="1" stop-color="#76818c"/></linearGradient>
 <linearGradient id="recess" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#141a21"/><stop offset="0.45" stop-color="#232a33"/><stop offset="1" stop-color="#333c46"/></linearGradient>
 <linearGradient id="pot" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f2f6fa"/><stop offset="0.34" stop-color="#c7d0d9"/><stop offset="0.7" stop-color="#98a3ae"/><stop offset="1" stop-color="#78838e"/></linearGradient>
 <linearGradient id="porc" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="0.62" stop-color="#f5f4f1"/><stop offset="1" stop-color="#dcd8d1"/></linearGradient>
 <linearGradient id="milk" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff"/><stop offset="0.5" stop-color="#fdfdfc"/><stop offset="1" stop-color="#ebe9e3"/></linearGradient>
 <linearGradient id="board" x1="0" y1="0" x2="0.4" y2="1"><stop offset="0" stop-color="#3b332c"/><stop offset="1" stop-color="#26201b"/></linearGradient>
</defs>`);

/* ---------------------------------------------------- wall + wall fittings */
s.push('<rect x="0" y="0" width="1600" height="820" fill="url(#wall)"/>');
s.push('<rect x="0" y="556" width="1600" height="264" fill="url(#tile)"/>');
for (let x = 0; x <= 1600; x += 100) s.push(`<line x1="${x}" y1="556" x2="${x}" y2="820" stroke="#a4beb7" stroke-width="1.6" opacity="0.65"/>`);
s.push('<line x1="0" y1="618" x2="1600" y2="618" stroke="#a4beb7" stroke-width="1.6" opacity="0.65"/>');
s.push('<line x1="0" y1="686" x2="1600" y2="686" stroke="#a4beb7" stroke-width="1.6" opacity="0.65"/>');
s.push('<rect x="0" y="550" width="1600" height="14" fill="#8dafa6"/>');
s.push('<rect x="0" y="0" width="1600" height="820" fill="url(#wallShade)"/>');

/* menu board on the wall (upper left) */
s.push(`<g id="menu-board">
 <line x1="215" y1="60" x2="215" y2="118" stroke="#8d7a63" stroke-width="4"/>
 <line x1="455" y1="60" x2="455" y2="118" stroke="#8d7a63" stroke-width="4"/>
 <line x1="150" y1="60" x2="520" y2="60" stroke="#8d7a63" stroke-width="6" stroke-linecap="round"/>
 <rect x="126" y="112" width="418" height="248" rx="14" fill="#7c5232"/>
 <rect x="140" y="126" width="390" height="220" rx="9" fill="url(#board)"/>
 <text x="335" y="182" font-family="Georgia,'DejaVu Serif',serif" font-size="40" font-weight="bold" fill="#f4e6cd" text-anchor="middle" letter-spacing="5">MENU</text>
 <line x1="180" y1="200" x2="490" y2="200" stroke="#f4e6cd" stroke-width="2.5" opacity="0.5"/>
 <rect x="180" y="220" width="180" height="11" rx="5.5" fill="#e8d9bd" opacity="0.72"/>
 <rect x="180" y="250" width="240" height="11" rx="5.5" fill="#e8d9bd" opacity="0.72"/>
 <rect x="180" y="280" width="150" height="11" rx="5.5" fill="#e8d9bd" opacity="0.72"/>
 <rect x="180" y="310" width="205" height="11" rx="5.5" fill="#e8d9bd" opacity="0.72"/>
</g>`);

/* wall clock */
const CKX = 1349, CKY = 161, CKR = 76;
s.push(`<g id="clock">
 <circle cx="${CKX + 4}" cy="${CKY + 6}" r="${CKR + 8}" fill="#4a3524" opacity="0.22"/>
 <circle cx="${CKX}" cy="${CKY}" r="${CKR + 7}" fill="#2f3742"/>
 <circle cx="${CKX}" cy="${CKY}" r="${CKR}" fill="#fcfbf8"/>
 <circle cx="${CKX}" cy="${CKY}" r="${CKR}" fill="none" stroke="#ded8cc" stroke-width="3"/>
 ${Array.from({ length: 12 }, (_, i) => { const a = i * 30 * Math.PI / 180, r1 = i % 3 === 0 ? CKR - 22 : CKR - 15; return `<line x1="${r(CKX + Math.sin(a) * r1)}" y1="${r(CKY - Math.cos(a) * r1)}" x2="${r(CKX + Math.sin(a) * (CKR - 6))}" y2="${r(CKY - Math.cos(a) * (CKR - 6))}" stroke="#3b424c" stroke-width="${i % 3 === 0 ? 5 : 2.4}" stroke-linecap="round"/>`; }).join('\n ')}
 <line x1="${CKX}" y1="${CKY}" x2="${r(CKX - 31)}" y2="${r(CKY - 18)}" stroke="#2b323b" stroke-width="8" stroke-linecap="round"/>
 <line x1="${CKX}" y1="${CKY}" x2="${r(CKX + 42)}" y2="${r(CKY - 24)}" stroke="#2b323b" stroke-width="5.5" stroke-linecap="round"/>
 <line x1="${CKX}" y1="${CKY}" x2="${r(CKX - 26)}" y2="${r(CKY + 46)}" stroke="#d8442f" stroke-width="2.6" stroke-linecap="round"/>
 <circle cx="${CKX}" cy="${CKY}" r="6" fill="#2b323b"/>
</g>`);

/* ------------------------------------------------------------- octopus body */
const BODY = `M890 396 C890 288 928 224 1000 224 C1072 224 1112 288 1112 396
 C1112 452 1128 490 1158 524 C1208 578 1232 644 1206 704
 C1176 776 1086 812 1000 812 C914 812 824 776 794 704
 C768 644 792 578 842 524 C872 490 890 452 890 396 Z`;
s.push(`<g id="octopus">
 <path d="${BODY}" fill="${SKIN}"/>
 <path d="M912 520 C900 620 934 700 1000 736 C1072 700 1108 610 1094 512 C1062 566 950 570 912 520 Z" fill="#000" opacity="0.085"/>
 <ellipse cx="952" cy="330" rx="54" ry="66" fill="#f8a97e" opacity="0.5"/>
 <ellipse cx="1042" cy="342" rx="30" ry="42" fill="#f8a97e" opacity="0.32"/>
 <path d="M894 448 C946 512 1060 512 1108 448" fill="none" stroke="#c1541f" stroke-width="3.6" opacity="0.55"/>
 <path d="${BODY}" fill="none" stroke="${SKIN_LINE}" stroke-width="4.2"/>
</g>`);
/* eyes */
s.push(`<g id="eyes">
 <ellipse cx="948" cy="386" rx="33" ry="31" fill="#fff9f2" stroke="${SKIN_LINE}" stroke-width="4"/>
 <rect x="924" y="376" width="47" height="19" rx="9.5" fill="#2a1c17"/>
 <circle cx="936" cy="371" r="6.5" fill="#fff"/>
 <ellipse cx="1052" cy="378" rx="37" ry="35" fill="#fff9f2" stroke="${SKIN_LINE}" stroke-width="4"/>
 <rect x="1026" y="367" width="53" height="21" rx="10.5" fill="#2a1c17"/>
 <circle cx="1040" cy="361" r="7.5" fill="#fff"/>
</g>`);

/* ---------------------------------------------------------- counter surface */
const CT = [P(-280, 0, 0), P(1720, 0, 0), P(1720, 300, 0), P(-280, 300, 0)];
s.push(`<g id="counter">
 <polygon points="${CT.map(p => r(p[0]) + ',' + r(p[1])).join(' ')}" fill="url(#woodTop)"/>
 <polygon points="${CT.map(p => r(p[0]) + ',' + r(p[1])).join(' ')}" fill="none" stroke="#c48d61" stroke-width="2" opacity="0.45"/>
 <rect x="-280" y="851" width="2000" height="9" fill="#b8814f"/>
 <rect x="-280" y="860" width="2000" height="300" fill="url(#woodFront)"/>
 <rect x="-280" y="1006" width="2000" height="7" fill="#331d0f" opacity="0.45"/>
 ${[40, 520, 1000, 1480].map(x => `<line x1="${x - 138}" y1="1006" x2="${x}" y2="878" stroke="#331d0f" stroke-width="4" opacity="0.3"/>`).join('')}
 ${[300, 780, 1260].map(x => `<rect x="${x}" y="908" width="290" height="72" rx="8" fill="#000" opacity="0.10"/>`).join('')}
</g>`);

/* --------------------------------------------------------- espresso machine */
const GH = { x0: 150, x1: 260, top: 639, bot: 690 };
s.push(`<g id="machine">
 <ellipse cx="${r((MX0 + MBX) / 2)}" cy="${r(MYB + 8)}" rx="340" ry="30" fill="#3b2413" opacity="0.3"/>
 <polygon points="${r(mFBL[0])},${r(MYB)} ${r(mFBR[0])},${r(MYB)} ${r(mBBR[0])},${r(MBY)} ${r(mBBL[0])},${r(MBY)}" fill="#2a3038" opacity="0.5"/>
 <polygon points="${r(mFBL[0])},${r(MYT)} ${r(mFBR[0])},${r(MYT)} ${r(mBBR[0])},${r(MBYT)} ${r(mBBL[0])},${r(MBYT)}" fill="url(#steelT)"/>
 <polygon points="${r(mFBR[0])},${r(MYT)} ${r(mBBR[0])},${r(MBYT)} ${r(mBBR[0])},${r(MBY)} ${r(mFBR[0])},${r(MYB)}" fill="url(#steelR)"/>
 <path d="M${r(MX0)} ${r(MYT)} H${r(MX1)} V${r(MYB)} H${r(MX0)} Z
          M58 639 H398 V${r(MYB)} H58 Z" fill="url(#steelF)" fill-rule="evenodd"/>
 <rect x="${r(MX0)}" y="${r(MYT)}" width="${r(MX1 - MX0)}" height="13" fill="url(#chrome)"/>
 <rect x="0" y="495" width="430" height="90" rx="12" fill="#1d232a"/>
 <rect x="9" y="504" width="412" height="72" rx="8" fill="#12171c"/>
 ${[90, 175, 260, 350].map(x => `<g><circle cx="${x}" cy="540" r="22" fill="#0d1116"/><circle cx="${x}" cy="538" r="17.5" fill="#d8442f"/><circle cx="${x}" cy="531" r="6" fill="#ff9d8b" opacity="0.6"/></g>`).join('')}
 <rect x="418" y="519" width="6" height="42" rx="3" fill="#39424c"/>
 <circle cx="${r(MX1 - 30)}" cy="540" r="15" fill="url(#chrome)" stroke="#5d6771" stroke-width="2"/>
 <rect x="58" y="639" width="340" height="200" fill="url(#recess)"/>
 <rect x="58" y="639" width="340" height="16" fill="#0e1319" opacity="0.85"/>
 <rect x="58" y="639" width="340" height="200" fill="none" stroke="#191e24" stroke-width="3"/>
 <polygon points="96,838 362,838 394,810 128,810" fill="#3b4450" stroke="#1e242b" stroke-width="2.5"/>
 ${Array.from({ length: 8 }, (_, i) => `<polygon points="${118 + i * 30},832 ${136 + i * 30},832 ${166 + i * 30},813 ${148 + i * 30},813" fill="#141a20"/>`).join('')}
 <polygon points="128,810 394,810 394,801 128,801" fill="#525d6a"/>
 <rect x="74" y="648" width="15" height="104" rx="7.5" fill="url(#chrome)" stroke="#69737d" stroke-width="2"/>
 <circle cx="81" cy="754" r="13" fill="url(#chrome)" stroke="#69737d" stroke-width="2"/>
 <g id="group-head">
  <path d="M${GH.x0} ${GH.top} H${GH.x1} V${GH.bot - 22} Q${GH.x1} ${GH.bot} ${GH.x1 - 22} ${GH.bot} H${GH.x0 + 22} Q${GH.x0} ${GH.bot} ${GH.x0} ${GH.bot - 22} Z" fill="url(#chrome)" stroke="#69737d" stroke-width="2.5"/>
  <rect x="${GH.x0 + 6}" y="${GH.top + 8}" width="${GH.x1 - GH.x0 - 12}" height="9" fill="#8b959f" opacity="0.65"/>
  <ellipse cx="${(GH.x0 + GH.x1) / 2}" cy="${GH.bot - 6}" rx="46" ry="10" fill="#3d454e"/>
  <ellipse cx="${(GH.x0 + GH.x1) / 2}" cy="${GH.bot - 10}" rx="40" ry="8" fill="#1c2229"/>
 </g>
 <g id="portafilter">
  <path d="M160 694 H258 V706 Q258 724 240 724 H178 Q160 724 160 706 Z" fill="url(#chrome)" stroke="#69737d" stroke-width="2.5"/>
  <rect x="154" y="690" width="110" height="13" rx="4" fill="#c3ccd4" stroke="#69737d" stroke-width="2"/>
  <path d="M166 700 H252 V710 Q252 718 240 718 H178 Q166 718 166 710 Z" fill="#12171d"/>
  <path d="M256 688 L401 714 Q414 718 410 730 Q406 741 393 738 L251 712 Z" fill="#2b323b" stroke="#171c22" stroke-width="2.5"/>
  <path d="M262 695 L397 719" fill="none" stroke="#59636e" stroke-width="5" stroke-linecap="round" opacity="0.8"/>
  <rect x="250" y="686" width="26" height="30" rx="3" fill="url(#chrome)" stroke="#69737d" stroke-width="2"/>
 </g>
</g>`);

/* ------------------------------------------------------------ digital scale */
s.push(`<g id="scale">
 <ellipse cx="${r((sFBL[0] + sBBR[0]) / 2 - 6)}" cy="${r(sFBL[1] + 8)}" rx="152" ry="26" fill="#3b2413" opacity="0.3"/>
 <polygon points="${r(sBBL[0])},${r(sBBL[1] - SH)} ${r(sBBR[0])},${r(sBBR[1] - SH)} ${r(sBBR[0])},${r(sBBR[1])} ${r(sBBL[0])},${r(sBBL[1])}" fill="#b4bdc5"/>
 <polygon points="${r(sFBL[0])},${r(sFBL[1] - SH)} ${r(sFBR[0])},${r(sFBR[1] - SH)} ${r(sFBR[0])},${r(sFBR[1])} ${r(sFBL[0])},${r(sFBL[1])}" fill="#f3f6f8" stroke="#c3ccd3" stroke-width="2.5"/>
 <polygon points="${r(sFBL[0])},${r(sFBL[1] - SH)} ${r(sFBR[0])},${r(sFBR[1] - SH)} ${r(sBBR[0])},${r(sBBR[1] - SH)} ${r(sBBL[0])},${r(sBBL[1] - SH)}" fill="#e4eaee" stroke="#c3ccd3" stroke-width="2.5" stroke-linejoin="round"/>
 <polygon points="${r(sFBL[0] + 20)},${r(sFBL[1] - SH - 9)} ${r(sFBR[0] - 20)},${r(sFBR[1] - SH - 9)} ${r(sBBR[0] - 20)},${r(sBBR[1] - SH - 9)} ${r(sBBL[0] + 20)},${r(sBBL[1] - SH - 9)}" fill="#fbfdfe" stroke="#cfd6dc" stroke-width="2"/>
 <rect x="${r(sFBL[0] + 30)}" y="${r(sFBL[1] - 40)}" width="112" height="30" rx="6" fill="#18262a" stroke="#98a4ac" stroke-width="2"/>
 <text x="${r(sFBL[0] + 86)}" y="${r(sFBL[1] - 17)}" font-family="Verdana,'DejaVu Sans',sans-serif" font-size="21" font-weight="bold" fill="#6ff0c8" text-anchor="middle">128.4</text>
 <rect x="${r(sFBR[0] - 42)}" y="${r(sFBR[1] - 36)}" width="26" height="20" rx="4" fill="#cfd6dc" stroke="#aab4bb" stroke-width="2"/>
</g>`);

/* ------------------------------------------------------------------- cup */
s.push(`<g id="cup">
 <ellipse cx="${r(CBX)}" cy="${r(CBY + 2)}" rx="66" ry="17" fill="#7d5a3c" opacity="0.4"/>
 <path d="M${r(CBX - 60)} ${r(CRIM)} A68 20 0 0 0 ${r(CBX + 60)} ${r(CRIM)}
          C${r(CBX + 62)} ${r(CBY - 92)} ${r(CBX + 58)} ${r(CBY - 46)} ${r(CBX + 52)} ${r(CBY)}
          A60 17 0 0 1 ${r(CBX - 52)} ${r(CBY)}
          C${r(CBX - 58)} ${r(CBY - 46)} ${r(CBX - 62)} ${r(CBY - 92)} ${r(CBX - 60)} ${r(CRIM)} Z"
       fill="url(#porc)" stroke="#c9c3ba" stroke-width="2.5"/>
 <ellipse cx="${r(CBX)}" cy="${r(CRIM)}" rx="68" ry="20" fill="#eeeadf"/>
 <ellipse cx="${r(CBX)}" cy="${r(CRIM + 2)}" rx="61" ry="16.5" fill="#43280f"/>
 <ellipse cx="${r(CBX - 3)}" cy="${r(CRIM + 3)}" rx="48" ry="12.5" fill="#8b5730"/>
 <ellipse cx="${r(CBX - 5)}" cy="${r(CRIM + 4)}" rx="31" ry="9" fill="#f3e4d0"/>
 <path d="M${r(CBX - 25)} ${r(CRIM + 4)} q10 -7 20 0 q10 7 20 0" fill="none" stroke="#d9c0a0" stroke-width="3"/>
 <ellipse cx="${r(CBX)}" cy="${r(CRIM)}" rx="68" ry="20" fill="none" stroke="#cbc4b9" stroke-width="2.5"/>
 <path d="M${r(CBX - 52)} ${r(CBY - 30)} C${r(CBX - 58)} ${r(CBY - 70)} ${r(CBX - 60)} ${r(CBY - 106)} ${r(CBX - 58)} ${r(CRIM + 6)}" fill="none" stroke="#ffffff" stroke-width="9" opacity="0.75" stroke-linecap="round"/>
</g>`);

/* ---------------------------------------------------------------- pitcher */
s.push(`<g id="pitcher" transform="translate(${PC[0]} ${PC[1]}) rotate(-50)">
 <path d="M-50 -76 C-54 -22 -46 30 -35 76 L35 76 C46 30 54 -22 50 -76 Z" fill="url(#pot)" stroke="#6f7a85" stroke-width="3"/>
 <path d="M-50 -76 C-58 -79 -64 -77 -68 -71 C-63 -62 -54 -59 -47 -61 Z" fill="url(#pot)" stroke="#6f7a85" stroke-width="3"/>
 <ellipse cx="0" cy="-76" rx="50" ry="13.5" fill="#8d97a1"/>
 <ellipse cx="0" cy="-76" rx="43" ry="10" fill="#f5f7f9"/>
 <ellipse cx="2" cy="-74" rx="36" ry="8" fill="#fdfdff"/>
 <path d="M47 -42 C78 -48 86 -10 79 15 C74 39 58 51 47 49" fill="none" stroke="#8d97a1" stroke-width="12" stroke-linecap="round"/>
 <path d="M47 -42 C78 -48 86 -10 79 15 C74 39 58 51 47 49" fill="none" stroke="#cbd4dc" stroke-width="6.5" stroke-linecap="round"/>
 <path d="M-40 -62 C-44 -16 -38 30 -30 64" fill="none" stroke="#ffffff" stroke-width="10" opacity="0.6" stroke-linecap="round"/>
</g>`);

/* ------------------------------------------------------------- tentacles */
s.push('<g id="tentacles">');
for (const id of DRAW_ORDER) {
  const a = ARMS.find(v => v.id === id), arm = buildArm(a.pts, a.w[0], a.w[1]);
  s.push(` <g id="${id}" data-role="${a.role}">`);
  s.push(`  <path d="${arm.fill}" fill="${SKIN}"/>`);
  s.push(`  <path d="${arm.outline}" fill="none" stroke="${SKIN_LINE}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>`);
  for (const [x, y, rr] of arm.suckers) s.push(`  <circle cx="${r(x)}" cy="${r(y)}" r="${r(rr)}" fill="${SUCKER}" stroke="${SUCKER_LINE}" stroke-width="1.5"/>`);
  s.push(' </g>');
}
s.push('</g>');

/* --------------------- continuous milk stream: pitcher spout -> into cup -- */
s.push(`<g id="milk-stream">
 <path d="M${r(SPX - 5.5)} ${r(SPY - 2)} C${r(SPX - 7.5)} ${r(SPY + 38)} ${r(SPX + 1)} ${r(SPY + 72)} ${r(SPX - 2.6)} ${r(SPY + 108)}
          L${r(SPX + 8.4)} ${r(SPY + 110)}
          C${r(SPX + 8)} ${r(SPY + 72)} ${r(SPX + 0.5)} ${r(SPY + 36)} ${r(SPX + 6.5)} ${r(SPY - 2)} Z"
       fill="url(#milk)" stroke="#dcd6cb" stroke-width="1.5"/>
 <ellipse cx="${r(SPX + 3)}" cy="${r(SPY + 114)}" rx="14" ry="5.5" fill="#ffffff" opacity="0.92"/>
</g>`);
s.push('</svg>');

fs.writeFileSync(process.argv[2] || 'octopus-barista.svg', s.join('\n'));
console.log('written', SPX.toFixed(1), SPY.toFixed(1), 'rim', CRIM.toFixed(1));
