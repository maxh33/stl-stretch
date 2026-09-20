"""Plot cross-sections of one body of an STL. usage: section_plot.py in.stl BODY_IDX out.png  (sections at bbox centre on X, Y, Z)"""
import sys, numpy as np, trimesh, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
b = trimesh.load(sys.argv[1]).split(only_watertight=False)[int(sys.argv[2])]
c = b.bounds.mean(axis=0)
fig, axs = plt.subplots(1, 3, figsize=(18, 7))
for ax, k in zip(axs, range(3)):
    n = np.eye(3)[k]; s = b.section(plane_origin=c, plane_normal=n)
    ax.set_title(f"section {'XYZ'[k]}={c[k]:.1f}")
    if s is not None:
        for e in s.entities: 
            p = s.vertices[e.points]; a, bb = [i for i in range(3) if i != k]
            ax.plot(p[:, a], p[:, bb], "b-", lw=.8)
        ax.set_xlabel("XYZ"[a]); ax.set_ylabel("XYZ"[bb])
    ax.set_aspect("equal"); ax.grid(alpha=.3)
plt.tight_layout(); plt.savefig(sys.argv[3], dpi=70)
