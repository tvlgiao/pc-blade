"""Audit every DXF: circles inside the outline, clearances between holes, holes vs outline edge."""
import sys, glob, math, itertools, ezdxf
from ezdxf import bbox
for f in sorted(glob.glob(sys.argv[1] + "/*.dxf")):
    doc = ezdxf.readfile(f); msp = doc.modelspace()
    circ = [(e.dxf.center.x, e.dxf.center.y, e.dxf.radius) for e in msp.query("CIRCLE")]
    polys = list(msp.query("LWPOLYLINE"))
    outer = max(polys, key=lambda p: bbox.extents([p]).size.x * bbox.extents([p]).size.y)
    ob = bbox.extents([outer]); x0, y0, x1, y1 = ob.extmin.x, ob.extmin.y, ob.extmax.x, ob.extmax.y
    issues = []
    for x, y, r in circ:
        m = min(x - r - x0, x1 - x - r, y - r - y0, y1 - y - r)
        if m < 2.0: issues.append(f"hole ({x:.1f},{y:.1f}) r{r} only {m:.1f} mm from outline")
    worst = (1e9, None)
    for a, b in itertools.combinations(circ, 2):
        g = math.hypot(a[0] - b[0], a[1] - b[1]) - a[2] - b[2]
        if g < worst[0]: worst = (g, (a, b))
        if g < 1.4 and not (abs(a[2] - 3) < 0.01 and abs(b[2] - 3) < 0.01):
            issues.append(f"holes too close {g:.2f} mm: ({a[0]:.1f},{a[1]:.1f}) r{a[2]} & ({b[0]:.1f},{b[1]:.1f}) r{b[2]}")
    rects = [p for p in polys if p is not outer]
    for p in rects:
        rb = bbox.extents([p])
        for x, y, r in circ:
            if rb.extmin.x - r - 1.5 < x < rb.extmax.x + r + 1.5 and rb.extmin.y - r - 1.5 < y < rb.extmax.y + r + 1.5 and not (rb.extmin.x < x < rb.extmax.x and rb.extmin.y < y < rb.extmax.y and (rb.size.x > 50)):
                inside_window = rb.extmin.x < x < rb.extmax.x and rb.extmin.y < y < rb.extmax.y
                if not inside_window: issues.append(f"hole ({x:.1f},{y:.1f}) within 1.5 mm of cut-out {rb.extmin.x:.0f}-{rb.extmax.x:.0f} x {rb.extmin.y:.0f}-{rb.extmax.y:.0f}")
    texts = [t.dxf.text for t in msp.query("TEXT")]
    print(f"{f.split('/')[-1]}: outline {x1-x0:.1f} x {y1-y0:.1f}, {len(circ)} circles, {len(rects)} inner cut-outs, text {texts}, min gap {worst[0]:.2f} mm")
    for i in issues[:8]: print("   !!", i)
    if len(issues) > 8: print(f"   … {len(issues)} issues")
