"""3D-printed riser foot (PETG, x4): 60 mm tall, bolted M5 x 25 up through the bottom panel into the post end.
The bolt head sits in a 45 mm deep pocket from below; a stick-on rubber pad closes the pocket."""
import sys, manifold3d as m3d, trimesh, numpy as np
OUT = sys.argv[1]
Hh, R0, R1 = 60.0, 18.0, 15.0                                   # height, base radius, top radius (post is 20 x 20)
body = m3d.Manifold.cylinder(Hh, R0, R1, 96)
pocket = m3d.Manifold.cylinder(45.0, 5.5, 5.5, 48).translate([0, 0, -1])     # Ø11 for the M5 head + hex key
bore = m3d.Manifold.cylinder(Hh + 2, 2.75, 2.75, 48).translate([0, 0, -1])   # Ø5.5 through
part = body - pocket - bore
mesh = part.to_mesh()
tm = trimesh.Trimesh(vertices=np.asarray(mesh.vert_properties)[:, :3], faces=np.asarray(mesh.tri_verts)); assert tm.is_watertight
tm.export(f"{OUT}/chan-cao_PETG_x4.stl")
print("feet vol cm3", round(tm.volume / 1000, 1), "g", round(tm.volume / 1000 * 1.27))
