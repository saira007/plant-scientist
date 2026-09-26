# HHTE graphical abstract

A from-scratch redesign of the manuscript's graphical abstract: the four-box "Drivers →
Hydrological alteration → HHTE pathway → Impacts" flowchart was replaced with a single wetland
cross-section illustration in which habitat, trophic structure, ecosystem functioning, the
process-based assessment indicators, and the adaptive-management loop are all shown as properties
of, or overlays on, one landscape.

## Files

- **`hhte_graphical_abstract.svg`** — editable vector source, full version (title + process
  annotations). Open/edit directly, or regenerate from `build/final.py`.
- **`hhte_graphical_abstract_clean.svg`** — minimal-text version intended for journal submission.
- **`exports/`** — rendered outputs of both versions:
  - `*.pdf` — vector PDF (resolution-independent)
  - `*_300dpi.png`, `*_600dpi.png` — raster exports at an assumed 180 mm print width; re-export
    at your target journal's exact pixel spec (see `design_rationale.md`)
- **`design_rationale.md`** — why this composition, the colour/typography system, what was
  tried and rejected, and known limitations of the medium used to build it.
- **`label_list.md`** — every text label on the figure, and what each abbreviation stands for.
- **`concepts/`** — the three competing layouts sketched and compared before this one was chosen.
- **`build/`** — the Python/SVG source (`final.py`, `helpers.py`) that generates the two SVGs.

## Regenerating or editing

```bash
cd figures/graphical_abstract/build
pip install cairosvg
python3 final.py
# then, to export PDF/PNG:
python3 -c "
import cairosvg
cairosvg.svg2pdf(url='final_full.svg', write_to='final_full.pdf')
cairosvg.svg2png(url='final_full.svg', write_to='final_full_300dpi.png', output_width=2126, output_height=1329)
"
```

All colours, fonts, gauge values, and text are parameters in `final.py` / `helpers.py` —
there is no rasterised artwork to redraw by hand.
