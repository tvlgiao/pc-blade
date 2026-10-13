"""Generate CNC/laser drawings (DXF + PDF) and comb STL for the 4-PC blade frame (2020 · 2 rails, N=4)."""
import math, os, sys
import ezdxf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle, Polygon
import numpy as np
import manifold3d as m3d
import trimesh

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
N, PF, PITCH, H, D = 4, 20, 72, 300, 260
W = 96 + 2 * PF + PITCH * N  # 424

# ---------- geometry helpers ----------
def rounded_poly(pts, r):
    """Axis-aligned polygon (CCW) -> list of (x, y, bulge) with every corner filleted r."""
    n, out = len(pts), []
    for i in range(n):
        p0, p1, p2 = np.array(pts[i - 1], float), np.array(pts[i], float), np.array(pts[(i + 1) % n], float)
        a, b = (p1 - p0) / np.linalg.norm(p1 - p0), (p2 - p1) / np.linalg.norm(p2 - p1)
        turn = a[0] * b[1] - a[1] * b[0]
        s, e = p1 - a * r, p1 + b * r
        out.append((s[0], s[1], math.tan(math.pi / 8) * (1 if turn > 0 else -1)))
        out.append((e[0], e[1], 0.0))
    return out

def rrect(x0, y0, x1, y1, r):
    return rounded_poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], r)

def bulge_to_points(pl, seg=8):
    """Polyline with bulges -> dense point list (for plotting)."""
    pts = []
    for i, (x, y, bu) in enumerate(pl):
        nx, ny, _ = pl[(i + 1) % len(pl)]
        pts.append((x, y))
        if bu:
            th = 4 * math.atan(bu)
            c = math.hypot(nx - x, ny - y); rr = c / (2 * math.sin(abs(th) / 2))
            mx, my = (x + nx) / 2, (y + ny) / 2
            d = math.sqrt(max(rr * rr - (c / 2) ** 2, 0))
            ux, uy = (nx - x) / c, (ny - y) / c
            sgn = 1 if th > 0 else -1
            cx, cy = mx - sgn * uy * d, my + sgn * ux * d
            a0 = math.atan2(y - cy, x - cx)
            for k in range(1, seg):
                a = a0 + th * k / seg
                pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts

def obround(cx, cy, L, Wd):
    """Slot along y: length L, width Wd."""
    r = Wd / 2
    return [(cx + r, cy - L / 2 + r, 0), (cx + r, cy + L / 2 - r, 1), (cx - r, cy + L / 2 - r, 0), (cx - r, cy - L / 2 + r, 1)]

# ---------- part 1: board plate (aluminium 2 mm) ----------
# Plate coords: X = depth, X 20 = rear face of the ear-stop bar (bend line of the tabs), Y = height above frame bottom.
# Board (244 x 201, I/O edge at rear) sits component side up; I/O edge at X 28, board spans Y 28..271.84.
# Standard microATX holes (x along I/O edge from slot-side edge, y from I/O edge) -> X = 28 + y, Y = 271.84 - x.
MATX = [(80.01, 10.16), (34.29, 10.16), (237.49, 33.02), (237.49, 165.10), (80.01, 165.10), (34.29, 165.10), (13.97, 165.10)]
SO = [(round(28 + y, 2), round(271.84 - x, 2)) for x, y in MATX]
# Notches (X 100-200) clear the top + bottom fans that sit inside the box: bottom edge Y 28.5, top edge Y 271.5 there.
# Rear ear (flat, X 0-20) sits behind the ear-stop bars. Two 2020 corner brackets per plate lock it:
# one leg on the bar's rear face (M5 + T-nut), the other on the ear (M5 + nut through T1/T2). No bending.
plate_outline = rounded_poly([(0, 2), (20, 2), (20, 22.5), (100, 22.5), (100, 28.5), (200, 28.5), (200, 22.5), (232, 22.5), (232, 276.5),
                              (200, 276.5), (200, 271.5), (100, 271.5), (100, 276.5), (20, 276.5), (20, 298), (0, 298)], 2)
plate_window = rrect(75, 55, 180, 175, 10)
plate_slot = obround(10, 150, 44, 12)
plate_tab_holes = [(10, 10), (10, 290)]
plate_bends = []

def plate_dxf(path):
    doc = ezdxf.new("R2010", setup=True); doc.units = ezdxf.units.MM
    msp = doc.modelspace(); doc.layers.add("CUT", color=7)
    for pl in (plate_outline, plate_window, plate_slot):
        msp.add_lwpolyline(pl, format="xyb", close=True, dxfattribs={"layer": "CUT"})
    for x, y in SO: msp.add_circle((x, y), 1.7, dxfattribs={"layer": "CUT"})
    for x, y in plate_tab_holes: msp.add_circle((x, y), 2.75, dxfattribs={"layer": "CUT"})
    doc.saveas(path)

# ---------- part 2: front acrylic 3 mm ----------
acr_outline = rrect(0, 0, W, H, 6)
X0 = -W / 2 + PF; sledW = PITCH * N + 4; cols = max(1, int(sledW // 120))
fx0 = X0 + sledW / 2 - (cols - 1) * 60
FANS = []  # front is solid now: the fans moved to the bottom panel (covers.py), air exits through the rear mesh
psuX = X0 + 4 + PITCH * N + 46 + W / 2
BTN = [(psuX, 255 - i * 28) for i in range(N)]
SW = (psuX, 140)
MOUNT = [(10, 10), (W / 2, 10), (W - 10, 10), (10, H / 2), (W - 10, H / 2), (10, H - 10), (W / 2, H - 10), (W - 10, H - 10)]

def acr_dxf(path):
    doc = ezdxf.new("R2010", setup=True); doc.units = ezdxf.units.MM
    msp = doc.modelspace(); doc.layers.add("CUT", color=7); doc.layers.add("ENGRAVE", color=1)
    msp.add_lwpolyline(acr_outline, format="xyb", close=True, dxfattribs={"layer": "CUT"})
    for x, y in MOUNT: msp.add_circle((x, y), 2.75, dxfattribs={"layer": "CUT"})
    for x, y in FANS:
        msp.add_circle((x, y), 58, dxfattribs={"layer": "CUT"})
        for dx in (-52.5, 52.5):
            for dy in (-52.5, 52.5): msp.add_circle((x + dx, y + dy), 2.25, dxfattribs={"layer": "CUT"})
    for i, (x, y) in enumerate(BTN):
        msp.add_circle((x, y), 8.1, dxfattribs={"layer": "CUT"})
        msp.add_text(str(i + 1), height=8, dxfattribs={"layer": "ENGRAVE"}).set_placement((x - 22, y), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    msp.add_circle(SW, 3.1, dxfattribs={"layer": "CUT"})
    msp.add_text("POWER", height=5, dxfattribs={"layer": "ENGRAVE"}).set_placement((SW[0], SW[1] - 14), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    doc.saveas(path)

# ---------- PDF drawings ----------
def setup(ax, title, w, h):
    ax.set_aspect("equal"); ax.set_xlim(-30, w + 30); ax.set_ylim(-35, h + 25); ax.axis("off")
    ax.set_title(title, fontsize=11, loc="left")

def dim(ax, p0, p1, off, text, vert=False):
    (x0, y0), (x1, y1) = p0, p1
    kw = dict(arrowstyle="<->", lw=0.6, color="#1f68c8", shrinkA=0, shrinkB=0)
    if vert:
        ax.annotate("", (x0 + off, y0), (x1 + off, y1), arrowprops=kw)
        ax.text(x0 + off - 2, (y0 + y1) / 2, text, rotation=90, va="center", ha="right", fontsize=7, color="#1f68c8")
    else:
        ax.annotate("", (x0, y0 + off), (x1, y1 + off), arrowprops=kw)
        ax.text((x0 + x1) / 2, y0 + off - 2, text, ha="center", va="top", fontsize=7, color="#1f68c8")

def draw_pl(ax, pl, **kw):
    ax.add_patch(Polygon(bulge_to_points(pl), closed=True, fill=False, lw=0.8, **kw))

def table(ax, rows, header, widths):
    ax.axis("off")
    t = ax.table(cellText=rows, colLabels=header, loc="upper left", cellLoc="center", colLoc="center", colWidths=widths)
    t.auto_set_font_size(False); t.set_fontsize(7.5); t.scale(1, 1.25)

def plate_pdf(path):
    with PdfPages(path) as pdf:
        fig = plt.figure(figsize=(11.69, 8.27))
        ax = fig.add_axes([0.03, 0.08, 0.55, 0.85]); setup(ax, "TẤM ĐỠ BO – nhôm 2 mm (5052/6061) – SL: 5 (4 + 1 dự phòng)", 232, 300)
        draw_pl(ax, plate_outline); draw_pl(ax, plate_window); draw_pl(ax, plate_slot)
        ax.add_patch(Polygon([(28, 28), (229, 28), (229, 271.84), (28, 271.84)], closed=True, fill=False, ls="--", lw=0.5, ec="#2e8b57"))
        ax.text(130, 265, "vị trí bo mạch 201 × 244 (nét đứt)", fontsize=6.5, color="#2e8b57", ha="center")
        for i, (x, y) in enumerate(SO):
            ax.add_patch(Circle((x, y), 1.7, fill=False, lw=0.8)); ax.text(x + 4, y + 3, f"H{i+1}", fontsize=7)
        for i, (x, y) in enumerate(plate_tab_holes):
            ax.add_patch(Circle((x, y), 2.75, fill=False, lw=0.8)); ax.text(x + 4, y + 3 if y < 150 else y - 8, f"T{i+1}", fontsize=7)
        ax.text(10, 150, "tay kéo", rotation=90, fontsize=6, ha="center", va="center")
        dim(ax, (0, 0), (232, 0), -14, "232"); dim(ax, (20, 0), (232, 0), -24, "212")
        dim(ax, (0, 2), (0, 298), -14, "296", vert=True); dim(ax, (232, 22.5), (232, 276.5), 14, "254", vert=True)
        ax.text(0, 306, "← SAU (phía cổng I/O; tai bắt ke góc vào thanh chặn sau)", fontsize=7)
        ax.text(232, 306, "TRƯỚC →", fontsize=7, ha="right")
        ax2 = fig.add_axes([0.6, 0.08, 0.38, 0.85])
        rows = [[f"H{i+1}", f"{x:.2f}", f"{y:.2f}", "Ø3,4", "M3 cột đồng 6 mm"] for i, (x, y) in enumerate(SO)]
        rows += [[f"T{i+1}", f"{x:.1f}", f"{y:.1f}", "Ø5,5", "M5 + đai ốc bắt ke góc 2020"] for i, (x, y) in enumerate(plate_tab_holes)]
        rows += [["Cửa sổ", "75–180", "55–175", "R10", "giảm khối lượng"], ["Tay kéo", "10", "128–172", "12 × 44", "rãnh ô van"]]
        table(ax2, rows, ["Lỗ", "X (mm)", "Y (mm)", "Kích thước", "Ghi chú"], [0.12, 0.14, 0.14, 0.17, 0.43])
        ax2.text(0, 0.42, "\n".join([
            "Gốc toạ độ: góc dưới‑trái của tai (X 20 = mặt sau thanh chặn).",
            "Tấm PHẲNG, không chấn. T1/T2: bắt 2 ke góc 2020 vào thanh chặn.",
            "Dung sai ±0,2 mm. Bo góc ngoài R2. Không vát mép, đánh ba via.",
            "H1–H7 = toạ độ lỗ chuẩn microATX. Bo 24,4 × 20,1 cm chỉ dùng",
            "  một phần các lỗ này; lỗ thừa để trống, không sao.",
            "Mặt linh kiện của bo hướng ra người nhìn (mặt này).",
            "Bản vẽ trang 2 in tỉ lệ 1:1 trên A3 để ướm bo trước khi đặt cắt.",
            "Khoét lõm X 100–200: mép dưới Y 28,5, mép trên Y 271,5 (chừa chỗ quạt).",
            "Khối lượng ≈ 215 g/tấm.",
        ]), fontsize=8, va="top", transform=ax2.transAxes)
        pdf.savefig(fig); plt.close(fig)
        # 1:1 template on A3 landscape (420 x 297 mm)
        fig = plt.figure(figsize=(420 / 25.4, 297 / 25.4))
        ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(-90, 330); ax.set_ylim(-1, 296); ax.set_aspect("equal"); ax.axis("off")
        draw_pl(ax, plate_outline); draw_pl(ax, plate_window); draw_pl(ax, plate_slot)
        ax.add_patch(Polygon([(28, 28), (229, 28), (229, 271.84), (28, 271.84)], closed=True, fill=False, ls="--", lw=0.5, ec="#2e8b57"))
        for i, (x, y) in enumerate(SO):
            ax.add_patch(Circle((x, y), 1.7, fill=False, lw=0.6)); ax.plot([x - 4, x + 4], [y, y], lw=0.3, c="k"); ax.plot([x, x], [y - 4, y + 4], lw=0.3, c="k")
            ax.text(x + 4, y + 3, f"H{i+1}", fontsize=7)
        ax.plot([-80, 20], [10, 10], lw=1, c="r"); ax.text(-80, 13, "thước kiểm tra: đoạn đỏ phải dài đúng 100 mm", fontsize=7, color="r")
        ax.text(-85, 285, "MẪU 1:1 – in A3, tỉ lệ 100 % (Actual size)\nĐặt bo mạch lên: lỗ bo phải trùng tâm H‑x.\n(Tấm cao 296 mm: tai chặn trên bị cắt vài mm khỏi khổ giấy – không ảnh hưởng.)", fontsize=8, va="top")
        pdf.savefig(fig); plt.close(fig)

def acr_pdf(path):
    with PdfPages(path) as pdf:
        fig = plt.figure(figsize=(11.69, 8.27))
        ax = fig.add_axes([0.03, 0.1, 0.6, 0.82]); setup(ax, f"MẶT TRƯỚC – mica đen trong 3 mm – SL: 1 (bản {N} máy, nhôm 2020)", W, H)
        draw_pl(ax, acr_outline)
        for x, y in MOUNT: ax.add_patch(Circle((x, y), 2.75, fill=False, lw=0.8))
        for i, (x, y) in enumerate(FANS):
            ax.add_patch(Circle((x, y), 58, fill=False, lw=0.8)); ax.text(x, y, f"F{i+1}\nØ116", ha="center", va="center", fontsize=7)
            for dx in (-52.5, 52.5):
                for dy in (-52.5, 52.5): ax.add_patch(Circle((x + dx, y + dy), 2.25, fill=False, lw=0.6))
        for i, (x, y) in enumerate(BTN):
            ax.add_patch(Circle((x, y), 8.1, fill=False, lw=0.8)); ax.text(x - 22, y, str(i + 1), ha="center", va="center", fontsize=8, color="r")
        ax.add_patch(Circle(SW, 3.1, fill=False, lw=0.8)); ax.text(SW[0], SW[1] - 14, "POWER", ha="center", fontsize=6, color="r")
        dim(ax, (0, 0), (W, 0), -14, f"{W}"); dim(ax, (0, 0), (0, H), -14, f"{H}", vert=True)
        ax2 = fig.add_axes([0.65, 0.1, 0.33, 0.82])
        rows = [[f"M{i+1}", f"{x:.0f}", f"{y:.0f}", "Ø5,5"] for i, (x, y) in enumerate(MOUNT)]
        rows += [[f"F{i+1}", f"{x:.0f}", f"{y:.0f}", "Ø116 + 4 lỗ Ø4,5 (vuông 105)"] for i, (x, y) in enumerate(FANS)]
        rows += [[f"B{i+1}", f"{x:.0f}", f"{y:.0f}", "Ø16,2"] for i, (x, y) in enumerate(BTN)]
        rows += [["S", f"{SW[0]:.0f}", f"{SW[1]:.0f}", "Ø6,2"]]
        table(ax2, rows, ["Lỗ", "X", "Y", "Kích thước (mm)"], [0.12, 0.13, 0.13, 0.62])
        ax2.text(0, 0.2, "\n".join([
            "Gốc: góc dưới‑trái, nhìn từ phía trước.",
            "Lớp CUT = cắt xuyên. Lớp ENGRAVE (đỏ) = khắc chữ.",
            "M1–M8: vít M5 × 10 vào con trượt T (thanh 2020).",
            "Mặt trước kín: quạt nằm ở tấm đáy, hút gió từ dưới lên.",
            "B: nút nhấn 16 mm có LED. S: CÔNG TẮC TỔNG (gạt, nối PS_ON nguồn).",
            "Bo góc R6. Dung sai ±0,3 mm.",
        ]), fontsize=8, va="top", transform=ax2.transAxes)
        pdf.savefig(fig); plt.close(fig)

# ---------- part 3: comb STL (3D print, PETG) ----------
def comb_stl(path, hole_y=30.0, lead_both=False):
    """hole_y: distance of the screw holes from the lead-in edge (30 = rail centre, 10 = edge bar)."""
    L, Dp, T = 72.0, 60.0, 6.0
    body = m3d.Manifold.cube([L, Dp, T])
    groove = m3d.Manifold.cube([2.6, Dp + 2, 3.6]).translate([5 - 1.3, -1, T - 3.5])
    lead = m3d.Manifold.batch_hull([
        m3d.Manifold.cube([4.6, 0.01, 3.6]).translate([5 - 2.3, -0.5, T - 3.5]),
        m3d.Manifold.cube([2.6, 0.01, 3.6]).translate([5 - 1.3, 3, T - 3.5])])
    cut = groove + lead
    if lead_both:
        cut = cut + lead.mirror([0, 1, 0]).translate([0, Dp, 0])
    for hx in (30.0, 58.0):
        cut = cut + m3d.Manifold.cylinder(T + 2, 2.75, 2.75, 48).translate([hx, hole_y, -1])
        cut = cut + m3d.Manifold.cylinder(3.2, 5.25, 5.25, 48).translate([hx, hole_y, T - 3])
    part = body - cut
    mesh = part.to_mesh()
    tm = trimesh.Trimesh(vertices=np.asarray(mesh.vert_properties)[:, :3], faces=np.asarray(mesh.tri_verts))
    assert tm.is_watertight
    tm.export(path)
    return tm.volume

plate_dxf(f"{OUT}/tam-do-bo_nhom-2mm_x5.dxf"); plate_pdf(f"{OUT}/tam-do-bo_nhom-2mm.pdf")
acr_dxf(f"{OUT}/mat-truoc_mica-3mm_x1.dxf"); acr_pdf(f"{OUT}/mat-truoc_mica-3mm.pdf")
vol = comb_stl(f"{OUT}/luoc_PETG_x16.stl", hole_y=10.0, lead_both=True)  # on the front + ear-stop bars, top and bottom, 2 per bay each
print("W", W, "fans", FANS, "btn", BTN, "SW", SW)
print("standoffs", SO)
print("comb volume cm3", round(vol / 1000, 2), "~g PETG", round(vol / 1000 * 1.27, 1))
