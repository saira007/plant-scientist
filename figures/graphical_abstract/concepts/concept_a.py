import math
from helpers import *

W, H = 1600, 950

def build():
    body = []
    defs = []

    defs.append(f'''
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{C["sky_top"]}"/>
      <stop offset="1" stop-color="{C["sky_bot"]}"/>
    </linearGradient>
    <linearGradient id="waterA" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{C["water_mid"]}"/>
      <stop offset="1" stop-color="{C["water_deep"]}"/>
    </linearGradient>
    {arrow_marker_defs()}
    ''')

    body.append(f'<rect x="0" y="0" width="{W}" height="460" fill="url(#sky)"/>')

    # ---- kicker
    body.append(pill(50, 34, 230, 30, 15, "#FFFFFF", stroke="#DADAD4", sw=1.2))
    body.append(text(165, 54, "HHTE FRAMEWORK", size=12.5, weight="700",
                      color=C["ink_soft"], anchor="middle", letter_spacing="1.3"))
    body.append(text(800, 54, "Hydrological alteration reorganizes wetland habitat, trophic structure and function",
                      size=13, color=C["ink_soft"], anchor="middle", style="italic"))

    ground_y = 420

    # ================= LEFT: pressures on upland =================
    body.append(f'<rect x="0" y="{ground_y}" width="380" height="{H-ground_y}" fill="{C["upland"]}"/>')
    # plowed field texture (below the pressures label, decorative only)
    for i in range(6):
        yy = ground_y + 78 + i * 20
        body.append(f'<line x1="30" y1="{yy}" x2="330" y2="{yy}" stroke="{C["mud_dark"]}" stroke-width="2" opacity="0.22"/>')
    # dam icon
    body.append(pill(150, ground_y - 92, 26, 92, 3, C["pressure"]))
    body.append(text(163, ground_y - 100, "dam / flow reg.", size=10.5, color=C["ink_soft"], anchor="middle"))
    # pump / diversion
    body.append(f'<circle cx="255" cy="{ground_y-40}" r="14" fill="{C["pressure_lt"]}"/>')
    body.append(f'<rect x="249" y="{ground_y-40}" width="30" height="6" fill="{C["pressure_lt"]}"/>')
    body.append(text(255, ground_y - 62, "diversion / pumping", size=10.5, color=C["ink_soft"], anchor="middle"))
    # climate glyph (sun + erratic drop)
    body.append(f'<circle cx="90" cy="{ground_y-120}" r="16" fill="none" stroke="{C["pressure"]}" stroke-width="2.4"/>')
    for a in range(0, 360, 45):
        x1 = 90 + 22*math.cos(math.radians(a)); y1 = (ground_y-120) + 22*math.sin(math.radians(a))
        x2 = 90 + 30*math.cos(math.radians(a)); y2 = (ground_y-120) + 30*math.sin(math.radians(a))
        body.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{C["pressure"]}" stroke-width="2"/>')
    body.append(text(90, ground_y-152, "climate change", size=10.5, color=C["ink_soft"], anchor="middle"))
    body.append(text(190, ground_y + 34, "DRIVERS & PRESSURES", size=13, weight="700",
                      color=C["pressure"], anchor="middle", letter_spacing="0.6"))

    # ================= RIVER / WETLAND STRIP (hydrology -> habitat) ====
    def top1(x):
        # calm regular wave near pressures, becoming disrupted mid-strip
        t = min(max((x-380)/700, 0), 1)
        amp = 10 + 26*abs(math.sin(t*9)) * (0.4+0.6*t)
        return 430 + 8*math.sin(x/40) - amp*0.15
    x0, x1 = 380, 1180
    top_y, bot_y = 260, 500
    body.append(f'<rect x="{x0}" y="{top_y}" width="{x1-x0}" height="{bot_y-top_y}" fill="url(#waterA)"/>')
    # hydrology signal: faint regular reference vs. bold irregular altered pulse
    ref_wave = wave_path(x0+10, x1-10, top_y+22, 6, 70, n=240)
    body.append(f'<path d="{ref_wave}" stroke="{C["water_light"]}" stroke-width="1.4" fill="none" stroke-dasharray="2,5" opacity="0.75"/>')
    # altered signal: piecewise -- drought flats + sharp flood pulses (visually irregular)
    segs = []
    xx = x0 + 10
    yb = top_y + 44
    import random as _r
    _r.seed(3)
    pts = [(xx, yb)]
    while xx < x1 - 20:
        kind = _r.choice(["flat", "spike", "spike", "dip"])
        seglen = _r.randint(60, 130)
        if kind == "flat":
            xx2 = min(xx + seglen, x1-10)
            pts.append((xx2, yb))
        elif kind == "spike":
            xm = xx + seglen*0.4
            xx2 = min(xx + seglen, x1-10)
            pts.append((xm, yb - _r.randint(26, 46)))
            pts.append((xx2, yb))
        else:
            xm = xx + seglen*0.4
            xx2 = min(xx + seglen, x1-10)
            pts.append((xm, yb + _r.randint(10, 20)))
            pts.append((xx2, yb))
        xx = xx2
    d = "M " + " L ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    body.append(f'<path d="{d}" stroke="{C["water_pulse"]}" stroke-width="3" fill="none" '
                f'stroke-linecap="round" stroke-linejoin="round" opacity="0.95"/>')
    body.append(text(x0+10, top_y-12, "HYDROLOGY  —  altered timing, magnitude, connectivity", size=12.5,
                      weight="700", color=C["water_deep"]))

    # habitat mosaic patches along the strip bottom half
    mosaic = [
        (x0+40, "marsh"), (x0+150, "mud"), (x0+260, "open"), (x0+380, "marsh"),
        (x0+500, "mud"), (x0+620, "open"), (x0+700, "marsh"),
    ]
    for mx, kind in mosaic:
        w = 92
        if kind == "marsh":
            body.append(f'<rect x="{mx}" y="{bot_y-46}" width="{w}" height="46" fill="{C["veg_mid"]}" opacity="0.92"/>')
            body.append(reed_cluster(mx+w/2, bot_y-46, n=6, spread=w*0.8, h=30, color=C["veg_dark"]))
        elif kind == "mud":
            body.append(f'<rect x="{mx}" y="{bot_y-30}" width="{w}" height="30" fill="{C["mud"]}" opacity="0.9"/>')
        else:
            body.append(f'<rect x="{mx}" y="{bot_y-38}" width="{w}" height="38" fill="{C["water_light"]}" opacity="0.55"/>')

    body.append(text(x0+40, bot_y+26, "HABITAT  —  marsh / mudflat / open-water mosaic", size=12.5,
                      weight="700", color=C["veg_dark"]))

    # trophic icons above mosaic, three stacks
    for i, tx in enumerate([x0+150, x0+430, x0+660]):
        body.append(algae_fleck(tx-14, bot_y-70, 1.3))
        body.append(algae_fleck(tx-6, bot_y-76, 1.0))
        body.append(invert_dot(tx+6, bot_y-72, 1.1))
        body.append(fish_silhouette(tx+30, bot_y-80, 0.9, color=C["ink_soft"]))
        if i < 2:
            body.append(bird_silhouette(tx+55, bot_y-118, 1.1, color=C["ink"]))
    body.append(text(x0+40, bot_y-96, "TROPHIC ORGANIZATION", size=12.5, weight="700",
                      color=C["trophic"], anchor="start"))

    # ecosystem functioning icon row just under water strip
    fy = bot_y + 56
    fx = x0 + 40
    func_icons = ["C", "N", "flood"]
    for i, lab in enumerate(func_icons):
        cx_i = fx + i * 46
        body.append(f'<circle cx="{cx_i}" cy="{fy}" r="15" fill="{C["func"]}" opacity="0.16"/>')
        if lab == "flood":
            body.append(f'<path d="M {cx_i-8},{fy+2} Q {cx_i-4},{fy-6} {cx_i},{fy+2} '
                        f'Q {cx_i+4},{fy-6} {cx_i+8},{fy+2}" stroke="{C["func"]}" stroke-width="2" fill="none"/>')
        else:
            body.append(text(cx_i, fy+5, lab, size=13, weight="700", color=C["func"], anchor="middle"))
    body.append(text(fx+150, fy+5, "ECOSYSTEM FUNCTIONING — carbon, nutrients, flood regulation",
                      size=12.5, weight="700", color=C["func"]))

    # ================= RIGHT: consequences =================
    ry = 290
    body.append(text(1200, ry-40, "ECOLOGICAL CONSEQUENCES", size=13, weight="700",
                      color=C["impact"], anchor="start"))
    cons = ["Habitat simplification, loss of ecotones", "Reduced trophic redundancy",
            "Resource–consumer timing mismatch", "Waterbird decline across flyways",
            "Reduced C storage, nutrient retention, flood buffering"]
    for i, c in enumerate(cons):
        yy = ry - 6 + i*30
        body.append(f'<circle cx="1204" cy="{yy-5}" r="3" fill="{C["impact"]}"/>')
        body.append(text(1216, yy, c, size=11.8, color=C["ink"]))
    # fragmented habitat + declining birds glyph
    for i in range(3):
        body.append(f'<rect x="{1200+i*34}" y="{ry+150}" width="22" height="16" fill="{C["mud"]}" opacity="{0.9-0.25*i}"/>')
    body.append(bird_silhouette(1330, ry+150, 1.0, color=C["ink_soft"]))
    body.append(bird_silhouette(1360, ry+158, 0.7, color="#B8B4AA"))

    # ================= ASSESSMENT BAND =================
    ay = 640
    body.append(pill(50, ay, W-100, 150, 16, C["assess_bg"], stroke="#DDDDD6", sw=1.4))
    body.append(text(80, ay+30, "PROCESS-BASED ASSESSMENT", size=13, weight="700",
                      color=C["assess"], letter_spacing="0.5"))
    gauges = [
        (170, "HVI", "hydroperiod var.", 0.72),
        (420, "HTR", "habitat turnover", 0.58),
        (680, "CI", "connectivity", 0.4),
        (940, "TRP", "trophic redundancy", 0.3),
        (1200, "EFS", "eco-hydro feedback", 0.45),
    ]
    for gx, lab, sub, frac in gauges:
        body.append(gauge(gx, ay+78, 30, frac, lab, sub))
    body.append(f'<line x1="1200" y1="{ay+48}" x2="1200" y2="{ay+38}" stroke="{C["trigger"]}" stroke-width="3"/>')
    body.append(text(1200+52, ay+40, "vs. trigger", size=9.5, color=C["trigger"], style="italic"))

    # ================= MANAGEMENT LOOP =================
    loop_y0 = ay + 150 + 14
    my = 900
    path = f"M 1480,{loop_y0} C 1250,{my} 500,{my} 170,{loop_y0}"
    body.append(f'<path d="{path}" stroke="{C["mgmt"]}" stroke-width="2.6" fill="none" '
                f'stroke-dasharray="1,9" stroke-linecap="round" marker-end="url(#arrowMgmt)" opacity="0.85"/>')
    p0 = (1480, loop_y0); p1 = (1250, my); p2 = (500, my); p3 = (170, loop_y0)
    for frac, lab in [(0.1, "MONITOR"), (0.36, "RESTORE"), (0.64, "MINIMIZE"), (0.9, "AVOID")]:
        t = frac
        x = (1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] + 3*(1-t)*t**2*p2[0] + t**3*p3[0]
        y = (1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] + 3*(1-t)*t**2*p2[1] + t**3*p3[1]
        body.append(text(x, y+18, lab, size=10.5, weight="700", color=C["mgmt"], anchor="middle", letter_spacing="0.5"))
    body.append(text(800, ay+178, "ADAPTIVE MANAGEMENT FEEDBACK", size=11, weight="700",
                      color=C["mgmt"], anchor="middle", letter_spacing="1"))

    return svg_doc(W, H, "".join(body), "".join(defs))


if __name__ == "__main__":
    with open("out/concept_a.svg", "w") as f:
        f.write(build())
    print("wrote concept_a.svg")
