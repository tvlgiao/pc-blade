"""Front = left side (C), rear = right side (D). Buttons + master switch move to C (12 mm extra lead
space so their bodies clear PC1's plate), with wiring drawn to each F_PANEL and to PS_ON.
Old front (A, z+) becomes the plain right side; old rear (B, z-) the left side with the PSU tail.
RJ45 keystone moves to the rear D."""
import re, sys
p = sys.argv[1]
s = open(p).read()
def R(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
def RX(pat, b, n=1):
    global s
    s2, c = re.subn(pat, b, s, flags=re.S); assert c == n, (c, pat[:90]); s = s2
R("W = 96 + 2 * PF + PITCH * N;                 // 2 posts + 4 lead + 72N bays + 92 PSU bay",
  "W = LEAD + BAY + 2 * PF + PITCH * N;         // 2 posts + 16 lead (button bodies on the front) + 72N bays + 92 PSU bay")
R("const H = 300, D = 260, DF = 20, DR = 50,", "const H = 300, D = 260, DF = 20, DR = 50, LEAD = 16,")
R("const slotX = Array.from({ length: N }, (_, i) => X0 + 4 + i * PITCH);", "const slotX = Array.from({ length: N }, (_, i) => X0 + LEAD + i * PITCH);")
R("const bayStart = X0 + 4 + PITCH * N;", "const bayStart = X0 + LEAD + PITCH * N;")
# old front (A, z+): plain side panel now -> drop buttons, switch, engraving
a = s.index("    CAT = 'front';\n    const frontG")
b = s.index("    /* Dust enclosure")
blk = s[a:b]
blk = blk.replace("    for (let i = 0; i < N; i++) hole(psuX, 255 - i * 28, 8.1);\n    hole(psuX, 140, 3.1);\n", "")
i0 = blk.index("    for (let i = 0; i < N; i++) {\n      const y = 255 - i * 28;")
blk = blk[:i0]
blk = blk.replace("    CAT = 'front';\n", "    CAT = 'cover';   // old front (z+) is now the plain right side panel\n")
s = s[:a] + blk + "\n" + s[b:]
# left side C = new FRONT: buttons, master switch, engraving, wiring
R("    edge(B(3, H, DD, mat.cover, -W / 2 - 1.5, H / 2, zc, null, panel));\n",
  "    /* FRONT = left side (C): 4 lit buttons + master switch, wired to each F_PANEL and to PS_ON */\n"
  "    CAT = 'front';\n"
  "    const BZ = 60, BY = i => 255 - i * 28;                 // button column on the front face (z, y)\n"
  "    const ls = new THREE.Shape();\n"
  "    ls.moveTo(ZR, 0); ls.lineTo(ZF, 0); ls.lineTo(ZF, H); ls.lineTo(ZR, H); ls.lineTo(ZR, 0);\n"
  "    const lh = (z, y, r) => { const q = new THREE.Path(); q.absarc(z, y, r, 0, Math.PI * 2, true); ls.holes.push(q); };\n"
  "    for (let i = 0; i < N; i++) lh(BZ, BY(i), 8.1);\n"
  "    lh(BZ, 140, 3.1);\n"
  "    const lside = tag(new THREE.Mesh(new THREE.ExtrudeGeometry(ls, { depth: 3, bevelEnabled: false, curveSegments: 24 }), mat.cover), null, panel);\n"
  "    lside.rotation.y = -Math.PI / 2; lside.position.x = -W / 2; edge(lside);\n"
  "    const LX = -W / 2 - 3;                                // outer face of the front panel\n"
  "    for (let i = 0; i < N; i++) {\n"
  "      C(9, 4, mat.btn, 'x', LX - 2, BY(i), BZ, `Nút 16 mm có đèn 5 V – máy ${i + 1}`, panel, 24);\n"
  "      C(6.5, 0.8, mat.led, 'x', LX - 4.3, BY(i), BZ, `Đèn nút máy ${i + 1} – sáng khi máy chạy`, panel, 24);\n"
  "      C(7, 28, mat.black, 'x', -W / 2 + 14, BY(i), BZ, `Thân nút máy ${i + 1} (≈ 28 mm, cách tấm đỡ PC1 ≈ 6 mm)`, panel, 16);\n"
  "      const e = engrave(String(i + 1), 9); e.rotation.y = -Math.PI / 2; e.position.set(LX - 0.15, BY(i), BZ - 22); panel.add(e);\n"
  "      /* 4 wires (PWR+, PWR−, LED+, LED−) through the 8 mm strip in front of the plates to F_PANEL of machine i */\n"
  "      const hx = slotX[i] + S + 13, wy = 262 - i * 3;\n"
  "      for (const [dz, m] of [[-1.5, mat.wireY], [1.5, mat.wireK]])\n"
  "        tube([[-W / 2 + 28, BY(i), BZ + dz], [-W / 2 + 34, wy, 86 + dz * 0.5], [hx - 6, wy, 86 + dz * 0.5], [hx, 262, 78], [hx, 258, 72 + dz]], m, 0.9, `Dây nút + LED máy ${i + 1} → header F_PANEL (PWRBTN, PLED)`, model);\n"
  "    }\n"
  "    C(6, 4, mat.ihs, 'x', LX - 2, 140, BZ, 'CÔNG TẮC TỔNG MTS‑102 – nối PS_ON ↔ COM của nguồn ATX: gạt lên = bật nguồn cho cả 4 máy', panel, 16);\n"
  "    const lev = C(1.5, 12, mat.ihs, 'x', LX - 8, 142, BZ, 'Công tắc gạt MTS‑102', panel, 10); lev.rotation.z = Math.PI / 2 + 0.35;\n"
  "    const pw = engrave('POWER', 7); pw.rotation.y = -Math.PI / 2; pw.position.set(LX - 0.15, 275, BZ); panel.add(pw);\n"
  "    CAT = 'psu';\n"
  "    for (const [dy, m] of [[-1.2, mat.wireG], [1.2, mat.wireK]])\n"
  "      tube([[-W / 2 + 20, 140 + dy, BZ], [-W / 2 + 34, 148 + dy, 86], [psuX - 40, 150 + dy, 86], [psuX - 22, 168 + dy, 20], [psuX - 18, 172 + dy, 7]], m, 1, 'Dây PS_ON (xanh lá) + COM (đen): 24‑pin nguồn → công tắc tổng mặt trước', model);\n"
  "    CAT = 'cover';\n")
# old PS_ON wiring to the old front
RX(r"    for \(const \[dx, m\] of \[\[-1\.2, mat\.wireG\], \[1\.2, mat\.wireK\]\]\) tube\(\[\[psuX - 18 \+ dx, 175, 8\].*?model\);\n", "")
# rear D: RJ45 keystone instead of on the old rear (B)
R("perf(rs, fanZ, 95, 56);", "perf(rs, fanZ, 95, 56);\n    { const q = new THREE.Path(); q.moveTo(-147.4, 231.8); q.lineTo(-147.4, 248.2); q.lineTo(-132.6, 248.2); q.lineTo(-132.6, 231.8); q.lineTo(-147.4, 231.8); rs.holes.push(q); }")
R("    box(psuX + 14 - 7.4, 240 - 8.2, psuX + 14 + 7.4, 240 + 8.2);\n", "")
R("B(14.5, 16, 26, mat.black, psuX + 14, 240, ZR + 10, 'Đầu nối RJ45 keystone Vention – cáp mạng ra router', panel);",
  "B(26, 16, 14.5, mat.black, W / 2 - 10, 240, -140, 'Đầu nối RJ45 keystone Vention ở mặt sau – cáp mạng ra router', panel);")
R("tube([[swX, swPortY(4), -116], [swX, swPortY(4) + 6, -150], [psuX + 14, 240, ZR + 26]], mat.usb, 2.6, 'Cáp LAN 30 cm: switch cổng 5 → đầu nối RJ45 mặt sau', model);",
  "tube([[swX, swPortY(4), -116], [swX + 8, swPortY(4) + 8, -134], [W / 2 - 30, 240, -140], [W / 2 - 23, 240, -140]], mat.usb, 2.6, 'Cáp LAN 30 cm: switch cổng 5 → đầu nối RJ45 mặt sau', model);")
# labels for the old rear (B) which now is the left-hand side when facing the front
s = s.replace("'Vít 6‑32 bắt nguồn vào mặt sau (4 lỗ chuẩn ATX)'", "'Vít 6‑32 bắt nguồn vào hông trái (4 lỗ chuẩn ATX)'")
s = s.replace("'Vít M5 × 10: bắt mặt sau vào cột sau (tháo 8 vít khi rút máy)'", "'Vít M5 × 10: bắt hông trái vào cột (tháo 8 vít khi rút máy)'")
s = s.replace("'Ổ cắm AC 220 V của nguồn – cắm dây từ ngoài mặt sau'", "'Ổ cắm AC 220 V của nguồn – cắm dây ở hông trái'")
s = s.replace("'Công tắc ở đuôi nguồn – để luôn ON (bật/tắt bằng công tắc mặt trước)'", "'Công tắc ở đuôi nguồn (hông trái) – để luôn ON, bật/tắt bằng công tắc mặt trước'")
s = s.replace("'LƯỚI LỌC 12 cm đen, đặt phía trong mica – gió vào quạt nguồn (hông phải)'", "'LƯỚI LỌC 12 cm đen, đặt phía trong mica – gió vào quạt nguồn (mặt sau)'")
s = s.replace("cổng hướng ra sau'", "cổng hướng ra hông trái'")
# camera presets: front looks at C (−x), rear at D (+x)
R("iso: [[720 * k, 470, 760 * k], [0, 140, 0]], front: [[0, 160, 1150 * k], [0, 150, 0]],",
  "iso: [[-760 * k, 470, 700 * k], [0, 140, -20]], front: [[-1150 * k, 160, -20], [0, 150, -20]],")
R("rear: [[-180 * k, 260, -1080 * k], [0, 150, 0]],", "rear: [[1100 * k, 260, -180 * k], [0, 150, -20]],")
# static texts
s = s.replace("<code>96 + 72 × số máy</code>", "<code>108 + 72 × số máy</code>").replace("bộ 4 máy (384 mm) và bộ 6 máy (528 mm)", "bộ 4 máy (396 mm) và bộ 6 máy (540 mm)")
s = s.replace('<b id="st-env">430 × 302 × 332 mm</b>', '<b id="st-env">442 × 302 × 332 mm</b>').replace('<b id="st-frame">424 × 290 × 300 mm</b>', '<b id="st-frame">436 × 290 × 300 mm</b>')
s = s.replace('id="c-wbar">4 × 384 mm</td>', 'id="c-wbar">4 × 396 mm</td>')
s = s.replace("2 × 424 × 290, 2 × 290 × 300, 1 × 424 × 300", "2 × 436 × 290, 2 × 290 × 300, 1 × 436 × 300")
s = s.replace("5 m; nhắn shop cắt 4×300, 4×250, 4×384, 2×200 mm", "5 m; nhắn shop cắt 4×300, 4×250, 4×396, 2×200 mm")
open(p, "w").write(s); print("ok", p)
