import math, random
from helpers import *

W, H = 1600, 1000
X0, X1 = 430, 1180
BASE_Y = 860
SOIL_H = 42
SOIL_TOP = BASE_Y - SOIL_H
WL_REF = 520
WL_ALT = 560
GAUGE_Y = 300
LAND_TOP_CLEAR = 372  # highest point the landform is allowed to reach


def elev(x):
    t = (x - X0) / (X1 - X0)
    basin = 250 * math.sin(math.pi * t) ** 1.2
    texture = 7 * math.sin(6 * math.pi * t + 0.6) + 4 * math.sin(11 * math.pi * t + 2.0)
    return LAND_TOP_CLEAR + 18 + basin + texture


def icon_dam(x, y, s, color):
    return (f'<g transform="translate({x},{y})">'
            f'<rect x="{-4*s}" y="{-16*s}" width="{8*s}" height="{28*s}" fill="{color}"/>'
            f'<path d="M {-4*s},{-16*s} L {-4*s},{12*s} M {4*s},{-16*s} L {4*s},{12*s}" '
            f'stroke="{color}" stroke-width="0"/></g>')


def icon_pressure_set(x, y, s, color):
    """Small clean line-icon cluster used for each pressure item (unit glyph)."""
    return ""


def line_icon(kind, cx, cy, r, color):
    sw = max(1.6, r * 0.14)
    if kind == "dam":
        return (f'<rect x="{cx-r*0.32:.1f}" y="{cy-r*0.9:.1f}" width="{r*0.64:.1f}" height="{r*1.7:.1f}" '
                f'fill="none" stroke="{color}" stroke-width="{sw}"/>'
                f'<line x1="{cx-r*0.32:.1f}" y1="{cy+r*0.1:.1f}" x2="{cx+r*0.32:.1f}" y2="{cy+r*0.1:.1f}" '
                f'stroke="{color}" stroke-width="{sw}"/>')
    if kind == "diversion":
        return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*0.62:.1f}" fill="none" stroke="{color}" stroke-width="{sw}"/>'
                f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx+r*0.62:.1f}" y2="{cy:.1f}" stroke="{color}" stroke-width="{sw}"/>')
    if kind == "drainage":
        out = []
        for i in range(3):
            xx = cx - r*0.5 + i*r*0.5
            out.append(f'<line x1="{xx:.1f}" y1="{cy-r*0.8:.1f}" x2="{xx:.1f}" y2="{cy+r*0.8:.1f}" '
                        f'stroke="{color}" stroke-width="{sw}"/>')
        return "".join(out)
    if kind == "land":
        return (f'<rect x="{cx-r*0.75:.1f}" y="{cy-r*0.55:.1f}" width="{r*0.9:.1f}" height="{r*0.9:.1f}" '
                f'fill="none" stroke="{color}" stroke-width="{sw}"/>'
                f'<rect x="{cx-r*0.05:.1f}" y="{cy-r*0.15:.1f}" width="{r*0.9:.1f}" height="{r*0.9:.1f}" '
                f'fill="{color}" opacity="0.35"/>')
    if kind == "climate":
        out = [f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*0.5:.1f}" fill="none" stroke="{color}" stroke-width="{sw}"/>']
        for a in range(0, 360, 45):
            x1 = cx + r*0.68*math.cos(math.radians(a)); y1 = cy + r*0.68*math.sin(math.radians(a))
            x2 = cx + r*0.95*math.cos(math.radians(a)); y2 = cy + r*0.95*math.sin(math.radians(a))
            out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{sw}"/>')
        return "".join(out)
    if kind == "fragment":
        out = []
        for i in range(3):
            out.append(f'<rect x="{cx-r+i*r*0.8:.1f}" y="{cy-r*0.3:.1f}" width="{r*0.55:.1f}" height="{r*0.55:.1f}" '
                        f'fill="{color}" opacity="{0.95-0.28*i:.2f}"/>')
        return "".join(out)
    if kind == "clock":
        return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*0.62:.1f}" fill="none" stroke="{color}" stroke-width="{sw}"/>'
                f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx:.1f}" y2="{cy-r*0.42:.1f}" stroke="{color}" stroke-width="{sw}"/>'
                f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx+r*0.32:.1f}" y2="{cy:.1f}" stroke="{color}" stroke-width="{sw}"/>')
    if kind == "funcdown":
        return (f'<path d="M {cx-r*0.5:.1f},{cy-r*0.35:.1f} Q {cx-r*0.2:.1f},{cy+r*0.15:.1f} {cx+r*0.05:.1f},{cy-r*0.05:.1f} '
                f'Q {cx+r*0.3:.1f},{cy-r*0.2:.1f} {cx+r*0.5:.1f},{cy+r*0.35:.1f}" fill="none" stroke="{color}" stroke-width="{sw}"/>'
                f'<path d="M {cx+r*0.32:.1f},{cy+r*0.15:.1f} L {cx+r*0.5:.1f},{cy+r*0.35:.1f} L {cx+r*0.68:.1f},{cy+r*0.1:.1f}" '
                f'fill="none" stroke="{color}" stroke-width="{sw}"/>')
    return ""


def build(clean=False):
    body = []
    defs = [f'''
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{C["sky_top"]}"/>
      <stop offset="1" stop-color="{C["sky_bot"]}"/>
    </linearGradient>
    <linearGradient id="waterB" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{C["water_mid"]}"/>
      <stop offset="0.55" stop-color="{C["water_deep"]}"/>
      <stop offset="1" stop-color="#154A5A"/>
    </linearGradient>
    <linearGradient id="soil" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{C["mud_dark"]}"/>
      <stop offset="1" stop-color="#4C3D2C"/>
    </linearGradient>
    <linearGradient id="uplandGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{C["upland"]}"/>
      <stop offset="1" stop-color="#B7A876"/>
    </linearGradient>
    {arrow_marker_defs()}
    ''']

    body.append(f'<rect x="0" y="0" width="{W}" height="360" fill="url(#sky)"/>')

    top_pad = 0
    if not clean:
        body.append(text(W/2, 42, "HHTE  —  a process-based framework for wetland assessment", size=16.5,
                          weight="700", color=C["ink"], anchor="middle", letter_spacing="0.3"))
        body.append(text(W/2, 65, "Hydrology  →  Habitat  →  Trophic organization  →  Ecosystem functioning",
                          size=12.5, color=C["ink_soft"], anchor="middle", style="italic"))
        top_pad = 0

    # ================= MANAGEMENT LOOP (arc above the wetland) =================
    p0 = (1500, 262); p1 = (1140, 128); p2 = (460, 128); p3 = (100, 262)
    path = f"M {p0[0]},{p0[1]} C {p1[0]},{p1[1]} {p2[0]},{p2[1]} {p3[0]},{p3[1]}"
    body.append(f'<path d="{path}" stroke="{C["mgmt"]}" stroke-width="2.2" fill="none" '
                f'stroke-dasharray="1,8" stroke-linecap="round" marker-end="url(#arrowMgmt)" opacity="0.82"/>')
    for frac, lab in [(0.05, "MONITOR"), (0.34, "RESTORE"), (0.66, "MINIMIZE"), (0.94, "AVOID")]:
        t = frac
        x = (1-t)**3*p0[0]+3*(1-t)**2*t*p1[0]+3*(1-t)*t**2*p2[0]+t**3*p3[0]
        y = (1-t)**3*p0[1]+3*(1-t)**2*t*p1[1]+3*(1-t)*t**2*p2[1]+t**3*p3[1]
        body.append(text(x, y-9, lab, size=10, weight="700", color=C["mgmt"], anchor="middle", letter_spacing="0.4"))
    body.append(text(800, 108, "ADAPTIVE MANAGEMENT FEEDBACK", size=10, weight="700",
                      color=C["mgmt"], anchor="middle", letter_spacing="1.1"))
    if not clean:
        body.append(text(105, 240, "acts on pressures", size=9, color=C["mgmt"], anchor="middle", style="italic"))

    # ================= LEFT PANEL: pressures =================
    body.append(pill(28, 250, 340, 610, 10, "#FFFFFF", stroke="#E6E6DF", sw=1.2))
    body.append(text(56, 288, "PRESSURES", size=13.5, weight="700", color=C["pressure"], letter_spacing="0.8"))
    body.append(text(56, 306, "anthropogenic + climatic drivers", size=10.5, color=C["ink_soft"]))
    items = [("dam", "Dams, flow regulation"), ("diversion", "Water diversion, pumping"),
             ("drainage", "Drainage, reclamation"), ("land", "Land-use change"),
             ("climate", "Climate: rainfall extremes, sea-level rise")]
    py = 350
    for kind, lab in items:
        body.append(line_icon(kind, 68, py, 18, C["pressure"]))
        body.append(text(102, py+5, lab, size=11.6, color=C["ink"]))
        py += 46
    body.append(f'<line x1="300" y1="500" x2="365" y2="500" stroke="{C["pressure"]}" stroke-width="3" marker-end="url(#arrowMain)"/>')

    # ================= RIGHT PANEL: consequences =================
    body.append(pill(1232, 250, 340, 610, 10, "#FFFFFF", stroke="#E6E6DF", sw=1.2))
    body.append(text(1260, 288, "ECOLOGICAL CONSEQUENCES", size=13.5, weight="700", color=C["impact"], letter_spacing="0.5"))
    cons = [["Habitat simplification, loss of ecotones"], ["Reduced trophic redundancy"],
            ["Resource–consumer timing mismatch"], ["Waterbird decline across flyways"],
            ["Reduced C storage, nutrient retention,", "flood-water buffering"]]
    cy = 322
    for lines in cons:
        body.append(f'<circle cx="{1264}" cy="{cy-4}" r="2.6" fill="{C["impact"]}"/>')
        for j, ln in enumerate(lines):
            body.append(text(1274, cy + j*17, ln, size=11.4, color=C["ink"]))
        cy += 24 + 17 * (len(lines) - 1)
    iy = cy + 26
    body.append(line_icon("fragment", 1274, iy, 16, C["mud_dark"]))
    body.append(bird_silhouette(1330, iy, 1.0, color=C["ink_soft"]))
    body.append(bird_silhouette(1356, iy+8, 0.7, color="#BDB9AD"))
    body.append(line_icon("clock", 1400, iy, 16, C["impact"]))
    body.append(line_icon("funcdown", 1448, iy, 18, C["func"]))
    body.append(f'<line x1="1215" y1="500" x2="1150" y2="500" stroke="{C["impact"]}" stroke-width="3" marker-end="url(#arrowMain)"/>')

    # ================= CENTRAL WETLAND CROSS-SECTION =================
    N = 300
    xs = [X0 + (X1 - X0) * i / N for i in range(N + 1)]
    es = [elev(x) for x in xs]

    land_d = f"M {xs[0]:.1f},{es[0]:.1f} " + " ".join(f"L {x:.1f},{y:.1f}" for x, y in zip(xs[1:], es[1:]))
    land_d += f" L {xs[-1]:.1f},{BASE_Y} L {xs[0]:.1f},{BASE_Y} Z"
    body.append(f'<path d="{land_d}" fill="url(#uplandGrad)"/>')

    # subtle hypsometric contour lines for depth
    for dz in (40, 90, 140):
        cd = []
        started = False
        for x, y in zip(xs, es):
            yy = y + dz
            if yy < BASE_Y:
                cd.append(("M" if not started else "L", x, yy))
                started = True
            else:
                started = False
        if cd:
            d2 = " ".join(f"{c} {x:.1f},{y:.1f}" for c, x, y in cd)
            body.append(f'<path d="{d2}" stroke="#00000012" stroke-width="1" fill="none"/>')

    body.append(f'<rect x="{X0}" y="{SOIL_TOP}" width="{X1-X0}" height="{SOIL_H}" fill="url(#soil)"/>')
    body.append(f'<line x1="{X0}" y1="{SOIL_TOP}" x2="{X1}" y2="{SOIL_TOP}" stroke="#3A2E20" stroke-width="1" opacity="0.5"/>')

    seg = [(x, max(y, WL_ALT)) for x, y in zip(xs, es)]
    water_d = f"M {seg[0][0]:.1f},{WL_ALT} " + " ".join(f"L {x:.1f},{y:.1f}" for x, y in seg[1:])
    water_d += f" L {xs[-1]:.1f},{WL_ALT} Z"
    body.append(f'<path d="{water_d}" fill="url(#waterB)"/>')
    # water surface highlight
    surf = [(x, min(y, WL_ALT)) for x, y in zip(xs, es) if y >= WL_ALT - 2]
    if surf:
        d3 = "M " + " L ".join(f"{x:.1f},{WL_ALT:.1f}" for x, y in surf)
        body.append(f'<path d="{d3}" stroke="{C["water_light"]}" stroke-width="1.6" opacity="0.55" fill="none"/>')

    # mudflat fringe ticks
    for x, y in zip(xs, es):
        if WL_ALT - 14 <= y < WL_ALT + 16:
            body.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y+5:.1f}" stroke="{C["mud"]}" stroke-width="2.4" opacity="0.85"/>')

    # marsh vegetation belt
    random.seed(11)
    i = 0
    while i < N:
        x, y = xs[i], es[i]
        if WL_ALT - 62 <= y < WL_ALT - 14:
            reed_h = 16 + random.random() * 20
            op = 0.7 + 0.25 * random.random()
            body.append(f'<rect x="{x-2:.1f}" y="{y-reed_h:.1f}" width="4" height="{reed_h:.1f}" '
                        f'fill="{C["veg_mid"]}" opacity="{op:.2f}"/>')
            if i % 10 == 0:
                body.append(reed_cluster(x, y, n=4, spread=15, h=24 + random.random()*10, color=C["veg_dark"]))
        i += 2

    # reference water level (natural regime)
    body.append(f'<line x1="{X0}" y1="{WL_REF}" x2="{X1}" y2="{WL_REF}" stroke="{C["water_light"]}" '
                f'stroke-width="1.5" stroke-dasharray="2,5" opacity="0.9"/>')
    gx = X0 + (X1-X0) * 0.24
    if not clean:
        body.append(text(X0+8, WL_REF-8, "natural hydroperiod (reference)", size=9.5, color=C["water_deep"], style="italic"))
        body.append(text(gx+10, (WL_REF+WL_ALT)/2+3, "hydroperiod shift", size=9, color=C["water_pulse"], style="italic"))
    body.append(f'<line x1="{gx}" y1="{WL_REF}" x2="{gx}" y2="{WL_ALT}" stroke="{C["water_pulse"]}" stroke-width="1.3"/>')
    body.append(f'<path d="M {gx-4},{WL_REF+4} L {gx},{WL_REF} L {gx+4},{WL_REF+4}" fill="none" stroke="{C["water_pulse"]}" stroke-width="1.3"/>')
    body.append(f'<path d="M {gx-4},{WL_ALT-4} L {gx},{WL_ALT} L {gx+4},{WL_ALT-4}" fill="none" stroke="{C["water_pulse"]}" stroke-width="1.3"/>')

    # trophic icons within habitat zones
    troph_x = [X0+(X1-X0)*f for f in (0.40, 0.50, 0.60, 0.72)]
    for tx in troph_x:
        ty = max(WL_ALT + 8, elev(tx) + 8)
        body.append(algae_fleck(tx-12, ty-6, 1.1))
        body.append(algae_fleck(tx-3, ty-13, 0.9))
        body.append(fish_silhouette(tx+16, ty-8, 0.95, color="#2E4A50"))
    body.append(invert_dot(X0+(X1-X0)*0.30, WL_ALT+10, 1.2, color=C["trophic"]))
    body.append(invert_dot(X0+(X1-X0)*0.80, WL_ALT+12, 1.2, color=C["trophic"]))
    body.append(bird_silhouette(X0+(X1-X0)*0.33, elev(X0+(X1-X0)*0.33)-40, 1.3, color=C["ink"]))
    body.append(bird_silhouette(X0+(X1-X0)*0.84, elev(X0+(X1-X0)*0.84)-36, 1.15, color=C["ink"]))

    # ecosystem-function icons embedded in soil band
    ftxs = [X0+80, X0+(X1-X0)/2, X1-80]
    flabs = ["C", "N", "flood"]
    for fx, lab in zip(ftxs, flabs):
        fyc = SOIL_TOP + SOIL_H/2 + 2
        body.append(f'<circle cx="{fx}" cy="{fyc}" r="13" fill="#FFFFFF" opacity="0.16"/>')
        if lab == "flood":
            body.append(line_icon("funcdown", fx, fyc, 20, "#F2EFE7"))
        else:
            body.append(text(fx, fyc+4, lab, size=11.5, weight="700", color="#F2EFE7", anchor="middle"))
    if not clean:
        body.append(text(X0+6, BASE_Y+26, "ECOSYSTEM FUNCTIONING — carbon storage · nutrient retention · flood regulation",
                          size=11, color=C["ink_soft"], style="italic"))

    # zone labels, single clean row between the management loop and the gauge instruments
    label_y = 246
    body.append(text(X0+4, label_y, "HYDROLOGY", size=12, weight="700", color=C["water_deep"], letter_spacing="0.5"))
    body.append(text(X0+150, label_y, "HABITAT", size=12, weight="700", color=C["veg_dark"], letter_spacing="0.5"))
    body.append(text(X0+280, label_y, "TROPHIC LINKS", size=12, weight="700", color=C["trophic"], letter_spacing="0.5"))
    body.append(text(X1-4, label_y, "ECOSYSTEM FUNCTIONING", size=12, weight="700", color=C["func"],
                      anchor="end", letter_spacing="0.5"))

    # ================= ASSESSMENT: gauge instrument row =================
    pins = [
        (X0+(X1-X0)*0.14, "HVI", "hydroperiod\nvariability", WL_ALT),
        (X0+(X1-X0)*0.36, "HTR", "habitat\nturnover", elev(X0+(X1-X0)*0.36)),
        (X0+(X1-X0)*0.50, "CI", "functional\nconnectivity", WL_ALT-10),
        (X0+(X1-X0)*0.66, "TRP", "trophic\nredundancy", elev(X0+(X1-X0)*0.66)),
        (X0+(X1-X0)*0.92, "EFS", "eco-hydrological\nfeedback strength", SOIL_TOP),
    ]
    for gx, lab, sub, anchor_y in pins:
        sub1 = sub.split("\n")
        body.append(gauge(gx, GAUGE_Y, 24, 0.55, lab, sub1[0]))
        body.append(text(gx, GAUGE_Y+24+44, sub1[1], size=8.6, color=C["ink_soft"], anchor="middle"))
        body.append(f'<line x1="{gx:.1f}" y1="{GAUGE_Y+24:.1f}" x2="{gx:.1f}" y2="{anchor_y-4:.1f}" '
                    f'stroke="#B9B9B2" stroke-width="1.1" stroke-dasharray="1.5,3"/>')
        body.append(f'<circle cx="{gx:.1f}" cy="{anchor_y:.1f}" r="2.8" fill="{C["assess"]}"/>')
    # trigger threshold: a red tick directly on the EFS dial + one shared legend line
    trig_x, trig_y = pins[-1][0], GAUGE_Y
    trig_a = math.radians(-220 + (40 - -220) * 0.78)
    r_in, r_out = 24 - 3, 24 + 6
    tix1, tiy1 = trig_x + r_in*math.cos(trig_a), trig_y + r_in*math.sin(trig_a)
    tix2, tiy2 = trig_x + r_out*math.cos(trig_a), trig_y + r_out*math.sin(trig_a)
    body.append(f'<line x1="{tix1:.1f}" y1="{tiy1:.1f}" x2="{tix2:.1f}" y2="{tiy2:.1f}" '
                f'stroke="{C["trigger"]}" stroke-width="2.6"/>')
    if not clean:
        body.append(text(trig_x, GAUGE_Y+24+68, "red tick = management-trigger threshold",
                          size=8.6, color=C["trigger"], anchor="middle", style="italic"))

    if not clean:
        body.append(text(W/2, 968, "Process-based indicators (HVI · HTR · CI · TRP · EFS) are compared with management "
                          "triggers to activate an avoid – minimize – restore – monitor response.",
                          size=10.5, color=C["ink_soft"], anchor="middle", style="italic"))

    return svg_doc(W, H, "".join(body), "".join(defs))


if __name__ == "__main__":
    with open("out/final_full.svg", "w") as f:
        f.write(build(clean=False))
    with open("out/final_clean.svg", "w") as f:
        f.write(build(clean=True))
    print("wrote final_full.svg, final_clean.svg")
