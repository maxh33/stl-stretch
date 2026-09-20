"""Render 3 orthographic views (XY, XZ, YZ) of an STL to PNG. usage: preview.py in.stl out.png"""
import sys, numpy as np, trimesh, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

m = trimesh.load(sys.argv[1])
fig, axs = plt.subplots(1, 3, figsize=(18, 6))
for ax, (a, b, n) in zip(axs, [(0, 1, 2), (0, 2, 1), (1, 2, 0)]):
    tri = m.triangles[:, :, [a, b]]
    shade = 0.35 + 0.65 * np.abs(m.face_normals[:, n])
    order = np.argsort(m.triangles_center[:, n]) if m.face_normals[:, n].mean() >= 0 else np.argsort(-m.triangles_center[:, n])
    ax.add_collection(PolyCollection(tri[order], facecolors=plt.cm.Blues(shade[order]), edgecolors="none"))
    ax.autoscale(); ax.set_aspect("equal"); ax.set_title("XYZ"[a] + "-" + "XYZ"[b]); ax.grid(alpha=.3)
plt.tight_layout(); plt.savefig(sys.argv[2], dpi=70)
