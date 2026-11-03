"""Quick isometric previews of STL files -> PNG (matplotlib). python render_stl.py cad/out docs/renders"""
import sys, os, glob
import numpy as np
from stl import mesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)
for f in sorted(glob.glob(os.path.join(src, "*.stl"))):
    m = mesh.Mesh.from_file(f)
    fig = plt.figure(figsize=(4, 4)); ax = fig.add_subplot(111, projection="3d")
    n = m.normals / (np.linalg.norm(m.normals, axis=1, keepdims=True) + 1e-9)
    shade = np.clip(0.35 + 0.65 * np.abs(n @ np.array([0.4, -0.5, 0.75])), 0, 1)
    ax.add_collection3d(Poly3DCollection(m.vectors, facecolors=[(0.2 * s, 0.45 * s, 0.75 * s) for s in shade], edgecolor="none"))
    pts = m.vectors.reshape(-1, 3); c = (pts.max(0) + pts.min(0)) / 2; r = (pts.max(0) - pts.min(0)).max() / 2
    ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(c[2] - r, c[2] + r)
    ax.view_init(28, -55); ax.set_axis_off(); ax.set_title(os.path.basename(f)[:-4], fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(dst, os.path.basename(f)[:-4] + ".png"), dpi=170); plt.close(fig)
print("rendered", len(glob.glob(os.path.join(dst, "*.png"))))
