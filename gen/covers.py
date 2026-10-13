"""Dust covers, all six faces closed (3 mm acrylic). Mesh filters only where air moves:
front = 4 fans in (front panel, gen.py), right side = PSU fan in, rear = 4 exhaust holes out.
Rear posts sit 50 mm behind the old rear bars (kept as ear stops), so the box is 424 x 310 x 300.
The PSU's rear end passes through a cut-out in the rear panel: AC inlet, switch and PSU exhaust stay outside."""
import sys, math
import ezdxf
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle, Rectangle

OUT = sys.argv[1]
W, H, D = 424, 300, 310                     # box: frame 260 + 50 mm rear bay
# Top/bottom: X from left (seen from front), Y from rear edge. Front bar Y 300, ear-stop bar Y 60, side bars X 10/414.
TOP = [(x, y) for x in (62, 212, 362) for y in (60, 300)] + [(x, y) for x in (10, W - 10) for y in (100, 220)]
# Sides: X from rear edge, Y height. Rear post X 10, front post X 300, side bars Y 10 / 290.
SIDE = [(x, y) for x in (10, D - 10) for y in (60, 240)] + [(x, y) for x in (100, 210) for y in (10, H - 10)]
PSU_FAN = (80, 95)                          # PSU (160 mm) pushed into the rear cut-out -> fan centre 80 mm from rear
# Rear: seen from BEHIND, X from left (= right side of the frame seen from front), Y height.
REAR = [(x, y) for x in (10, W - 10) for y in (30, 110, 190, 270)]
EXH = [(x, y) for x in (198, 318) for y in (85, 205)]       # behind the 4 front fans
PSU_CUT = (22, 19, 110, 171)                # 88 x 152 opening for the PSU rear end (PSU 86 x 150)
KEY = (52, 240, 14.8, 16.4)                 # keystone RJ45 coupler: centre, w, h

def outline(msp, w, h, r=6):
    b = math.tan(math.pi / 8)
    msp.add_lwpolyline([(r, 0, 0), (w - r, 0, b), (w, r, 0), (w, h - r, b), (w - r, h, 0), (r, h, b), (0, h - r, 0), (0, r, b)],
                       format="xyb", close=True, dxfattribs={"layer": "CUT"})

def filt(msp, c):
    msp.add_circle(c, 58, dxfattribs={"layer": "CUT"})
    for dx in (-52.5, 52.5):
        for dy in (-52.5, 52.5): msp.add_circle((c[0] + dx, c[1] + dy), 2.25, dxfattribs={"layer": "CUT"})

def rect(msp, x0, y0, x1, y1):
    msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True, dxfattribs={"layer": "CUT"})

def dxf(path, w, h, holes, fans=(), rects=()):
    doc = ezdxf.new("R2010", setup=True); doc.units = ezdxf.units.MM
    msp = doc.modelspace(); doc.layers.add("CUT", color=7)
    outline(msp, w, h)
    for p in holes: msp.add_circle(p, 2.75, dxfattribs={"layer": "CUT"})
    for c in fans: filt(msp, c)
    for r in rects: rect(msp, *r)
    doc.saveas(path)

def page(pdf, title, w, h, holes, notes, fans=(), rects=(), xlab="", ylab=""):
    fig = plt.figure(figsize=(11.69, 8.27))
    ax = fig.add_axes([0.03, 0.1, 0.6, 0.82]); ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-30, w + 30); ax.set_ylim(-35, h + 25); ax.set_title(title, fontsize=11, loc="left")
    ax.add_patch(Rectangle((0, 0), w, h, fill=False, lw=0.8))
    for i, (x, y) in enumerate(holes):
        ax.add_patch(Circle((x, y), 2.75, fill=False, lw=0.8)); ax.text(x + 4, y + 3, f"M{i+1}", fontsize=7)
    for i, c in enumerate(fans):
        ax.add_patch(Circle(c, 58, fill=False, lw=0.8, hatch="++", ec="#33475b")); ax.text(*c, f"L{i+1}\nØ116", ha="center", va="center", fontsize=7, backgroundcolor="white")
        for dx in (-52.5, 52.5):
            for dy in (-52.5, 52.5): ax.add_patch(Circle((c[0] + dx, c[1] + dy), 2.25, fill=False, lw=0.6))
    for name, (x0, y0, x1, y1) in rects:
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, lw=0.8)); ax.text((x0 + x1) / 2, (y0 + y1) / 2, name, ha="center", va="center", fontsize=6.5)
    kw = dict(arrowstyle="<->", lw=0.6, color="#1f68c8")
    ax.annotate("", (0, -14), (w, -14), arrowprops=kw); ax.text(w / 2, -18, f"{w}", ha="center", va="top", fontsize=7, color="#1f68c8")
    ax.annotate("", (-14, 0), (-14, h), arrowprops=kw); ax.text(-18, h / 2, f"{h}", rotation=90, ha="right", va="center", fontsize=7, color="#1f68c8")
    ax.text(0, h + 8, xlab, fontsize=7); ax.text(w, h + 8, ylab, fontsize=7, ha="right")
    ax2 = fig.add_axes([0.65, 0.1, 0.33, 0.82]); ax2.axis("off")
    rows = [[f"M{i+1}", f"{x:.0f}", f"{y:.0f}", "Ø5,5"] for i, (x, y) in enumerate(holes)]
    rows += [[f"L{i+1}", f"{c[0]}", f"{c[1]}", "Ø116 + 4 lỗ Ø4,5 (vuông 105)"] for i, c in enumerate(fans)]
    rows += [[n.split()[0], f"{x0}–{x1}", f"{y0}–{y1}", "khoét chữ nhật"] for n, (x0, y0, x1, y1) in rects]
    t = ax2.table(cellText=rows, colLabels=["Lỗ", "X", "Y", "Kích thước (mm)"], loc="upper left", cellLoc="center", colWidths=[0.14, 0.15, 0.15, 0.56])
    t.auto_set_font_size(False); t.set_fontsize(7); t.scale(1, 1.15)
    ax2.text(0, 0.36, "\n".join(notes), fontsize=7.5, va="top", transform=ax2.transAxes)
    pdf.savefig(fig); plt.close(fig)

kx, ky, kw_, kh = KEY
key_r = (round(kx - kw_ / 2, 1), round(ky - kh / 2, 1), round(kx + kw_ / 2, 1), round(ky + kh / 2, 1))
dxf(f"{OUT}/nap-tren-duoi_mica-3mm_x2.dxf", W, D, TOP)
dxf(f"{OUT}/hong-trai_mica-3mm_x1.dxf", D, H, SIDE)
dxf(f"{OUT}/hong-phai_mica-3mm_x1.dxf", D, H, SIDE, [PSU_FAN])
dxf(f"{OUT}/mat-sau_mica-3mm_x1.dxf", W, H, REAR, EXH, [PSU_CUT, key_r])
common = ["Lớp CUT = cắt xuyên. Bo góc R6. Dung sai ±0,3 mm.", "M: vít M5 × 10 + long đền vào con trượt T (rãnh 2020).",
          "L (gạch chéo): lỗ có LƯỚI LỌC 12 cm, vít M4 × 10 + đai ốc."]
with PdfPages(f"{OUT}/tam-che-bui_mica-3mm.pdf") as pdf:
    page(pdf, "NẮP TRÊN + ĐÁY – mica 3 mm – SL: 2 (cùng một mẫu), kín hoàn toàn", W, D, TOP,
         ["Gốc: góc trái‑sau. X từ trái (nhìn từ trước), Y từ mép sau.", *common[:2],
          "Y 300 = thanh trước, Y 60 = thanh chặn tai, X 10/414 = thanh hông.", "Tấm đáy: dán 4 chân cao su ở 4 góc."],
         xlab="↑ mép TRƯỚC (Y = 310); mép dưới hình = SAU (Y = 0)")
    page(pdf, "HÔNG TRÁI – mica 3 mm – SL: 1, kín hoàn toàn", D, H, SIDE,
         ["Gốc: góc dưới‑sau. X từ mép sau, Y chiều cao.", *common[:2], "Mica trong 2 mặt như nhau: lật tấm nào cũng được."],
         xlab="← SAU", ylab="TRƯỚC →")
    page(pdf, "HÔNG PHẢI (phía nguồn) – mica 3 mm – SL: 1", D, H, SIDE,
         ["Gốc: góc dưới‑sau. X từ mép sau, Y chiều cao.", *common,
          "L1: gió vào quạt nguồn. Nguồn đút đuôi qua lỗ mặt sau,", "  tâm quạt cách mép sau ≈ 80 mm (nguồn dài 140–180",
          "  -> lệch tối đa 10 mm, quạt vẫn hút qua lưới)."], fans=[PSU_FAN], xlab="← SAU", ylab="TRƯỚC →")
    page(pdf, "MẶT SAU – mica 3 mm – SL: 1 (tháo ra khi rút máy)", W, H, REAR,
         ["Gốc: góc dưới‑trái NHÌN TỪ PHÍA SAU. Y chiều cao.", *common,
          "L1–L4: gió nóng thoát ra (sau 4 khoang máy).", "PSU: lỗ 88 × 152 cho đuôi nguồn: ổ cắm AC, công tắc,",
          "  quạt thoát của nguồn lộ ra ngoài. Dán ron xốp quanh khe.", "RJ45: keystone 14,8 × 16,4 – cáp mạng ra router.",
          "  Mica 3 mm dày hơn chuẩn keystone: nếu lẫy không ăn,", "  cố định bằng keo nến/keo 2 thành phần.",
          "M: bắt vào 2 cột sau (X 10 / 414)."], fans=EXH,
         rects=[("PSU đuôi nguồn", PSU_CUT), ("RJ45", key_r)], xlab="← phía NGUỒN (bên phải khi nhìn từ trước)", ylab="")
print("ok")
