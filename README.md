# stl-stretch

[![GitHub stars](https://img.shields.io/github/stars/maxh33/stl-stretch?style=social)](https://github.com/maxh33/stl-stretch)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> 🇧🇷 [Versão em Português](README.pt-BR.md) &nbsp;|&nbsp; [github.com/maxh33/stl-stretch](https://github.com/maxh33/stl-stretch)

Lengthen an STL or 3MF part for 3D printing **without distorting its holes, threads or chamfers**.
No CAD source needed: cut the mesh where the cross-section is constant, shift one half, fill the gap.

You downloaded a model, it is 10 cm too short, and all you have is an STL. Scaling the mesh stretches every
feature with it: round holes turn into ovals, flanges get thicker. `stl-stretch` only adds material where the part is a
straight prism, so everything else stays exactly as designed.

![original vs naive scaling vs stl-stretch](docs/before-after.png)

---

## Why this exists

I'm a computer science student and a developer, not a 3D-printing person. I needed a tube squeezer that takes a
16 cm wide bag of cream cheese, and the model I found was about 10 cm too short. The 3D-printing professional I use
doesn't customize or edit files, so I told them lengthening a part wasn't that complicated, looked up how it's done and
sent them the instructions. They didn't want to go deeper into customizing files for clients who ask for it.

So one evening, out of curiosity, I did it myself: found the dependencies, worked out how to lengthen a mesh without
ruining the holes and ratchet teeth, and adjusted the part to what I needed. Then I sent back the finished, customized
files, and all that was left for the professional was to press print. This repo is that evening, cleaned up so the next
person with the same problem doesn't need one.

---

## How it works

```
part.stl
    ↓
find_cut — samples the cross-section area along the axis, picks the middle of the longest constant run
    ↓
stretch — cuts the mesh at that plane, shifts one half by --delta, extrudes the section to fill the gap
    ↓
one welded, watertight mesh — checked: length = original + delta, volume = original + section area x delta
    ↓
longer.stl (or 3MF, OBJ, ...)
```

Built on [trimesh](https://trimesh.org) and manifold3d. Reads and writes STL, 3MF, OBJ and anything else trimesh supports.

---

## Quick start

```bash
uv sync
uv run python src/stretch.py part.stl longer.stl --axis y --delta 107          # auto cut
uv run python src/stretch.py part.stl longer.stl --axis y --delta 107 --cut 35 # explicit cut
uv run python examples/demo.py      # regenerates the image above from a generated part
uv run python tests/test_stretch.py
```

Multi-body file? `--body N` stretches only body N. Not sure where it is safe to cut? `src/sections.py part.stl` prints the
section area along Y, so you can see the constant ranges yourself.

## Other small tools (command line, all in `src/`)

| Script | What it does |
|---|---|
| `inspect_stl.py` | Bounding box, watertightness and body count of every STL under `input/` |
| `sections.py` | Cross-section area along an axis (finds the ranges where stretching is safe) |
| `orient.py` | Scores the 6 axis-aligned print orientations by overhang area vs bed contact |
| `preview.py`, `section_plot.py` | Headless PNG renders and section plots, handy to check a result without opening a slicer |
| `examples/make_plates.py` | Arranges oriented parts on a 256 mm bed and writes one 3MF per project, ready for Bambu Studio |

---

## Real-world use

I used it to lengthen a ratcheted toothpaste-tube squeezer so it takes a 16 cm wide bag (tube slot 63 mm to 170 mm),
and to widen a kids' toothpaste stand for a 62 mm tube. Both models are by other authors on MakerWorld and are **not** in
this repo, check their licenses before redistributing anything derived from them:

- [Ratcheted Toothpaste Tube Squeezer](https://makerworld.com/en/models/30246-ratcheted-toothpaste-tube-squeezer) (remix by Roland Deschain)
- [Stand for Toothpaste V5.0 (Kids' version)](https://makerworld.com/en/models/831100-stand-for-toothpaste-v5-0-kids-version) (3DKUB)

`examples/make_plates.py` is my personal script for those two; paths and measures are specific to them.

## Limits

- The part must be a straight prism at the cut plane, along one axis at a time. Organic shapes have no such plane and
  `find_cut` will say so.
- Equal cross-section area does not strictly prove equal outline, so look at a render before printing an unusual part.
- It edits geometry only. Slicer settings, supports and material are your call.

## Contributing

Ideas that would make this more useful, not promises: stretching along several planes in one run, detecting the axis
automatically, a proper `stl-stretch` command instead of `python src/stretch.py`, and generalizing `make_plates.py`.
Issues and pull requests are welcome, especially with parts where `find_cut` picks a bad plane.

---

Open source, MIT license (see [LICENSE](LICENSE)). If this saved you an evening, a ⭐ helps other people find it.
