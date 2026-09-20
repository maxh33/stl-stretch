"""Lengthen a mesh along one axis without distorting holes, threads or chamfers.

Cut the mesh at a plane where the cross-section is constant, shift one half away, fill the gap with the extruded section.
Plain scaling would stretch every feature; this only adds material where the part is a straight prism.

usage: stretch.py in.stl out.stl --axis y --delta 107 [--cut 35] [--body 11]
--cut defaults to the middle of the longest constant-section run (see find_cut). Reads/writes STL, 3MF, OBJ, ...
"""
import argparse, numpy as np, trimesh

def section_area(m, k, pos):
    n = np.eye(3)[k]
    s = m.section(plane_origin=n * pos, plane_normal=n)
    return sum(p.area for p in s.to_2D()[0].polygons_full) if s else 0.0

def find_cut(m, k, steps=100, tol=1e-3):
    """Middle of the longest run of equal cross-section area along axis k.
    ponytail: equal area does not strictly prove equal outline; look at the render before trusting an odd part."""
    lo, hi = m.bounds[:, k]
    pos = np.linspace(lo, hi, steps + 2)[1:-1]
    area = np.array([section_area(m, k, p) for p in pos])
    same = np.abs(np.diff(area)) <= tol * np.maximum(area[1:], 1e-9)      # same[i]: samples i and i+1 match
    best, i = (0, 0), 0
    while i < len(same):
        j = i
        while same[i] and j < len(same) and same[j]: j += 1
        if same[i] and j - i > best[1] - best[0]: best = (i, j)
        i = max(j, i + 1)
    if best[1] == best[0]: raise ValueError("no constant-section range found: pass --cut, or the part is not prismatic on this axis")
    return float(pos[(best[0] + best[1]) // 2])

OVERLAP = 0.01  # mm: the filler pokes into both halves so the union welds by volume overlap, not by coplanar faces (float noise left 2 bodies)

def stretch(m, k, cut, delta):
    n = np.eye(3)[k]; o = n * cut
    # boolean half-space cuts (manifold) instead of slice_plane(cap=True): the latter fails to cap some meshes
    big = m.extents.max() * 2
    def half(sign):
        box = trimesh.creation.box(extents=[big] * 3)
        box.apply_translation(m.centroid + n * (cut - m.centroid[k] + sign * big / 2))
        return trimesh.boolean.intersection([m, box], engine="manifold")
    lower, upper = half(-1), half(+1)
    upper.apply_translation(n * delta)
    path2d, T = m.section(plane_origin=o, plane_normal=n).to_2D()
    prism = trimesh.util.concatenate([trimesh.creation.extrude_polygon(p, delta + 2 * OVERLAP) for p in path2d.polygons_full])
    prism.apply_transform(T)
    prism.apply_translation(n * (cut - OVERLAP - prism.bounds[0, k]))  # extrusion may go either way along the axis
    return trimesh.boolean.union([lower, prism, upper], engine="manifold"), sum(p.area for p in path2d.polygons_full)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--axis", choices="xyz", default="z"); ap.add_argument("--delta", type=float, required=True, help="mm to add")
    ap.add_argument("--cut", type=float, help="cut position along the axis (default: auto)")
    ap.add_argument("--body", type=int, help="stretch only this body of a multi-body file")
    a = ap.parse_args()
    k, m = "xyz".index(a.axis), trimesh.load(a.src, force="mesh")
    if a.body is not None: m = m.split(only_watertight=False)[a.body]
    cut = a.cut if a.cut is not None else find_cut(m, k)
    out, area = stretch(m, k, cut, a.delta)
    print(f"cut at {a.axis}={cut:.2f}")
    print(f"length {m.extents[k]:.2f} -> {out.extents[k]:.2f} mm (expected {m.extents[k]+a.delta:.2f})")
    print(f"volume {m.volume:.1f} -> {out.volume:.1f} mm3 (expected {m.volume+area*a.delta:.1f})")
    print(f"watertight={out.is_watertight} bodies={len(out.split(only_watertight=False))}")
    out.export(a.dst)
