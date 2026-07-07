"""Build labeled contact-sheet montages of food images for quick review."""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FOODS = ROOT / "assets" / "foods"
OUT = ROOT / "scripts" / "montage"

CELL = 220
LABEL_H = 26
COLS = 6


def load_font(size):
    for name in ["arial.ttf", "DejaVuSans.ttf", "segoeui.ttf"]:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def build(keys, out_name):
    font = load_font(13)
    rows = (len(keys) + COLS - 1) // COLS
    W = COLS * CELL
    H = rows * (CELL + LABEL_H)
    sheet = Image.new("RGB", (W, H), (245, 245, 245))
    draw = ImageDraw.Draw(sheet)
    for i, key in enumerate(keys):
        r, c = divmod(i, COLS)
        x = c * CELL
        y = r * (CELL + LABEL_H)
        p = FOODS / f"{key}.jpg"
        if p.exists():
            im = Image.open(p).convert("RGB").resize((CELL, CELL))
            sheet.paste(im, (x, y))
        else:
            draw.rectangle([x, y, x + CELL, y + CELL], fill=(210, 210, 210))
            draw.text((x + 8, y + 8), "MISSING", fill=(150, 0, 0), font=font)
        draw.rectangle([x, y + CELL, x + CELL, y + CELL + LABEL_H], fill=(30, 30, 30))
        draw.text((x + 4, y + CELL + 6), key, fill=(255, 255, 255), font=font)
    OUT.mkdir(parents=True, exist_ok=True)
    out_path = OUT / out_name
    sheet.save(out_path, "JPEG", quality=85)
    print(out_path)


GROUPS = {
    "01_mezeler": ["peynir", "kavun", "patlican-salata", "soslu-patlican", "haydari",
                    "acili-ezme", "havuc-tarator", "zencefilli-cibez", "barbunya-pilaki",
                    "al-biber", "tursu", "cali-fasulye", "zeytinyagli-enginar", "fava",
                    "deniz-borulcesi", "semizotu", "midye-dolma", "ahtapot", "lakerda",
                    "soslu-hamsi", "soya-soslu-uskumru", "kalamar-cibez", "ciroz",
                    "levrek-marin", "sogus-karides", "beyin-salata", "ciger",
                    "feslegenli-levrek-marin", "patlican-tava", "soguk-meze", "sicak-pazi"],
    "02_ara_sicak": ["kalamar-tava", "kalamar-izgara", "karides-guvec", "tereyagli-karides",
                      "jumbo-karides", "balik-mucver", "balik-kokorec", "balik-kofte",
                      "pacanga-boregi", "sigara-boregi", "yaprak-ciger", "ahtapot-izgara",
                      "pastirmali-humus", "patates-tava", "yunan-usulu-kabak", "levrek-simit",
                      "balik-boregi"],
    "03_salata_baliklar": ["coban-salata", "mevsim-salata", "yesil-salata", "gobek-salata",
                            "gavurdagi-salata", "sefin-salatasi", "hamsi-izgara",
                            "sardalya-izgara", "cupra", "levrek-izgara", "somon-izgara",
                            "cinekop", "sarikanat", "lufer", "kofana", "kalkan", "kilic-sis",
                            "akya", "lagos", "deniz-levregi", "deniz-cuprasi", "palamut-izgara"],
    "04_tava_et_tatli": ["hamsi-tava", "sardalya-tava", "istavrit", "tekir", "mezgit",
                          "somon-tava", "levrek-tava", "barbun", "palamut-tava", "tavuk-sis",
                          "tavuk-sote", "tavuk-pirzola", "kanat-izgara", "pilic-sarma", "kofte",
                          "inegol-kofte", "dana-bonfile", "dana-antrikot", "kuzu-sis",
                          "kuzu-tandir", "kuzu-pirzola", "cop-sis", "coban-kavurma", "et-sote",
                          "karisik-izgara", "dondurmali-irmik", "firinda-helva",
                          "mevsim-meyveleri"],
}


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    for name, keys in GROUPS.items():
        if which in ("all", name):
            build(keys, name + ".jpg")
