import glob, trimesh
for f in sorted(glob.glob("input/**/*.stl", recursive=True)):
    m = trimesh.load(f)
    print(f"{f}\n  bbox mm: {[round(float(x),2) for x in m.extents]}  watertight={m.is_watertight}  bodies={len(m.split(only_watertight=False))}  faces={len(m.faces)}")
