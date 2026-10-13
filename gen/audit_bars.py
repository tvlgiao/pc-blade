"""Every Ø5.5 mounting hole must sit on a 2020 slot centre line, inside the member span. Frame W 424, z from -180 to 110."""
import sys, ezdxf
OUT = sys.argv[1]
def members(face):
    # (axis, const, lo, hi): hole (X, Y) lies on line X==const (axis 'X') with lo<=Y<=hi, or Y==const (axis 'Y')
    if face in ("top", "bottom"):        # X = x + 212, Y = z + 180
        m = [("Y", 280, 20, 404), ("Y", 60, 20, 404), ("X", 10, 20, 270), ("X", 414, 20, 270)]
        m += [("X", 372, 70, 270)] if face == "top" else [("X", 320, 70, 270), ("X", 10, 0, 20), ("X", 414, 0, 20), ("X", 10, 270, 290), ("X", 414, 270, 290)]
        return m
    if face in ("front", "rear"):        # side faces: X = z + 180, Y = height
        return [("X", 10, 0, 300), ("X", 280, 0, 300), ("Y", 10, 20, 270), ("Y", 290, 20, 270)]
    if face == "right":                  # A face z 110: X = x + 212
        return [("X", 10, 0, 300), ("X", 414, 0, 300), ("Y", 10, 20, 404), ("Y", 290, 20, 404)]
    if face == "left":                   # B face z -180: rear posts only
        return [("X", 10, 0, 300), ("X", 414, 0, 300)]
files = {"nap-tren": "top", "day": "bottom", "mat-truoc": "front", "mat-sau": "rear", "hong-phai": "right", "hong-trai": "left"}
bad = 0
for name, face in files.items():
    msp = ezdxf.readfile(f"{OUT}/{name}_mica-3mm_x1.dxf").modelspace()
    holes = [(round(c.dxf.center.x, 1), round(c.dxf.center.y, 1)) for c in msp.query("CIRCLE") if abs(c.dxf.radius - 2.75) < 0.01]
    for X, Y in holes:
        ok = any((ax == "X" and abs(X - k) < 0.6 and lo <= Y <= hi) or (ax == "Y" and abs(Y - k) < 0.6 and lo <= X <= hi) for ax, k, lo, hi in members(face))
        if not ok: bad += 1; print(f"  !! {name}: M5 hole ({X},{Y}) not on any bar slot")
    print(f"{name}: {len(holes)} M5 holes checked")
print("problems:", bad)
