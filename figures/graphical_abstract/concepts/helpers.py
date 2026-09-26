"""Shared SVG primitives + style tokens for the HHTE graphical-abstract concepts."""
import math

# ---------------------------------------------------------------- palette --
C = {
    "bg":        "#FAFAF7",
    "sky_top":   "#EEF3F1",
    "sky_bot":   "#FAFAF7",
    "ink":       "#2B2B28",
    "ink_soft":  "#5A5A54",
    "line":      "#3A3A36",

    # water / hydrology
    "water_deep":  "#1E6E86",
    "water_mid":   "#3E93AC",
    "water_light": "#8FC4D4",
    "water_pulse": "#0F4C5C",

    # habitat / vegetation
    "veg_dark":   "#4C7A4A",
    "veg_mid":    "#6E9B5C",
    "veg_light":  "#9CBB7C",
    "mud":        "#B79A6B",
    "mud_dark":   "#9C7F52",
    "upland":     "#C9BE97",

    # trophic
    "trophic":    "#C2793C",
    "trophic_lt": "#DDA664",

    # pressures / human
    "pressure":     "#6B5A4B",
    "pressure_lt":  "#8A7A69",
    "concrete":     "#9B968C",

    # ecosystem function
    "func":       "#3E7C6B",

    # assessment
    "assess":     "#4B4E52",
    "assess_bg":  "#FFFFFF",
    "trigger":    "#B4483E",

    # management
    "mgmt":       "#5B5A8C",
    "mgmt_lt":    "#8B89B8",

    # consequence
    "impact":     "#8C4B3E",
}

FONT = "Arial, 'Liberation Sans', 'Helvetica Neue', sans-serif"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=14, weight="400", color=None, anchor="start",
          style="normal", letter_spacing=None, family=None):
    color = color or C["ink"]
    ls = f' letter-spacing="{letter_spacing}"' if letter_spacing else ""
    fam = family or FONT
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" '
            f'font-size="{size}" font-weight="{weight}" font-style="{style}" '
            f'fill="{color}" text-anchor="{anchor}"{ls}>{esc(s)}</text>')


def tspan_block(x, y, lines, size=13, weight="400", color=None, anchor="start",
                 leading=1.32, family=None):
    color = color or C["ink"]
    fam = family or FONT
    out = [f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}" '
           f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}">']
    for i, ln in enumerate(lines):
        dy = 0 if i == 0 else size * leading
        out.append(f'<tspan x="{x:.1f}" dy="{dy:.1f}">{esc(ln)}</tspan>')
    out.append("</text>")
    return "".join(out)


def wave_path(x0, x1, y, amp, wavelength, phase=0.0, n=200):
    pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        yy = y + amp * math.sin(2 * math.pi * (x - x0) / wavelength + phase)
        pts.append((x, yy))
    d = f"M {pts[0][0]:.1f},{pts[0][1]:.1f} " + " ".join(
        f"L {px:.1f},{py:.1f}" for px, py in pts[1:])
    return d


def water_fill_path(x0, x1, y_top_func, y_bottom, n=160):
    """Closed path: top boundary follows y_top_func(x), flat bottom."""
    pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        pts.append((x, y_top_func(x)))
    d = f"M {pts[0][0]:.1f},{pts[0][1]:.1f} "
    d += " ".join(f"L {px:.1f},{py:.1f}" for px, py in pts[1:])
    d += f" L {x1:.1f},{y_bottom:.1f} L {x0:.1f},{y_bottom:.1f} Z"
    return d


def reed(x, y, h=34, w=5, color=None, tilt=0, opacity=1.0):
    color = color or C["veg_dark"]
    dx = tilt
    return (f'<path d="M {x:.1f},{y:.1f} '
            f'C {x-w:.1f},{y-h*0.5:.1f} {x-w+dx:.1f},{y-h*0.85:.1f} {x+dx:.1f},{y-h:.1f} '
            f'C {x+w+dx:.1f},{y-h*0.85:.1f} {x+w:.1f},{y-h*0.5:.1f} {x:.1f},{y:.1f} Z" '
            f'fill="{color}" opacity="{opacity}"/>')


def reed_cluster(cx, y, n=5, spread=26, h=34, color=None, seed=0):
    out = []
    for i in range(n):
        t = (i / max(n - 1, 1)) - 0.5
        x = cx + t * spread
        hh = h * (0.75 + 0.5 * abs(math.sin(i * 2.1 + seed)))
        tilt = t * 10
        out.append(reed(x, y, h=hh, w=3.2, color=color, tilt=tilt))
    return "".join(out)


def shrub(cx, cy, r=16, color=None):
    color = color or C["veg_mid"]
    blobs = []
    offs = [(-r*0.5, r*0.15, r*0.7), (r*0.5, r*0.15, r*0.7),
            (0, -r*0.35, r*0.85), (-r*0.15, r*0.4, r*0.55), (r*0.2, r*0.4, r*0.55)]
    for dx, dy, rr in offs:
        blobs.append(f'<circle cx="{cx+dx:.1f}" cy="{cy+dy:.1f}" r="{rr:.1f}" fill="{color}"/>')
    return f'<g opacity="0.96">{"".join(blobs)}</g>'


def bird_silhouette(cx, cy, s=1.0, color=None, flip=False):
    color = color or C["ink"]
    sx = -s if flip else s
    d = (f"M {-10*sx:.1f},{0:.1f} "
         f"C {-5*sx:.1f},{-6*s:.1f} {-2*sx:.1f},{-2*s:.1f} {0:.1f},{0:.1f} "
         f"C {2*sx:.1f},{-2*s:.1f} {5*sx:.1f},{-6*s:.1f} {10*sx:.1f},{0:.1f}")
    return (f'<g transform="translate({cx:.1f},{cy:.1f})">'
            f'<path d="{d}" stroke="{color}" stroke-width="{1.8*s:.1f}" '
            f'fill="none" stroke-linecap="round"/></g>')


def fish_silhouette(cx, cy, s=1.0, color=None, flip=False):
    color = color or C["ink_soft"]
    sx = -1 if flip else 1
    body = (f"M {-12*s*sx:.1f},{0:.1f} "
            f"Q {-4*s*sx:.1f},{-7*s:.1f} {8*s*sx:.1f},{0:.1f} "
            f"Q {-4*s*sx:.1f},{7*s:.1f} {-12*s*sx:.1f},{0:.1f} Z")
    tail = (f"M {8*s*sx:.1f},{0:.1f} L {14*s*sx:.1f},{-5*s:.1f} "
            f"L {13*s*sx:.1f},{0:.1f} L {14*s*sx:.1f},{5*s:.1f} Z")
    eye = f'<circle cx="{-8*s*sx:.1f}" cy="{-0.5*s:.1f}" r="{1.2*s:.1f}" fill="{C["bg"]}"/>'
    return (f'<g transform="translate({cx:.1f},{cy:.1f})">'
            f'<path d="{body}" fill="{color}"/><path d="{tail}" fill="{color}"/>{eye}</g>')


def invert_dot(cx, cy, s=1.0, color=None):
    color = color or C["trophic"]
    return (f'<g transform="translate({cx:.1f},{cy:.1f})">'
            f'<circle r="{3.4*s:.1f}" fill="{color}"/>'
            f'<path d="M {-5*s:.1f},0 L {-9*s:.1f},{-3*s:.1f} M {-5*s:.1f},0 L {-9*s:.1f},{3*s:.1f} '
            f'M {5*s:.1f},0 L {9*s:.1f},{-3*s:.1f} M {5*s:.1f},0 L {9*s:.1f},{3*s:.1f}" '
            f'stroke="{color}" stroke-width="{1.1*s:.1f}" fill="none" stroke-linecap="round"/></g>')


def algae_fleck(cx, cy, s=1.0, color=None):
    color = color or C["veg_light"]
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{2.2*s:.1f}" fill="{color}" opacity="0.85"/>'


def arrow_marker_defs():
    return '''
    <marker id="arrowMain" markerWidth="10" markerHeight="10" refX="7" refY="3.5" orient="auto">
      <path d="M0,0 L8,3.5 L0,7 Z" fill="#3A3A36"/>
    </marker>
    <marker id="arrowMgmt" markerWidth="10" markerHeight="10" refX="7" refY="3.5" orient="auto">
      <path d="M0,0 L8,3.5 L0,7 Z" fill="%s"/>
    </marker>
    ''' % C["mgmt"]


def gauge(cx, cy, r, frac, label, sublabel, color=None, tone=False):
    """Small diagnostic dial: arc gauge with needle, acronym label under it."""
    color = color or C["assess"]
    start_a = -220
    end_a = 40
    sweep = end_a - start_a
    val_a = start_a + sweep * frac

    def pt(a, rr):
        rad = math.radians(a)
        return cx + rr * math.cos(rad), cy + rr * math.sin(rad)

    x0, y0 = pt(start_a, r)
    x1, y1 = pt(end_a, r)
    large = 1 if abs(sweep) > 180 else 0
    track = (f'<path d="M {x0:.1f},{y0:.1f} A {r},{r} 0 {large} 1 {x1:.1f},{y1:.1f}" '
              f'stroke="#D8D8D2" stroke-width="4.2" fill="none" stroke-linecap="round"/>')
    xv, yv = pt(val_a, r)
    large_v = 1 if abs(val_a - start_a) > 180 else 0
    val_arc = (f'<path d="M {x0:.1f},{y0:.1f} A {r},{r} 0 {large_v} 1 {xv:.1f},{yv:.1f}" '
               f'stroke="{color}" stroke-width="4.2" fill="none" stroke-linecap="round"/>')
    nx, ny = pt(val_a, r * 0.62)
    needle = (f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{nx:.1f}" y2="{ny:.1f}" '
              f'stroke="{color}" stroke-width="2"/>'
              f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="2.6" fill="{color}"/>')
    ring = f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r+7:.1f}" fill="{C["assess_bg"]}" stroke="#DADAD4" stroke-width="1.2"/>'
    lbl = text(cx, cy + r + 20, label, size=11.5, weight="700", color=C["assess"], anchor="middle", letter_spacing="0.3")
    sub = text(cx, cy + r + 33, sublabel, size=8.6, weight="400", color=C["ink_soft"], anchor="middle") if sublabel else ""
    return f'<g>{ring}{track}{val_arc}{needle}{lbl}{sub}</g>'


def pill(x, y, w, h, r, fill, stroke=None, sw=1.4, opacity=1.0):
    stroke_attr = f'stroke="{stroke}" stroke-width="{sw}"' if stroke else 'stroke="none"'
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" ry="{r}" '
            f'fill="{fill}" opacity="{opacity}" {stroke_attr}/>')


def svg_doc(width, height, body, defs="", bg=None):
    bg = bg if bg is not None else C["bg"]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
<defs>
{defs}
</defs>
<rect x="0" y="0" width="{width}" height="{height}" fill="{bg}"/>
{body}
</svg>'''
