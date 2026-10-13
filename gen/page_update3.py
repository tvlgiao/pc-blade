"""Vertical airflow: 3 x 92 mm fans on top (intake, blowing down) + 3 on the bottom (exhaust), centre rails removed,
combs on the edge bars, 90-degree z-bars (bottom: PSU support, top: switch holder). Front + rear solid acrylic."""
import re, sys
p = sys.argv[1]
s = open(p).read()
def R(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
def RX(pat, b):
    global s
    s2, c = re.subn(pat, b, s, flags=re.S); assert c == 1, (c, pat[:80]); s = s2

R("PITCH = 72, BAY = 92, FEET = 10;", "PITCH = 72, BAY = 92, FEET = 60;")
R("'Chân cao su 10 mm', model, 20);", "'Chân cao 60 mm, bắt vít M5 vào đầu cột – chừa khe ≈ 30 mm cho gió thoát ở đáy', model, 20);")
R("const rails = FRAME === 'std' ? [-90, 50] : [-20];\n    const combD = rails.length === 1 ? 60 : 16;",
  "const rails = [];            // no centre rails: the top and bottom fan rows need that space\n    const combD = 60;")
R("      for (const z of rails) B(W - 2 * PF, PF, PF, mat.alu, 0, y, z, `Nhôm ${prof} – ray đỡ lược ${W - 2 * PF} mm`, frame);",
  "      /* 90° brace instead of the centre rail: bottom one carries the PSU's left edge, top one hangs the switch holder */\n"
  "      B(PF, PF, D - 2 * PF, mat.alu, y < H / 2 ? psuX - 38 : psuX + 14, y, 0, `Nhôm ${prof} – thanh dọc ${y < H / 2 ? 'đáy (đỡ nguồn)' : 'nóc (treo giá switch)'} ${D - 2 * PF} mm – thay ray giữa, xoay 90°`, frame);")
R("      for (const z of rails) {\n        slotX.forEach((sx, i) => {\n          const lab = `Mảnh lược ${where} khoang ${i + 1}",
  "      for (const z of [D / 2 - 30, -D / 2 + 30]) {\n        slotX.forEach((sx, i) => {\n          const lab = `Mảnh lược ${where} ${z > 0 ? 'trước' : 'sau'} khoang ${i + 1}")
RX(r"    const sledW = bayStart - X0, cols = .*?for \(let c = 0; c < cols; c\+\+\) for \(const cy of \[85, 205\]\) \{ makeFan\(fx0 \+ c \* 120, cy\); fans\.push\(\[fx0 \+ c \* 120, cy\]\); \}\n",
   "    /* One row of 3 × 92 mm fans over and under the 4 bays: top pulls filtered air in, bottom pushes it out */\n"
   "    const sledW = bayStart - X0, ROW = [-1, 0, 1].map(k => X0 + sledW / 2 + k * 96);\n"
   "    const fans = [];   // front and rear are solid now\n"
   "    CAT = 'fan';\n"
   "    for (const fx of ROW) { makeFan(fx, H + 3 + 12.5, 0, true); makeFan(fx, -3 - 12.5, 0, false); }\n")
RX(r"  function makeFan\(cx, cy\) \{\n    const g = new THREE.Group\(\); g.position.set\(cx, cy, 117.5\); model.add\(g\);\n    const label = 'Quạt 120 mm PWM – hút gió mát vào';",
   "  function makeFan(cx, cy, cz, top) {\n"
   "    const g = new THREE.Group(); g.position.set(cx, cy, cz); g.rotation.x = Math.PI / 2; g.scale.set(92 / 120, 92 / 120, 1); model.add(g);\n"
   "    const label = top ? 'Quạt 92 mm PWM trên nóc – HÚT gió vào, thổi xuống qua các bo' : 'Quạt 92 mm PWM dưới đáy – ĐẨY gió nóng ra';\n"
   "    B(94, 1, 94, mat.filter, cx, cy + (top ? 13 : -13), cz, `LƯỚI LỌC 9 cm – ${top ? 'gió vào (nóc)' : 'gió ra (đáy)'}, vít M4 × 40 xuyên lưới + quạt + mica`, model);")
# top/bottom panels with the fan holes
R("    for (const y of [-1.5, H + 1.5]) edge(B(W, 3, DD, mat.cover, 0, y, zc, null, panel));",
  "    for (const y of [0, H + 3]) {\n"
  "      const sh = new THREE.Shape();\n"
  "      sh.moveTo(-W / 2, ZR); sh.lineTo(W / 2, ZR); sh.lineTo(W / 2, D / 2); sh.lineTo(-W / 2, D / 2); sh.lineTo(-W / 2, ZR);\n"
  "      for (const fx of ROW) { const q = new THREE.Path(); q.absarc(fx, 0, 44, 0, Math.PI * 2, true); sh.holes.push(q); }\n"
  "      const pm = tag(new THREE.Mesh(new THREE.ExtrudeGeometry(sh, { depth: 3, bevelEnabled: false, curveSegments: 32 }), mat.cover), null, panel);\n"
  "      pm.rotation.x = Math.PI / 2; pm.position.y = y; edge(pm);\n"
  "    }")
# switch holder hangs from the top z-bar
R("for (const [x, z] of [[HX - 6, -120], [HX + 36.6, -20]]) C(4.5, 3, mat.ihs, 'y', x, H - PF - 5.5, z, 'Vít M5 bắt giá switch vào rãnh nhôm', model, 16);",
  "for (const z of [-98, -28]) C(4.5, 3, mat.ihs, 'y', HX + 15.3, H - PF - 5.5, z, 'Vít M5 bắt giá switch vào thanh dọc nóc', model, 16);")
R("const hl = 'Giá switch in PETG – bắt 2 vít M5 vào thanh sau trên (z −120) và ray giữa trên (z −20)';",
  "const hl = 'Giá switch in PETG – treo dưới thanh dọc nóc bằng 2 vít M5';")
# dimensions + stats
R("dimLine([-W / 2 - 24, -FEET - 3, D / 2 + 9], [-W / 2 - 24, H + 3, D / 2 + 9], [1, 0, 0], `C ${H + FEET + 6} mm`);",
  "dimLine([-W / 2 - 24, -FEET - 3, D / 2 + 9], [-W / 2 - 24, H + 29, D / 2 + 9], [1, 0, 0], `C ${H + FEET + 32} mm`);")
R("envH = H + FEET + 6,", "envH = H + FEET + 32,")
R("$('c-wbar-name').textContent = `thanh ngang (4 viền + ${2 * R} ray đỡ lược)`;\n    $('c-wbar').textContent = `${4 + 2 * R} × ${W - 2 * PF} mm`;",
  "$('c-wbar-name').textContent = 'thanh ngang (trước + chặn sau, trên + dưới)';\n    $('c-wbar').textContent = `4 × ${W - 2 * PF} mm`;")
R("$('c-comb').textContent = `${2 * R * N} mảnh`;\n    $('c-comb-name').textContent = `Mảnh lược in PETG, rãnh 2,6 × 3,5 mm, 72 × ${R === 1 ? 60 : 16} × 6 mm`;",
  "$('c-comb').textContent = `${4 * N} mảnh`;\n    $('c-comb-name').textContent = 'Mảnh lược in PETG (1 mẫu), rãnh 2,6 × 3,5 mm, 72 × 60 × 6 mm, bắt vào thanh trước + chặn sau, trên + dưới';")
R("const cols = Math.max(1, Math.floor((4 + PITCH * N) / 120));\n    $('e-fan').textContent = `${cols * 2} + 1`;", "$('e-fan').textContent = '3 + 3 + 1';")
R("(4 + 2 * R) * (W - 2 * PF) / 1000);", "4 * (W - 2 * PF) / 1000 + 2 * (D - 2 * PF) / 1000);")
R("const keKg = (24 + 4 * R) *", "const keKg = 28 *")
R("const acrKg = (W / 1000 * H / 1000 - cols * 2 * Math.PI * 0.0575 ** 2) * 0.003 * 1190;\n    const frontKg = acrKg + cols * 2 * 0.13 + 0.05;",
  "const acrKg = W / 1000 * H / 1000 * 0.003 * 1190;\n    const frontKg = acrKg + 6 * 0.09 + 0.05;")
R("- 5 * Math.PI * 58 ** 2 - 88 * 152)", "- 6 * Math.PI * 44 ** 2 - Math.PI * 58 ** 2 - 88 * 152)")
# static HTML
R('<span id="c-wbar-name">thanh ngang (4 viền + 4 ray đỡ lược)</span></td><td class="n" id="c-wbar">8 × 384 mm</td></tr>',
  '<span id="c-wbar-name">thanh ngang (trước + chặn sau, trên + dưới)</span></td><td class="n" id="c-wbar">4 × 384 mm</td></tr>\n'
  '        <tr><td>Nhôm <span class="prof">2020</span>, thanh dọc giữa nóc + đáy (thay ray giữa, xoay 90°: đáy đỡ nguồn, nóc treo giá switch)</td><td class="n">2 × 220 mm</td></tr>')
R('<td id="c-comb-name">Mảnh lược in 3D, khe 3,5 mm, dài 72 mm</td><td class="n" id="c-comb">16 mảnh</td>',
  '<td id="c-comb-name">Mảnh lược in PETG (1 mẫu), bắt vào thanh trước + chặn sau</td><td class="n" id="c-comb">16 mảnh</td>')
R('<tr><td>Quạt 120 mm PWM + hub quạt (PWM từ SYS_FAN máy 1)</td><td class="n" id="e-fan">4 + 1</td></tr>',
  '<tr><td>Quạt 92 mm PWM: 3 trên nóc hút vào + 3 dưới đáy đẩy ra, hub quạt (PWM từ SYS_FAN máy 1)</td><td class="n" id="e-fan">3 + 3 + 1</td></tr>')
R('<tr><td>Mica mặt trước, quạt 120 mm (≈ 130 g/cái), hub</td>', '<tr><td>Mica mặt trước, 6 quạt 92 mm (≈ 90 g/cái), hub</td>')
R("<tr><td>Hộp kín 6 mặt, mica 3 mm: nắp + đáy, 2 hông, mặt sau (lỗ có gió đi qua mới gắn lưới lọc)</td>",
  "<tr><td>Hộp kín 6 mặt, mica 3 mm: nắp + đáy (mỗi tấm 3 lỗ quạt 92 mm + lưới), 2 hông, mặt sau kín</td>")
R("<tr><td>Chân cao su 10 mm (dán dưới tấm đáy)</td><td class=\"n\">4</td></tr>", "<tr><td>Chân cao 60 mm bắt vít M5 xuyên tấm đáy vào đầu cột (taro M5 lỗ tâm đầu cột)</td><td class=\"n\">4</td></tr>")
RX(r'<p class="warn">Hộp kín cả 6 mặt\..*?</p>',
   '<p class="warn">Hộp kín cả 6 mặt. Gió đi <b>từ trên xuống</b>: 3 quạt 92 mm trên nóc hút gió qua lưới lọc, thổi xuống theo khe dọc giữa các bo, 3 quạt dưới đáy đẩy gió nóng ra qua lưới lọc. Lấy gió ở nóc vì không khí trên cao ít bụi hơn sát mặt bàn. Mặt trước, mặt sau, 2 hông là mica kín; chỉ hông phải có 1 lưới cho quạt hút của nguồn. Đuôi nguồn (ổ cắm AC, công tắc) lộ ra qua lỗ mặt sau; cáp mạng ra router qua đầu nối RJ45. Chân cao 60 mm để gió ra ở đáy có khe ≈ 30 mm. Vệ sinh lưới nóc 1 lần/tháng.</p>')
R('<button class="chip" id="o-std" aria-pressed="false">2020 · 4 ray</button>', '<button class="chip" id="o-std" aria-pressed="false" hidden>2020 · 4 ray</button>')
R('2020 · 2 ray (đã chốt)</button>', '2020 (đã chốt)</button>')
R('>1515 · 2 ray</button>', '>1515</button>')
s = s.replace("['cover', 'Hộp kín + lưới lọc']", "['cover', 'Hộp kín + lưới lọc']")
s = s.replace("Lược in rời từng khoang, trượt trên ray 2020.", "Lược in rời từng khoang, bắt vào thanh trước và thanh chặn sau.")
RX(r"<li>Ráp khung 2020, bắt ray giữa trên và dưới, bắt mảnh lược vào ray bằng vít M5 × 10 \+ long đền\.</li>",
   "<li>Ráp khung 2020 (không có ray giữa). Bắt 2 thanh dọc giữa: dưới đáy ở mép trái khoang nguồn, trên nóc giữa khoang nguồn. Bắt 16 mảnh lược vào thanh trước và thanh chặn sau, trên và dưới, bằng vít M5 × 10 + long đền.</li>")
s = s.replace("Treo giá switch lên thanh chặn sau và ray giữa phía trên, luồn switch vào từ phía sau.", "Treo giá switch dưới thanh dọc nóc (2 vít M5), luồn switch vào từ phía sau.")
RX(r"<li>Bắt tấm đáy \(dán chân cao su trước\).*?</li>",
   "<li>Bắt tấm đáy (vặn 4 chân cao 60 mm xuyên tấm vào đầu cột), 2 tấm hông, nắp trên, rồi mặt sau (đuôi nguồn lọt qua lỗ chữ nhật, dán ron xốp quanh khe): vít M5 × 10 + long đền. Bắt 3 quạt 92 mm trên nóc (thổi xuống) và 3 quạt dưới đáy (thổi ra ngoài), mỗi quạt kẹp lưới lọc 9 cm ở mặt ngoài, vít M4 × 40 + đai ốc. Lưới 12 cm ở hông phải: vít M4 × 10. Cắm đầu nối RJ45 keystone, nối cáp 30 cm từ cổng 5 của switch.</li>")
open(p, "w").write(s); print("ok", p)
