"""Texts for the final orientation: front = left side C (plain), rear = right side D (PSU fan + RJ45),
buttons + master switch on the top panel, PSU bolted to the left side B."""
import re, sys
p, mode = sys.argv[1], sys.argv[2]
s = open(p).read()
def RX(pat, b, n=1):
    global s
    s2, c = re.subn(pat, b, s, flags=re.S); assert c == n, (c, pat[:90]); s = s2
L = (lambda f: f'<a href="files/{f}" download>{f}</a>') if mode == "link" else (lambda f: f'<code>{f}</code>')
RX(r"\) và tấm mica mặt trước</td>", ") và tấm mica nắp, đáy, 2 hông</td>")
RX(r"<tr><td>Mica 3 mm bắt ngoài mặt trước, cắt theo file DXF \(lỗ quạt Ø116, nút Ø16,2, công tắc Ø6,2, 8 lỗ M5\)</td><td class=\"n\" id=\"c-acr\">[^<]*</td></tr>\n\s*",
   "")
RX(r"<tr><td>Hộp kín 6 mặt, mica đen trong \(mica khói\) 3 mm:[^<]*</td>",
   "<tr><td>Hộp kín 6 mặt, mica đen trong (mica khói) 3 mm: nắp (3 vùng quạt + 4 nút + công tắc tổng), đáy (3 vùng quạt), mặt trước kín, mặt sau (lưới quạt nguồn + RJ45), hông trái (bắt nguồn), hông phải kín</td>")
RX(r"Công tắc tổng ở mặt trước: MTS‑102", "Công tắc tổng trên nắp: MTS‑102")
RX(r"<tr><td>Mica mặt trước, 6 quạt 92 mm", "<tr><td>Mica hông phải, 6 quạt 92 mm")
RX(r"Tấm che bụi mica 3 mm \(nắp, đáy, 2 hông, mặt sau\)", "Tấm che bụi mica 3 mm (nắp, đáy, mặt trước, mặt sau, hông trái)")
RX(r"<li>Đặt nguồn ATX dựng đứng vào khoang phải.*?</li>",
   "<li>Đặt nguồn ATX dựng đứng vào khoang nguồn (phía mặt sau), quạt nguồn quay ra mặt sau, đuôi nguồn (ổ cắm AC) quay ra hông trái. Nối 2 dây PS_ON (xanh lá) + COM (đen) từ 24‑pin của nguồn (cắt từ cáp nối dài 24‑pin) lên công tắc gạt MTS‑102 trên nắp; công tắc ở đuôi nguồn gạt ON và để nguyên. Treo giá switch dưới thanh dọc nóc (2 vít M5).</li>")
RX(r"<li>Trượt từng tấm bo vào lược từ phía sau đến khi tai sau áp vào mặt sau thanh chặn, cổng I/O ra sau\.",
   "<li>Trượt từng tấm bo vào lược từ phía hông trái đến khi tai áp vào thanh chặn, cổng I/O quay ra hông trái.")
RX(r"Muốn rút máy sau này: tháo tấm sau,", "Muốn rút máy sau này: tháo tấm hông trái,")
RX(r"<li>Bắt mica ra ngoài mặt trước bằng 8 vít M5\. Quạt \+ lưới lọc bắt xuyên mica bằng vít M4 × 40\. Nối nút có đèn vào F_PANEL từng máy\.</li>",
   "<li>Lắp 4 nút có đèn + công tắc tổng vào nắp. Dây mỗi nút (PWR + LED, 4 sợi dupont) đi qua khe 8 mm trước các tấm đỡ tới header F_PANEL của máy tương ứng.</li>")
RX(r"2 tấm hông, nắp trên, rồi mặt sau \(bắt nguồn vào mặt sau bằng 4 vít 6‑32 trước\)",
   "mặt trước, mặt sau, hông phải, nắp, rồi hông trái (bắt nguồn vào hông trái bằng 4 vít 6‑32 trước)")
RX(r"Nguồn bắt 4 vít 6‑32 vào mặt sau như case thường, ổ cắm AC \+ công tắc lộ ra qua ô hở;",
   "Mặt trước kín; 4 nút + công tắc tổng nằm trên nắp phía khoang nguồn. Nguồn bắt 4 vít 6‑32 vào hông trái, ổ cắm AC + công tắc đuôi lộ ra qua ô hở; quạt nguồn hút gió qua lưới ở mặt sau;")
RX(r"Mặt trước, mặt sau, 2 hông là mica kín; chỉ hông phải có 1 lưới cho quạt hút của nguồn\.",
   "Mặt trước, hông phải là mica kín; mặt sau có 1 lưới cho quạt hút của nguồn và đầu nối RJ45.")
RX(r"<tr><td>" + (r'<a href="files/mat-truoc_mica-3mm_x1\.dxf" download>mat-truoc_mica-3mm_x1\.dxf</a> · <a href="files/mat-truoc_mica-3mm\.pdf" target="_blank">PDF</a>' if mode == "link" else r'<code>mat-truoc_mica-3mm_x1\.dxf</code> · <a href="files/mat-truoc_mica-3mm\.pdf" target="_blank">PDF</a>') + r"</td>.*?</tr>",
   f'<tr><td>{L("hong-phai_mica-3mm_x1.dxf")} · <a href="files/hong-phai_mica-3mm.pdf" target="_blank">PDF</a></td><td>Hông phải, mica đen trong 3 mm, kín (chỉ 8 lỗ M5).</td><td class="n">1</td></tr>')
RX(r'<tr><td>(?:<a href="files/nap-tren_mica-3mm_x1\.dxf" download>|<code>)nap-tren_mica-3mm_x1\.dxf.*?</tr>',
   f'<tr><td>{L("nap-tren_mica-3mm_x1.dxf")}, {L("day_mica-3mm_x1.dxf")}, {L("mat-truoc_mica-3mm_x1.dxf")}, {L("mat-sau_mica-3mm_x1.dxf")}, {L("hong-trai_mica-3mm_x1.dxf")} · <a href="files/tam-che-bui_mica-3mm.pdf" target="_blank">PDF</a></td>'
   '<td>Mica đen trong 3 mm. Nắp: 3 vùng đục lỗ quạt + 4 lỗ nút Ø16,2 + công tắc tổng Ø6,2, khắc số 1–4 và POWER. Đáy: 3 vùng đục lỗ quạt + 4 lỗ chân. Mặt trước kín. Mặt sau: vùng đục lỗ quạt nguồn + lỗ RJ45. Hông trái: 6 lỗ vít nguồn + ô hở ổ cắm AC.</td><td class="n">5</td></tr>')
RX(r"\(gửi mat-truoc \+ nap-tren \+ day \+ hong-trai \+ hong-phai \+ mat-sau\)", "(gửi nap-tren + day + mat-truoc + mat-sau + hong-trai + hong-phai)")
RX(r"(Công tắc gạt MTS‑102, gói 5</a></td><td>1 gói )\(1 cái làm công tắc tổng mặt trước\)", r"\1(1 cái làm công tắc tổng trên nắp)")
open(p, "w").write(s); print("ok", p)
