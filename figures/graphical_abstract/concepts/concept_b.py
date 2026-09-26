import math
from helpers import *

W, H = 1600, 950
X0, X1 = 430, 1170   # wetland cross-section extent
BASE_Y = 760          # bottom of cross-section block
WL_REF = 470          # reference (natural) water level y
WL_ALT = 500          # altered (current) water level y


def elev(x):
    """Ground-surface elevation profile (larger y = deeper / wetter ground)."""
    t = (x - X0) / (X1 - X0)
    basin = 230 * math.sin(math.pi * t) ** 1.15
    texture = 8 * math.sin(6 * math.pi * t + 0.7) + 5 * math.sin(11 * math.pi * t + 2.1)
    return 330 + basin + texture


def zone_of(x):
    e = elev(x)
    if e < WL_ALT - 55:
        return "upland"
    if e < WL_ALT - 12:
        return "marsh"
    if e < WL_ALT + 14:
        return "mudflat"
    return "water"


def build():
    body = []
    defs = [f'''
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{C["sky_top"]}"/>
      <stop offset="1" stop-color="{C["sky_bot"]}"/>
    </linearGradient>
    <linearGradient id="waterB" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{C["water_mid"]}"/>
      <stop offset="1" stop-color="{C["water_deep"]}"/>
    </linearGradient>
    <linearGradient id="soil" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{C["mud_dark"]}"/>
      <stop offset="1" stop-color="#5C4A34"/>
    </linearGradient>
    {arrow_marker_defs()}
    ''']

    body.append(f'<rect x="0" y="0" width="{W}" height="330" fill="url(#sky)"/>')

    # ---- kicker
    body.append(text(W/2, 44, "HHTE  —  a process-based wetland assessment framework", size=15,
                      weight="700", color=C["ink"], anchor="middle", letter_spacing="0.4"))
    body.append(text(W/2, 66, "Hydrology  →  Habitat  →  Trophic organization  →  Ecosystem functioning",
                      size=12.5, color=C["ink_soft"], anchor="middle", style="italic"))

    # ================= MANAGEMENT LOOP (arcs above the wetland) =================
    p0 = (1500, 250); p1 = (1150, 130); p2 = (450, 130); p3 = (100, 250)
    path = f"M {p0[0]},{p0[1]} C {p1[0]},{p1[1]} {p2[0]},{p2[1]} {p3[0]},{p3[1]}"
    body.append(f'<path d="{path}" stroke="{C["mgmt"]}" stroke-width="2.2" fill="none" '
                f'stroke-dasharray="1,8" stroke-linecap="round" marker-end="url(#arrowMgmt)" opacity="0.8"/>')
    for frac, lab in [(0.06, "MONITOR"), (0.36, "RESTORE"), (0.64, "MINIMIZE"), (0.92, "AVOID")]:
        t = frac
        x = (1-t)**3*p0[0]+3*(1-t)**2*t*p1[0]+3*(1-t)*t**2*p2[0]+t**3*p3[0]
        y = (1-t)**3*p0[1]+3*(1-t)**2*t*p1[1]+3*(1-t)*t**2*p2[1]+t**3*p3[1]
        body.append(text(x, y-10, lab, size=10, weight="700", color=C["mgmt"], anchor="middle", letter_spacing="0.4"))
    body.append(text(800, 108, "ADAPTIVE MANAGEMENT FEEDBACK", size=10.5, weight="700",
                      color=C["mgmt"], anchor="middle", letter_spacing="1"))

    # ================= LEFT PANEL: pressures =================
    body.append(pill(30, 260, 330, 500, 10, "#FFFFFF", stroke="#E3E3DC", sw=1.2))
    body.append(text(60, 296, "PRESSURES", size=13, weight="700", color=C["pressure"], letter_spacing="0.8"))
    body.append(text(60, 314, "anthropogenic + climatic drivers", size=10.5, color=C["ink_soft"]))
    py = 350
    items = [("dam", "Dams, flow regulation"), ("div", "Water diversion, pumping"),
             ("drain", "Drainage, reclamation"), ("land", "Land-use change"),
             ("clim", "Climate: rainfall extremes, sea-level rise")]
    for kind, lab in items:
        cy = py
        if kind == "dam":
            body.append(f'<rect x="52" y="{cy-14}" width="14" height="28" fill="{C["pressure"]}"/>')
            body.append(f'<line x1="66" y1="{cy}" x2="86" y2="{cy}" stroke="{C["pressure"]}" stroke-width="3"/>')
        elif kind == "div":
            body.append(f'<circle cx="60" cy="{cy}" r="9" fill="{C["pressure_lt"]}"/>')
            body.append(f'<line x1="69" y1="{cy}" x2="86" y2="{cy}" stroke="{C["pressure_lt"]}" stroke-width="3"/>')
        elif kind == "drain":
            for i in range(3):
                body.append(f'<line x1="{54+i*8}" y1="{cy-10}" x2="{54+i*8}" y2="{cy+10}" stroke="{C["pressure_lt"]}" stroke-width="2.4"/>')
        elif kind == "land":
            body.append(f'<rect x="52" y="{cy-9}" width="16" height="16" fill="none" stroke="{C["pressure"]}" stroke-width="2"/>')
            body.append(f'<rect x="68" y="{cy-3}" width="16" height="10" fill="{C["pressure_lt"]}"/>')
        else:
            body.append(f'<circle cx="60" cy="{cy}" r="10" fill="none" stroke="{C["pressure"]}" stroke-width="2.2"/>')
            for a in range(0, 360, 60):
                x1 = 60+13*math.cos(math.radians(a)); y1=cy+13*math.sin(math.radians(a))
                x2 = 60+18*math.cos(math.radians(a)); y2=cy+18*math.sin(math.radians(a))
                body.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{C["pressure"]}" stroke-width="1.8"/>')
        body.append(text(96, cy+4, lab, size=11.3, color=C["ink"]))
        py += 42
    body.append(f'<line x1="290" y1="500" x2="345" y2="500" stroke="{C["pressure"]}" stroke-width="3.2" marker-end="url(#arrowMain)"/>')

    # ================= RIGHT PANEL: consequences =================
    body.append(pill(1240, 260, 330, 500, 10, "#FFFFFF", stroke="#E3E3DC", sw=1.2))
    body.append(text(1270, 296, "ECOLOGICAL CONSEQUENCES", size=13, weight="700", color=C["impact"], letter_spacing="0.5"))
    cons = ["Habitat simplification, loss of ecotones", "Reduced trophic redundancy",
            "Resource–consumer timing mismatch", "Waterbird decline across flyways",
            "Reduced C storage, nutrient retention,", "and flood-water buffering"]
    cy2 = 336
    for c in cons:
        body.append(f'<circle cx="1274" cy="{cy2-4}" r="2.6" fill="{C["impact"]}"/>')
        body.append(text(1284, cy2, c, size=11.3, color=C["ink"]))
        cy2 += 24
    # small fragmented-habitat + declining bird glyph
    fy0 = cy2 + 20
    for i in range(4):
        body.append(f'<rect x="{1270+i*22}" y="{fy0}" width="14" height="14" fill="{C["mud"]}" opacity="{1.0-0.2*i}"/>')
    body.append(bird_silhouette(1420, fy0+6, 0.9, color=C["ink_soft"]))
    body.append(bird_silhouette(1445, fy0+12, 0.65, color="#C6C2B6"))
    body.append(f'<line x1="1225" y1="500" x2="1180" y2="500" stroke="{C["impact"]}" stroke-width="3.2" marker-end="url(#arrowMain)"/>')

    # ================= CENTRAL WETLAND CROSS-SECTION =================
    N = 260
    xs = [X0 + (X1 - X0) * i / N for i in range(N + 1)]
    es = [elev(x) for x in xs]

    # land mass (everything below surface elevation) as base earth colour
    land_d = f"M {xs[0]:.1f},{es[0]:.1f} " + " ".join(f"L {x:.1f},{y:.1f}" for x, y in zip(xs[1:], es[1:]))
    land_d += f" L {xs[-1]:.1f},{BASE_Y} L {xs[0]:.1f},{BASE_Y} Z"
    body.append(f'<path d="{land_d}" fill="{C["upland"]}"/>')

    # soil / root band at the very base -> ecosystem functioning layer
    soil_top = BASE_Y - 34
    body.append(f'<rect x="{X0}" y="{soil_top}" width="{X1-X0}" height="34" fill="url(#soil)"/>')

    # water body: fill between WL_ALT and elevation, wherever elevation > WL_ALT (basin)
    water_d = f"M {xs[0]:.1f},{WL_ALT}"
    seg = []
    for x, y in zip(xs, es):
        yy = max(y, WL_ALT)
        seg.append((x, yy))
    water_d = f"M {seg[0][0]:.1f},{WL_ALT} " + " ".join(f"L {x:.1f},{y:.1f}" for x, y in seg[1:])
    water_d += f" L {xs[-1]:.1f},{WL_ALT} Z"
    body.append(f'<path d="{water_d}" fill="url(#waterB)"/>')

    # mudflat tint: where elevation is between WL_ALT-12 and WL_ALT+14 (very shallow fringe), overlay tan
    for i in range(N):
        x, y = xs[i], es[i]
        if WL_ALT - 12 <= y < WL_ALT + 14:
            body.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y+6:.1f}" stroke="{C["mud"]}" stroke-width="3" opacity="0.9"/>')

    # marsh belt vegetation: where elevation between WL_ALT-55 and WL_ALT-12
    i = 0
    while i < N:
        x, y = xs[i], es[i]
        if WL_ALT - 55 <= y < WL_ALT - 12:
            reed_h = 24
            body.append(f'<rect x="{x-2.5:.1f}" y="{y-reed_h:.1f}" width="5" height="{reed_h:.1f}" '
                        f'fill="{C["veg_mid"]}" opacity="0.85"/>')
            if i % 9 == 0:
                body.append(reed_cluster(x, y, n=4, spread=16, h=28, color=C["veg_dark"]))
        i += 3

    # reference water level (natural regime) — thin dashed line, shows the hydroperiod shift
    body.append(f'<line x1="{X0}" y1="{WL_REF}" x2="{X1}" y2="{WL_REF}" stroke="{C["water_light"]}" '
                f'stroke-width="1.6" stroke-dasharray="2,5" opacity="0.9"/>')
    body.append(text(X0+6, WL_REF-6, "natural hydroperiod (reference)", size=9.5, color=C["water_deep"], style="italic"))
    body.append(text(X1-6, WL_ALT+16, "altered water level — drier, less variable", size=9.5,
                      color=C["water_pulse"], anchor="end", style="italic"))
    # gap hatch between the two levels near mid-basin to show the shift visually
    gx = X0 + (X1-X0)*0.30
    body.append(f'<line x1="{gx}" y1="{WL_REF}" x2="{gx}" y2="{WL_ALT}" stroke="{C["water_pulse"]}" stroke-width="1.4"/>')
    body.append(f'<path d="M {gx-4},{WL_REF+4} L {gx},{WL_REF} L {gx+4},{WL_REF+4}" fill="none" stroke="{C["water_pulse"]}" stroke-width="1.4"/>')
    body.append(f'<path d="M {gx-4},{WL_ALT-4} L {gx},{WL_ALT} L {gx+4},{WL_ALT-4}" fill="none" stroke="{C["water_pulse"]}" stroke-width="1.4"/>')

    # trophic icons placed within their habitat zone
    trophic_x = [X0+(X1-X0)*f for f in (0.42, 0.55, 0.68, 0.5)]
    for tx in trophic_x:
        ty = max(WL_ALT + 6, elev(tx) + 6)
        body.append(algae_fleck(tx-10, ty-4, 1.1))
        body.append(algae_fleck(tx-2, ty-10, 0.9))
        body.append(fish_silhouette(tx+14, ty-6, 0.85, color=C["ink_soft"]))
    body.append(invert_dot(X0+(X1-X0)*0.30, WL_ALT+8, 1.1))
    body.append(invert_dot(X0+(X1-X0)*0.74, WL_ALT+10, 1.1))
    body.append(bird_silhouette(X0+(X1-X0)*0.36, elev(X0+(X1-X0)*0.36)-34, 1.15, color=C["ink"]))
    body.append(bird_silhouette(X0+(X1-X0)*0.78, elev(X0+(X1-X0)*0.78)-30, 1.0, color=C["ink"]))

    # function icons in soil band
    ftxs = [X0+70, X0+(X1-X0)/2, X1-70]
    flabs = ["C", "N", "flood"]
    for fx, lab in zip(ftxs, flabs):
        fyc = soil_top + 17
        body.append(f'<circle cx="{fx}" cy="{fyc}" r="12.5" fill="#FFFFFF" opacity="0.18"/>')
        if lab == "flood":
            body.append(f'<path d="M {fx-7},{fyc+2} Q {fx-3},{fyc-5} {fx},{fyc+2} Q {fx+3},{fyc-5} {fx+7},{fyc+2}" '
                        f'stroke="#F2EFE7" stroke-width="2" fill="none"/>')
        else:
            body.append(text(fx, fyc+4, lab, size=11.5, weight="700", color="#F2EFE7", anchor="middle"))
    body.append(text(X0+6, BASE_Y+22, "ECOSYSTEM FUNCTIONING — carbon storage · nutrient retention · flood regulation",
                      size=11, color=C["ink_soft"], style="italic"))

    # zone labels (compact, integrated, not boxes) -- one clear row, no overlap with gauges/icons
    body.append(text(X0+10, 300, "HYDROLOGY", size=12, weight="700", color=C["water_deep"], letter_spacing="0.5"))
    body.append(text(X0+150, 300, "HABITAT MOSAIC", size=12, weight="700",
                      color=C["veg_dark"], letter_spacing="0.4"))
    body.append(text(X0+330, 300, "TROPHIC LINKS", size=12, weight="700",
                      color=C["trophic"], letter_spacing="0.4"))

    # ================= ASSESSMENT: gauge pins on the landscape =================
    pins = [
        (X0+(X1-X0)*0.20, WL_REF-30, "HVI", "hydroperiod var."),
        (X0+(X1-X0)*0.42, elev(X0+(X1-X0)*0.42)-70, "HTR", "habitat turnover"),
        (X0+(X1-X0)*0.58, WL_ALT-55, "CI", "connectivity"),
        (X0+(X1-X0)*0.72, elev(X0+(X1-X0)*0.72)-72, "TRP", "trophic redundancy"),
        (X0+(X1-X0)*0.90, soil_top-46, "EFS", "eco-hydro feedback"),
    ]
    for gx, gy, lab, sub in pins:
        anchor_y = gy + 34
        body.append(f'<line x1="{gx:.1f}" y1="{gy+22:.1f}" x2="{gx:.1f}" y2="{anchor_y:.1f}" '
                    f'stroke="#B9B9B2" stroke-width="1.2" stroke-dasharray="1.5,3"/>')
        body.append(f'<circle cx="{gx:.1f}" cy="{anchor_y:.1f}" r="2.6" fill="{C["assess"]}"/>')
        body.append(gauge(gx, gy, 19, 0.55, lab, sub))
    # trigger flag on EFS
    tgx, tgy = pins[-1][0], pins[-1][1]
    body.append(f'<line x1="{tgx+15:.1f}" y1="{tgy-14:.1f}" x2="{tgx+15:.1f}" y2="{tgy-24:.1f}" stroke="{C["trigger"]}" stroke-width="3"/>')
    body.append(text(tgx+20, tgy-16, "trigger exceeded", size=8.6, color=C["trigger"], style="italic"))

    return svg_doc(W, H, "".join(body), "".join(defs))


if __name__ == "__main__":
    with open("out/concept_b.svg", "w") as f:
        f.write(build())
    print("wrote concept_b.svg")
