"""Front face 20 mm closer (DF): frame 424 x 290 x 300, envelope 430 x 302 x 332. Rear geometry unchanged."""
import re, sys
p = sys.argv[1]
s = open(p).read()
def R(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
def RX(pat, b, n=1):
    global s
    s2, c = re.subn(pat, b, s, flags=re.S); assert c == n, (c, pat[:80]); s = s2
R("const H = 300, D = 260, DR = 50,", "const H = 300, D = 260, DF = 20, DR = 50,")
R("FEET = 25;   // DR: rear bay behind the ear-stop bars", "FEET = 25;   // DR: rear bay behind the ear-stop bars; DF: front trimmed 20 mm (empty space)\n  const ZF = D / 2 - DF;            // outer front face of the frame (z 110)")
R("sx * px, H / 2, sz > 0 ? pz : -pz - DR,", "sx * px, H / 2, sz > 0 ? ZF - PF / 2 : -pz - DR,")
R("sx * px, -3 - FEET / 2, sz > 0 ? pz : -pz - DR,", "sx * px, -3 - FEET / 2, sz > 0 ? ZF - PF / 2 : -pz - DR,")
R("B(W - 2 * PF, PF, PF, mat.alu, 0, y, sz * pz,", "B(W - 2 * PF, PF, PF, mat.alu, 0, y, sz > 0 ? ZF - PF / 2 : -pz,")
R("B(PF, PF, D + DR - 2 * PF, mat.alu, sx * px, y, -DR / 2, `Nhôm ${prof} – thanh dọc ${D + DR - 2 * PF} mm (cố định)`, frame);",
  "B(PF, PF, D - DF + DR - 2 * PF, mat.alu, sx * px, y, (ZF - D / 2 - DR) / 2, `Nhôm ${prof} – thanh dọc ${D - DF + DR - 2 * PF} mm (cố định)`, frame);")
R("B(PF, PF, D - 2 * PF, mat.alu, y < H / 2 ? psuX - 38 : psuX + 14, y, 0, `Nhôm ${prof} – thanh dọc ${y < H / 2 ? 'đáy (đỡ nguồn)' : 'nóc (treo giá switch)'} ${D - 2 * PF} mm",
  "B(PF, PF, D - DF - 2 * PF, mat.alu, y < H / 2 ? psuX - 38 : psuX + 14, y, -DF / 2, `Nhôm ${prof} – thanh dọc ${y < H / 2 ? 'đáy (đỡ nguồn)' : 'nóc (treo giá switch)'} ${D - DF - 2 * PF} mm")
R("for (const z of [D / 2 - 30, -D / 2 + 30]) {", "for (const z of [ZF - 30, -D / 2 + 30]) {")
R("[psuX - 8 + dx, 145, 110], [psuX + dx, 140, 128]]", "[psuX - 8 + dx, 145, 90], [psuX + dx, 140, 108]]")
R("B(56, 26, 70, mat.fuse, psuX, 215, 50,", "B(56, 26, 70, mat.fuse, psuX, 215, 40,")
# whole front block (acrylic, buttons, switch, screws, engraving) moves back by DF
R("    CAT = 'front';\n", "    CAT = 'front';\n    const frontG = new THREE.Group(); frontG.position.z = -DF; panel.add(frontG);\n")
a = s.index("    const frontG = new THREE.Group();")
b = s.index("    /* Dust enclosure")
blk = s[a:b]
blk = blk.replace("panel.add(frontG);", "panel.add(frontG);#KEEP#").replace(", panel)", ", frontG)").replace(", panel, ", ", frontG, ").replace("panel.add(e)", "frontG.add(e)").replace("panel.add(pw)", "frontG.add(pw)").replace("#KEEP#", "")
s = s[:a] + blk + s[b:]
# covers + dims use the trimmed front
R("const ZR = -D / 2 - DR, DD = D + DR, zc = (ZR + D / 2) / 2;", "const ZR = -D / 2 - DR, DD = ZF - ZR, zc = (ZR + ZF) / 2;")
R("sh.moveTo(-W / 2, ZR); sh.lineTo(W / 2, ZR); sh.lineTo(W / 2, D / 2); sh.lineTo(-W / 2, D / 2); sh.lineTo(-W / 2, ZR);",
  "sh.moveTo(-W / 2, ZR); sh.lineTo(W / 2, ZR); sh.lineTo(W / 2, ZF); sh.lineTo(-W / 2, ZF); sh.lineTo(-W / 2, ZR);")
R("rs.moveTo(ZR, 0); rs.lineTo(D / 2, 0); rs.lineTo(D / 2, H); rs.lineTo(ZR, H); rs.lineTo(ZR, 0);",
  "rs.moveTo(ZR, 0); rs.lineTo(ZF, 0); rs.lineTo(ZF, H); rs.lineTo(ZR, H); rs.lineTo(ZR, 0);")
R("dimLine([-W / 2 - 3, -34, D / 2 + 10], [W / 2 + 3, -34, D / 2 + 10],", "dimLine([-W / 2 - 3, -34, ZF + 10], [W / 2 + 3, -34, ZF + 10],")
R("dimLine([-W / 2 - 24, -FEET - 3, D / 2 + 9], [-W / 2 - 24, H + 4, D / 2 + 9],", "dimLine([-W / 2 - 24, -FEET - 3, ZF + 9], [-W / 2 - 24, H + 4, ZF + 9],")
R("dimLine([W / 2 + 24, -34, -D / 2 - DR - 3], [W / 2 + 24, -34, D / 2 + 9], [0, 1, 0], `S ${D + DR + 12} mm`);",
  "dimLine([W / 2 + 24, -34, -D / 2 - DR - 3], [W / 2 + 24, -34, ZF + 9], [0, 1, 0], `S ${D - DF + DR + 12} mm`);")
R("dimLine([slotX[0], H + 20, D / 2], [slotX[0] + PITCH, H + 20, D / 2],", "dimLine([slotX[0], H + 20, ZF], [slotX[0] + PITCH, H + 20, ZF],")
R("const envD = D + DR + 12,", "const envD = D - DF + DR + 12,")
R("$('st-frame').textContent = `${W} × ${D + DR} × ${H} mm`;", "$('st-frame').textContent = `${W} × ${D - DF + DR} × ${H} mm`;")
R("$('c-dbar').textContent = `4 × ${D + DR - 2 * PF} mm`;", "$('c-dbar').textContent = `4 × ${D - DF + DR - 2 * PF} mm`;")
R("4 * (D + DR - 2 * PF) / 1000 + 4 * (W - 2 * PF) / 1000 + 2 * (D - 2 * PF) / 1000", "4 * (D - DF + DR - 2 * PF) / 1000 + 4 * (W - 2 * PF) / 1000 + 2 * (D - DF - 2 * PF) / 1000")
R("const DD = D + DR, covKg", "const DD = D - DF + DR, covKg")
# static texts
s = s.replace('<b id="st-env">430 × 322 × 332 mm</b>', '<b id="st-env">430 × 302 × 332 mm</b>').replace('<b id="st-frame">424 × 310 × 300 mm</b>', '<b id="st-frame">424 × 290 × 300 mm</b>')
s = s.replace('<td class="n" id="c-dbar">4 × 270 mm</td>', '<td class="n" id="c-dbar">4 × 250 mm</td>').replace("4 thanh dọc 270 mm", "4 thanh dọc 250 mm")
s = s.replace('xoay 90°: đáy đỡ nguồn, nóc treo giá switch)</td><td class="n">2 × 220 mm</td>', 'xoay 90°: đáy đỡ nguồn, nóc treo giá switch)</td><td class="n">2 × 200 mm</td>')
s = s.replace("2 × 424 × 310, 2 × 310 × 300, 1 × 424 × 300", "2 × 424 × 290, 2 × 290 × 300, 1 × 424 × 300")
RX(r"5 m; nhắn shop cắt 4×300, 4×270, 6×384 mm", "5 m; nhắn shop cắt 4×300, 4×250, 4×384, 2×200 mm")
open(p, "w").write(s); print("ok", p)
