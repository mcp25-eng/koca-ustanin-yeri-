"""DEPRECATED — do not use for the live menu.

WhatsApp menu scans are name references only. Use scripts/download_food_images.py
to fetch professional stock photos from TheMealDB instead.
"""
from PIL import Image, ImageEnhance
import numpy as np
import os
import shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "assets", "foods")
os.makedirs(OUT, exist_ok=True)

PAGES = [
    ("WhatsApp Image 2026-07-06 at 13.49.38.jpeg", "right",
     ["peynir", "kavun", "patlican-salata", "soslu-patlican", "haydari", "acili-ezme", "havuc-tarator", "zencefilli-cibez"]),
    ("WhatsApp Image 2026-07-06 at 13.49.47.jpeg", "left",
     ["barbunya-pilaki", "al-biber", "tursu", "cali-fasulye", "zeytinyagli-enginar", "fava", "deniz-borulcesi"]),
    ("WhatsApp Image 2026-07-06 at 13.49.55.jpeg", "right",
     ["semizotu", "midye-dolma", "ahtapot", "lakerda", "soslu-hamsi", "soya-soslu-uskumru", "kalamar-cibez"]),
    ("WhatsApp Image 2026-07-06 at 13.50.02.jpeg", "left",
     ["ciroz", "levrek-marin", "sogus-karides", "beyin-salata", "ciger", "feslegenli-levrek-marin", "patlican-tava"]),
    ("WhatsApp Image 2026-07-06 at 13.50.07.jpeg", "right",
     ["kalamar-tava", "kalamar-izgara", "karides-guvec", "tereyagli-karides", "jumbo-karides", "balik-mucver", "balik-kokorec"]),
    ("WhatsApp Image 2026-07-06 at 13.50.12.jpeg", "left",
     ["balik-kofte", "pacanga-boregi", "sigara-boregi", "yaprak-ciger", "ahtapot-izgara", "pastirmali-humus", "patates-tava"]),
    ("WhatsApp Image 2026-07-06 at 13.51.23.jpeg", "right",
     ["coban-salata", "mevsim-salata", "yesil-salata", "gobek-salata", "gavurdagi-salata", "sefin-salatasi"]),
    ("WhatsApp Image 2026-07-06 at 13.51.31.jpeg", "left",
     ["hamsi-izgara", "sardalya-izgara", "cupra", "levrek-izgara", "somon-izgara", "cinekop", "sarikanat", "lufer"]),
    ("WhatsApp Image 2026-07-06 at 13.51.37.jpeg", "right",
     ["kofana", "kalkan", "kilic-sis", "akya", "lagos", "deniz-levregi", "deniz-cuprasi", "palamut-izgara"]),
    ("WhatsApp Image 2026-07-06 at 13.51.42.jpeg", "left",
     ["hamsi-tava", "sardalya-tava", "istavrit", "tekir", "mezgit", "somon-tava", "levrek-tava", "barbun", "palamut-tava"]),
    ("WhatsApp Image 2026-07-06 at 13.51.50.jpeg", "right",
     ["tavuk-sis", "tavuk-sote", "tavuk-pirzola", "kanat-izgara", "pilic-sarma", "kofte", "inegol-kofte", "dana-bonfile"]),
    ("WhatsApp Image 2026-07-06 at 13.51.54.jpeg", "left",
     ["dana-antrikot", "kuzu-sis", "kuzu-tandir", "kuzu-pirzola", "cop-sis", "coban-kavurma", "et-sote", "karisik-izgara"]),
    ("WhatsApp Image 2026-07-06 at 13.52.02.jpeg", "right",
     ["dondurmali-irmik", "firinda-helva", "mevsim-meyveleri"]),
]

X = {
    "right": (0.755, 0.925),
    "left": (0.050, 0.285),
}


def detect_photo_regions(img, side, y_scan=280, y_end=1920):
    w, h = img.size
    x1, x2 = int(w * X[side][0]), int(w * X[side][1])
    ye = min(y_end, h)
    rgb = np.array(img.crop((x1, y_scan, x2, ye)))
    gray = rgb.mean(axis=2)
    std = rgb.std(axis=2)
    wood = (gray > 105) & (gray < 210) & (std < 16)
    food = (gray > 38) & (std > 7) & (~wood)
    row = food.mean(axis=1)
    active = row > 0.095

    regions = []
    i = 0
    while i < len(active):
        if active[i]:
            s = i
            while i < len(active) and active[i]:
                i += 1
            if i - s > 32:
                regions.append((y_scan + s, y_scan + i))
        else:
            i += 1
    return regions


MIN_REGION_HEIGHT = 95


def merge_close_regions(regions, gap=15, max_height=90):
    """Merge only tiny adjacent bands (spurious splits within one photo row)."""
    if not regions:
        return []
    merged = [regions[0]]
    for a, b in regions[1:]:
        pa, pb = merged[-1]
        if a - pb < gap and (pb - pa) < max_height and (b - a) < max_height:
            merged[-1] = (pa, b)
        else:
            merged.append((a, b))
    return merged


def drop_leading_spurious(regions, page_height=1920):
    regions = list(regions)
    while len(regions) >= 2:
        r0, r1 = regions[0], regions[1]
        if (r0[1] - r0[0]) < 110 and r1[0] - r0[1] < 15:
            regions = regions[1:]
        else:
            break
    return regions


def boxes_from_centers(regions, n, y_scan=320, y_end=1860):
    raw = drop_leading_spurious(sorted(regions, key=lambda r: r[0]))
    usable = [(a, b) for a, b in raw if b - a >= 50]
    if len(usable) == n:
        heights = [b - a for a, b in usable]
        if max(heights) <= 2.2 * min(heights):
            centers = [(a + b) / 2 for a, b in usable]
            boxes = []
            for i in range(n):
                h = usable[i][1] - usable[i][0]
                if h < 100:
                    boxes.append((usable[i][0] + 4, usable[i][1] - 4))
                else:
                    ya = int((centers[i - 1] + centers[i]) / 2) if i else usable[i][0]
                    yb = int((centers[i] + centers[i + 1]) / 2) if i < n - 1 else usable[i][1]
                    boxes.append((ya + 4, yb - 4))
            return boxes

    raw = drop_leading_spurious(merge_close_regions(sorted(regions, key=lambda r: r[0])))
    usable = [(a, b) for a, b in raw if b - a >= 50]
    if len(usable) == n:
        heights = [b - a for a, b in usable]
        if max(heights) <= 2.2 * min(heights):
            centers = [(a + b) / 2 for a, b in usable]
            boxes = []
            for i in range(n):
                h = usable[i][1] - usable[i][0]
                if h < 100:
                    boxes.append((usable[i][0] + 4, usable[i][1] - 4))
                else:
                    ya = int((centers[i - 1] + centers[i]) / 2) if i else usable[i][0]
                    yb = int((centers[i] + centers[i + 1]) / 2) if i < n - 1 else usable[i][1]
                    boxes.append((ya + 4, yb - 4))
            return boxes

    return None


def equal_row_boxes(regions, n, y_scan=320, y_end=1860):
    """Use detected photo bands when possible; otherwise split evenly."""
    centered = boxes_from_centers(regions, n, y_scan, y_end)
    if centered:
        return centered

    regions = merge_close_regions(sorted(regions, key=lambda r: r[0]))
    regions = drop_leading_spurious(regions)

    filtered = [(a, b) for a, b in regions if b - a >= MIN_REGION_HEIGHT]
    if not filtered:
        filtered = [(a, b) for a, b in regions if b - a >= 55]

    if len(filtered) == n:
        pad = 4
        return [(a + pad, b - pad) for a, b in filtered]

    if len(filtered) > n:
        idx = np.linspace(0, len(filtered) - 1, n).astype(int)
        pad = 4
        return [(filtered[i][0] + pad, filtered[i][1] - pad) for i in idx]

    if not filtered:
        return fallback_boxes(n, y_scan, y_end)

    y_top, y_bot = filtered[0][0], filtered[-1][1]
    seg = (y_bot - y_top) / n
    margin = max(4, int(seg * 0.08))
    return [
        (int(y_top + i * seg) + margin, int(y_top + (i + 1) * seg) - margin)
        for i in range(n)
    ]


def fallback_boxes(n, y_scan=320, y_end=1860):
    seg = (y_end - y_scan) / n
    m = int(seg * 0.1)
    return [(int(y_scan + i * seg) + m, int(y_scan + (i + 1) * seg) - m) for i in range(n)]


def trim_column_side(img, side):
    """Crop to the food-photo block, dropping wood margins and black frame lines."""
    cw, ch = img.size
    rgb = np.array(img.convert("RGB"))
    gray = rgb.mean(axis=2)
    sat = rgb.max(axis=2).astype(float) - rgb.min(axis=2).astype(float)
    wood = (gray > 105) & (gray < 210) & (sat < 16)
    black = gray < 48
    food = (gray > 38) & (sat > 8) & (~wood) & (~black)
    col_food = food.mean(axis=0)
    col_wood = wood.mean(axis=0)
    col_black = black.mean(axis=0)

    start, end = 0, cw
    for x in range(cw):
        if col_food[x] > 0.15 and col_black[x] < 0.30:
            start = x
            break

    for x in range(start, cw):
        if col_black[x] > 0.28 or (col_wood[x] > 0.40 and col_food[x] < 0.12):
            end = x
            break
        if col_food[x] < 0.10 and x > start + 24:
            end = x
            break

    if side == "left":
        for x in range(start, min(end, cw)):
            if col_food[x] > 0.22 and col_wood[x] < 0.45:
                start = x
                break

    pad = 2
    if end - start < 20:
        if side == "left":
            return img.crop((int(cw * 0.22), 0, cw, ch))
        return img.crop((0, 0, int(cw * 0.72), ch))
    return img.crop((max(0, start - pad), 0, min(cw, end + pad), ch))


def crop_food_region(img):
    rgb = np.array(img.convert("RGB"))
    gray = rgb.mean(axis=2)
    sat = rgb.max(axis=2).astype(float) - rgb.min(axis=2).astype(float)
    wood = (gray > 110) & (gray < 205) & (sat < 14)
    mask = (gray > 40) & (sat > 10) & (~wood)
    if mask.sum() < 50:
        mask = gray > 38

    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    if not rows.any() or not cols.any():
        return img

    y1 = int(np.argmax(rows))
    y2 = int(len(rows) - np.argmax(rows[::-1]))
    x1 = int(np.argmax(cols))
    x2 = int(len(cols) - np.argmax(cols[::-1]))
    pad = 2
    return img.crop((
        max(0, x1 - pad), max(0, y1 - pad),
        min(rgb.shape[1], x2 + pad), min(rgb.shape[0], y2 + pad),
    ))


def trim_black_edges(img):
    gray = np.array(img.convert("L"))
    top, left, bottom, right = 0, 0, gray.shape[0], gray.shape[1]
    for _ in range(12):
        changed = False
        if top < bottom - 14 and (gray[top, left:right] < 50).mean() > 0.25:
            top += 1
            changed = True
        if bottom > top + 14 and (gray[bottom - 1, left:right] < 50).mean() > 0.25:
            bottom -= 1
            changed = True
        if left < right - 14 and (gray[top:bottom, left] < 50).mean() > 0.25:
            left += 1
            changed = True
        if right > left + 14 and (gray[top:bottom, right - 1] < 50).mean() > 0.25:
            right -= 1
            changed = True
        if not changed:
            break
    if bottom - top < 18 or right - left < 18:
        return img
    return img.crop((left, top, right, bottom))


def enhance(img):
    img = ImageEnhance.Contrast(img).enhance(1.1)
    img = ImageEnhance.Sharpness(img).enhance(1.15)
    img = ImageEnhance.Color(img).enhance(1.05)
    return img


def to_square(img, size=600):
    rgb = np.array(img.convert("RGB"))
    gray = rgb.mean(axis=2)
    sat = rgb.max(axis=2).astype(float) - rgb.min(axis=2).astype(float)
    wood = (gray > 110) & (gray < 205) & (sat < 14)
    mask = (gray > 40) & (sat > 10) & (~wood)
    cw, ch = img.size
    if mask.sum() > 80:
        ys, xs = np.where(mask)
        cy, cx = int(ys.mean()), int(xs.mean())
    else:
        cy, cx = ch // 2, cw // 2
    side = min(cw, ch)
    left = max(0, min(cw - side, cx - side // 2))
    top = max(0, min(ch - side, cy - side // 2))
    sq = img.crop((left, top, left + side, top + side))
    return sq.resize((size, size), Image.LANCZOS)


ok = 0
for page_file, side, slugs in PAGES:
    path = os.path.join(BASE, page_file)
    if not os.path.exists(path):
        print(f"SKIP {page_file}")
        continue

    img = Image.open(path)
    w, img_h = img.size
    x1, x2 = int(w * X[side][0]), int(w * X[side][1])
    scan_bot = 930 if "13.52.02" in page_file else min(1920, img_h - 10)

    regions = detect_photo_regions(img, side, y_scan=320, y_end=scan_bot)
    boxes = equal_row_boxes(regions, len(slugs), y_scan=320, y_end=scan_bot)
    print(f"{page_file[-18:]}: {len(regions)} boxes")

    for slug, (ya, yb) in zip(slugs, boxes):
        crop = img.crop((x1, ya, x2, yb))
        crop = trim_column_side(crop, side)
        crop = crop_food_region(crop)
        crop = trim_black_edges(crop)
        crop = enhance(to_square(crop))
        crop.save(os.path.join(OUT, f"{slug}.jpg"), "JPEG", quality=93)
        ok += 1
        print(f"  OK {slug}")

COPIES = {
    "yunan-usulu-kabak": "balik-mucver",
    "levrek-simit": "levrek-izgara",
    "balik-boregi": "sigara-boregi",
    "soguk-meze": "haydari",
    "sicak-pazi": "zencefilli-cibez",
}
for dst, src in COPIES.items():
    sp, dp = os.path.join(OUT, f"{src}.jpg"), os.path.join(OUT, f"{dst}.jpg")
    if os.path.exists(sp):
        shutil.copy(sp, dp)
        print(f"COPY {dst} <- {src}")

print(f"\nDone: {ok} images extracted.")
