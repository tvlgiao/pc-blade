"""Add a thumbnail column to the Shopee buy list (images hot-linked from Shopee's CDN)."""
import re, sys
IMG = {
 "18582419413": "vn-11134207-7r98o-lm5r12l7oyxr42", "19991324646": "vn-11134207-7r98o-lm5r12l830m79d",
 "18526140511": "sg-11134201-824ga-mptw6jqo0sg2c4", "21167497169": "vn-11134207-7ra0g-m81rlklvkghz18",
 "18076698796": "sg-11134201-824gq-mptwibbvk1lbfc", "22909947653": "vn-11134207-7ra0g-m81hewfefl9q86",
 "44010994681": "vn-11134207-7ras8-mcub1a0e1uwd19", "26786094388": "vn-11134207-7ra0g-m9enhmi0rxqa1d",
 "27985190123": "vn-11134207-81ztc-mp9cqa4q8f0v8f", "15351869899": "342503842050066124b717bd4223176e",
 "11571929527": "f22b3ca50d5c5a38000eb3039d58ce35", "17389446702": "sg-11134201-22110-7jckqpdm6ojvbd",
 "9381418486": "6a982955d694b6ad62579d768713ab92", "23283879160": "vn-11134207-81ztc-mlt1lj0rev4373",
 "24602052203": "vn-11134207-7r98o-lolbb0c7320j3b",
 "21982369902": "vn-11134207-7r98o-lm5thnp31zvj28",
 "41226017692": "sg-11134201-821d7-mghfl2ecqubsc8",
 "27202373150": "sg-11134201-7rd4x-lwdq26icbb0s21",
 "8062317661": "vn-11134207-7r98o-lzyzpdv7m0y5a8",
 "44424996827": "vn-11134207-820l4-mh23y88slfym31",
 "19490785453": "vn-11134201-7qukw-lj7xaaby21akf8",
 "4548917504": "8e5d28d71bf02dda88f9d82b69aac8e4",
 "18513528585": "18e50cfeac0478474e3015313eedfc20",
 "20093258607": "vn-11134207-7r98o-llul2wf2aqjj6d",
 "18669823642": "sg-11134201-22120-4anboq3z7jlvbe",
 "20950360510": "vn-11134207-7ras8-m4zyya113o6ub3",
 "29857473563": "vn-11134207-7ra0g-m93zhqo9o28485",
 "19740502842": "cn-11134207-820l4-mqr1cz3ggm4i2d",
 "43561265978": "vn-11134207-81ztc-mlzayb9gnuvj7b",
 "23475983346": "vn-11134207-7r98o-lrgm7m8j14n8f4",
 "55414655516": "vn-11134207-81ztc-mqzzom3fiolo74",
 "22676249970": "vn-11110105-7r98o-lujiu7k2tuez42",
 "17164097346": "bbf87dbfcd0a2cc8ddfe7afedc07bd69",
}
for p in sys.argv[1:]:
    s = open(p).read()
    if 'class="thumb"' in s: continue
    def row(m):
        url, item = m.group(1), m.group(2)
        img = IMG.get(item)
        cell = (f'<img src="https://down-vn.img.susercontent.com/file/{img}_tn" alt="" loading="lazy" width="56" height="56">'
                if img else '<span>Xem ảnh trên Shopee</span>')
        return f'<tr><td class="thumb"><a href="{url}" target="_blank" rel="noopener">{cell}</a></td><td><a href="{url}"'
    s = re.sub(r'<tr><td><a href="(https://shopee\.vn/product/\d+/(\d+))"', row, s)
    s = s.replace('<tr><td>Cắt laser nhôm 2 mm', '<tr><td class="thumb"><span>—</span></td><td>Cắt laser nhôm 2 mm')
    s = s.replace('<tr><th>Món (bấm để mở Shopee)</th>', '<tr><th>Ảnh</th><th>Món (bấm để mở Shopee)</th>')
    s = s.replace('<tr class="grp"><td colspan="3">', '<tr class="grp"><td colspan="4">')
    s = s.replace('tr.grp td {', 'td.thumb { width: 64px; padding-right: 10px; }\ntd.thumb img { display: block; width: 56px; height: 56px; object-fit: cover; border-radius: 6px; border: 1px solid var(--line); background: #fff; }\ntd.thumb span { display: grid; place-items: center; width: 56px; height: 56px; border-radius: 6px; border: 1px dashed var(--line); font-size: 10px; line-height: 1.2; text-align: center; color: var(--muted); }\ntr.grp td {')
    open(p, 'w').write(s)
    print(p, s.count('class="thumb"'), s.count('_tn"'))
