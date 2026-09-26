import math, random
from helpers import *

W, H = 1600, 950
Y0 = 430  # ribbon baseline


def build():
    body = []
    defs = [arrow_marker_defs()]
    body.append(text(W/2, 50, "HHTE  —  a process-based wetland assessment framework", size=15,
                      weight="700", color=C["ink"], anchor="middle", letter_spacing="0.4"))
    body.append(text(W/2, 72, "hydrological alteration propagates into habitat, trophic and functional change",
                      size=12.5, color=C["ink_soft"], anchor="middle", style="italic"))

    # ---------- pressures (above ribbon, left) ----------
    body.append(text(150, 150, "PRESSURES", size=12.5, weight="700", color=C["pressure"], letter_spacing="0.6"))
    icons_x = [150, 210, 270, 330]
    for ix in icons_x:
        body.append(f'<circle cx="{ix}" cy="190" r="12" fill="none" stroke="{C["pressure"]}" stroke-width="2"/>')
        body.append(f'<line x1="{ix}" y1="204" x2="{ix}" y2="{Y0-30}" stroke="{C["pressure"]}" stroke-width="1.6" '
                    f'stroke-dasharray="2,3" marker-end="url(#arrowMain)"/>')
    body.append(text(150, 235, "dams · diversion · drainage · climate", size=10, color=C["ink_soft"]))

    # ---------- main ribbon ----------
    # phase 1: natural reference (thin dashed, regular)
    ref = wave_path(150, 380, Y0, 16, 66, n=160)
    body.append(f'<path d="{ref}" stroke="{C["water_light"]}" stroke-width="2" fill="none" stroke-dasharray="2,5" opacity="0.85"/>')
    nat = wave_path(150, 380, Y0, 20, 66, n=160)
    body.append(f'<path d="{nat}" stroke="{C["water_mid"]}" stroke-width="4" fill="none" stroke-linecap="round" opacity="0.95"/>')

    # phase 2: altered / erratic (380-950)
    random.seed(7)
    pts = [(380, Y0)]
    xx = 380
    while xx < 950:
        seglen = random.randint(50, 110)
        xx2 = min(xx + seglen, 950)
        kind = random.choice(["spike", "flat", "dip", "spike"])
        xm = xx + (xx2 - xx) * 0.45
        if kind == "spike":
            pts.append((xm, Y0 - random.randint(34, 58)))
        elif kind == "dip":
            pts.append((xm, Y0 + random.randint(20, 38)))
        else:
            pts.append((xm, Y0))
        pts.append((xx2, Y0))
        xx = xx2
    d = "M " + " L ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    body.append(f'<path d="{d}" stroke="{C["water_pulse"]}" stroke-width="4.6" fill="none" '
                f'stroke-linecap="round" stroke-linejoin="round"/>')

    # phase 3: fragmenting (950-1180)
    for i in range(6):
        x1 = 950 + i * 40
        x2 = x1 + 24
        yy = Y0 + (8 if i % 2 else -8)
        body.append(f'<line x1="{x1}" y1="{yy}" x2="{x2}" y2="{yy}" stroke="{C["water_pulse"]}" '
                    f'stroke-width="{4.2 - i*0.3:.1f}" stroke-linecap="round" opacity="{max(0.25,1-i*0.14):.2f}"/>')

    body.append(text(150, Y0-40, "HYDROLOGY", size=12, weight="700", color=C["water_deep"]))

    # ---------- habitat sprouts growing from the altered ribbon ----------
    for i, xx in enumerate(range(410, 940, 46)):
        side = 1 if i % 2 == 0 else -1
        base_y = Y0 + side * 10
        if i % 3 == 0:
            reed_h = 30
            body.append(f'<rect x="{xx-2:.1f}" y="{base_y - (reed_h if side>0 else 0):.1f}" width="4" '
                        f'height="{reed_h}" fill="{C["veg_mid"]}" opacity="0.9"/>')
        elif i % 3 == 1:
            body.append(f'<rect x="{xx-9:.1f}" y="{base_y + (0 if side>0 else -14):.1f}" width="18" height="14" '
                        f'fill="{C["mud"]}" opacity="0.85"/>')
        else:
            body.append(shrub(xx, base_y - side*18, r=12, color=C["veg_light"]))
    body.append(text(430, Y0+110, "HABITAT  —  mosaic emerging from the altered signal", size=12,
                      weight="700", color=C["veg_dark"]))

    # ---------- trophic nodes along the ribbon ----------
    troph_x = [520, 650, 780]
    prev = None
    for tx in troph_x:
        ty = Y0 - 70
        body.append(algae_fleck(tx-16, ty+6, 1.1))
        body.append(invert_dot(tx, ty, 1.1))
        body.append(fish_silhouette(tx+22, ty-6, 0.9, color=C["ink_soft"]))
        body.append(bird_silhouette(tx+10, ty-34, 1.0, color=C["ink"]))
        if prev:
            body.append(f'<line x1="{prev}" y1="{ty}" x2="{tx}" y2="{ty}" stroke="{C["trophic"]}" '
                        f'stroke-width="1.2" stroke-dasharray="1,4" opacity="0.7"/>')
        prev = tx
    body.append(text(520, Y0-108, "TROPHIC ORGANIZATION", size=12, weight="700", color=C["trophic"]))

    # ---------- ecosystem function band beneath ----------
    body.append(f'<rect x="410" y="{Y0+130}" width="520" height="26" rx="13" fill="{C["func"]}" opacity="0.14"/>')
    flabs = ["C", "N", "flood"]
    for i, lab in enumerate(flabs):
        fx = 440 + i * 60
        fy = Y0 + 143
        if lab == "flood":
            body.append(f'<path d="M {fx-7},{fy+3} Q {fx-3},{fy-4} {fx},{fy+3} Q {fx+3},{fy-4} {fx+7},{fy+3}" '
                        f'stroke="{C["func"]}" stroke-width="2" fill="none"/>')
        else:
            body.append(text(fx, fy+4, lab, size=11.5, weight="700", color=C["func"], anchor="middle"))
    body.append(text(600, Y0+180, "ECOSYSTEM FUNCTIONING — carbon · nutrients · flood buffering",
                      size=11, color=C["ink_soft"], style="italic"))

    # ---------- consequences ----------
    body.append(text(1220, Y0-108, "ECOLOGICAL CONSEQUENCES", size=12.5, weight="700", color=C["impact"]))
    cons = ["Habitat simplification, loss of ecotones", "Reduced trophic redundancy",
            "Resource–consumer timing mismatch", "Waterbird decline across flyways",
            "Reduced C storage, nutrient retention, flood buffering"]
    cy = Y0 - 78
    for c in cons:
        body.append(f'<circle cx="1224" cy="{cy-4}" r="2.6" fill="{C["impact"]}"/>')
        body.append(text(1234, cy, c, size=11.2, color=C["ink"]))
        cy += 24
    body.append(bird_silhouette(1230, Y0+50, 0.85, color=C["ink_soft"]))
    body.append(bird_silhouette(1255, Y0+58, 0.6, color="#C6C2B6"))
    for i in range(3):
        body.append(f'<rect x="{1300+i*20}" y="{Y0+46}" width="13" height="13" fill="{C["mud"]}" opacity="{0.9-0.25*i}"/>')

    # ---------- assessment ticks on ribbon ----------
    pins = [(380, Y0, "HVI"), (560, Y0-30, "HTR"), (720, Y0+22, "CI"),
            (860, Y0-24, "TRP"), (950, Y0+150, "EFS")]
    for gx, gy, lab in pins:
        body.append(gauge(gx, gy-70, 16, 0.55, lab, None))
        body.append(f'<line x1="{gx}" y1="{gy-52}" x2="{gx}" y2="{gy-6}" stroke="#B9B9B2" stroke-width="1.1" stroke-dasharray="1.5,3"/>')
        body.append(f'<circle cx="{gx}" cy="{gy}" r="2.4" fill="{C["assess"]}"/>')
    body.append(f'<line x1="866" y1="{Y0-140}" x2="866" y2="{Y0-150}" stroke="{C["trigger"]}" stroke-width="3"/>')
    body.append(text(872, Y0-142, "trigger exceeded", size=8.6, color=C["trigger"], style="italic"))

    # ---------- management ribbon (return path) ----------
    my = 760
    p0 = (1350, my); p1 = (1000, my+70); p2 = (500, my+70); p3 = (170, my)
    path = f"M {p0[0]},{p0[1]} C {p1[0]},{p1[1]} {p2[0]},{p2[1]} {p3[0]},{p3[1]}"
    body.append(f'<path d="{path}" stroke="{C["mgmt"]}" stroke-width="2.6" fill="none" '
                f'stroke-dasharray="1,8" stroke-linecap="round" marker-end="url(#arrowMgmt)" opacity="0.85"/>')
    body.append(f'<line x1="1350" y1="{my}" x2="1350" y2="{Y0+165}" stroke="{C["mgmt"]}" stroke-width="1.6" stroke-dasharray="2,4"/>')
    body.append(f'<line x1="170" y1="{my}" x2="170" y2="235" stroke="{C["mgmt"]}" stroke-width="1.6" stroke-dasharray="2,4"/>')
    for frac, lab in [(0.08, "MONITOR"), (0.36, "RESTORE"), (0.64, "MINIMIZE"), (0.92, "AVOID")]:
        t = frac
        x = (1-t)**3*p0[0]+3*(1-t)**2*t*p1[0]+3*(1-t)*t**2*p2[0]+t**3*p3[0]
        y = (1-t)**3*p0[1]+3*(1-t)**2*t*p1[1]+3*(1-t)*t**2*p2[1]+t**3*p3[1]
        body.append(text(x, y+20, lab, size=10.2, weight="700", color=C["mgmt"], anchor="middle", letter_spacing="0.4"))
    body.append(text(760, my+18, "ADAPTIVE MANAGEMENT FEEDBACK", size=10.5, weight="700",
                      color=C["mgmt"], anchor="middle", letter_spacing="1"))

    return svg_doc(W, H, "".join(body), "".join(defs))


if __name__ == "__main__":
    with open("out/concept_c.svg", "w") as f:
        f.write(build())
    print("wrote concept_c.svg")
