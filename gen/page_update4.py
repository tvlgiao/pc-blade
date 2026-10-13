"""Buy list + files table for the vertical-airflow version (3 + 3 fans 92 mm, 16 combs, new panels)."""
import re, sys, base64, urllib.request
p, mode = sys.argv[1], sys.argv[2]
s = open(p).read()
def RX(pat, b):
    global s
    s2, c = re.subn(pat, b, s, flags=re.S); assert c == 1, (c, pat[:80]); s = s2
def img(id_):
    u = f"https://down-vn.img.susercontent.com/file/{id_}_tn"
    return u if mode == "link" else "data:image/jpeg;base64," + base64.b64encode(urllib.request.urlopen(u, timeout=20).read()).decode()
def row(url, thumb, name, qty, price):
    t = f'<a href="{url}" target="_blank" rel="noopener"><img src="{thumb}" alt="" loading="lazy" width="56" height="56"></a>' if thumb else '<span>Shopee chặn tìm</span>'
    return f'<tr><td class="thumb">{t}</td><td><a href="{url}" target="_blank" rel="noopener">{name}</a></td><td>{qty}</td><td class="n">{price}</td></tr>'
fan_q = "https://shopee.vn/search?keyword=qu%E1%BA%A1t%209cm%204%20pin%20PWM"
feet_q = "https://shopee.vn/search?keyword=ch%C3%A2n%20t%C4%83ng%20ch%E1%BB%89nh%20ren%20M5%2060mm"
RX(r'<tr><td class="thumb"><a href="https://shopee\.vn/product/83109123/23283879160".*?</tr>',
   row(fan_q, None, "Quạt 92 mm PWM 4‑pin – chưa chọn được shop (Shopee chặn tìm kiếm), bấm để tìm", "6 (3 nóc hút vào, 3 đáy đẩy ra)", "≈ 50k"))
RX(r'(Lưới lọc bụi 12 cm kèm ốc</a></td><td>)9 \(4 quạt trước, 1 quạt nguồn, 4 lỗ thoát sau\)(</td><td class="n">12,9k</td></tr>)',
   r'\g<1>1 (quạt hút của nguồn, hông phải)\g<2>' + "\n        " +
   row("https://shopee.vn/product/110272203/27608833519", img("vn-11134207-7r98o-lz9i4frrgkgx53"), "Lưới lọc bụi nylon mịn 9 cm, có lỗ bắt ốc (cùng shop hub quạt)", "6, chọn 9 cm", "44,1k"))
RX(r'<tr><td class="thumb"><a href="https://shopee\.vn/product/36387091/43561265978".*?</tr>',
   row(feet_q, None, "Chân tăng chỉnh ren M5 cao ≈ 60 mm – chưa chọn được shop, bấm để tìm", "4 (vặn vào lỗ tâm đầu cột, taro M5)", "—"))
RX(r'(Vít pake M4 × 40 \(bắt quạt\)</a></td><td>)[^<]*', r'\g<1>3 gói (24 vít cho 6 quạt 92 mm); thêm 4 vít M4 × 10 cho lưới hông phải nếu shop có phân loại này')
RX(r'(Đai ốc M4</a></td><td>)2 gói', r'\g<1>3 gói')
RX(r'(Cáp nối dài quạt 4‑pin PWM</a></td><td>)1, loại 40 cm', r'\g<1>2, loại 40 cm (quạt nóc + đáy về hub)')
RX(r'In 3D PETG \(gửi luoc_PETG_x8\.stl \+ gia-switch_PETG_x1\.stl\)(</a></td><td>)8 lược \+ 1 giá', r'In 3D PETG (gửi luoc_PETG_x16.stl + gia-switch_PETG_x1.stl)\g<1>16 lược + 1 giá')
RX(r'\(gửi mat-truoc \+ nap-tren-duoi \+ hong-trai \+ hong-phai \+ mat-sau\)', '(gửi mat-truoc + nap-tren + day + hong-trai + hong-phai + mat-sau)')
RX(r'Tổng ước tính ≈ 4,5 triệu đồng', 'Tổng ước tính ≈ 4,8 triệu đồng')
# files table
L = (lambda f: f'<a href="files/{f}" download>{f}</a>') if mode == "link" else (lambda f: f'<code>{f}</code>')
RX(r'<tr><td>(?:<a href="files/nap-tren-duoi_mica-3mm_x2\.dxf" download>|<code>)nap-tren-duoi_mica-3mm_x2\.dxf.*?</tr>',
   f'<tr><td>{L("nap-tren_mica-3mm_x1.dxf")}, {L("day_mica-3mm_x1.dxf")}, {L("hong-trai_mica-3mm_x1.dxf")}, {L("hong-phai_mica-3mm_x1.dxf")}, {L("mat-sau_mica-3mm_x1.dxf")} · <a href="files/tam-che-bui_mica-3mm.pdf" target="_blank">PDF</a></td>'
   '<td>Hộp kín 6 mặt, mica trong 3 mm, cùng tiệm cắt mặt trước. Nắp và đáy mỗi tấm 3 lỗ quạt 92 mm (lưới 9 cm); hông phải 1 lỗ quạt nguồn (lưới 12 cm); mặt trước, mặt sau, hông trái kín. Mặt sau có lỗ đuôi nguồn và lỗ RJ45 keystone.</td><td class="n">1 + 1 + 1 + 1 + 1</td></tr>')
RX(r'<tr><td>(?:<a href="files/luoc_PETG_x8\.stl" download>luoc_PETG_x8\.stl</a>|<code>luoc_PETG_x8\.stl</code>)</td><td>In 3D PETG, 3 vách, 40 % infill, mặt phẳng úp xuống\.</td><td class="n">8</td></tr>',
   f'<tr><td>{L("luoc_PETG_x16.stl")}</td><td>In 3D PETG, 3 vách, 40 % infill, mặt phẳng úp xuống. 1 mẫu cho cả 16 mảnh (trước/sau, trên/dưới).</td><td class="n">16</td></tr>')
RX(r'Dài 114 mm, 2 lỗ M5 cách 100 mm \(bản sửa 13/10\)\.', 'Dài 114 mm, treo dưới thanh dọc nóc bằng 2 lỗ M5 trên đường tâm (cách 70 mm).')
open(p, "w").write(s); print("ok", p)
