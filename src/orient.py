"""Score the 6 axis-aligned print orientations of each STL (overhang area vs bed contact). usage: orient.py file.stl ..."""
import sys, numpy as np, trimesh

def poses(m):
    for k in range(3):
        for s in (1, -1):
            v = np.eye(3)[k] * s                                   # this direction goes DOWN (onto the bed)
            R = trimesh.geometry.align_vectors(v, [0, 0, -1])
            t = m.copy(); t.apply_transform(R); t.apply_translation([0, 0, -t.bounds[0, 2]])
            low = t.triangles[:, :, 2].max(axis=1) < 0.05          # faces lying on the bed
            down = t.face_normals[:, 2] < -0.707                   # steeper than 45 deg overhang
            yield "XYZ"[k] * 1 + ("+" if s > 0 else "-"), R, t, t.area_faces[low].sum(), t.area_faces[down & ~low].sum(), t.extents[2]

def best(m, max_h=245):
    ok = [p for p in poses(m) if p[5] <= max_h and p[3] > 20]
    return min(ok, key=lambda p: (round(p[4], -1), -p[3]))

if __name__ == "__main__":
    for f in sys.argv[1:]:
        m = trimesh.load(f); print(f)
        for n, R, t, c, o, h in poses(m): print(f"  down={n} contact={c:8.1f} overhang={o:8.1f} height={h:6.1f}")
