"""Lengthen an STL along an axis: cut at a constant-section plane, shift one half, fill the gap with the extruded section.
usage: stretch.py in.stl out.stl AXIS(x|y|z) CUT DELTA_MM [BODY_IDX]
CUT must lie inside a constant-section range (see sections.py). BODY_IDX stretches only that body of a multi-body STL."""
import sys, numpy as np, trimesh

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
    prism = trimesh.util.concatenate([trimesh.creation.extrude_polygon(p, delta) for p in path2d.polygons_full])
    prism.apply_transform(T)
    prism.apply_translation(n * (cut - prism.bounds[0, k]))  # extrusion may go either way along the axis
    return trimesh.boolean.union([lower, prism, upper], engine="manifold"), sum(p.area for p in path2d.polygons_full)

if __name__ == "__main__":
    src, dst, ax, cut, delta = sys.argv[1], sys.argv[2], "xyz".index(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
    m = trimesh.load(src)
    if len(sys.argv) > 6: m = m.split(only_watertight=False)[int(sys.argv[6])]
    out, area = stretch(m, ax, cut, delta)
    print(f"length {m.extents[ax]:.2f} -> {out.extents[ax]:.2f} mm (expected {m.extents[ax]+delta:.2f})")
    print(f"volume {m.volume:.1f} -> {out.volume:.1f} mm3 (expected {m.volume+area*delta:.1f})")
    print(f"watertight={out.is_watertight} bodies={len(out.split(only_watertight=False))}")
    out.export(dst)
