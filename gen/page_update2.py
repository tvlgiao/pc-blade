"""Six-face dust enclosure: 50 mm rear bay, rear panel, clearly drawn mesh filters; buy list + texts."""
import re, sys, base64, urllib.request
p, mode = sys.argv[1], sys.argv[2]          # mode: link | embed
s = open(p).read()
def R(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:70]); s = s.replace(a, b)
def RX(pat, b):
    global s
    s2, c = re.subn(pat, b, s, flags=re.S); assert c == 1, (c, pat[:70]); s = s2

# --- constants, mesh material ---
R("const H = 300, D = 260, PITCH = 72, BAY = 92, FEET = 10;", "const H = 300, D = 260, DR = 50, PITCH = 72, BAY = 92, FEET = 10;   // DR: rear bay behind the ear-stop bars")
R("filter: M(0x30343a, { t: 0.55, r: 0.8, side: THREE.DoubleSide }),", "filter: meshMat(),")
R("  /* Every mesh is tagged", """  /* Dust filter: dark frame + visible wire grid (alpha-tested so you see through the holes) */
  function meshMat() {
    const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d');
    g.strokeStyle = '#22262c'; g.lineWidth = 2.2;
    for (let i = 4; i < 256; i += 9) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i, 256); g.moveTo(0, i); g.lineTo(256, i); g.stroke(); }
    g.lineWidth = 16; g.strokeRect(8, 8, 240, 240);
    const t = new THREE.CanvasTexture(c); t.encoding = THREE.sRGBEncoding; t.anisotropy = 8;
    const m = new THREE.MeshStandardMaterial({ map: t, transparent: true, alphaTest: 0.3, side: THREE.DoubleSide, roughness: 0.7 });
    m.userData.keep = true;
    return m;
  }

  /* Every mesh is tagged""")
R("if (o.isMesh && o.material.map) {", "if (o.isMesh && o.material.map && !o.material.userData.keep) {")

# --- frame: rear posts 50 mm further back, side bars 270 ---
R("B(PF, H, PF, mat.alu, sx * px, H / 2, sz * pz, `Nhôm ${prof} – cột góc 300 mm`, frame);",
  "B(PF, H, PF, mat.alu, sx * px, H / 2, sz > 0 ? pz : -pz - DR, `Nhôm ${prof} – cột góc 300 mm${sz < 0 ? ' (cột sau, lùi 50 mm tạo khoang sau kín)' : ''}`, frame);")
R("C(12, FEET, mat.foot, 'y', sx * px, -3 - FEET / 2, sz * pz,", "C(12, FEET, mat.foot, 'y', sx * px, -3 - FEET / 2, sz > 0 ? pz : -pz - DR,")
R("for (const sz of [-1, 1]) B(W - 2 * PF, PF, PF, mat.alu, 0, y, sz * pz, `Nhôm ${prof} – thanh ngang ${W - 2 * PF} mm (đổi theo số máy)`, frame);",
  "for (const sz of [-1, 1]) B(W - 2 * PF, PF, PF, mat.alu, 0, y, sz * pz, `Nhôm ${prof} – ${sz < 0 ? 'thanh chặn tai tấm đỡ' : 'thanh ngang trước'} ${W - 2 * PF} mm (đổi theo số máy)`, frame);")
R("B(PF, PF, D - 2 * PF, mat.alu, sx * px, y, 0, `Nhôm ${prof} – thanh dọc ${D - 2 * PF} mm (cố định)`, frame);",
  "B(PF, PF, D + DR - 2 * PF, mat.alu, sx * px, y, -DR / 2, `Nhôm ${prof} – thanh dọc ${D + DR - 2 * PF} mm (cố định)`, frame);")

# --- PSU pushed into the rear-panel cut-out (160 mm long assumed) ---
R("B(86, 150, 140, mat.psu, psuX, 95, -50, 'Nguồn ATX đang có – dựng đứng, hút gió từ hông', model);",
  "B(86, 150, 160, mat.psu, psuX, 95, -100, 'Nguồn ATX đang có – đuôi lọt qua lỗ mặt sau, hút gió qua lưới hông phải', model);")
R("C(55, 1.5, mat.grille, 'x', psuX + 43.8, 95, -50,", "C(55, 1.5, mat.grille, 'x', psuX + 43.8, 95, -100,")
R("B(28, 20, 2, mat.black, psuX - 10, 140, -126, 'Ổ cắm AC 220 V của nguồn', model);",
  "B(28, 20, 2, mat.black, psuX - 10, 140, -181, 'Ổ cắm AC 220 V của nguồn – cắm dây từ ngoài mặt sau', model);")
R("B(10, 14, 2, mat.ramTop, psuX + 22, 140, -126, 'Công tắc nguồn tổng', model);",
  "B(10, 14, 2, mat.ramTop, psuX + 22, 140, -181, 'Công tắc nguồn tổng – bấm từ ngoài mặt sau', model);")
R("tube([[psuX + 20 + dx, 160, 16], [psuX + 20 + dx, 185, 26], [psuX + 20 + dx, 203, 40]]",
  "tube([[psuX + 20 + dx, 160, -16], [psuX + 20 + dx, 185, 10], [psuX + 20 + dx, 203, 40]]")
R("tube([[psuX - 30 + dx, 168, 10], [psuX - 34 + dx, 172, -60],", "tube([[psuX - 30 + dx, 166, -16], [psuX - 34 + dx, 173, -60],")

# --- LAN: route above the PSU, down the bay edge, then behind the ears ---
R("const lan = [[swX, swPortY(i), -116], [swX, swPortY(i), lz + 6], [swX, swPortY(i) - 8, lz], [swX, ly + 10, lz], [swX - 10, ly, lz], [lx + 10, ly, lz], [lx, ly + 8, lz + 4], [lx, Yv(28), -128]];",
  "const lan = [[swX, swPortY(i), -116], [swX, swPortY(i) - 4, lz + 4], [swX - 10, 180 + i * 4, lz], [bayStart - 2, 180 + i * 4, lz], [bayStart - 6, ly + 10, lz], [lx + 10, ly, lz], [lx, ly + 8, lz + 4], [lx, Yv(28), -128]];")

# --- covers: six faces ---
RX(r"    /\* Dust covers: 3 mm acrylic top, bottom, both sides; rear stays open as the exhaust \*/.*?(?=    /\* Dimensions)", r"""    /* Dust enclosure, all 6 faces: solid 3 mm acrylic; mesh filters only where air moves
       (front: 4 fans in · right side: PSU fan in · rear: 4 exhaust holes out) */
    CAT = 'cover';
    const edge = m => { m.userData.skip = true; m.add(new THREE.LineSegments(new THREE.EdgesGeometry(m.geometry, 30), mat.coverEdge)); return m; };
    const ZR = -D / 2 - DR, DD = D + DR, zc = (ZR + D / 2) / 2;
    const filterAt = (rot, x, y, z, label) => { const f = B(122, 122, 1, mat.filter, x, y, z, label, panel); f.rotation.y = rot; return f; };
    for (const y of [-1.5, H + 1.5]) edge(B(W, 3, DD, mat.cover, 0, y, zc, null, panel));
    edge(B(3, H, DD, mat.cover, -W / 2 - 1.5, H / 2, zc, null, panel));
    const fanZ = ZR + 80;
    const rs = new THREE.Shape();
    rs.moveTo(ZR, 0); rs.lineTo(D / 2, 0); rs.lineTo(D / 2, H); rs.lineTo(ZR, H); rs.lineTo(ZR, 0);
    const fh = new THREE.Path(); fh.absarc(fanZ, 95, 58, 0, Math.PI * 2, true); rs.holes.push(fh);
    const rside = tag(new THREE.Mesh(new THREE.ExtrudeGeometry(rs, { depth: 3, bevelEnabled: false, curveSegments: 32 }), mat.cover), null, panel);
    rside.rotation.y = -Math.PI / 2; rside.position.x = W / 2 + 3; edge(rside);
    filterAt(Math.PI / 2, W / 2 + 3.6, 95, fanZ, 'LƯỚI LỌC 12 cm – gió vào quạt nguồn (hông phải)');
    const rp = new THREE.Shape();
    rp.moveTo(-W / 2, 0); rp.lineTo(W / 2, 0); rp.lineTo(W / 2, H); rp.lineTo(-W / 2, H); rp.lineTo(-W / 2, 0);
    const box = (x0, y0, x1, y1) => { const q = new THREE.Path(); q.moveTo(x0, y0); q.lineTo(x0, y1); q.lineTo(x1, y1); q.lineTo(x1, y0); q.lineTo(x0, y0); rp.holes.push(q); };
    box(psuX - 44, 19, psuX + 44, 171);
    box(psuX + 14 - 7.4, 240 - 8.2, psuX + 14 + 7.4, 240 + 8.2);
    for (const [fx, fy] of fans) { const q = new THREE.Path(); q.absarc(fx, fy, 58, 0, Math.PI * 2, true); rp.holes.push(q); }
    const rear = tag(new THREE.Mesh(new THREE.ExtrudeGeometry(rp, { depth: 3, bevelEnabled: false, curveSegments: 32 }), mat.cover), null, panel);
    rear.position.z = ZR - 3; edge(rear);
    for (const [fx, fy] of fans) filterAt(0, fx, fy, ZR - 3.6, 'LƯỚI LỌC 12 cm – lỗ thoát gió mặt sau (vít M4 × 10)');
    B(14.5, 16, 26, mat.black, psuX + 14, 240, ZR + 10, 'Đầu nối RJ45 keystone Vention – cáp mạng ra router', panel);
    for (const x of [-W / 2 + 10, W / 2 - 10]) for (const y of [30, 110, 190, 270]) C(5, 3, mat.ihs, 'z', x, y, ZR - 4.5, 'Vít M5 × 10: bắt mặt sau vào cột sau (tháo 8 vít khi rút máy)', panel, 16);
    CAT = 'net';
    tube([[swX, swPortY(4), -116], [swX, swPortY(4) + 6, -150], [psuX + 14, 240, ZR + 26]], mat.usb, 2.6, 'Cáp LAN 30 cm: switch cổng 5 → đầu nối RJ45 mặt sau', model);

""")

# --- dimensions + stats ---
R("dimLine([W / 2 + 24, -34, -D / 2 - 20], [W / 2 + 24, -34, D / 2 + 9], [0, 1, 0], `S ${D + 29} mm`);",
  "dimLine([W / 2 + 24, -34, -D / 2 - DR - 3], [W / 2 + 24, -34, D / 2 + 9], [0, 1, 0], `S ${D + DR + 12} mm`);")
R("const envD = D + 29,", "const envD = D + DR + 12,")
R("$('st-frame').textContent = `${W} × ${D} × ${H} mm`;", "$('st-frame').textContent = `${W} × ${D + DR} × ${H} mm`;")
R("$('c-dbar').textContent = `4 × ${D - 2 * PF} mm`;", "$('c-dbar').textContent = `4 × ${D + DR - 2 * PF} mm`;")
R("4 * (D - 2 * PF) / 1000", "4 * (D + DR - 2 * PF) / 1000")
R("const covKg = (2 * W * D + 2 * D * H - Math.PI * 58 ** 2) / 1e6 * 0.003 * 1190;\n    $('w-cov').textContent = f2(covKg); $('c-cov').textContent = `2 × ${W} × ${D}, 2 × ${D} × ${H}`;",
  "const DD = D + DR, covKg = (2 * W * DD + 2 * DD * H + W * H - 5 * Math.PI * 58 ** 2 - 88 * 152) / 1e6 * 0.003 * 1190;\n    $('w-cov').textContent = f2(covKg); $('c-cov').textContent = `2 × ${W} × ${DD}, 2 × ${DD} × ${H}, 1 × ${W} × ${H}`;")

# --- static texts ---
R('<span>Khung <b id="st-frame">424 × 260 × 300 mm</b></span>', '<span>Khung <b id="st-frame">424 × 310 × 300 mm</b></span>')
R('<b id="st-env">430 × 289 × 316 mm</b>', '<b id="st-env">430 × 322 × 316 mm</b>')
R('<td class="n" id="c-dbar">4 × 220 mm</td>', '<td class="n" id="c-dbar">4 × 270 mm</td>')
s = s.replace("4 thanh dọc 220 mm", "4 thanh dọc 270 mm")
R("<tr><td>Tấm che bụi mica 3 mm: nắp + đáy, 2 hông (hông phải có lỗ quạt nguồn + lưới lọc)</td><td class=\"n\" id=\"c-cov\">2 × 424 × 260, 2 × 260 × 300</td></tr>",
  "<tr><td>Hộp kín 6 mặt, mica 3 mm: nắp + đáy, 2 hông, mặt sau (lỗ có gió đi qua mới gắn lưới lọc)</td><td class=\"n\" id=\"c-cov\">2 × 424 × 310, 2 × 310 × 300, 1 × 424 × 300</td></tr>")
R("<tr><td>Tấm che bụi mica 3 mm (nắp, đáy, 2 hông)</td>", "<tr><td>Tấm che bụi mica 3 mm (nắp, đáy, 2 hông, mặt sau)</td>")
RX(r'<p class="warn">Phủ bì đã gồm tai chặn sau 20 mm.*?</p>',
   '<p class="warn">Hộp kín cả 6 mặt. Gió chỉ đi qua 9 lưới lọc 12 cm: <b>vào</b> qua 4 quạt mặt trước + quạt nguồn (hông phải), <b>ra</b> qua 4 lỗ mặt sau. Mọi chỗ khác là mica kín. Quạt hút vào mạnh hơn lỗ thoát → áp suất dương nhẹ, bụi không lọt qua khe. Đuôi nguồn (ổ cắm AC, công tắc, quạt thoát của nguồn) lộ ra ngoài qua lỗ mặt sau; cáp mạng ra router qua đầu nối RJ45. Vệ sinh lưới 1 lần/tháng. Phủ bì đã gồm mica + đầu nút trước 9 mm, mặt sau 3 mm và chân 10 mm.</p>')
RX(r"<li>Đặt nguồn ATX dựng đứng.*?</li>",
   "<li>Đặt nguồn ATX dựng đứng vào khoang phải, quạt nguồn ra hông phải, đuôi nguồn (ổ cắm AC) quay ra sau. Cắm jumper PS_ON. Treo giá switch lên thanh chặn sau và ray giữa phía trên, luồn switch vào từ phía sau.</li>")
RX(r"<li>Trượt từng tấm bo vào lược từ phía sau(.*?)</li>", r"<li>Trượt từng tấm bo vào lược từ phía sau\1 Muốn rút máy sau này: tháo 8 vít mặt sau trước.</li>")
RX(r"<li>Bắt tấm đáy \(dán chân cao su trước\).*?</li>",
   "<li>Bắt tấm đáy (dán chân cao su trước), 2 tấm hông, nắp trên, rồi mặt sau (đuôi nguồn lọt qua lỗ chữ nhật, dán ron xốp quanh khe): vít M5 × 10 + long đền. Gắn 5 lưới lọc không có quạt (4 lỗ sau + hông phải) bằng vít M4 × 10 + đai ốc. Cắm đầu nối RJ45 keystone, nối cáp 30 cm từ cổng 5 của switch.</li>")
# buy list
R("5 m; nhắn shop cắt 4×300, 4×220, 6×384 mm", "5 m; nhắn shop cắt 4×300, 4×270, 6×384 mm")
R("<td>13 gói (130 con, gồm 36 con cho tấm che bụi)</td>", "<td>14 gói (140 con, gồm 44 con cho 6 mặt che bụi)</td>")
R("<td>≈ 130 M5 + 30 M3</td>", "<td>≈ 140 M5 + 30 M3</td>")
R("<td>≈ 130 con</td>", "<td>≈ 140 con</td>")
R("thêm 4 vít M4 × 10 cho lưới lọc hông phải nếu shop có phân loại này", "thêm 20 vít M4 × 10 cho 5 lưới lọc không có quạt (4 lỗ sau + hông phải), nếu shop có phân loại này")
R("Lưới lọc bụi 12 cm kèm ốc</a></td><td>5 (4 quạt trước + 1 quạt nguồn)</td>", "Lưới lọc bụi 12 cm kèm ốc</a></td><td>9 (4 quạt trước, 1 quạt nguồn, 4 lỗ thoát sau)</td>")
R("(gửi mat-truoc + nap-tren-duoi + hong-trai + hong-phai)</a></td><td>5 tấm mica trong 3 mm</td>", "(gửi mat-truoc + nap-tren-duoi + hong-trai + hong-phai + mat-sau)</a></td><td>6 tấm mica trong 3 mm</td>")
R("Tổng ước tính ≈ 4,3 triệu đồng", "Tổng ước tính ≈ 4,5 triệu đồng")
key_img = "https://down-vn.img.susercontent.com/file/cn-11134207-7r98o-lqx7m49vthwd0a_tn"
if mode == "embed": key_img = "data:image/jpeg;base64," + base64.b64encode(urllib.request.urlopen(key_img, timeout=20).read()).decode()
RX(r'(<tr><td class="thumb"><a href="https://shopee\.vn/product/177448719/29857473563".*?Cáp LAN Cat6 đúc sẵn 30 cm</a></td><td>)4(</td>.*?</tr>)',
   r'\g<1>5 (4 máy + 1 switch → mặt sau)\g<2>' + f'\n        <tr><td class="thumb"><a href="https://shopee.vn/product/95236094/5223846243" target="_blank" rel="noopener"><img src="{key_img}" alt="" loading="lazy" width="56" height="56"></a></td><td><a href="https://shopee.vn/product/95236094/5223846243" target="_blank" rel="noopener">Đầu nối RJ45 keystone Vention (cáp mạng xuyên mặt sau)</a></td><td>1</td><td class="n">52,8k</td></tr>')
# files table
if mode == "link":
    R('<a href="files/hong-phai_mica-3mm_x1.dxf" download>hong-phai_mica-3mm_x1.dxf</a>', '<a href="files/hong-phai_mica-3mm_x1.dxf" download>hong-phai_mica-3mm_x1.dxf</a>, <a href="files/mat-sau_mica-3mm_x1.dxf" download>mat-sau_mica-3mm_x1.dxf</a>')
else:
    R('<code>hong-phai_mica-3mm_x1.dxf</code>', '<code>hong-phai_mica-3mm_x1.dxf</code>, <code>mat-sau_mica-3mm_x1.dxf</code>')
R("Hông phải có lỗ quạt nguồn cố định; khi lắp trượt nguồn tới/lui cho quạt trùng lỗ.</td><td class=\"n\">2 + 1 + 1</td>",
  "Hộp kín 6 mặt. Lưới lọc ở hông phải (quạt nguồn) và 4 lỗ thoát mặt sau; mặt sau có lỗ đuôi nguồn và lỗ RJ45 keystone.</td><td class=\"n\">2 + 1 + 1 + 1</td>")
R("['cover', 'Tấm che bụi']", "['cover', 'Hộp kín + lưới lọc']")
open(p, "w").write(s); print("ok", p, len(s) // 1024, "KB")
