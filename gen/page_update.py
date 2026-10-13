"""One-off page update: fill missing thumbnails, add dust covers (model, buy list, files table)."""
import re, sys, base64, urllib.request
src = open(sys.argv[1]).read()
IMG = dict(re.findall(r'"(\d+)": "([^"]+)"', open(sys.argv[2]).read()))
embed = sys.argv[3] == "embed"
plate_png = sys.argv[4]
s = src
def img_src(url):
    if not embed: return url
    return "data:image/jpeg;base64," + base64.b64encode(urllib.request.urlopen(url, timeout=20).read()).decode()
def fill(m):
    item = m.group(2)
    return f'<a href="{m.group(1)}" target="_blank" rel="noopener"><img src="{img_src(f"https://down-vn.img.susercontent.com/file/{IMG[item]}_tn")}" alt="" loading="lazy" width="56" height="56"></a>'
s = re.sub(r'<a href="(https://shopee\.vn/product/\d+/(\d+))" target="_blank" rel="noopener"><span>Xem ảnh trên Shopee</span></a>', fill, s)
p_src = ("data:image/png;base64," + base64.b64encode(open(plate_png, "rb").read()).decode()) if embed else "files/tam-do-bo_xem-truoc.png"
s = s.replace('<td class="thumb"><span>—</span></td>', f'<td class="thumb"><img src="{p_src}" alt="" width="56" height="56"></td>')

def R(a, b):
    global s
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
# buy list quantities for covers
R('<td>9 gói (90 con)</td>', '<td>13 gói (130 con, gồm 36 con cho tấm che bụi)</td>')
R('<td>≈ 90 M5 + 30 M3</td>', '<td>≈ 130 M5 + 30 M3</td>')
R('<td>≈ 90 con</td>', '<td>≈ 130 con</td>')
R('<td>2 gói</td><td class="n">—</td></tr>\n        <tr><td class="thumb"><a href="https://shopee.vn/product/59961430/22909947653"',
  '<td>2 gói; thêm 4 vít M4 × 10 cho lưới lọc hông phải nếu shop có phân loại này</td><td class="n">—</td></tr>\n        <tr><td class="thumb"><a href="https://shopee.vn/product/59961430/22909947653"')
R('Lưới lọc bụi 12 cm kèm ốc</a></td><td>4</td>', 'Lưới lọc bụi 12 cm kèm ốc</a></td><td>5 (4 quạt trước + 1 quạt nguồn)</td>')
R('Cắt laser mica theo file (gửi mat-truoc_mica-3mm_x1.dxf)</a></td><td>1 tấm mica trong 3 mm</td>',
  'Cắt laser mica theo file (gửi mat-truoc + nap-tren-duoi + hong-trai + hong-phai)</a></td><td>5 tấm mica trong 3 mm</td>')
R('Tổng ước tính ≈ 4,2 triệu đồng', 'Tổng ước tính ≈ 4,3 triệu đồng')
# files table
R('<tr><td><a href="files/luoc_PETG_x8.stl"' if not embed else '<tr><td><code>luoc_PETG_x8.stl</code>',
  ('<tr><td><a href="files/nap-tren-duoi_mica-3mm_x2.dxf" download>nap-tren-duoi_mica-3mm_x2.dxf</a>, <a href="files/hong-trai_mica-3mm_x1.dxf" download>hong-trai_mica-3mm_x1.dxf</a>, <a href="files/hong-phai_mica-3mm_x1.dxf" download>hong-phai_mica-3mm_x1.dxf</a> · <a href="files/tam-che-bui_mica-3mm.pdf" target="_blank">PDF</a></td>'
   if not embed else '<tr><td><code>nap-tren-duoi_mica-3mm_x2.dxf</code>, <code>hong-trai_mica-3mm_x1.dxf</code>, <code>hong-phai_mica-3mm_x1.dxf</code> · <a href="files/tam-che-bui_mica-3mm.pdf" target="_blank">PDF</a></td>')
  + '<td>Tấm che bụi, mica trong 3 mm, cùng tiệm cắt mặt trước. Hông phải có lỗ quạt nguồn: đo tâm quạt nguồn thật trước khi cắt.</td><td class="n">2 + 1 + 1</td></tr>\n        '
  + ('<tr><td><a href="files/luoc_PETG_x8.stl"' if not embed else '<tr><td><code>luoc_PETG_x8.stl</code>'))
# cut table + weights + notes
R('<tr><td>Chân cao su 10 mm</td><td class="n">4</td></tr>',
  '<tr><td>Tấm che bụi mica 3 mm: nắp + đáy, 2 hông (hông phải có lỗ quạt nguồn + lưới lọc)</td><td class="n" id="c-cov">2 × 424 × 260, 2 × 260 × 300</td></tr>\n        <tr><td>Chân cao su 10 mm (dán dưới tấm đáy)</td><td class="n">4</td></tr>')
R('<tr><td>Hộp cầu chì, dây 12 V, chân cao su, switch + giá in</td><td class="n">0,65</td></tr>',
  '<tr><td>Hộp cầu chì, dây 12 V, chân cao su, switch + giá in</td><td class="n">0,65</td></tr>\n        <tr><td>Tấm che bụi mica 3 mm (nắp, đáy, 2 hông)</td><td class="n" id="w-cov">1,34</td></tr>')
R('Phủ bì đã gồm tai chặn sau 20 mm, mica + đầu nút trước 9 mm và chân 10 mm.',
  'Phủ bì đã gồm tai chặn sau 20 mm, mica + đầu nút trước 9 mm, tấm che bụi 3 mm và chân 10 mm. Chống bụi: gió chỉ vào qua lưới lọc (4 quạt trước + quạt nguồn), nắp/đáy/2 hông kín, chỉ mặt sau hở để gió thoát → áp suất dương nhẹ, bụi không lọt qua khe. Vệ sinh lưới lọc 1 lần/tháng.')
R('<li>BIOS từng máy:', '<li>Bắt tấm đáy (dán chân cao su trước), 2 tấm hông, nắp trên: vít M5 × 10 + long đền. Lưới lọc 12 cm ở lỗ quạt nguồn, vít M4 × 10 + đai ốc.</li>\n        <li>BIOS từng máy:')
# model: covers
R("['net', 'Switch + LAN'], ['front', 'Mica + nút'],", "['net', 'Switch + LAN'], ['front', 'Mica + nút'], ['cover', 'Tấm che bụi'],")
R("C(12, FEET, mat.foot, 'y', sx * px, -FEET / 2, sz * pz,", "C(12, FEET, mat.foot, 'y', sx * px, -3 - FEET / 2, sz * pz,")
R("B(86, 150, 140, mat.psu, psuX, 95, -55,", "B(86, 150, 140, mat.psu, psuX, 95, -50,")
R("C(55, 1.5, mat.grille, 'x', psuX + 43.8, 95, -55,", "C(55, 1.5, mat.grille, 'x', psuX + 43.8, 95, -50,")
R("    /* Dimensions (envelope", """    /* Dust covers: 3 mm acrylic top, bottom, both sides; rear stays open as the exhaust */
    CAT = 'cover';
    for (const y of [-1.5, H + 1.5]) B(W, 3, D, mat.acrylic, 0, y, 0, null, panel).userData.skip = true;
    B(3, H, D, mat.acrylic, -W / 2 - 1.5, H / 2, 0, null, panel).userData.skip = true;
    const rs = new THREE.Shape();
    rs.moveTo(-D / 2, 0); rs.lineTo(D / 2, 0); rs.lineTo(D / 2, H); rs.lineTo(-D / 2, H); rs.lineTo(-D / 2, 0);
    const fh = new THREE.Path(); fh.absarc(-50, 95, 58, 0, Math.PI * 2, true); rs.holes.push(fh);
    const rside = tag(new THREE.Mesh(new THREE.ExtrudeGeometry(rs, { depth: 3, bevelEnabled: false, curveSegments: 32 }), mat.acrylic), null, panel);
    rside.rotation.y = -Math.PI / 2; rside.position.x = W / 2 + 3; rside.userData.skip = true;
    B(1, 122, 122, mat.filter, W / 2 + 3.6, 95, -50, 'Lưới lọc 12 cm cho quạt nguồn – tấm hông phải', panel);

    /* Dimensions (envelope""")
R("dimLine([-W / 2, -34, D / 2 + 10], [W / 2, -34, D / 2 + 10], [0, 1, 0], `R ${W} mm`);",
  "dimLine([-W / 2 - 3, -34, D / 2 + 10], [W / 2 + 3, -34, D / 2 + 10], [0, 1, 0], `R ${W + 6} mm`);")
R("dimLine([-W / 2 - 24, -FEET, D / 2 + 9], [-W / 2 - 24, H, D / 2 + 9], [1, 0, 0], `C ${H + FEET} mm`);",
  "dimLine([-W / 2 - 24, -FEET - 3, D / 2 + 9], [-W / 2 - 24, H + 3, D / 2 + 9], [1, 0, 0], `C ${H + FEET + 6} mm`);")
R("const envD = D + 29, envH = H + FEET,", "const envD = D + 29, envH = H + FEET + 6,")
R("$('st-env').textContent = `${W} × ${envD} × ${envH} mm`;", "$('st-env').textContent = `${W + 6} × ${envD} × ${envH} mm`;")
R("Math.round(W * envD * envH / 1e6)", "Math.round((W + 6) * envD * envH / 1e6)")
R("const total = N * sledKg + aluKg + keKg + frontKg + psuKg + 0.65;",
  "const covKg = (2 * W * D + 2 * D * H - Math.PI * 58 ** 2) / 1e6 * 0.003 * 1190;\n    $('w-cov').textContent = f2(covKg); $('c-cov').textContent = `2 × ${W} × ${D}, 2 × ${D} × ${H}`;\n    const total = N * sledKg + aluKg + keKg + frontKg + psuKg + 0.65 + covKg;")
R('<span>Phủ bì <b id="st-env">424 × 289 × 310 mm</b></span>', '<span>Phủ bì <b id="st-env">430 × 289 × 316 mm</b></span>')
open(sys.argv[1], "w").write(s)
print("ok", sys.argv[1], s.count("Xem ảnh trên Shopee"), len(s) // 1024, "KB")
