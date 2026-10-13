"""Dust covers, all six faces closed (3 mm acrylic). Mesh filters only where air moves:
top = 3 x 92 mm fans in (blowing down), bottom = 3 x 92 mm fans out, right side = PSU fan in. Front + rear solid.
Rear posts sit 50 mm behind the old rear bars (kept as ear stops), so the box is 424 x 290 x 300 (front trimmed 20 mm).
The PSU's rear end passes through a cut-out in the rear panel: AC inlet, switch and PSU exhaust stay outside."""
import sys, math
import ezdxf
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle, Rectangle

OUT = sys.argv[1]
W, H, D = 424, 300, 290                     # box: frame 240 (front trimmed 20 mm) + 50 mm rear bay
# Top/bottom: X from left (seen from front), Y from rear edge. Front bar Y 300, ear-stop bar Y 60, side bars X 10/414.
TOP = [(x, y) for x in (62, 212, 362) for y in (60, D - 10)] + [(x, y) for x in (10, W - 10) for y in (100, 220)]
# Sides: X from rear edge, Y height. Rear post X 10, front post X 300, side bars Y 10 / 290.
SIDE = [(x, y) for x in (10, D - 10) for y in (60, 240)] + [(x, y) for x in (100, 210) for y in (10, H - 10)]
PSU_FAN = (80, 95)                          # PSU (160 mm) pushed into the rear cut-out -> fan centre 80 mm from rear
# Rear: seen from BEHIND, X from left (= right side of the frame seen from front), Y height.
REAR = [(x, y) for x in (10, W - 10) for y in (30, 110, 190, 270)]
EXH = []                                    # rear is solid now (air leaves through the bottom fans)
ROW = [(68, 180), (164, 180), (260, 180)]   # 3 x 92 mm fans, one row over/under the 4 bays (X = x + 212, Y = z + 180)
ZBAR_BOT = [(320, 130), (320, 230)]         # bottom 90-degree bar under the PSU's left edge (x 108)
ZBAR_TOP = [(372, 130), (372, 230)]         # top 90-degree bar that hangs the switch holder (x 160)
FEET = [(10, 10), (W - 10, 10), (10, D - 10), (W - 10, D - 10)]   # M5 feet into the post ends
# PSU bolted to the rear panel with the standard ATX 6-32 pattern (138 / 74 / 114 mm on the 150 x 86 face).
# PSU face spans X 23-109 (seen from behind), Y 20-170. Fan side (X 29) gets both possible 3rd-hole spots.
PSU_CUT = (35, 32, 97, 158)                 # 62 x 126 opening: AC inlet, switch, PSU exhaust stay outside
PSU_HOLES = [(103, 26), (103, 164), (29, 26), (29, 50), (29, 140), (29, 164)]
KEY = (52, 240, 14.8, 16.4)                 # keystone RJ45 coupler: centre, w, h

def outline(msp, w, h, r=6):
    b = math.tan(math.pi / 8)
    msp.add_lwpolyline([(r, 0, 0), (w - r, 0, b), (w, r, 0), (w, h - r, b), (w - r, h, 0), (r, h, b), (0, h - r, 0), (0, r, b)],
                       format="xyb", close=True, dxfattribs={"layer": "CUT"})

PERF_D, PERF_P = 6.0, 7.5                   # perforation: Ø6 holes on a 7.5 mm hex grid (~58 % open)
def perf(c, r):
    """Hex grid of small round holes filling a circle of radius r (filter sits behind them, inside)."""
    pts, dy = [], PERF_P * 0.8660254
    for j in range(-int(r / dy) - 1, int(r / dy) + 2):
        for i in range(-int(r / PERF_P) - 1, int(r / PERF_P) + 2):
            x, y = i * PERF_P + (PERF_P / 2 if j % 2 else 0), j * dy
            if math.hypot(x, y) <= r - PERF_D / 2: pts.append((c[0] + x, c[1] + y))
    return pts

def filt(msp, c, r=58, sq=52.5):
    for q in perf(c, r - 2): msp.add_circle(q, PERF_D / 2, dxfattribs={"layer": "CUT"})
    for dx in (-sq, sq):
        for dy in (-sq, sq): msp.add_circle((c[0] + dx, c[1] + dy), 2.25, dxfattribs={"layer": "CUT"})

def rect(msp, x0, y0, x1, y1):
    msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True, dxfattribs={"layer": "CUT"})

def dxf(path, w, h, holes, fans=(), rects=(), fans92=(), small=()):
    doc = ezdxf.new("R2010", setup=True); doc.units = ezdxf.units.MM
    msp = doc.modelspace(); doc.layers.add("CUT", color=7)
    outline(msp, w, h)
    for p in holes: msp.add_circle(p, 2.75, dxfattribs={"layer": "CUT"})
    for p in small: msp.add_circle(p, 1.9, dxfattribs={"layer": "CUT"})
    for c in fans: filt(msp, c)
    for c in fans92: filt(msp, c, 44, 41.25)
    for r in rects: rect(msp, *r)
    doc.saveas(path)

def page(pdf, title, w, h, holes, notes, fans=(), rects=(), xlab="", ylab="", fans92=(), small=()):
    fig = plt.figure(figsize=(11.69, 8.27))
    ax = fig.add_axes([0.03, 0.1, 0.6, 0.82]); ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-30, w + 30); ax.set_ylim(-35, h + 25); ax.set_title(title, fontsize=11, loc="left")
    ax.add_patch(Rectangle((0, 0), w, h, fill=False, lw=0.8))
    for i, (x, y) in enumerate(holes):
        ax.add_patch(Circle((x, y), 2.75, fill=False, lw=0.8)); ax.text(x + 4, y + 3, f"M{i+1}", fontsize=7)
    for i, (x, y) in enumerate(small):
        ax.add_patch(Circle((x, y), 1.9, fill=False, lw=0.8)); ax.text(x + 3, y - 6, f"N{i+1}", fontsize=6)
    for i, c in enumerate(fans):
        for q in perf(c, 56): ax.add_patch(Circle(q, PERF_D / 2, fill=False, lw=0.3))
        ax.text(*c, f"L{i+1}", ha="center", va="center", fontsize=7, backgroundcolor="white")
        for dx in (-52.5, 52.5):
            for dy in (-52.5, 52.5): ax.add_patch(Circle((c[0] + dx, c[1] + dy), 2.25, fill=False, lw=0.6))
    for i, c in enumerate(fans92):
        for q in perf(c, 42): ax.add_patch(Circle(q, PERF_D / 2, fill=False, lw=0.3))
        ax.text(*c, f"Q{i+1}", ha="center", va="center", fontsize=7, backgroundcolor="white")
        for dx in (-41.25, 41.25):
            for dy in (-41.25, 41.25): ax.add_patch(Circle((c[0] + dx, c[1] + dy), 2.25, fill=False, lw=0.6))
    for name, (x0, y0, x1, y1) in rects:
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, lw=0.8)); ax.text((x0 + x1) / 2, (y0 + y1) / 2, name, ha="center", va="center", fontsize=6.5)
    kw = dict(arrowstyle="<->", lw=0.6, color="#1f68c8")
    ax.annotate("", (0, -14), (w, -14), arrowprops=kw); ax.text(w / 2, -18, f"{w}", ha="center", va="top", fontsize=7, color="#1f68c8")
    ax.annotate("", (-14, 0), (-14, h), arrowprops=kw); ax.text(-18, h / 2, f"{h}", rotation=90, ha="right", va="center", fontsize=7, color="#1f68c8")
    ax.text(0, h + 8, xlab, fontsize=7); ax.text(w, h + 8, ylab, fontsize=7, ha="right")
    ax2 = fig.add_axes([0.65, 0.1, 0.33, 0.82]); ax2.axis("off")
    rows = [[f"M{i+1}", f"{x:.0f}", f"{y:.0f}", "Ø5,5"] for i, (x, y) in enumerate(holes)]
    rows += [[f"L{i+1}", f"{c[0]}", f"{c[1]}", f"{len(perf(c, 56))} lỗ Ø6 + 4 lỗ Ø4,5"] for i, c in enumerate(fans)]
    rows += [[f"Q{i+1}", f"{c[0]}", f"{c[1]}", f"{len(perf(c, 42))} lỗ Ø6 + 4 lỗ Ø4,5"] for i, c in enumerate(fans92)]
    rows += [[n.split()[0], f"{x0}–{x1}", f"{y0}–{y1}", "khoét chữ nhật"] for n, (x0, y0, x1, y1) in rects]
    rows += [[f"N{i+1}", f"{x}", f"{y}", "Ø3,8 (vít nguồn 6‑32)"] for i, (x, y) in enumerate(small)]
    t = ax2.table(cellText=rows, colLabels=["Lỗ", "X", "Y", "Kích thước (mm)"], loc="upper left", cellLoc="center", colWidths=[0.14, 0.15, 0.15, 0.56])
    t.auto_set_font_size(False); t.set_fontsize(7); t.scale(1, 1.15)
    ax2.text(0, 0.36, "\n".join(notes), fontsize=7.5, va="top", transform=ax2.transAxes)
    pdf.savefig(fig); plt.close(fig)

kx, ky, kw_, kh = KEY
key_r = (round(kx - kw_ / 2, 1), round(ky - kh / 2, 1), round(kx + kw_ / 2, 1), round(ky + kh / 2, 1))
dxf(f"{OUT}/nap-tren_mica-3mm_x1.dxf", W, D, TOP + ZBAR_TOP, fans92=ROW)
dxf(f"{OUT}/day_mica-3mm_x1.dxf", W, D, TOP + ZBAR_BOT + FEET, fans92=ROW)
dxf(f"{OUT}/hong-trai_mica-3mm_x1.dxf", D, H, SIDE)
dxf(f"{OUT}/hong-phai_mica-3mm_x1.dxf", D, H, SIDE, [PSU_FAN])
dxf(f"{OUT}/mat-sau_mica-3mm_x1.dxf", W, H, REAR, rects=[PSU_CUT, key_r], small=PSU_HOLES)
common = ["Lớp CUT = cắt xuyên. Bo góc R6. Dung sai ±0,3 mm.", "M: vít M5 × 10 + long đền vào con trượt T (rãnh 2020).",
          "L / Q: vùng đục lỗ Ø6 (lưới tổ ong); LƯỚI LỌC đen đặt PHÍA TRONG."]
with PdfPages(f"{OUT}/tam-che-bui_mica-3mm.pdf") as pdf:
    page(pdf, "NẮP TRÊN – mica đen trong 3 mm – SL: 1 – 3 quạt 92 mm HÚT VÀO", W, D, TOP + ZBAR_TOP,
         ["Gốc: góc trái‑sau. X từ trái (nhìn từ trước), Y từ mép sau.", *common,
          "Q1–Q3: quạt 92 mm nằm TRONG thùng sát dưới tấm, thổi XUỐNG;", "  lưới 9 cm dán ngoài; vít M4 × 12 + đai ốc (bích ngoài quạt).",
          "Y 280 = thanh trước, Y 60 = thanh chặn tai, X 10/414 = hông,", "  X 372 = thanh dọc nóc (treo giá switch)."],
         xlab="↑ mép TRƯỚC (Y = 310); mép dưới hình = SAU (Y = 0)", fans92=ROW)
    page(pdf, "ĐÁY – mica đen trong 3 mm – SL: 1 – 3 quạt 92 mm ĐẨY RA", W, D, TOP + ZBAR_BOT + FEET,
         ["Gốc: góc trái‑sau, NHÌN TỪ TRÊN XUỐNG. X từ trái, Y từ mép sau.", *common,
          "Q1–Q3: quạt 92 mm nằm TRONG thùng sát trên tấm, thổi ra;", "  lưới 9 cm dán ngoài; vít M4 × 12 + đai ốc.",
          "X 320 = thanh dọc đáy (đỡ nguồn).", "4 lỗ góc: chân in 25 mm, vít M5 × 30 vào lỗ tâm đầu cột", "  (taro M5 đầu cột)."],
         xlab="↑ mép TRƯỚC (Y = 310); mép dưới hình = SAU (Y = 0)", fans92=ROW)
    page(pdf, "HÔNG TRÁI – mica đen trong 3 mm – SL: 1, kín hoàn toàn", D, H, SIDE,
         ["Gốc: góc dưới‑sau. X từ mép sau, Y chiều cao.", *common[:2], "Mica trong 2 mặt như nhau: lật tấm nào cũng được."],
         xlab="← SAU", ylab="TRƯỚC →")
    page(pdf, "HÔNG PHẢI (phía nguồn) – mica đen trong 3 mm – SL: 1", D, H, SIDE,
         ["Gốc: góc dưới‑sau. X từ mép sau, Y chiều cao.", *common,
          "L1: gió vào quạt nguồn. Nguồn đút đuôi qua lỗ mặt sau,", "  tâm quạt cách mép sau ≈ 80 mm (nguồn dài 140–180",
          "  -> lệch tối đa 10 mm, quạt vẫn hút qua lưới)."], fans=[PSU_FAN], xlab="← SAU", ylab="TRƯỚC →")
    page(pdf, "MẶT SAU – mica đen trong 3 mm – SL: 1, kín (tháo ra khi rút máy)", W, H, REAR,
         ["Gốc: góc dưới‑trái NHÌN TỪ PHÍA SAU. Y chiều cao.", *common,
"PSU: lỗ 62 × 126 lộ ổ cắm AC, công tắc, quạt thoát nguồn.",
          "N1–N6: bắt nguồn bằng 4 vít 6‑32 (chuẩn ATX); 2 lỗ thừa",
          "  để nguồn quay chiều nào cũng bắt được.", "RJ45: keystone 14,8 × 16,4 – cáp mạng ra router.",
          "  Mica 3 mm dày hơn chuẩn keystone: nếu lẫy không ăn,", "  cố định bằng keo nến/keo 2 thành phần.",
          "M: bắt vào 2 cột sau (X 10 / 414)."],
         rects=[("PSU đuôi nguồn", PSU_CUT), ("RJ45", key_r)], small=PSU_HOLES, xlab="← phía NGUỒN (bên phải khi nhìn từ trước)", ylab="")
print("ok")
