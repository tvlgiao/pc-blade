"""Pick the 92 mm fan, swap the tall feet for printed PETG risers."""
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
    return (f'<tr><td class="thumb"><a href="{url}" target="_blank" rel="noopener"><img src="{thumb}" alt="" loading="lazy" width="56" height="56"></a></td>'
            f'<td><a href="{url}" target="_blank" rel="noopener">{name}</a></td><td>{qty}</td><td class="n">{price}</td></tr>')
RX(r'<tr><td class="thumb"><span>Shopee chặn tìm</span></td><td><a href="https://shopee\.vn/search\?keyword=qu%E1%BA%A1t%209cm.*?</tr>',
   row("https://shopee.vn/product/159645906/17165836926", img("f1901ea895a9ac6f8e0fd7e3d2c7d142"),
       "Quạt 9 cm tháo máy đồng bộ (Dell/HP), chọn loại 4pin PWM – 162 lượt bán, 4,8★", "6 (3 nóc hút vào, 3 đáy đẩy ra)", "35k"))
RX(r'<tr><td class="thumb"><span>Shopee chặn tìm</span></td><td><a href="https://shopee\.vn/search\?keyword=ch%C3%A2n.*?</tr>',
   row("https://shopee.vn/product/36387091/43561265978", img("vn-11134207-81ztc-mlzayb9gnuvj7b"),
       "Chân cao su dán – dán dưới 4 chân in PETG cao 60 mm", "4", "—"))
RX(r'(Vít đầu dù M5 × 10</a></td><td>)([^<]*)', r'\g<1>\g<2>; thêm 4 vít M5 × 25 cho 4 chân in (nếu shop có phân loại dài 25)')
RX(r'In 3D PETG \(gửi luoc_PETG_x16\.stl \+ gia-switch_PETG_x1\.stl\)(</a></td><td>)16 lược \+ 1 giá',
   r'In 3D PETG (gửi luoc_PETG_x16.stl + gia-switch_PETG_x1.stl + chan-cao_PETG_x4.stl)\g<1>16 lược + 1 giá + 4 chân')
RX(r'(<tr><td>(?:<a href="files/gia-switch_PETG_x1\.stl" download>gia-switch_PETG_x1\.stl</a>|<code>gia-switch_PETG_x1\.stl</code>))',
   (('<tr><td><a href="files/chan-cao_PETG_x4.stl" download>chan-cao_PETG_x4.stl</a>' if mode == "link" else '<tr><td><code>chan-cao_PETG_x4.stl</code>')
    + '</td><td>In 3D PETG, 4 vách, 40 % infill, đứng thẳng. Chân cao 60 mm, vít M5 × 25 từ dưới lên xuyên tấm đáy vào đầu cột; dán chân cao su dưới đáy.</td><td class="n">4</td></tr>\n        \\1'))
RX(r'<tr><td>Chân cao 60 mm bắt vít M5 xuyên tấm đáy vào đầu cột \(taro M5 lỗ tâm đầu cột\)</td>',
   '<tr><td>Chân in PETG cao 60 mm, vít M5 × 25 xuyên tấm đáy vào đầu cột (taro M5 lỗ tâm đầu cột)</td>')
RX(r"'Chân cao 60 mm, bắt vít M5 vào đầu cột – chừa khe ≈ 30 mm cho gió thoát ở đáy'",
   "'Chân in PETG cao 60 mm (vít M5 × 25 vào đầu cột) – chừa khe ≈ 30 mm cho gió thoát ở đáy'")
RX(r'Tổng ước tính ≈ 4,8 triệu đồng', 'Tổng ước tính ≈ 4,5 triệu đồng')
RX(r'(DC‑ATX ra 12 V 8 A \(≈ 96 W\): đặt PL2 ≈ 80 W trong BIOS cho dư\.)',
   r'\1 Quạt 92 mm: muốn êm và mới thì thay bằng Thermalright TL‑C9 PWM (<a href="https://shopee.vn/product/196261835/51365967891" target="_blank" rel="noopener">link</a>, 167k/cái).')
RX(r'(<li>Bắt tấm đáy \()vặn 4 chân cao 60 mm xuyên tấm vào đầu cột(\))', r'\1bắt 4 chân in 60 mm bằng vít M5 × 25 xuyên tấm vào đầu cột\2')
open(p, "w").write(s); print("ok", p)
