"""Master switch on the front: MTS-102 toggle wired to PS_ON + COM of the PSU 24-pin (replaces the jumper)."""
import re, sys
p = sys.argv[1]
s = open(p).read()
def R(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
R("'Công tắc nguồn tổng – bấm từ ngoài mặt sau'", "'Công tắc ở đuôi nguồn – để luôn ON (bật/tắt bằng công tắc mặt trước)'")
R("B(24, 10, 34, mat.black, psuX - 18, 175, -10, '24‑pin của nguồn + jumper PS_ON (chân 16 ↔ COM)', model);\n    C(3, 12, mat.wireG, 'x', psuX - 18, 182, 2, 'Jumper PS_ON – nguồn luôn bật', model, 12);",
  "B(24, 10, 34, mat.black, psuX - 18, 175, -10, '24‑pin của nguồn: lấy 2 dây PS_ON (chân 16, xanh lá) + COM (đen) ra công tắc mặt trước', model);\n"
  "    for (const [dx, m] of [[-1.2, mat.wireG], [1.2, mat.wireK]]) tube([[psuX - 18 + dx, 175, 8], [psuX - 22 + dx, 160, 60], [psuX - 8 + dx, 145, 110], [psuX + dx, 140, 128]], m, 1, 'Dây PS_ON + COM → công tắc tổng mặt trước', model);")
R("'Công tắc gạt MTS‑102 (lỗ S Ø6,2 trên mica)'", "'CÔNG TẮC TỔNG MTS‑102 – nối PS_ON ↔ COM của nguồn ATX: gạt lên = bật nguồn cho cả 4 máy'")
R("<tr><td>Jumper PS_ON: chân 16 (xanh lá) nối COM (đen) trên 24‑pin</td><td class=\"n\">1</td></tr>",
  "<tr><td>Công tắc tổng ở mặt trước: MTS‑102 nối PS_ON (chân 16, xanh lá) ↔ COM (đen) của 24‑pin nguồn; công tắc ở đuôi nguồn để luôn ON</td><td class=\"n\">1</td></tr>")
R("Cắm jumper PS_ON.", "Nối 2 dây PS_ON (xanh lá) + COM (đen) từ 24‑pin của nguồn (cắt từ cáp nối dài 24‑pin) ra công tắc gạt MTS‑102 ở mặt trước; công tắc ở đuôi nguồn gạt ON và để nguyên.")
s = s.replace("Công tắc gạt MTS‑102, gói 5 cái</a></td><td>1 gói", "Công tắc gạt MTS‑102, gói 5 cái</a></td><td>1 gói (1 cái làm công tắc tổng mặt trước)")
s = s.replace("Cáp nối dài 24‑pin, 30 cm</a></td><td>1", "Cáp nối dài 24‑pin, 30 cm</a></td><td>1 (cắt lấy 2 dây PS_ON + COM ra công tắc tổng)")
open(p, "w").write(s); print("ok", p)
