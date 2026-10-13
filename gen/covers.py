"""Dust covers (3 mm acrylic): top + bottom (same part, x2), left side, right side with a filtered PSU-fan hole.
Front = filtered fan intake, rear left open as the only exhaust -> slight positive pressure keeps dust out."""
import sys
import ezdxf
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle

OUT = sys.argv[1]
W, H, D = 424, 300, 260
# Top/bottom: X = from left (seen from front), Y = from rear edge. Holes land on the top slots of the
# front/rear bars (Y 10 / 250) and side bars (X 10 / 414); corners avoided (post ends have no slot).
TOP = [(x, y) for x in (62, 212, 362) for y in (10, 250)] + [(x, y) for x in (10, W - 10) for y in (70, 190)]
# Sides: X = from rear edge, Y = height. Holes on the posts (X 10 / 250) and the side bars (Y 10 / 290).
SIDE = [(x, y) for x in (10, D - 10) for y in (60, 240)] + [(x, y) for x in (70, 190) for y in (10, H - 10)]
PSU_FAN = (80, 95)  # PSU on the bottom bars -> fan centre Y 95; the PSU slides along Z on velcro to meet the hole

def rect(msp, w, h, r=6):
    import math
    b = math.tan(math.pi / 8)
    pts = [(r, 0, 0), (w - r, 0, b), (w, r, 0), (w, h - r, b), (w - r, h, 0), (r, h, b), (0, h - r, 0), (0, r, b)]
    msp.add_lwpolyline(pts, format="xyb", close=True, dxfattribs={"layer": "CUT"})

def fan(msp, c):
    msp.add_circle(c, 58, dxfattribs={"layer": "CUT"})
    for dx in (-52.5, 52.5):
        for dy in (-52.5, 52.5): msp.add_circle((c[0] + dx, c[1] + dy), 2.25, dxfattribs={"layer": "CUT"})

def dxf(path, w, h, holes, fan_at=None):
    doc = ezdxf.new("R2010", setup=True); doc.units = ezdxf.units.MM
    msp = doc.modelspace(); doc.layers.add("CUT", color=7)
    rect(msp, w, h)
    for p in holes: msp.add_circle(p, 2.75, dxfattribs={"layer": "CUT"})
    if fan_at: fan(msp, fan_at)
    doc.saveas(path)

def page(pdf, title, w, h, holes, notes, fan_at=None, xlab="", ylab=""):
    fig = plt.figure(figsize=(11.69, 8.27))
    ax = fig.add_axes([0.03, 0.1, 0.6, 0.82]); ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-30, w + 30); ax.set_ylim(-35, h + 25); ax.set_title(title, fontsize=11, loc="left")
    ax.add_patch(plt.Rectangle((0, 0), w, h, fill=False, lw=0.8))
    for i, (x, y) in enumerate(holes):
        ax.add_patch(Circle((x, y), 2.75, fill=False, lw=0.8)); ax.text(x + 4, y + 3, f"M{i+1}", fontsize=7)
    if fan_at:
        ax.add_patch(Circle(fan_at, 58, fill=False, lw=0.8)); ax.text(*fan_at, "F\nØ116", ha="center", va="center", fontsize=7)
        for dx in (-52.5, 52.5):
            for dy in (-52.5, 52.5): ax.add_patch(Circle((fan_at[0] + dx, fan_at[1] + dy), 2.25, fill=False, lw=0.6))
    kw = dict(arrowstyle="<->", lw=0.6, color="#1f68c8")
    ax.annotate("", (0, -14), (w, -14), arrowprops=kw); ax.text(w / 2, -18, f"{w}", ha="center", va="top", fontsize=7, color="#1f68c8")
    ax.annotate("", (-14, 0), (-14, h), arrowprops=kw); ax.text(-18, h / 2, f"{h}", rotation=90, ha="right", va="center", fontsize=7, color="#1f68c8")
    ax.text(0, h + 8, xlab, fontsize=7); ax.text(w, h + 8, ylab, fontsize=7, ha="right")
    ax2 = fig.add_axes([0.65, 0.1, 0.33, 0.82]); ax2.axis("off")
    rows = [[f"M{i+1}", f"{x:.0f}", f"{y:.0f}", "Ø5,5"] for i, (x, y) in enumerate(holes)]
    if fan_at: rows.append(["F", f"{fan_at[0]}", f"{fan_at[1]}", "Ø116 + 4 lỗ Ø4,5 (vuông 105)"])
    t = ax2.table(cellText=rows, colLabels=["Lỗ", "X", "Y", "Kích thước (mm)"], loc="upper left", cellLoc="center", colWidths=[0.12, 0.13, 0.13, 0.62])
    t.auto_set_font_size(False); t.set_fontsize(7.5); t.scale(1, 1.25)
    ax2.text(0, 0.42, "\n".join(notes), fontsize=8, va="top", transform=ax2.transAxes)
    pdf.savefig(fig); plt.close(fig)

dxf(f"{OUT}/nap-tren-duoi_mica-3mm_x2.dxf", W, D, TOP)
dxf(f"{OUT}/hong-trai_mica-3mm_x1.dxf", D, H, SIDE)
dxf(f"{OUT}/hong-phai_mica-3mm_x1.dxf", D, H, SIDE, PSU_FAN)
common = ["Lớp CUT = cắt xuyên. Bo góc R6. Dung sai ±0,3 mm.", "M: vít M5 × 10 + long đền vào con trượt T (rãnh 2020)."]
with PdfPages(f"{OUT}/tam-che-bui_mica-3mm.pdf") as pdf:
    page(pdf, "NẮP TRÊN + ĐÁY – mica 3 mm – SL: 2 (cùng một mẫu)", W, D, TOP,
         ["Gốc: góc trái‑sau. X = từ trái sang (nhìn từ trước), Y = từ mép sau.", *common,
          "Lỗ nằm trên rãnh mặt trên của 4 thanh viền,", "  tránh góc (đầu cột không có rãnh).",
          "Tấm đáy: dán 4 chân cao su dưới tấm, ở 4 góc."], xlab="↑ mép TRƯỚC (Y = 260); mép dưới hình = SAU (Y = 0)", ylab="")
    page(pdf, "HÔNG TRÁI – mica 3 mm – SL: 1", D, H, SIDE,
         ["Gốc: góc dưới‑sau. X = từ mép sau, Y = chiều cao.", *common, "Mica trong 2 mặt như nhau: lật tấm nào cũng được."],
         xlab="← SAU", ylab="TRƯỚC →")
    page(pdf, "HÔNG PHẢI (phía nguồn) – mica 3 mm – SL: 1", D, H, SIDE,
         ["Gốc: góc dưới‑sau. X = từ mép sau, Y = chiều cao.", *common,
          "F: lỗ cho quạt hút của nguồn ATX + lưới lọc 12 cm,", "  bắt vít M4 × 10 + đai ốc.",
          "Không cần đo nguồn: nguồn ATX cao 150 mm, đặt trên 2 thanh đáy", "  -> tâm quạt luôn ở Y ≈ 95. Khi lắp, trượt nguồn tới/lui", "  (dán gai) cho quạt trùng lỗ F, nhìn qua mica. Hợp nguồn", "  dài 140–180 mm, quạt 120/135/140 mm."],
         fan_at=PSU_FAN, xlab="← SAU", ylab="TRƯỚC →")
print("ok")
