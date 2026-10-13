"""Fans inside the box, flush with the bar faces; plate notches; 25 mm feet -> envelope 430 x 322 x 332."""
import re, sys
p = sys.argv[1]
s = open(p).read()
def R(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
def RX(pat, b):
    global s
    s2, c = re.subn(pat, b, s, flags=re.S); assert c == 1, (c, pat[:80]); s = s2
R("PITCH = 72, BAY = 92, FEET = 60;", "PITCH = 72, BAY = 92, FEET = 25;")
R("'Chân in PETG cao 60 mm (vít M5 × 25 vào đầu cột) – chừa khe ≈ 30 mm cho gió thoát ở đáy'",
  "'Chân in PETG cao 25 mm (vít M5 × 30 vào đầu cột) – chừa khe ≈ 20 mm cho gió thoát ở đáy'")
R("[[0, 2], [20, 2], [20, 22.5], [232, 22.5], [232, 276.5], [20, 276.5], [20, 298], [0, 298]]",
  "[[0, 2], [20, 2], [20, 22.5], [100, 22.5], [100, 27], [200, 27], [200, 22.5], [232, 22.5], [232, 276.5], [200, 276.5], [200, 272.5], [100, 272.5], [100, 276.5], [20, 276.5], [20, 298], [0, 298]]")
R("for (const fx of ROW) { makeFan(fx, H + 3 + 12.5, 0, true); makeFan(fx, -3 - 12.5, 0, false); }",
  "for (const fx of ROW) { makeFan(fx, H - 12.5, 0, true); makeFan(fx, 12.5, 0, false); }   // inside the box, outer face flush with the bars")
R("B(94, 1, 94, mat.filter, cx, cy + (top ? 13 : -13), cz, `LƯỚI LỌC 9 cm – ${top ? 'gió vào (nóc)' : 'gió ra (đáy)'}, vít M4 × 40 xuyên lưới + quạt + mica`, model);",
  "B(94, 1, 94, mat.filter, cx, cy + (top ? 16 : -16), cz, `LƯỚI LỌC 9 cm ngoài mica – ${top ? 'gió vào (nóc)' : 'gió ra (đáy)'}, vít M4 × 12 + đai ốc kẹp lưới + mica + bích quạt`, model);")
R("const label = top ? 'Quạt 92 mm PWM trên nóc – HÚT gió vào, thổi xuống qua các bo' : 'Quạt 92 mm PWM dưới đáy – ĐẨY gió nóng ra';",
  "const label = top ? 'Quạt 92 mm PWM trong thùng, sát nóc – HÚT gió vào, thổi xuống qua các bo' : 'Quạt 92 mm PWM trong thùng, sát đáy – ĐẨY gió nóng ra';")
R("dimLine([-W / 2 - 24, -FEET - 3, D / 2 + 9], [-W / 2 - 24, H + 29, D / 2 + 9], [1, 0, 0], `C ${H + FEET + 32} mm`);",
  "dimLine([-W / 2 - 24, -FEET - 3, D / 2 + 9], [-W / 2 - 24, H + 4, D / 2 + 9], [1, 0, 0], `C ${H + FEET + 7} mm`);")
R("envH = H + FEET + 32,", "envH = H + FEET + 7,")
s = s.replace('<b id="st-env">430 × 322 × 316 mm</b>', '<b id="st-env">430 × 322 × 332 mm</b>')
R("<tr><td>Chân in PETG cao 60 mm, vít M5 × 25 xuyên tấm đáy vào đầu cột (taro M5 lỗ tâm đầu cột)</td>",
  "<tr><td>Chân in PETG cao 25 mm, vít M5 × 30 xuyên tấm đáy vào đầu cột (taro M5 lỗ tâm đầu cột)</td>")
RX(r"Chân cao 60 mm để gió ra ở đáy có khe ≈ 30 mm\.", "Quạt nằm trong thùng, mặt ngoài bằng mặt thanh nhôm; lưới lọc dán ngoài mica, tháo vệ sinh không cần mở thùng. Chân cao 25 mm chừa khe ≈ 20 mm cho gió ra ở đáy. Tấm đỡ bo khoét lõm 4–5 mm mép trên và dưới ở vùng quạt.")
RX(r"bắt 4 chân in 60 mm bằng vít M5 × 25", "bắt 4 chân in 25 mm bằng vít M5 × 30")
RX(r"Bắt 3 quạt 92 mm trên nóc \(thổi xuống\) và 3 quạt dưới đáy \(thổi ra ngoài\), mỗi quạt kẹp lưới lọc 9 cm ở mặt ngoài, vít M4 × 40 \+ đai ốc\.",
   "Bắt 3 quạt 92 mm sát dưới tấm nóc (thổi xuống) và 3 quạt sát trên tấm đáy (thổi ra ngoài), nằm trong thùng; lưới lọc 9 cm dán mặt ngoài mica; vít M4 × 12 + đai ốc kẹp lưới + mica + bích ngoài của quạt.")
RX(r"(Vít pake M4 × 40 \(bắt quạt\)</a></td><td>)[^<]*", r"\1chọn phân loại M4 × 12: 24 con cho 6 quạt + 4 con M4 × 10 cho lưới hông phải")
RX(r"thêm 4 vít M5 × 25 cho 4 chân in \(nếu shop có phân loại dài 25\)", "thêm 4 vít M5 × 30 cho 4 chân in (nếu shop có phân loại dài 30)")
RX(r"Chân cao 60 mm, vít M5 × 25 từ dưới lên xuyên tấm đáy vào đầu cột; dán chân cao su dưới đáy\.", "Chân cao 25 mm, vít M5 × 30 từ dưới lên xuyên tấm đáy vào đầu cột; dán chân cao su dưới đáy.")
RX(r"Chân cao su dán – dán dưới 4 chân in PETG cao 60 mm", "Chân cao su dán – dán dưới 4 chân in PETG cao 25 mm")
open(p, "w").write(s); print("ok", p)
