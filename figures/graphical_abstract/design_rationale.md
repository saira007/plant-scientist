# Design rationale — HHTE graphical abstract

## The one message
"Human and climatic pressures alter wetland hydrology; altered hydrological dynamics reorganize
habitat and trophic structure, which changes ecosystem functioning. The HHTE framework detects
these process changes using linked indicators and supports adaptive management."

## Why this architecture (Concept B of three tested)
Three fundamentally different layouts were prototyped and compared (see `concepts/`):
a continuous left-to-right landscape strip (A), a central wetland cross-section (B), and an
abstract flowing-signal pathway (C). B was selected because it is the only one of the three in
which **the wetland itself carries the mechanism** rather than illustrating it beside a diagram:

- The land-surface elevation profile and a single water-level line jointly determine, at every
  point along the cross-section, whether that point is upland, marsh, mudflat, or open water.
  Habitat heterogeneity is therefore a direct, visible consequence of hydrology — not an
  independent box connected by an arrow.
- Moving the water line from the dashed "natural hydroperiod" reference down to the solid
  "altered" level physically shrinks the marsh/open-water area and expands mudflat/upland —
  the same homogenization the manuscript describes — so the causal step is shown, not asserted.
- This is a recognised, respected genre in wetland/ecological-indicator literature (the
  cross-section conceptual diagram, in the tradition popularised by the Integration & Application
  Network), which reduces the risk of the figure reading as a generic AI infographic.

Concept A read as three stacked "rows" behind a strip (closer to an illustrated flowchart);
Concept C communicated the process elegantly but abandoned the literal wetland the brief asked
to keep as the visual anchor.

## Visual language
| Element | Colour | Rationale |
|---|---|---|
| Water / hydrology | Blue–teal (`#1E6E86` → `#8FC4D4`) | Standard hydrological convention |
| Vegetation / habitat | Muted greens (`#4C7A4A`, `#6E9B5C`) | Standard ecological convention |
| Mudflat / upland substrate | Warm tans (`#B79A6B`, `#C9BE97`) | Neutral earth tone, keeps focus on water/vegetation |
| Trophic interactions | Restrained amber (`#C2793C`) | Distinct warm accent, not competing with habitat green |
| Human pressures | Muted brown-grey (`#6B5A4B`) | Deliberately desaturated — pressures are not the hero |
| Ecosystem functioning | Deep teal-green (`#3E7C6B`) | Distinguishes function from habitat while staying in the natural palette |
| Assessment / gauges | Neutral dark grey (`#4B4E52`) on white | Reads as instrumentation, not narrative |
| Management feedback | Muted indigo (`#5B5A8C`) | Only accent outside the natural palette — signals "intervention" |
| Trigger threshold | Red (`#B4483E`) | Universal warning convention, used once, sparingly |

Saturation is used hierarchically: the wetland and its water are the most saturated elements;
the pressure/consequence side panels and gauge instrumentation are kept neutral so the eye lands
on the wetland first (per Nature/Cell Press figure-hierarchy guidance — most important element
most saturated, context desaturated).

## The five process-based indicators
Shown as instrument-style dial gauges in a single row above the landscape, each with a thin
leader line down to the process it measures (hydrology, habitat edge, a connectivity point,
the trophic-icon cluster, and the functional soil/root band respectively) — "measurement pins"
rather than a grey text box. One dial (EFS) carries a small red tick marking comparison against
a management trigger, with a one-line legend rather than repeated text on every gauge.

## Management loop
A single thin dashed arc in the indigo accent sweeps from the consequences side back over the
top of the wetland into the pressures panel, carrying the four waypoints (Avoid → Minimize →
Restore → Monitor) as compact labels on the arc itself — an adaptive feedback pathway that frames
the wetland without competing with it for attention.

## Two output variants
- **`hhte_graphical_abstract.svg` / `.pdf` / `_300dpi.png` / `_600dpi.png`** — full version with
  a one-line framework title/kicker and the italic process annotations, for internal review and
  presentations.
- **`hhte_graphical_abstract_clean.*`** — the minimal-text version intended for journal
  submission: no kicker/title, no italic explanatory asides, only the labels that are part of the
  figure's own logic (panel headers, zone labels, gauge acronyms + one-line spellouts, waypoint
  labels).

## Honesty about the medium and process
- All literature/design research for this figure was done through live web search during this
  session (Cell Press graphical-abstract guidelines, ecological colour-palette conventions, and
  the IAN wetland cross-section conceptual-diagram tradition — see chat for sources); no published
  figure was copied or traced.
- The BioRender plugin (for painterly, illustration-grade organism/landscape assets) was not
  available in this session, so the figure is hand-authored, precise vector SVG rather than
  BioRender-rendered artwork. It reads as a clean, credible scientific conceptual diagram in the
  genre used by wetland/ecology journals, not as painterly illustration. If BioRender becomes
  available later, the marsh vegetation, fish/bird/invertebrate icons, and pressure/consequence
  icons are the elements most worth swapping for BioRender assets — the composition, layout,
  colour system, and gauge/loop logic in this SVG can stay unchanged.
- Canvas is 1600×1000 (1.6:1), exported assuming a 180 mm print width. Re-export at the exact
  pixel/DPI specification once the target journal is confirmed (Cell Press wants 1200×1200 @
  300 dpi; Elsevier journals typically want ~1328×531 @ 300 dpi) — the SVG source scales cleanly
  to either.

## Regenerating
```
cd figures/graphical_abstract/build
pip install cairosvg
python3 final.py        # writes final_full.svg / final_clean.svg next to this script
```
Edit `final.py` (geometry, text, gauge values) or `helpers.py` (colour tokens, icon primitives)
and re-run; then re-export PDF/PNG with `cairosvg` as shown in the session log.
