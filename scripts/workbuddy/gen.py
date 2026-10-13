# -*- coding: utf-8 -*-
"""Generates a self-contained SVG: an octopus working as a barista in a coffee shop.
Tentacle outlines are computed from bezier centrelines with a width profile."""
import math

def bez(p, t):
    (x0,y0),(x1,y1),(x2,y2),(x3,y3) = p
    mt = 1-t
    a,b,c,d = mt*mt*mt, 3*mt*mt*t, 3*mt*t*t, t*t*t
    return (a*x0+b*x1+c*x2+d*x3, a*y0+b*y1+c*y2+d*y3)

def centerline(segs, per=18):
    pts=[]
    for si,seg in enumerate(segs):
        for i in range(per+1):
            if si>0 and i==0: continue
            pts.append(bez(seg, i/per))
    return pts

def arclen(pts):
    d=[0.0]
    for i in range(1,len(pts)):
        d.append(d[-1]+math.dist(pts[i],pts[i-1]))
    return d

def f(v): return ("%.1f" % v).rstrip('0').rstrip('.')

def arm(segs, w0, w1, p_exp=1.1, per=15):
    pts = centerline(segs, per)
    L = arclen(pts); tot = L[-1] or 1
    A=[];B=[];H=[]
    for i,p in enumerate(pts):
        s = L[i]/tot
        w = w0 + (w1-w0)*(s**p_exp)
        if i==0: t=(pts[1][0]-pts[0][0], pts[1][1]-pts[0][1])
        elif i==len(pts)-1: t=(pts[-1][0]-pts[-2][0], pts[-1][1]-pts[-2][1])
        else: t=(pts[i+1][0]-pts[i-1][0], pts[i+1][1]-pts[i-1][1])
        n = math.hypot(*t) or 1
        tx,ty = t[0]/n, t[1]/n
        nx,ny = -ty,tx
        A.append((p[0]+nx*w/2, p[1]+ny*w/2))
        B.append((p[0]-nx*w/2, p[1]-ny*w/2))
        H.append((p[0]+nx*w*0.28, p[1]+ny*w*0.28))
    d = "M %s,%s" % (f(A[0][0]),f(A[0][1]))
    for q in A[1:]: d += " L %s,%s" % (f(q[0]),f(q[1]))
    d += " A %s,%s 0 0 0 %s,%s" % (f(w1/2),f(w1/2),f(B[-1][0]),f(B[-1][1]))
    for q in reversed(B[:-1]): d += " L %s,%s" % (f(q[0]),f(q[1]))
    d += " Z"
    H2 = H[::2] + [H[-1]]
    hl = "M %s,%s" % (f(H2[0][0]),f(H2[0][1]))
    for q in H2[1:]: hl += " L %s,%s" % (f(q[0]),f(q[1]))
    return d, hl

HEAD  = dict(cx=560, cy=330, rx=106, ry=100)
SKIRT = dict(cx=562, cy=399, rx=110, ry=84)

# --------------------------------------------------------------- the 8 arms
#  1 point  : gestures at the wall clock
#  2 pour   : carries the milk pitcher (wrapped round its body)
#  3 porta  : holds the portafilter under the group head
#  4 press  : presses a button on the machine
#  5..8 four more arms, all visible
TENT = [
 dict(id="point",  w=(34,10), pe=2.0,
      segs=[((476.5,391.6),(462,340),(432,292),(356,250))]),
 dict(id="pour",   w=(38,20), pe=1.1,
      segs=[((497.7,410.9),(470,432),(430,450),(402,454))]),
 dict(id="spareL", w=(38,20), pe=1.15,
      segs=[((523.7,424),(512,472),(478,540),(455,592))]),
 dict(id="spareC", w=(38,20), pe=1.15,
      segs=[((550.8,429.6),(552,486),(572,548),(600,600))]),
 dict(id="spareR", w=(38,20), pe=1.15,
      segs=[((578.4,428.5),(592,482),(636,538),(706,584))]),
 dict(id="porta",  w=(40,22), pe=1.1,
      segs=[((606.5,419.9),(646,448),(700,490),(766,524))]),
 dict(id="press",  w=(36,18), pe=1.1,
      segs=[((628.1,406.6),(690,412),(770,388),(846,376))]),
 dict(id="spareU", w=(38,10), pe=1.5,
      segs=[((644.7,390.2),(676,346),(714,300),(722,264)),
            ((722,264),(724,236),(708,220),(688,220))]),
]
COL = {"spareU":"#7c4bb2","press":"#8756bd","porta":"#9161c7","spareR":"#8d5cc3",
       "spareC":"#9565ca","spareL":"#8d5cc3","pour":"#9e6ed4","point":"#a372d8"}

def arms_svg():
    out=[]
    for t_ in TENT:
        d,hl = arm(t_["segs"], t_["w"][0], t_["w"][1], t_["pe"])
        c = COL[t_["id"]]
        out.append('    <path d="%s" fill="%s" stroke="#3a1f4f" stroke-width="3.4" stroke-linejoin="round"/>' % (d,c))
        out.append('    <path d="%s" fill="none" stroke="#e0c6f6" stroke-width="3.4" stroke-linecap="round" opacity=".45"/>' % hl)
    return "\n".join(out)

WD, WHL = arm([((456,432),(424,450),(394,456),(364,446))], 30, 9, 1.2)
WRAP = ('<path d="%s" fill="#9e6ed4" stroke="#3a1f4f" stroke-width="3.4" stroke-linejoin="round"/>\n'
        '<path d="%s" fill="none" stroke="#e0c6f6" stroke-width="3.4" stroke-linecap="round" opacity=".45"/>') % (WD, WHL)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" width="1200" height="800">
<defs>
  <linearGradient id="wall" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f9eee2"/><stop offset="1" stop-color="#ead5c0"/>
  </linearGradient>
  <radialGradient id="glow" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="#fff6e8" stop-opacity=".9"/><stop offset="1" stop-color="#fff6e8" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="ctop" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#dbb083"/><stop offset=".55" stop-color="#c9975f"/><stop offset="1" stop-color="#b8824a"/>
  </linearGradient>
  <linearGradient id="cfront" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ab784c"/><stop offset="1" stop-color="#7b5130"/>
  </linearGradient>
  <linearGradient id="steel" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#eaecf1"/><stop offset=".42" stop-color="#c3c7d0"/><stop offset="1" stop-color="#989da7"/>
  </linearGradient>
  <linearGradient id="steelTop" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#f4f6fa"/><stop offset="1" stop-color="#c6cad3"/>
  </linearGradient>
  <linearGradient id="octo" x1=".2" y1="0" x2=".85" y2="1">
    <stop offset="0" stop-color="#c9a2ee"/><stop offset=".5" stop-color="#9763ce"/><stop offset="1" stop-color="#6d3da6"/>
  </linearGradient>
  <linearGradient id="skirtG" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#8d58c2"/><stop offset="1" stop-color="#6b3ba1"/>
  </linearGradient>
  <linearGradient id="cup" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="#f7f4ef"/><stop offset="1" stop-color="#dcd8d0"/>
  </linearGradient>
  <linearGradient id="milk" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fffdf9"/><stop offset="1" stop-color="#efdcc0"/>
  </linearGradient>
  <linearGradient id="scale" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#e6e9ef"/><stop offset="1" stop-color="#adb2bb"/>
  </linearGradient>
  <linearGradient id="hopper" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#cdac7b"/><stop offset=".5" stop-color="#a9834f"/><stop offset="1" stop-color="#83623a"/>
  </linearGradient>
  <linearGradient id="jug" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#f3f5f9"/><stop offset=".45" stop-color="#c9cdd6"/><stop offset="1" stop-color="#9297a1"/>
  </linearGradient>
  <radialGradient id="clock" cx=".42" cy=".38" r=".62">
    <stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#eaddc9"/>
  </radialGradient>
  <radialGradient id="lampglow" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="#ffdca6" stop-opacity=".8"/><stop offset="1" stop-color="#ffdca6" stop-opacity="0"/>
  </radialGradient>
</defs>

<!-- ===================== WALL ===================== -->
<rect x="0" y="0" width="1200" height="560" fill="url(#wall)"/>
<ellipse cx="560" cy="330" rx="450" ry="380" fill="url(#glow)"/>

<!-- ===================== WALL CLOCK ===================== -->
<g>
  <ellipse cx="193" cy="186" rx="99" ry="99" fill="#000" opacity=".08"/>
  <circle cx="185" cy="175" r="96" fill="#7c4c2c" stroke="#5a3620" stroke-width="4"/>
  <circle cx="185" cy="175" r="87" fill="#5f3823"/>
  <circle cx="185" cy="175" r="80" fill="url(#clock)" stroke="#d8c7b0" stroke-width="2.5"/>
  <g stroke="#5f3823" stroke-width="4" stroke-linecap="round">
    <line x1="185" y1="101" x2="185" y2="112"/>
    <line x1="185" y1="101" x2="185" y2="112" transform="rotate(30 185 175)"/>
    <line x1="185" y1="101" x2="185" y2="112" transform="rotate(60 185 175)"/>
    <line x1="185" y1="101" x2="185" y2="112" transform="rotate(90 185 175)"/>
    <line x1="185" y1="101" x2="185" y2="112" transform="rotate(120 185 175)"/>
    <line x1="185" y1="101" x2="185" y2="112" transform="rotate(150 185 175)"/>
    <line x1="185" y1="101" x2="185" y2="112" transform="rotate(180 185 175)"/>
    <line x1="185" y1="101" x2="185" y2="112" transform="rotate(210 185 175)"/>
    <line x1="185" y1="101" x2="185" y2="112" transform="rotate(240 185 175)"/>
    <line x1="185" y1="101" x2="185" y2="112" transform="rotate(270 185 175)"/>
    <line x1="185" y1="101" x2="185" y2="112" transform="rotate(300 185 175)"/>
    <line x1="185" y1="101" x2="185" y2="112" transform="rotate(330 185 175)"/>
  </g>
  <line x1="185" y1="175" x2="185" y2="145" stroke="#4a2a18" stroke-width="9" stroke-linecap="round" transform="rotate(305 185 175)"/>
  <line x1="185" y1="175" x2="185" y2="122" stroke="#4a2a18" stroke-width="6" stroke-linecap="round" transform="rotate(60 185 175)"/>
  <circle cx="185" cy="175" r="7.5" fill="#4a2a18"/><circle cx="185" cy="175" r="3.2" fill="#c8a06a"/>
</g>

<!-- ===================== PENDANT LAMP ===================== -->
<g>
  <circle cx="1046" cy="152" r="88" fill="url(#lampglow)"/>
  <line x1="1046" y1="0" x2="1046" y2="86" stroke="#4e3f38" stroke-width="4"/>
  <path d="M1046,84 L1094,142 L998,142 Z" fill="#bd7833" stroke="#3b2b30" stroke-width="3" stroke-linejoin="round"/>
  <ellipse cx="1046" cy="142" rx="48" ry="11" fill="#ffd9a0" stroke="#3b2b30" stroke-width="3"/>
  <path d="M1032,86 L1006,138" stroke="#e2a765" stroke-width="5" opacity=".8" fill="none"/>
</g>

<!-- ===================== COUNTER ===================== -->
<rect x="0" y="556" width="1200" height="60" fill="url(#ctop)"/>
<rect x="0" y="556" width="1200" height="9" fill="#8d6140" opacity=".45"/>
<rect x="0" y="610" width="1200" height="6" fill="#eacba8" opacity=".55"/>
<rect x="0" y="616" width="1200" height="184" fill="url(#cfront)"/>
<rect x="0" y="616" width="1200" height="9" fill="#c99a6b"/>
<g stroke="#6d4526" stroke-width="2" opacity=".35">
  <line x1="160" y1="628" x2="160" y2="800"/><line x1="420" y1="628" x2="420" y2="800"/>
  <line x1="680" y1="628" x2="680" y2="800"/><line x1="940" y1="628" x2="940" y2="800"/>
</g>

<!-- ============ ESPRESSO MACHINE (rests on the counter) ============ -->
<ellipse cx="946" cy="581" rx="176" ry="17" fill="#000" opacity=".16"/>
<polygon points="800,336 776,316 776,560 800,580" fill="#8b8f98" stroke="#33333b" stroke-width="3" stroke-linejoin="round"/>
<polygon points="800,336 1080,336 1056,316 776,316" fill="url(#steelTop)" stroke="#33333b" stroke-width="3" stroke-linejoin="round"/>
<rect x="800" y="336" width="280" height="244" fill="url(#steel)" stroke="#33333b" stroke-width="3"/>
<rect x="812" y="350" width="244" height="56" rx="7" fill="#3f434c" stroke="#2b2f36" stroke-width="2.5"/>
<circle cx="857" cy="377" r="16" fill="#8d2a1b" stroke="#2b2f36" stroke-width="2.5"/>
<circle cx="857" cy="375" r="14" fill="#e0472f" stroke="#2b2f36" stroke-width="2.5"/>
<circle cx="900" cy="378" r="13" fill="#e0a23c" stroke="#2b2f36" stroke-width="2.5"/>
<circle cx="1015" cy="378" r="26" fill="#f9f7f1" stroke="#2b2f36" stroke-width="2.5"/>
<path d="M1000,362 A19,19 0 0 1 1030,362" fill="none" stroke="#8b909a" stroke-width="2"/>
<line x1="1015" y1="378" x2="1025" y2="361" stroke="#2b2f36" stroke-width="2.6" stroke-linecap="round"/>
<circle cx="1015" cy="378" r="3.6" fill="#2b2f36"/>
<!-- group head -->
<rect x="846" y="416" width="112" height="56" rx="8" fill="#b7bbc4" stroke="#33333b" stroke-width="3"/>
<rect x="856" y="424" width="92" height="8" rx="3" fill="#8f949d" stroke="#33333b" stroke-width="2"/>
<circle cx="862" cy="454" r="4" fill="#7f848d"/><circle cx="942" cy="454" r="4" fill="#7f848d"/>
<ellipse cx="902" cy="470" rx="50" ry="13" fill="#8f949d" stroke="#33333b" stroke-width="3"/>
<ellipse cx="902" cy="470" rx="33" ry="8" fill="#65696f"/>
<!-- portafilter, locked up into the group head -->
<g>
  <line x1="879" y1="470" x2="786" y2="514" stroke="#33333b" stroke-width="22" stroke-linecap="round"/>
  <line x1="879" y1="470" x2="786" y2="514" stroke="#b9bec8" stroke-width="17" stroke-linecap="round"/>
  <line x1="872" y1="474" x2="792" y2="512" stroke="#e6e9ee" stroke-width="4" stroke-linecap="round" opacity=".7"/>
  <rect x="876" y="462" width="52" height="18" rx="4" fill="#d8dce3" stroke="#33333b" stroke-width="3"/>
  <rect x="886" y="474" width="32" height="22" fill="#b0b5be" stroke="#33333b" stroke-width="3"/>
  <line x1="893" y1="478" x2="893" y2="492" stroke="#8f949d" stroke-width="2.6"/>
  <line x1="902" y1="478" x2="902" y2="492" stroke="#8f949d" stroke-width="2.6"/>
  <line x1="911" y1="478" x2="911" y2="492" stroke="#8f949d" stroke-width="2.6"/>
  <ellipse cx="902" cy="496" rx="16" ry="5.5" fill="#9aa0aa" stroke="#33333b" stroke-width="2.5"/>
  <circle cx="778" cy="518" r="15" fill="#a3a8b1" stroke="#33333b" stroke-width="3"/>
  <circle cx="778" cy="518" r="5.5" fill="#7f848d"/>
</g>
<!-- drip tray / steam wand / bean hopper -->
<rect x="818" y="536" width="244" height="18" fill="#a8adb6" stroke="#33333b" stroke-width="3"/>
<g stroke="#767b84" stroke-width="2.2">
  <line x1="843" y1="539" x2="843" y2="551"/><line x1="873" y1="539" x2="873" y2="551"/>
  <line x1="903" y1="539" x2="903" y2="551"/><line x1="933" y1="539" x2="933" y2="551"/>
  <line x1="963" y1="539" x2="963" y2="551"/><line x1="993" y1="539" x2="993" y2="551"/>
  <line x1="1023" y1="539" x2="1023" y2="551"/>
</g>
<rect x="818" y="554" width="244" height="10" fill="#8d9199" stroke="#33333b" stroke-width="2.5"/>
<path d="M1076,468 C1098,498 1102,530 1090,552" fill="none" stroke="#33333b" stroke-width="13" stroke-linecap="round"/>
<path d="M1076,468 C1098,498 1102,530 1090,552" fill="none" stroke="#c3c7d0" stroke-width="9" stroke-linecap="round"/>
<circle cx="1089" cy="555" r="7" fill="#2b2f36" stroke="#33333b" stroke-width="2"/>
<polygon points="902,336 1006,336 982,316 878,316" fill="#a98b62" stroke="#33333b" stroke-width="3" stroke-linejoin="round"/>
<path d="M902,336 L1006,336 L990,272 Q988,262 976,262 L932,262 Q920,262 918,272 Z" fill="url(#hopper)" stroke="#33333b" stroke-width="3" stroke-linejoin="round"/>
<line x1="909" y1="308" x2="999" y2="308" stroke="#7a5d38" stroke-width="2.5" opacity=".8"/>
<ellipse cx="954" cy="262" rx="31" ry="9" fill="#8d6f4c" stroke="#33333b" stroke-width="2.5"/>
<g fill="#5d3f28" opacity=".85">
  <ellipse cx="936" cy="326" rx="7" ry="5" transform="rotate(-20 936 326)"/>
  <ellipse cx="956" cy="330" rx="7" ry="5" transform="rotate(15 956 330)"/>
  <ellipse cx="976" cy="324" rx="7" ry="5" transform="rotate(-10 976 324)"/>
  <ellipse cx="948" cy="312" rx="7" ry="5" transform="rotate(25 948 312)"/>
</g>

<!-- loose coffee beans on the counter top -->
<g fill="#6b4326" stroke="#452a17" stroke-width="2">
  <ellipse cx="1104" cy="600" rx="11" ry="7.5" transform="rotate(-18 1104 600)"/>
  <ellipse cx="1134" cy="604" rx="11" ry="7.5" transform="rotate(12 1134 604)"/>
  <ellipse cx="1163" cy="598" rx="11" ry="7.5" transform="rotate(-6 1163 598)"/>
  <ellipse cx="1128" cy="592" rx="11" ry="7.5" transform="rotate(24 1128 592)"/>
</g>
<g fill="none" stroke="#9c6b42" stroke-width="2">
  <path d="M1094,604 C1100,599 1108,598 1113,601"/>
  <path d="M1124,607 C1130,602 1138,602 1143,605"/>
  <path d="M1153,601 C1159,596 1167,595 1172,598"/>
  <path d="M1118,589 C1124,584 1132,584 1137,587"/>
</g>

<!-- ============ DIGITAL SCALE (stands on the countertop) ============ -->
<ellipse cx="318" cy="606" rx="112" ry="13" fill="#000" opacity=".16"/>
<polygon points="245,574 221,554 221,592 245,612" fill="#8e9199" stroke="#33333b" stroke-width="3" stroke-linejoin="round"/>
<polygon points="245,574 405,574 381,554 221,554" fill="url(#steelTop)" stroke="#33333b" stroke-width="3" stroke-linejoin="round"/>
<rect x="245" y="574" width="160" height="38" fill="url(#scale)" stroke="#33333b" stroke-width="3"/>
<rect x="286" y="580" width="78" height="26" rx="4" fill="#2b3a30" stroke="#33333b" stroke-width="2.5"/>
<g stroke="#86e39a" stroke-width="3" fill="none">
  <rect x="293" y="586" width="14" height="15" rx="3"/>
  <rect x="325" y="586" width="14" height="15" rx="3"/>
</g>
<rect x="314" y="597" width="4.5" height="4.5" fill="#86e39a"/>

<!-- ============ CUP standing directly on the scale ============ -->
<ellipse cx="318" cy="564" rx="50" ry="11" fill="#000" opacity=".18"/>
<ellipse cx="318" cy="487" rx="57" ry="15" fill="#4a3226" stroke="#33333b" stroke-width="2.5"/>
<ellipse cx="318" cy="499" rx="51" ry="13" fill="url(#milk)"/>
<ellipse cx="318" cy="504" rx="25" ry="7" fill="#fffdf6" opacity=".55"/>
<path d="M305,418 C300,452 312,474 314,506 L325,506 C325,474 315,452 318,418 Z"
      fill="url(#milk)" stroke="#e2d0b6" stroke-width="1.6"/>
<path d="M308,420 C303,450 313,472 316,502" stroke="#ffffff" stroke-width="2.4" fill="none" opacity=".9"/>
<path d="M256,486 L274,562 A 44,12 0 0 0 362,562 L380,486 A 62,17 0 0 1 256,486 Z"
      fill="url(#cup)" stroke="#33333b" stroke-width="3" stroke-linejoin="round"/>
<path d="M374,498 C410,494 416,540 376,548" fill="none" stroke="#33333b" stroke-width="17" stroke-linecap="round"/>
<path d="M374,498 C410,494 416,540 376,548" fill="none" stroke="#f4f1eb" stroke-width="12" stroke-linecap="round"/>

<!-- gesturing sight line toward the clock -->
<line x1="338" y1="242" x2="272" y2="214" stroke="#b98ae0" stroke-width="3" stroke-dasharray="9 11" stroke-linecap="round" opacity=".6"/>

<!-- ===================== EIGHT TENTACLES ===================== -->
{arms_svg()}

<!-- ===================== ARM WEB + HEAD ===================== -->
<ellipse cx="{SKIRT['cx']}" cy="{SKIRT['cy']}" rx="{SKIRT['rx']}" ry="{SKIRT['ry']}" fill="url(#skirtG)" stroke="#3a1f4f" stroke-width="3.4"/>
<path d="M560,230 C620,230 660,272 666,330 C670,378 640,420 560,430 C480,420 450,378 454,330 C460,272 500,230 560,230 Z"
      fill="url(#octo)" stroke="#3a1f4f" stroke-width="3.4"/>
<path d="M508,250 C470,268 456,300 456,330 C456,352 464,374 478,390 C468,360 470,300 508,250 Z" fill="#dcc2f5" opacity=".5"/>
<g fill="#6a3aa0" opacity=".4">
  <ellipse cx="524" cy="268" rx="11" ry="8" transform="rotate(-20 524 268)"/>
  <ellipse cx="576" cy="252" rx="9" ry="7" transform="rotate(15 576 252)"/>
  <ellipse cx="616" cy="292" rx="10" ry="8" transform="rotate(-30 616 292)"/>
  <ellipse cx="632" cy="344" rx="8" ry="11" transform="rotate(10 632 344)"/>
  <ellipse cx="590" cy="288" rx="7" ry="6"/>
  <ellipse cx="536" cy="238" rx="7" ry="5" transform="rotate(-8 536 238)"/>
</g>
<g>
  <ellipse cx="522" cy="322" rx="27" ry="28" fill="#ffffff" stroke="#3a1f4f" stroke-width="3.2"/>
  <ellipse cx="600" cy="314" rx="24" ry="25" fill="#ffffff" stroke="#3a1f4f" stroke-width="3.2"/>
  <ellipse cx="517" cy="326" rx="12" ry="13" fill="#2b1a38"/>
  <ellipse cx="595" cy="318" rx="11" ry="12" fill="#2b1a38"/>
  <circle cx="513" cy="320" r="4" fill="#ffffff"/>
  <circle cx="591" cy="312" r="3.6" fill="#ffffff"/>
  <path d="M499,306 C508,298 522,296 532,302" fill="none" stroke="#3a1f4f" stroke-width="3" stroke-linecap="round"/>
  <path d="M581,300 C590,292 604,292 614,298" fill="none" stroke="#3a1f4f" stroke-width="3" stroke-linecap="round"/>
  <path d="M540,384 C554,394 572,394 586,384" fill="none" stroke="#5f3490" stroke-width="3.4" stroke-linecap="round"/>
</g>

<!-- ============ MILK PITCHER, tilted, pouring into the cup ============ -->
<g transform="translate(416,448) rotate(-42)">
  <path d="M40,-84 C76,-80 76,-26 40,-22" fill="none" stroke="#3b2b30" stroke-width="16" stroke-linecap="round"/>
  <path d="M40,-84 C76,-80 76,-26 40,-22" fill="none" stroke="#bcc1cb" stroke-width="11" stroke-linecap="round"/>
  <path d="M-40,-90 L-28,-6 Q-26,0 -18,0 L18,0 Q26,0 28,-6 L40,-90 Z" fill="url(#jug)" stroke="#3b2b30" stroke-width="3.4" stroke-linejoin="round"/>
  <path d="M-44,-84 L-62,-99 L-32,-101 L-26,-92 Z" fill="#d3d7de" stroke="#3b2b30" stroke-width="3.4" stroke-linejoin="round"/>
  <ellipse cx="0" cy="-92" rx="40" ry="11" fill="#6f5a45" stroke="#3b2b30" stroke-width="3"/>
  <ellipse cx="0" cy="-90" rx="33" ry="8" fill="#fdf8ef"/>
  <path d="M-24,-80 C-18,-44 -16,-20 -14,-8" stroke="#ffffff" stroke-width="7" fill="none" opacity=".5"/>
</g>
<!-- the same tentacle closes round the pitcher's near side -->
{WRAP}
<circle cx="368" cy="445" r="3" fill="#e0c6f6" opacity=".7"/>
</svg>
'''

open("octopus_barista.svg","w",encoding="utf-8").write(svg)
print("bytes:", len(svg))
