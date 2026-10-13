"""3D-printed sleeve holding a 5-port switch (TP-Link TL-SG105, 99.8 x 98 x 25 mm) above the PSU, hung from the top 2020 bars."""
import sys, numpy as np, manifold3d as m3d, trimesh
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
OUT = sys.argv[1]
IX, IY, LEN = 25.6, 100.6, 114.0          # inner cavity (switch + clearance), sleeve length along depth
WALL, BOT, FL = 2.5, 2.5, 4.0             # side walls, bottom wall, top flange thickness
OX, OY = IX + 2 * WALL, BOT + IY + FL     # 30.6 x 107.1
C = lambda x, y, z, dx, dy, dz: m3d.Manifold.cube([dx, dy, dz]).translate([x, y, z])
body = C(0, 0, 0, OX, OY, LEN) + C(-12, OY - FL, 0, OX + 24, FL, LEN)      # sleeve + wide top flange
cut = C(WALL, BOT, -1, IX, IY, LEN - 3 + 1)                                  # cavity, open at rear (Z=0)
cut += C(WALL + 4, BOT + 4, LEN - 4, IX - 8, IY - 8, 6)                      # front lip opening (4 mm stop lip)
for z in np.arange(14, LEN - 12, 12):                                              # louvres on both side walls (8 mm bridges)
    cut += C(-1, BOT + 10, z, OX + 2, IY - 20, 8)
cut += C(WALL + 5, -1, 14, IX - 10, BOT + 2, 86)                             # bottom vent
for x, z in ((OX / 2, 30), (OX / 2, 100)):                                  # M5 holes on the top 90-degree bar slot (x 160), z -98 / -28
    cut += m3d.Manifold.cylinder(FL + 2, 2.75, 2.75, 40).translate([x, OY - FL - 1, z]).rotate([0, 0, 0]) if False else \
        m3d.Manifold.cylinder(FL + 2, 2.75, 2.75, 40).rotate([-90, 0, 0]).translate([x, OY - FL - 1, z])
part = body - cut
mesh = part.to_mesh()
v = np.asarray(mesh.vert_properties)[:, :3]; f = np.asarray(mesh.tri_verts)
tm = trimesh.Trimesh(vertices=v, faces=f); assert tm.is_watertight
tm.export(f"{OUT}/gia-switch_PETG_x1.stl")
print("bounds", tm.bounds.tolist(), "vol cm3", round(tm.volume / 1000, 1), "g", round(tm.volume / 1000 * 1.27))
fig = plt.figure(figsize=(7, 6)); ax = fig.add_subplot(projection="3d")
ax.add_collection3d(Poly3DCollection(v[f][:, :, [0, 2, 1]], facecolor="#9fc1e6", edgecolor="#33475b", lw=0.1, alpha=1))
ax.set_xlim(-20, 90); ax.set_ylim(-5, 115); ax.set_zlim(-5, 110); ax.set_box_aspect((110, 120, 115)); ax.view_init(22, -50)
ax.set_xlabel("ngang (mm)"); ax.set_ylabel("sâu (mm, 0 = phía sau)"); ax.set_zlabel("cao (mm)")
ax.set_title("Giá switch in 3D – mặt bích trên treo dưới thanh dọc nóc (2 vít M5)", fontsize=9)
fig.savefig(f"{OUT}/gia-switch_xem-truoc.png", dpi=130, bbox_inches="tight")
