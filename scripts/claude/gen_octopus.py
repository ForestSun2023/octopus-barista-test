import math

W, H = 1200, 900

# ---------------------------------------------------------------- geometry --

def cr(points, n=14):
    """Catmull-Rom spline through the given control points."""
    pts = [points[0]] + list(points) + [points[-1]]
    out = []
    for i in range(len(pts) - 3):
        p0, p1, p2, p3 = pts[i], pts[i + 1], pts[i + 2], pts[i + 3]
        for j in range(n):
            t = j / n
            t2 = t * t
            t3 = t2 * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t
                       + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                       + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t
                       + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                       + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    out.append(points[-1])
    return out


def tentacle(points, w0, w1, n=14):
    """Filled outline of a tapered limb swept along a spline."""
    pts = cr(points, n)
    m = len(pts)
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        if i == 0:
            dx, dy = pts[1][0] - x, pts[1][1] - y
        elif i == m - 1:
            dx, dy = x - pts[i - 1][0], y - pts[i - 1][1]
        else:
            dx, dy = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
        ln = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / ln, dx / ln
        t = i / (m - 1)
        e = t * t * (3 - 2 * t)          # smooth taper
        w = w0 + (w1 - w0) * e
        left.append((x + nx * w / 2, y + ny * w / 2))
        right.append((x - nx * w / 2, y - ny * w / 2))
    d = "M " + " L ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in left)
    d += " L " + " L ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in reversed(right))
    return d + " Z"


# ------------------------------------------------------------------ palette --
OCT = "#ea7a42"
OCT_EDGE = "#b04a1c"
OCT_DARK = "#c85f2b"

# ------------------------------------------------------------------ layout --
CLK = (250, 140)                                  # wall clock centre, r = 78
BODY = "M 495,470 C 495,380 535,330 600,330 C 665,330 705,380 705,470 " \
       "C 705,540 680,585 640,592 C 620,596 580,596 560,592 C 520,585 495,540 495,470 Z"

MX0, MY0, MX1, MY1 = 130, 470, 370, 700           # espresso machine front face
DX, DY = 50, -26                                  # oblique depth vector

CUPX, CUPTOP, CUPBASE = 920, 602, 668             # cup
SX0, SY0, SX1, SY1 = 830, 685, 1010, 712          # scale front face
SDX, SDY = 30, -17

BTN = (302, 454)                                  # button T3 presses

# Spout lip ends up at (899.6, 482.2) under this transform.
PITCHER_XF = "translate(977.5,462.5) rotate(-60) scale(0.8)"

# Each arm: control points from base to tip, base width, tip width.
# Drawn AFTER the counter objects so the four working arms visibly sit in
# front of the things they hold or press.
R = 33   # limb radius at the shoulder — narrow enough that the eight bases
         # stay legible where they bunch under the mantle

TENTACLES = [
    # T1  grips the portafilter handle beneath the group head
    ([(560, 586), (528, 648), (484, 680), (436, 692), (400, 682)], R + 5, 6),
    # T2  grips the milk pitcher by its handle
    ([(698, 538), (772, 462), (872, 382), (958, 332), (1012, 392)], R + 5, 6),
    # T3  presses the button on the top of the machine
    ([(535, 566), (500, 528), (430, 488), (358, 458), (306, 450)], R + 3, 6),
    # T4  points at the wall clock
    ([(515, 543), (462, 458), (410, 362), (368, 264), (330, 224)], R + 5, 6),
    # T5 - T8  the four free arms, fanned wide so each stays distinct
    ([(596, 584), (560, 644), (516, 688), (470, 708)], R - 3, 6),
    ([(626, 586), (632, 644), (626, 692), (610, 722)], R - 3, 6),
    ([(656, 580), (688, 634), (714, 682), (730, 712)], R - 5, 6),
    ([(682, 562), (736, 608), (788, 644), (820, 666)], R - 5, 6),
]

s = []
a = s.append

a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
a('<title>Octopus barista working an espresso machine</title>')

# --------------------------------------------------------------------- defs --
a('<defs>')
a('<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1">'
  '<stop offset="0" stop-color="#f7ece0"/><stop offset="1" stop-color="#dfc9b1"/></linearGradient>')
a('<linearGradient id="counterTop" x1="0" y1="0" x2="0" y2="1">'
  '<stop offset="0" stop-color="#c28d5f"/><stop offset="1" stop-color="#a56f49"/></linearGradient>')
a('<linearGradient id="counterFront" x1="0" y1="0" x2="0" y2="1">'
  '<stop offset="0" stop-color="#8a5533"/><stop offset="1" stop-color="#5a3420"/></linearGradient>')
a('<radialGradient id="skin" cx="0.36" cy="0.28" r="0.85">'
  '<stop offset="0" stop-color="#f5915c"/><stop offset="0.62" stop-color="#e87940"/>'
  '<stop offset="1" stop-color="#c95b28"/></radialGradient>')
a('<linearGradient id="steelF" x1="0" y1="0" x2="0" y2="1">'
  '<stop offset="0" stop-color="#eef1f5"/><stop offset="0.45" stop-color="#dfe4ea"/>'
  '<stop offset="1" stop-color="#bfc6cf"/></linearGradient>')
a('<linearGradient id="steelS" x1="0" y1="0" x2="1" y2="0">'
  '<stop offset="0" stop-color="#9ba3ad"/><stop offset="1" stop-color="#848c96"/></linearGradient>')
a('<linearGradient id="milk" x1="0" y1="0" x2="0" y2="1">'
  '<stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#f3efe4"/></linearGradient>')
a('<linearGradient id="cupShade" x1="0" y1="0" x2="1" y2="0">'
  '<stop offset="0" stop-color="#ccd1d7"/><stop offset="0.35" stop-color="#ffffff"/>'
  '<stop offset="0.75" stop-color="#ffffff"/><stop offset="1" stop-color="#c6ccd3"/></linearGradient>')
a('<linearGradient id="jug" x1="0" y1="0" x2="1" y2="1">'
  '<stop offset="0" stop-color="#ffffff"/><stop offset="0.6" stop-color="#eef1f6"/>'
  '<stop offset="1" stop-color="#cdd4dd"/></linearGradient>')
a('<radialGradient id="vig" cx="0.5" cy="0.42" r="0.78">'
  '<stop offset="0.6" stop-color="#000000" stop-opacity="0"/>'
  '<stop offset="1" stop-color="#3a2412" stop-opacity="0.18"/></radialGradient>')
a('</defs>')

# --------------------------------------------------------------------- wall --
a(f'<rect width="{W}" height="{H}" fill="url(#wall)"/>')
a('<g opacity="0.3" stroke="#cbb49a" stroke-width="1.5">')
for x in range(60, W, 96):
    a(f'<line x1="{x}" y1="300" x2="{x}" y2="648"/>')
for y in (300, 400, 500, 600):
    a(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>')
a('</g>')

# -------------------------------------------------------------------- clock --
a(f'<circle cx="{CLK[0]}" cy="{CLK[1]}" r="86" fill="#00000018"/>'
  f'<circle cx="{CLK[0]}" cy="{CLK[1]}" r="78" fill="#7a5433"/>'
  f'<circle cx="{CLK[0]}" cy="{CLK[1]}" r="66" fill="#fdf8ef"/>'
  f'<circle cx="{CLK[0]}" cy="{CLK[1]}" r="66" fill="none" stroke="#e3d7c4" stroke-width="2"/>')
a('<g stroke="#4a3520" stroke-width="4" stroke-linecap="round">')
for k in range(12):
    ang = math.radians(k * 30)
    r0, r1 = (52, 61) if k % 3 else (46, 61)
    a(f'<line x1="{CLK[0]+r0*math.sin(ang):.1f}" y1="{CLK[1]-r0*math.cos(ang):.1f}" '
      f'x2="{CLK[0]+r1*math.sin(ang):.1f}" y2="{CLK[1]-r1*math.cos(ang):.1f}"/>')
a('</g>')
hx, hy = CLK[0] + 36 * math.sin(math.radians(305)), CLK[1] - 36 * math.cos(math.radians(305))
mx, my = CLK[0] + 54 * math.sin(math.radians(60)), CLK[1] - 54 * math.cos(math.radians(60))
a(f'<line x1="{CLK[0]}" y1="{CLK[1]}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="#4a3520" '
  f'stroke-width="7" stroke-linecap="round"/>')
a(f'<line x1="{CLK[0]}" y1="{CLK[1]}" x2="{mx:.1f}" y2="{my:.1f}" stroke="#4a3520" '
  f'stroke-width="4.5" stroke-linecap="round"/>')
a(f'<circle cx="{CLK[0]}" cy="{CLK[1]}" r="5" fill="#4a3520"/>')

# ------------------------------------------------------------------ counter --
a('<polygon points="70,648 1140,648 1170,726 40,726" fill="url(#counterTop)"/>')
a('<polygon points="40,726 1170,726 1170,812 40,812" fill="url(#counterFront)"/>')
a('<rect x="40" y="722" width="1130" height="9" rx="4" fill="#e0b184"/>')
a('<polygon points="70,648 1140,648 1141,653 69,653" fill="#8c5c38" opacity="0.6"/>')
a('<ellipse cx="600" cy="656" rx="150" ry="26" fill="#4a2a12" opacity="0.22"/>')

# --------------------------------------------------------- espresso machine --
a(f'<polygon points="{MX0},{MY0} {MX0+DX},{MY0+DY} {MX1+DX},{MY0+DY} {MX1},{MY0}" '
  f'fill="#e6ebf0"/>')                                        # top face
a(f'<polygon points="{MX1},{MY0} {MX1+DX},{MY0+DY} {MX1+DX},{MY1+DY} {MX1},{MY1}" '
  f'fill="url(#steelS)"/>')                                   # right side
a(f'<rect x="{MX0}" y="{MY0}" width="{MX1-MX0}" height="{MY1-MY0}" fill="url(#steelF)"/>')
a(f'<rect x="{MX0}" y="{MY0}" width="{MX1-MX0}" height="{MY1-MY0}" fill="none" '
  f'stroke="#aab2bc" stroke-width="2"/>')
a(f'<rect x="{MX0+18}" y="{MY0+18}" width="{MX1-MX0-36}" height="{MY1-MY0-36}" rx="10" '
  f'fill="#f3f6f9" stroke="#c3cad3" stroke-width="2"/>')
# pressure gauge
a('<circle cx="196" cy="536" r="36" fill="#fbfcfd" stroke="#98a0aa" stroke-width="6"/>')
a('<circle cx="196" cy="536" r="27" fill="none" stroke="#dde2e8" stroke-width="1.5"/>')
a('<path d="M196,536 L214,516" stroke="#c0392b" stroke-width="4" stroke-linecap="round"/>')
a('<circle cx="196" cy="536" r="4.5" fill="#6e747c"/>')
# buttons on the top face (the red one is the one being pressed)
a('<g transform="rotate(-27.5 248 466)"><ellipse cx="248" cy="466" rx="21" ry="10.5" '
  'fill="#7f868f"/></g>')
a(f'<g transform="rotate(-27.5 {BTN[0]} {BTN[1]+2})">'
  f'<ellipse cx="{BTN[0]}" cy="{BTN[1]+2}" rx="23" ry="11.5" fill="#4f565e"/>'
  f'<ellipse cx="{BTN[0]}" cy="{BTN[1]}" rx="19" ry="9" fill="#d0453c"/>'
  f'<ellipse cx="{BTN[0]-3}" cy="{BTN[1]-2}" rx="7" ry="3.5" fill="#ef9089" opacity="0.75"/></g>')
# drip tray
a('<rect x="158" y="662" width="188" height="24" rx="5" fill="#767d86"/>')
a('<g stroke="#4f555d" stroke-width="2">')
for gy in (668, 674, 680):
    a(f'<line x1="166" y1="{gy}" x2="338" y2="{gy}"/>')
a('</g>')
# group head
a('<rect x="232" y="602" width="100" height="34" rx="7" fill="#8f969f"/>')
a('<rect x="232" y="602" width="100" height="10" rx="5" fill="#aab1ba"/>')
a('<rect x="244" y="632" width="76" height="16" rx="5" fill="#6f767f"/>')
# portafilter locked under the group head, chunky handle out to the right
a('<path d="M262,676 L306,676 L316,644 L252,644 Z" fill="#4d545c"/>')
a('<rect x="246" y="638" width="82" height="10" rx="4" fill="#b3bac3"/>')
a('<rect x="254" y="644" width="66" height="6" rx="3" fill="#7c848d"/>')
a('<path d="M318,662 L442,695" stroke="#2f3339" stroke-width="17" stroke-linecap="round"/>')
a('<path d="M322,663 L340,668" stroke="#9aa2ac" stroke-width="11" stroke-linecap="round"/>')

# ------------------------------------------------------------ scale + cup ----
a('<ellipse cx="920" cy="708" rx="104" ry="16" fill="#4a2a12" opacity="0.22"/>')
a(f'<polygon points="{SX1},{SY0} {SX1+SDX},{SY0+SDY} {SX1+SDX},{SY1+SDY} {SX1},{SY1}" fill="#1d2126"/>')
a(f'<polygon points="{SX0},{SY0} {SX0+SDX},{SY0+SDY} {SX1+SDX},{SY0+SDY} {SX1},{SY0}" fill="#464d56"/>')
a(f'<rect x="{SX0}" y="{SY0}" width="{SX1-SX0}" height="{SY1-SY0}" rx="4" fill="#2b3037"/>')
a(f'<rect x="{SX0+26}" y="{SY0+5}" width="120" height="18" rx="3" fill="#0a1a0c"/>')
a('<text x="858" y="700" font-family="Consolas,monospace" font-size="15" font-weight="bold" '
  'fill="#7dff9b" letter-spacing="1">18.0 g</text>')
a('<circle cx="980" cy="698" r="7.5" fill="#6b727b"/><circle cx="980" cy="698" r="3.2" fill="#3a4046"/>')
a('<ellipse cx="920" cy="672" rx="46" ry="11" fill="#2a1a0c" opacity="0.25"/>')
a(f'<path d="M{CUPX-44},{CUPTOP} C{CUPX-38},638 {CUPX-32},656 {CUPX-28},{CUPBASE} '
  f'L{CUPX+28},{CUPBASE} C{CUPX+32},656 {CUPX+38},638 {CUPX+44},{CUPTOP} Z" fill="url(#cupShade)"/>')
a(f'<path d="M{CUPX+42},616 C{CUPX+82},618 {CUPX+82},652 {CUPX+40},654" fill="none" '
  f'stroke="#dfe3e8" stroke-width="12" stroke-linecap="round"/>')
a(f'<ellipse cx="{CUPX}" cy="{CUPTOP}" rx="44" ry="13" fill="#ffffff" stroke="#d5d9de" stroke-width="2"/>')
a(f'<ellipse cx="{CUPX}" cy="{CUPTOP+3}" rx="37" ry="10" fill="#6d3a1c"/>')
a(f'<ellipse cx="{CUPX-8}" cy="{CUPTOP+1}" rx="20" ry="5" fill="#a8673a" opacity="0.75"/>')

# ---------------------------------------------------------------- pitcher ----
# Local shape is upright with the spout at the top-left; rotate(-60) tips it to
# pour, so the spout lip becomes the lowest point of the rim.
a(f'<g transform="{PITCHER_XF}">')
a('<path d="M45,-38 C90,-32 90,24 42,32" fill="none" stroke="#c3cad3" stroke-width="12" '
  'stroke-linecap="round"/>')
a('<path d="M-45,-55 C-47,-15 -41,25 -34,50 C-30,62 30,62 34,50 C41,25 47,-15 45,-55 Z" '
  'fill="url(#jug)" stroke="#a9b1bb" stroke-width="2.5" stroke-linejoin="round"/>')
a('<path d="M-45,-55 L-70,-72 L-44,-40 Z" fill="#eef2f7" stroke="#a9b1bb" stroke-width="2.5" '
  'stroke-linejoin="round"/>')
a('<path d="M-22,-44 C-30,-14 -28,18 -24,42" fill="none" stroke="#ffffff" stroke-width="11" '
  'opacity="0.7" stroke-linecap="round"/>')
a('<ellipse cx="0" cy="-55" rx="45" ry="12" fill="#f8fafc" stroke="#a9b1bb" stroke-width="2.5"/>')
a('<ellipse cx="0" cy="-54" rx="36" ry="8" fill="#ccd6e1"/>')
a('</g>')

# ---------------------------------------------------------------- octopus ----
# Body first, then every arm on top, so each base reads as emerging from the mantle.
a(f'<path d="{BODY}" fill="url(#skin)" stroke="{OCT_EDGE}" stroke-width="3.5"/>')
a('<ellipse cx="556" cy="392" rx="42" ry="26" fill="#ffffff" opacity="0.22"/>')
a(f'<path d="M522,584 C562,598 638,598 680,582" fill="none" stroke="{OCT_DARK}" '
  f'stroke-width="7" opacity="0.3"/>')
for ex in (562, 642):
    a(f'<ellipse cx="{ex}" cy="448" rx="31" ry="33" fill="#ffffff" stroke="{OCT_EDGE}" stroke-width="3"/>')
    a(f'<circle cx="{ex+7}" cy="455" r="15" fill="#2b2018"/>')
    a(f'<circle cx="{ex+1}" cy="449" r="5" fill="#ffffff"/>')
a('<path d="M534,414 C548,404 578,404 590,414" fill="none" stroke="#a8491b" stroke-width="5" '
  'stroke-linecap="round"/>')
a('<path d="M614,414 C626,404 656,404 670,414" fill="none" stroke="#a8491b" stroke-width="5" '
  'stroke-linecap="round"/>')
a('<path d="M583,522 C600,534 620,534 637,522" fill="none" stroke="#a8491b" stroke-width="5" '
  'stroke-linecap="round"/>')
a('<ellipse cx="536" cy="492" rx="16" ry="9" fill="#d9532a" opacity="0.35"/>')
a('<ellipse cx="668" cy="492" rx="16" ry="9" fill="#d9532a" opacity="0.35"/>')

# ------------------------------------------------------------------- arms ----
for i, (pts, w0, w1) in enumerate(TENTACLES, 1):
    a(f'<path id="tentacle-{i}" d="{tentacle(pts, w0, w1)}" fill="{OCT}" stroke="{OCT_EDGE}" '
      f'stroke-width="3" stroke-linejoin="round"/>')
    tx, ty = pts[-1]
    a(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="{w1/2:.1f}" fill="{OCT}"/>')

# ------------------------------------------------------- milk stream / pour --
a('<path d="M900,486 C905,522 913,560 918,594" fill="none" stroke="url(#milk)" '
  'stroke-width="7.5" stroke-linecap="round"/>')
a('<path d="M899,492 C902,522 908,556 913,588" fill="none" stroke="#ffffff" '
  'stroke-width="2.5" stroke-linecap="round" opacity="0.9"/>')
a(f'<ellipse cx="918" cy="{CUPTOP+2}" rx="18" ry="6.5" fill="#fdfbf4" opacity="0.95"/>')
a(f'<ellipse cx="918" cy="{CUPTOP+3}" rx="11" ry="4" fill="#ffffff"/>')

a(f'<rect width="{W}" height="{H}" fill="url(#vig)" pointer-events="none"/>')
a('</svg>')

svg = "\n".join(s)
open("octopus_barista.svg", "w", encoding="utf-8").write(svg)
print("wrote octopus_barista.svg", len(svg), "bytes")
