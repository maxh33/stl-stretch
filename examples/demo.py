"""Demo on a generated part (no third-party files): a tube with a flange and a cross hole, lengthened by 40 mm.
usage, from the repo root: python examples/demo.py   (writes docs/before-after.png)"""
import sys, numpy as np, trimesh, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, "src")
from stretch import find_cut, stretch

def demo_part():
    """Tube r=13 x 80 mm along Z, flange r=18 x 4 mm at the bottom, bore r=9, cross hole r=3 through the wall at z=8."""
    cyl = lambda r, h, z, s=96: trimesh.creation.cylinder(radius=r, height=h, sections=s).apply_translation([0, 0, z])
    hole = trimesh.creation.cylinder(radius=3, height=60, sections=64)
    hole.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0])); hole.apply_translation([0, 0, 8])
    solid = trimesh.boolean.union([cyl(13, 80, 40), cyl(18, 4, 2)], engine="manifold")
    return trimesh.boolean.difference([solid, cyl(9, 100, 40), hole], engine="manifold")

def plot(ax, m, title):
    s = m.section(plane_origin=[0, 0, 0], plane_normal=[0, 1, 0])           # slice through the axis, cross hole shows as a gap
    for e in s.entities: ax.plot(*s.vertices[e.points][:, [0, 2]].T, "b-", lw=1)
    ax.set_title(title, fontsize=10); ax.set_aspect("equal"); ax.set_xlim(-22, 22); ax.set_ylim(-3, 125); ax.grid(alpha=.3)

if __name__ == "__main__":
    part = demo_part()
    cut = find_cut(part, 2); longer, _ = stretch(part, 2, cut, 40)
    naive = part.copy(); naive.apply_scale([1, 1, 1.5])
    fig, axs = plt.subplots(1, 3, figsize=(12, 6))
    plot(axs[0], part, "original: 80 mm")
    plot(axs[1], naive, "naive scale z x1.5\nhole turns into an oval, flange thickens")
    plot(axs[2], longer, f"stretch +40 mm (auto cut z={cut:.0f})\nhole and flange untouched")
    plt.tight_layout(); plt.savefig("docs/before-after.png", dpi=80)
    print(f"cut z={cut:.1f}  length {part.extents[2]:.0f} -> {longer.extents[2]:.0f} mm  watertight={longer.is_watertight}")
