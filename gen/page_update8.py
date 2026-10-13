"""Plates screwed to the frame: two 90-degree rear tabs bolted to the ear-stop bars (M5 x 10 + T-nut)."""
import re, sys
p = sys.argv[1]
s = open(p).read()
def R(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
def RX(pat, b, n=1):
    global s
    s2, c = re.subn(pat, b, s, flags=re.S); assert c == n, (c, pat[:80]); s = s2
R("[[0, 2], [20, 2], [20, 22.5], [100, 22.5], [100, 28.5], [200, 28.5], [200, 22.5], [232, 22.5], [232, 276.5], [200, 276.5], [200, 271.5], [100, 271.5], [100, 276.5], [20, 276.5], [20, 298], [0, 298]]",
  "[[20, 22.5], [100, 22.5], [100, 28.5], [200, 28.5], [200, 22.5], [232, 22.5], [232, 276.5], [200, 276.5], [200, 271.5], [100, 271.5], [100, 276.5], [20, 276.5]]")
RX(r"      const slot = new THREE\.Path\(\);\n.*?      s\.holes\.push\(win, slot\);\n      for \(const y of \[10, 290\]\) \{ const h = new THREE\.Path\(\); h\.absarc\(10, y, 2\.5, 0, Math\.PI \* 2, true\); s\.holes\.push\(h\); \}\n",
   "      s.holes.push(win);\n")
RX(r"const pm = tag\(new THREE\.Mesh\(plateGeo, mat\.plate\), `Tấm đỡ nhôm 2 mm[^`]*`, g\);\n        pm\.rotation\.y = -Math\.PI / 2; pm\.position\.set\(2, 0, -150\);",
   "const pm = tag(new THREE.Mesh(plateGeo, mat.plate), `Tấm đỡ nhôm 2 mm – máy ${n}`, g);\n"
   "        pm.rotation.y = -Math.PI / 2; pm.position.set(2, 0, -150);\n"
   "        /* Two 90° tabs on the rear face of the ear-stop bars, one M5 × 10 + T-nut each: the plate cannot slide or tip */\n"
   "        for (const y of [21, 279]) B(14, 38, 2, mat.plate, 7, y, -131, `Tai gấp 90° của tấm máy ${n} – bắt vít vào thanh chặn sau`, g);\n"
   "        for (const y of [10, 290]) C(4.5, 3, mat.ihs, 'z', 9, y, -133.5, `Vít M5 × 10 khóa tấm máy ${n} vào thanh chặn (tháo 2 vít để rút máy)`, g, 16);")
# texts
RX(r"đến khi tai chặn chạm thanh sau, cổng I/O ra sau, buộc dây rút qua 2 lỗ ở tai\.",
   "đến khi 2 tai gấp áp vào mặt sau thanh chặn, cổng I/O ra sau, bắt 2 vít M5 × 10 vào con trượt T (mỗi tấm 2 vít).")
RX(r"Muốn rút máy sau này: tháo 8 vít mặt sau trước\.", "Muốn rút máy sau này: tháo tấm sau, mở 2 vít ở tai, kéo tấm ra bằng 2 tai.")
RX(r"<td>14 gói \(140 con, gồm 44 con cho 6 mặt che bụi\)", "<td>15 gói (150 con, gồm 44 con cho 6 mặt che bụi + 8 con khóa tấm đỡ)")
RX(r"<td>≈ 140 M5 \+ 30 M3</td>", "<td>≈ 150 M5 + 30 M3</td>")
RX(r"<td>≈ 140 con</td>", "<td>≈ 150 con</td>")
RX(r"Tấm đỡ bo, nhôm 2 mm, cắt laser theo file DXF \(có tai chặn, lỗ tay kéo, cửa sổ giảm nặng\)",
   "Tấm đỡ bo, nhôm 2 mm, cắt laser + chấn theo file DXF (2 tai gấp 90° bắt vít vào khung, cửa sổ giảm nặng)")
RX(r"`\$\{N\} \(\+1\) × 232 × 296`", "`${N} (+1) × 226 × 296`")
open(p, "w").write(s); print("ok", p)
