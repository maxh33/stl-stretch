"""Build one print-ready 3MF per project: each part oriented for printing, arranged on a 256x256 bed, one object per part.
usage: make_plates.py   (writes output/*.3mf)"""
import numpy as np, trimesh
from orient import poses

BED, GAP = 256.0, 8.0
S = "input/squeezer-catupiry/"; ST = "input/stand-bepantol/"

def oriented(path, down):
    m = trimesh.load(path)
    R = next(p[1] for p in poses(m) if p[0] == down)
    m.apply_transform(R); m.apply_translation([0, 0, -m.bounds[0, 2]])
    if m.extents[1] > m.extents[0]:                                  # long side along X
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 0, 1])); m.apply_translation([0, 0, -m.bounds[0, 2]])
    return m

def shelf_pack(items):                                                # items: [(name, mesh)] -> placed in rows, min corner at (x, y)
    x = y = row_h = 0.0
    for name, m in sorted(items, key=lambda i: -i[1].extents[1]):
        w, d = m.extents[:2]
        if x + w > BED - 2 * GAP: x, y, row_h = 0.0, y + row_h + GAP, 0.0
        m.apply_translation([x - m.bounds[0, 0], y - m.bounds[0, 1], 0]); x += w + GAP; row_h = max(row_h, d)

def write(name, items, out):
    allm = trimesh.util.concatenate([m for _, m in items])
    off = np.array([BED / 2, BED / 2, 0]) - np.array([*allm.bounds.mean(axis=0)[:2], 0])   # centre layout on the bed
    sc = trimesh.Scene()
    for n, m in items:
        m.apply_translation(off); sc.add_geometry(m, node_name=n, geom_name=n)
    lo, hi = np.array([m.bounds for _, m in items]).min(axis=(0, 1)), np.array([m.bounds for _, m in items]).max(axis=(0, 1))
    assert lo[0] >= 0 and lo[1] >= 0 and hi[0] <= BED and hi[1] <= BED, f"{name} does not fit on {BED:.0f} bed: {lo}..{hi}"
    sc.export(out); print(f"{out}: {len(items)} objects, footprint {hi[0]-lo[0]:.0f} x {hi[1]-lo[1]:.0f} mm, max height {hi[2]:.0f} mm")

def squeezer(body, shaft, out):
    parts = [("Body", oriented(body, "Y-")), ("Shaft", oriented(shaft, "Z-")),
             ("Handle_knob", oriented(S + "Handle.stl", "Y-")), ("Ratchet_lado_plano_p_baixo", oriented(S + "Ratchet.stl", "Y-"))]
    shelf_pack(parts); write("squeezer", parts, out)

squeezer("output/squeezer-catupiry/Body_170.stl", "output/squeezer-catupiry/Shaft_170.stl", "output/1_espremedor_catupiry_16cm.3mf")
squeezer(S + "Body.stl", S + "Shaft.stl", "output/2_espremedor_pasta_dente_padrao.3mf")

# stand: parts of the original plate file stay where the designer put them (already flat on the bed); winder replaced by the longer one
plate = trimesh.load(ST + "Stand for Toothpaste V5 .0.stl").split(only_watertight=False)
winder = trimesh.load("output/stand-bepantol/Winder_88.stl")
items = [("Eixo_enrolador_88mm", winder)] + [(f"Peca_{i:02d}", b) for i, b in enumerate(plate) if i != 0]
body = oriented("output/stand-bepantol/Stand_body_71.stl", "Z+")
lo, hi = np.array([m.bounds for _, m in items]).min(axis=(0, 1)), np.array([m.bounds for _, m in items]).max(axis=(0, 1))
body.apply_translation([hi[0] + GAP - body.bounds[0, 0], lo[1] - body.bounds[0, 1], 0])
items.append(("Corpo_suporte_71mm", body)); write("stand", items, "output/3_suporte_infantil_bepantol.3mf")
