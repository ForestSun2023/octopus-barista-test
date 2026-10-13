# -*- coding: utf-8 -*-
"""Audit: pairwise limb clearance + is every tight spot hidden by the arm web?"""
import math
import gen

HEAD, SKIRT = gen.HEAD, gen.SKIRT

def samples(t_):
    w0,w1 = t_["w"]; pe = t_["pe"]
    pts = gen.centerline(t_["segs"], 30)
    L = gen.arclen(pts); tot = L[-1]
    return [(p, w0+(w1-w0)*((L[i]/tot)**pe), L[i]/tot) for i,p in enumerate(pts)]

def inside_skirt(p):
    return ((p[0]-SKIRT['cx'])/SKIRT['rx'])**2 + ((p[1]-SKIRT['cy'])/SKIRT['ry'])**2 <= 1.0

S = {t_["id"]: samples(t_) for t_ in gen.TENT}
ids = [t_["id"] for t_ in gen.TENT]

print("%-8s %-22s %-14s %s" % ("id","root -> tip","width","len"))
for t_ in gen.TENT:
    s = S[t_["id"]]
    print("%-8s (%6.0f,%6.0f)->(%6.0f,%6.0f) %4.0f->%-4.0f %6.0f" % (
        t_["id"], s[0][0][0], s[0][0][1], s[-1][0][0], s[-1][0][1], s[0][1], s[-1][1],
        sum(math.dist(s[i][0],s[i-1][0]) for i in range(1,len(s)))))

print("\n%-9s %-9s %10s %10s  %s" % ("arm A","arm B","min gap","at","hidden by web?"))
visible_bad = 0
for i in range(len(ids)):
    for j in range(i+1, len(ids)):
        best=1e9; bp=None
        for (p1,w1,s1) in S[ids[i]]:
            for (p2,w2,s2) in S[ids[j]]:
                if min(s1,s2) < 0.16: continue      # web region
                g = math.dist(p1,p2) - (w1+w2)/2
                if g < best: best=g; bp=(p1,p2)
        hid = inside_skirt(bp[0]) or inside_skirt(bp[1])
        note = "hidden" if hid else ("NO  <-- VISIBLE CROWDING" if best < 16 else "n/a (clear)")
        if not hid and best < 14: visible_bad += 1
        print("%-9s %-9s %10.1f %10s  %s" % (ids[i], ids[j], best,
              "(%.0f,%.0f)"%bp[0], note))
print("\nvisible crowding problems:", visible_bad)

# sanity: arm tips must not stick through the counter front face
print("\nall tips on/above counter surface (y<=616):",
      all(S[t_["id"]][-1][0][1] <= 616 for t_ in gen.TENT))
