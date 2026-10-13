"""Buttons + master switch on the TOP panel above the PSU bay (no extra width): LEAD back to 4 mm,
front (left side C) is a plain panel again. Wiring drawn to each F_PANEL and to PS_ON."""
import re, sys
p = sys.argv[1]
s = open(p).read()
def R(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
def RX(pat, b, n=1):
    global s
    s2, c = re.subn(pat, b, s, flags=re.S); assert c == n, (c, pat[:90]); s = s2
R("DR = 50, LEAD = 16,", "DR = 50, LEAD = 4,")
R("// 2 posts + 16 lead (button bodies on the front) + 72N bays + 92 PSU bay", "// 2 posts + 4 lead + 72N bays + 92 PSU bay")
# front C: plain again
RX(r"    /\* FRONT = left side \(C\): 4 lit buttons.*?    CAT = 'cover';\n",
   "    /* FRONT = left side (C): plain smoked panel; the buttons sit on the top panel above the PSU bay */\n"
   "    edge(B(3, H, DD, mat.cover, -W / 2 - 1.5, H / 2, zc, null, panel));\n")
# top panel: button + switch holes above the PSU bay
R("      for (const fx of ROW) perf(sh, fx, 0, 42);\n",
  "      for (const fx of ROW) perf(sh, fx, 0, 42);\n"
  "      if (y > 0) { for (const bz of BTZ) { const q = new THREE.Path(); q.absarc(TX, bz, 8.1, 0, Math.PI * 2, true); sh.holes.push(q); }\n"
  "                   const q = new THREE.Path(); q.absarc(TX, SWZ, 3.1, 0, Math.PI * 2, true); sh.holes.push(q); }\n")
R("    for (const y of [0, H + 3]) {\n      const sh = new THREE.Shape();",
  "    /* Buttons on the top panel, one row front→back above the PSU bay (clear of the switch holder and the top z-bar) */\n"
  "    const TX = psuX - 27, BTZ = Array.from({ length: N }, (_, i) => 70 - i * 25), SWZ = 70 - N * 25;\n"
  "    for (const y of [0, H + 3]) {\n      const sh = new THREE.Shape();")
# objects + wiring, placed right after the top/bottom panel loop
R("    edge(B(3, H, DD, mat.cover, -W / 2 - 1.5, H / 2, zc, null, panel));\n",
  "    edge(B(3, H, DD, mat.cover, -W / 2 - 1.5, H / 2, zc, null, panel));\n"
  "    CAT = 'front';\n"
  "    BTZ.forEach((bz, i) => {\n"
  "      C(9, 4, mat.btn, 'y', TX, H + 5, bz, `Nút 16 mm có đèn 5 V trên nóc – máy ${i + 1}`, panel, 24);\n"
  "      C(6.5, 0.8, mat.led, 'y', TX, H + 7.3, bz, `Đèn nút máy ${i + 1} – sáng khi máy chạy`, panel, 24);\n"
  "      C(7, 28, mat.black, 'y', TX, H - 14, bz, `Thân nút máy ${i + 1} (≈ 28 mm, thả xuống khoang nguồn)`, panel, 16);\n"
  "      const e = engrave(String(i + 1), 9); e.rotation.set(-Math.PI / 2, 0, Math.PI / 2); e.position.set(TX - 20, H + 3.15, bz); panel.add(e);\n"
  "      const hx = slotX[i] + S + 13, wy = 262 - i * 3;\n"
  "      for (const [dx, m] of [[-1.5, mat.wireY], [1.5, mat.wireK]])\n"
  "        tube([[TX + dx, H - 28, bz], [TX + dx - 4, wy, Math.max(bz, 60)], [TX - 14 + dx, wy, 86], [hx + 6, wy, 86], [hx, 262, 78], [hx, 258, 72 + dx]], m, 0.9, `Dây nút + LED máy ${i + 1} → header F_PANEL (PWRBTN, PLED)`, model);\n"
  "    });\n"
  "    C(6, 4, mat.ihs, 'y', TX, H + 5, SWZ, 'CÔNG TẮC TỔNG MTS‑102 trên nóc – nối PS_ON ↔ COM của nguồn ATX: gạt = bật/tắt nguồn cả 4 máy', panel, 16);\n"
  "    const lev = C(1.5, 12, mat.ihs, 'y', TX, H + 11, SWZ + 2, 'Công tắc gạt MTS‑102', panel, 10); lev.rotation.x = 0.35;\n"
  "    const pw = engrave('POWER', 7); pw.rotation.set(-Math.PI / 2, 0, Math.PI / 2); pw.position.set(TX - 20, H + 3.15, SWZ); panel.add(pw);\n"
  "    CAT = 'psu';\n"
  "    for (const [dx, m] of [[-1.2, mat.wireG], [1.2, mat.wireK]])\n"
  "      tube([[TX + dx, H - 10, SWZ], [TX + dx, 240, SWZ + 10], [psuX - 18 + dx, 200, 0], [psuX - 18 + dx, 178, 7]], m, 1, 'Dây PS_ON (xanh lá) + COM (đen): 24‑pin nguồn → công tắc tổng trên nóc', model);\n"
  "    CAT = 'cover';\n", n=1)
s = s.replace('<b id="st-env">442 × 302 × 332 mm</b>', '<b id="st-env">430 × 302 × 332 mm</b>').replace('<b id="st-frame">436 × 290 × 300 mm</b>', '<b id="st-frame">424 × 290 × 300 mm</b>')
s = s.replace('id="c-wbar">4 × 396 mm</td>', 'id="c-wbar">4 × 384 mm</td>').replace("2 × 436 × 290, 2 × 290 × 300, 1 × 436 × 300", "2 × 424 × 290, 2 × 290 × 300, 1 × 424 × 300")
s = s.replace("5 m; nhắn shop cắt 4×300, 4×250, 4×396, 2×200 mm", "5 m; nhắn shop cắt 4×300, 4×250, 4×384, 2×200 mm")
s = s.replace("<code>108 + 72 × số máy</code>", "<code>96 + 72 × số máy</code>").replace("bộ 4 máy (396 mm) và bộ 6 máy (540 mm)", "bộ 4 máy (384 mm) và bộ 6 máy (528 mm)")
open(p, "w").write(s); print("ok", p)
