"""Smoked (black transparent) acrylic, perforated filter zones with the black filter inside,
PSU bolted to the rear panel (ATX 6-32 pattern), deeper plate notches."""
import re, sys
p = sys.argv[1]
s = open(p).read()
def R(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
def RX(pat, b, n=1):
    global s
    s2, c = re.subn(pat, b, s, flags=re.S); assert c == n, (c, pat[:80]); s = s2
# materials: smoked acrylic, dark edges
R("acrylic: M(0x9fc1e6, { t: 0.16, r: 0.1, side: THREE.DoubleSide }),", "acrylic: M(0x15171b, { t: 0.42, r: 0.08, m: 0.1, side: THREE.DoubleSide }),")
R("cover: M(0x7fb3e6, { t: 0.3, r: 0.1, side: THREE.DoubleSide }), coverEdge: new THREE.LineBasicMaterial({ color: 0x1f68c8 }),",
  "cover: M(0x15171b, { t: 0.42, r: 0.08, m: 0.1, side: THREE.DoubleSide }), coverEdge: new THREE.LineBasicMaterial({ color: 0x0a0b0d }),")
# perforation helper (same grid as gen/covers.py: Ø6 on 7.5 mm hex)
R("  /* Model state, rebuilt whenever the bay count changes */",
  "  /* Perforated filter zone: Ø6 holes on a 7.5 mm hex grid inside a circle (matches gen/covers.py) */\n"
  "  function perf(path, cx, cy, r) {\n"
  "    const P = 7.5, dy = P * 0.8660254;\n"
  "    for (let j = -Math.ceil(r / dy); j <= Math.ceil(r / dy); j++) for (let i = -Math.ceil(r / P) - 1; i <= Math.ceil(r / P) + 1; i++) {\n"
  "      const x = i * P + (j % 2 ? P / 2 : 0), y = j * dy;\n"
  "      if (Math.hypot(x, y) <= r - 3) { const h = new THREE.Path(); h.absarc(cx + x, cy + y, 3, 0, Math.PI * 2, true); path.holes.push(h); }\n"
  "    }\n"
  "  }\n\n"
  "  /* Model state, rebuilt whenever the bay count changes */")
R("      for (const fx of ROW) { const q = new THREE.Path(); q.absarc(fx, 0, 44, 0, Math.PI * 2, true); sh.holes.push(q); }\n      const pm = tag(new THREE.Mesh(new THREE.ExtrudeGeometry(sh, { depth: 3, bevelEnabled: false, curveSegments: 32 }), mat.cover), null, panel);",
  "      for (const fx of ROW) perf(sh, fx, 0, 42);\n      const pm = tag(new THREE.Mesh(new THREE.ExtrudeGeometry(sh, { depth: 3, bevelEnabled: false, curveSegments: 6 }), mat.cover), null, panel);")
R("const fh = new THREE.Path(); fh.absarc(fanZ, 95, 58, 0, Math.PI * 2, true); rs.holes.push(fh);\n    const rside = tag(new THREE.Mesh(new THREE.ExtrudeGeometry(rs, { depth: 3, bevelEnabled: false, curveSegments: 32 }), mat.cover), null, panel);",
  "perf(rs, fanZ, 95, 56);\n    const rside = tag(new THREE.Mesh(new THREE.ExtrudeGeometry(rs, { depth: 3, bevelEnabled: false, curveSegments: 6 }), mat.cover), null, panel);")
R("filterAt(Math.PI / 2, W / 2 + 3.6, 95, fanZ, 'LƯỚI LỌC 12 cm – gió vào quạt nguồn (hông phải)');",
  "filterAt(Math.PI / 2, W / 2 - 0.6, 95, fanZ, 'LƯỚI LỌC 12 cm đen, đặt phía trong mica – gió vào quạt nguồn (hông phải)');")
# fans + filters inside: panel -> filter -> fan
R("for (const fx of ROW) { makeFan(fx, H - 12.5, 0, true); makeFan(fx, 12.5, 0, false); }",
  "for (const fx of ROW) { makeFan(fx, H - 13.5, 0, true); makeFan(fx, 13.5, 0, false); }")
R("B(94, 1, 94, mat.filter, cx, cy + (top ? 16 : -16), cz, `LƯỚI LỌC 9 cm ngoài mica – ${top ? 'gió vào (nóc)' : 'gió ra (đáy)'}, vít M4 × 12 + đai ốc kẹp lưới + mica + bích quạt`, model);",
  "B(94, 1, 94, mat.filter, cx, cy + (top ? 13 : -13), cz, `LƯỚI LỌC 9 cm đen, phía trong mica đục lỗ – ${top ? 'gió vào (nóc)' : 'gió ra (đáy)'}, vít M4 × 12 + đai ốc kẹp mica + lưới + bích quạt`, model);")
# plate notch deeper
R("[100, 22.5], [100, 27], [200, 27], [200, 22.5]", "[100, 22.5], [100, 28.5], [200, 28.5], [200, 22.5]")
R("[200, 276.5], [200, 272.5], [100, 272.5], [100, 276.5]", "[200, 276.5], [200, 271.5], [100, 271.5], [100, 276.5]")
# PSU bolted to the rear panel
R("box(psuX - 44, 19, psuX + 44, 171);", "box(psuX - 31, 32, psuX + 31, 158);")
R("    const rear = tag(new THREE.Mesh(", "    const rear = tag(new THREE.Mesh(")
R("    rear.position.z = ZR - 3; edge(rear);",
  "    rear.position.z = ZR - 3; edge(rear);\n"
  "    for (const [x, y] of [[psuX - 37, 26], [psuX - 37, 164], [psuX + 37, 26], [psuX + 37, 140]]) C(3.2, 2.5, mat.ihs, 'z', x, y, ZR - 4.3, 'Vít 6‑32 bắt nguồn vào mặt sau (4 lỗ chuẩn ATX)', panel, 12);")
R("'Nguồn ATX đang có – đuôi lọt qua lỗ mặt sau, hút gió qua lưới hông phải'", "'Nguồn ATX đang có – bắt 4 vít 6‑32 vào mặt sau như case thường, hút gió qua lưới hông phải'")
# texts
s = s.replace("mica trong 3 mm", "mica đen trong 3 mm").replace("Mica 3 mm mặt trước", "Mica đen trong 3 mm mặt trước").replace("6 tấm mica trong 3 mm", "6 tấm mica đen trong (mica khói) 3 mm")
RX(r"Hộp kín 6 mặt, mica 3 mm:", "Hộp kín 6 mặt, mica đen trong (mica khói) 3 mm:")
RX(r"Quạt nằm trong thùng, mặt ngoài bằng mặt thanh nhôm; lưới lọc dán ngoài mica, tháo vệ sinh không cần mở thùng\.",
   "Quạt nằm trong thùng, mặt ngoài bằng mặt thanh nhôm. Chỗ có gió, mica đục lỗ tròn Ø6 xếp tổ ong; lưới lọc màu đen đặt phía trong, nhìn ngoài chỉ thấy mặt mica đen trong đục lỗ.")
RX(r"Đuôi nguồn \(ổ cắm AC, công tắc\) lộ ra qua lỗ mặt sau;", "Nguồn bắt 4 vít 6‑32 vào mặt sau như case thường, ổ cắm AC + công tắc lộ ra qua ô hở;")
RX(r"lưới lọc 9 cm dán mặt ngoài mica; vít M4 × 12 \+ đai ốc kẹp lưới \+ mica \+ bích ngoài của quạt\.",
   "lưới lọc 9 cm đen kẹp giữa mica và quạt (phía trong); vít M4 × 12 + đai ốc kẹp mica + lưới + bích quạt.")
RX(r"rồi mặt sau \(đuôi nguồn lọt qua lỗ chữ nhật, dán ron xốp quanh khe\)", "rồi mặt sau (bắt nguồn vào mặt sau bằng 4 vít 6‑32 trước)")
RX(r"Lưới 12 cm ở hông phải: vít M4 × 10\.", "Lưới 12 cm ở hông phải đặt phía trong: vít M4 × 10.")
RX(r"(Băng dán gai 5 m × 12 mm )\(giữ nguồn\)", r"\1(bó dây gọn)")
RX(r"Hông phải có lỗ quạt nguồn \(lưới 12 cm\)|hông phải 1 lỗ quạt nguồn \(lưới 12 cm\)", "hông phải 1 vùng đục lỗ cho quạt nguồn (lưới 12 cm phía trong)")
RX(r"Nắp và đáy mỗi tấm 3 lỗ quạt 92 mm \(lưới 9 cm\)", "Nắp và đáy mỗi tấm 3 vùng đục lỗ Ø6 cho quạt 92 mm (lưới 9 cm đen phía trong)")
RX(r"Mặt sau có lỗ đuôi nguồn và lỗ RJ45 keystone\.", "Mặt sau: 6 lỗ vít nguồn 6‑32 (chuẩn ATX), ô hở ổ cắm AC, lỗ RJ45 keystone.")
RX(r"(Lưới lọc bụi nylon mịn 9 cm, có lỗ bắt ốc \(cùng shop hub quạt\)</a></td><td>)6, chọn 9 cm", r"\g<1>6, chọn 9 cm, màu đen")
open(p, "w").write(s); print("ok", p)
