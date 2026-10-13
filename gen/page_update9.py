"""Flat plates again: the rear ear is locked to the ear-stop bars by two 2020 corner brackets (no bending)."""
import re, sys
p = sys.argv[1]
s = open(p).read()
def R(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
def RX(pat, b, n=1):
    global s
    s2, c = re.subn(pat, b, s, flags=re.S); assert c == n, (c, pat[:80]); s = s2
R("[[20, 22.5], [100, 22.5], [100, 28.5], [200, 28.5], [200, 22.5], [232, 22.5], [232, 276.5], [200, 276.5], [200, 271.5], [100, 271.5], [100, 276.5], [20, 276.5]]",
  "[[0, 2], [20, 2], [20, 22.5], [100, 22.5], [100, 28.5], [200, 28.5], [200, 22.5], [232, 22.5], [232, 276.5], [200, 276.5], [200, 271.5], [100, 271.5], [100, 276.5], [20, 276.5], [20, 298], [0, 298]]")
R("      s.holes.push(win);\n",
  "      const slot = new THREE.Path();\n"
  "      slot.moveTo(4, 128); slot.absarc(10, 128, 6, Math.PI, 0); slot.lineTo(16, 172); slot.absarc(10, 172, 6, 0, Math.PI); slot.lineTo(4, 128);\n"
  "      s.holes.push(win, slot);\n"
  "      for (const y of [10, 290]) { const h = new THREE.Path(); h.absarc(10, y, 2.75, 0, Math.PI * 2, true); s.holes.push(h); }\n")
RX(r"        /\* Two 90° tabs on the rear face.*?\n        for \(const y of \[21, 279\]\).*?\n        for \(const y of \[10, 290\]\) C\(4\.5, 3, mat\.ihs, 'z', 9, y, -133\.5,.*?\n",
   "        /* Two 2020 corner brackets lock the flat rear ear to the ear-stop bars (one leg each side of the corner) */\n"
   "        for (const y of [10, 290]) {\n"
   "          const kl = `Ke góc 2020 khóa tấm máy ${n}: vít M5 + con trượt T vào thanh chặn, vít M5 + đai ốc qua tai`;\n"
   "          B(20, 20, 3, mat.alu, 12, y, -131.5, kl, g);                    // leg on the bar's rear face\n"
   "          B(3, 20, 20, mat.alu, 3.5, y, -140, kl, g);                     // leg on the ear\n"
   "          const gs = B(2, 18, 24, mat.alu, 10, y, -137, kl, g); gs.rotation.y = Math.PI / 4;   // gusset\n"
   "          C(4.5, 3, mat.ihs, 'z', 14, y, -134.5, `Vít M5 × 10 vào con trượt T – mở vít này để rút máy ${n}`, g, 16);\n"
   "          C(4.5, 3, mat.ihs, 'x', 6.5, y, -140, `Vít M5 × 10 + đai ốc: ke góc bắt vào tai tấm máy ${n}`, g, 16);\n"
   "        }\n")
RX(r"`Tấm đỡ nhôm 2 mm – máy \$\{n\}`", "`Tấm đỡ nhôm 2 mm phẳng (tai sau + lỗ tay kéo) – máy ${n}`")
# texts
RX(r"đến khi 2 tai gấp áp vào mặt sau thanh chặn, cổng I/O ra sau, bắt 2 vít M5 × 10 vào con trượt T \(mỗi tấm 2 vít\)\.",
   "đến khi tai sau áp vào mặt sau thanh chặn, cổng I/O ra sau. Khóa bằng 2 ke góc 2020 (trên + dưới): mỗi ke 1 vít M5 + con trượt T vào thanh, 1 vít M5 + đai ốc qua lỗ ở tai.")
RX(r"Muốn rút máy sau này: tháo tấm sau, mở 2 vít ở tai, kéo tấm ra bằng 2 tai\.", "Muốn rút máy sau này: tháo tấm sau, mở 2 vít bắt ke vào thanh (ke vẫn gắn trên tai), kéo tấm ra bằng lỗ tay kéo.")
RX(r"<td>15 gói \(150 con, gồm 44 con cho 6 mặt che bụi \+ 8 con khóa tấm đỡ\)", "<td>16 gói (160 con, gồm 44 con cho 6 mặt che bụi + 16 con cho 8 ke khóa tấm đỡ)")
RX(r"Cắt laser \+ chấn nhôm 2 mm \(gửi tam-do-bo_nhom-2mm_x5\.dxf, gấp 2 tai 90°\)", "Cắt laser nhôm 2 mm (gửi tam-do-bo_nhom-2mm_x5.dxf, tấm phẳng, không chấn)")
RX(r"<td>Xưởng cắt laser \+ chấn nhôm 2 mm \(5052/6061\): gấp 2 tai 90° theo nét đỏ\.", "<td>Xưởng cắt laser nhôm 2 mm (5052/6061), tấm phẳng không chấn.")
RX(r"Tấm đỡ bo, nhôm 2 mm, cắt laser \+ chấn theo file DXF \(2 tai gấp 90° bắt vít vào khung, cửa sổ giảm nặng\)",
   "Tấm đỡ bo, nhôm 2 mm phẳng, cắt laser theo file DXF (tai sau khóa bằng 2 ke góc, lỗ tay kéo, cửa sổ giảm nặng)")
RX(r"`\$\{N\} \(\+1\) × 226 × 296`", "`${N} (+1) × 232 × 296`")
RX(r"(Ke góc ngoài 2020</a></td><td>)30 cái", r"\g<1>38 cái (30 cho khung + 8 khóa tấm đỡ)")
RX(r"(Đai ốc M4</a></td><td>)3 gói", r"\g<1>3 gói M4 + 1 gói M5 (8 đai ốc khóa ke vào tai)")
open(p, "w").write(s); print("ok", p)
