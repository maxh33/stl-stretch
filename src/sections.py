"""Section area along Y for an STL, to find constant-section (safe to stretch) ranges. usage: sections.py in.stl"""
import sys, numpy as np, trimesh
m = trimesh.load(sys.argv[1]); y0, y1 = m.bounds[:, 1]
prev = None
for y in np.arange(y0 + 0.5, y1, 2.5):
    s = m.section(plane_origin=[0, y, 0], plane_normal=[0, 1, 0])
    a = sum(p.area for p in s.to_2D()[0].polygons_full) if s else 0
    print(f"y={y:7.1f} area={a:8.2f}" + ("  <- same" if prev is not None and abs(a - prev) < 0.05 else ""))
    prev = a
