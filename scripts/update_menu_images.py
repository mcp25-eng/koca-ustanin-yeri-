"""Add image paths to menu.json items."""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (category_id, item_name) -> image slug
IMAGE_SLUGS = {
    ("mezeler", "Peynir"): "peynir",
    ("mezeler", "Kavun"): "kavun",
    ("mezeler", "Patlıcan Salata"): "patlican-salata",
    ("mezeler", "Soslu Patlıcan"): "soslu-patlican",
    ("mezeler", "Haydari"): "haydari",
    ("mezeler", "Acılı Ezme"): "acili-ezme",
    ("mezeler", "Havuç Tarator"): "havuc-tarator",
    ("mezeler", "Zencefilli Cibez"): "zencefilli-cibez",
    ("mezeler", "Barbunya Pilaki"): "barbunya-pilaki",
    ("mezeler", "Al Biber"): "al-biber",
    ("mezeler", "Turşu"): "tursu",
    ("mezeler", "Çalı Fasulye"): "cali-fasulye",
    ("mezeler", "Zeytinyağlı Enginar"): "zeytinyagli-enginar",
    ("mezeler", "Fava"): "fava",
    ("mezeler", "Deniz Börülcesi"): "deniz-borulcesi",
    ("mezeler", "Semizotu"): "semizotu",
    ("mezeler", "Midye Dolma"): "midye-dolma",
    ("mezeler", "Ahtapot"): "ahtapot",
    ("mezeler", "Lakerda"): "lakerda",
    ("mezeler", "Soslu Hamsi"): "soslu-hamsi",
    ("mezeler", "Soya Soslu Uskumru"): "soya-soslu-uskumru",
    ("mezeler", "Kalamar Cibez"): "kalamar-cibez",
    ("mezeler", "Çiroz"): "ciroz",
    ("mezeler", "Levrek Marin"): "levrek-marin",
    ("mezeler", "Söğüş Karides"): "sogus-karides",
    ("mezeler", "Beyin Salata"): "beyin-salata",
    ("mezeler", "Ciğer"): "ciger",
    ("mezeler", "Fesleğenli Levrek Marin"): "feslegenli-levrek-marin",
    ("mezeler", "Patlıcan Tava"): "patlican-tava",
    ("ara-sicaklar", "Kalamar Tava"): "kalamar-tava",
    ("ara-sicaklar", "Kalamar Izgara"): "kalamar-izgara",
    ("ara-sicaklar", "Karides Güveç"): "karides-guvec",
    ("ara-sicaklar", "Tereyağlı Karides"): "tereyagli-karides",
    ("ara-sicaklar", "Jumbo Karides"): "jumbo-karides",
    ("ara-sicaklar", "Balık Mücver"): "balik-mucver",
    ("ara-sicaklar", "Balık Kokoreç"): "balik-kokorec",
    ("ara-sicaklar", "Balık Köfte"): "balik-kofte",
    ("ara-sicaklar", "Paçanga Böreği"): "pacanga-boregi",
    ("ara-sicaklar", "Sigara Böreği"): "sigara-boregi",
    ("ara-sicaklar", "Yaprak Ciğer"): "yaprak-ciger",
    ("ara-sicaklar", "Ahtapot Izgara"): "ahtapot-izgara",
    ("ara-sicaklar", "Pastırmalı Humus"): "pastirmali-humus",
    ("ara-sicaklar", "Patates Tava"): "patates-tava",
    ("salatalar", "Çoban Salata"): "coban-salata",
    ("salatalar", "Mevsim Salata"): "mevsim-salata",
    ("salatalar", "Yeşil Salata"): "yesil-salata",
    ("salatalar", "Göbek Salata"): "gobek-salata",
    ("salatalar", "Gavurdağı Salata"): "gavurdagi-salata",
    ("salatalar", "Şefin Salatası"): "sefin-salatasi",
    ("izgara-baliklar", "Hamsi"): "hamsi-izgara",
    ("izgara-baliklar", "Sardalya"): "sardalya-izgara",
    ("izgara-baliklar", "Çupra"): "cupra",
    ("izgara-baliklar", "Levrek"): "levrek-izgara",
    ("izgara-baliklar", "Somon"): "somon-izgara",
    ("izgara-baliklar", "Çinekop"): "cinekop",
    ("izgara-baliklar", "Sarıkanat"): "sarikanat",
    ("izgara-baliklar", "Lüfer"): "lufer",
    ("izgara-baliklar", "Kofana"): "kofana",
    ("izgara-baliklar", "Kalkan"): "kalkan",
    ("izgara-baliklar", "Kılıç Şiş"): "kilic-sis",
    ("izgara-baliklar", "Akya"): "akya",
    ("izgara-baliklar", "Lagos"): "lagos",
    ("izgara-baliklar", "Deniz Levreği"): "deniz-levregi",
    ("izgara-baliklar", "Deniz Çuprası"): "deniz-cuprasi",
    ("izgara-baliklar", "Palamut"): "palamut-izgara",
    ("tava-baliklar", "Hamsi"): "hamsi-tava",
    ("tava-baliklar", "Sardalya"): "sardalya-tava",
    ("tava-baliklar", "İstavrit"): "istavrit",
    ("tava-baliklar", "Tekir"): "tekir",
    ("tava-baliklar", "Mezgit"): "mezgit",
    ("tava-baliklar", "Somon"): "somon-tava",
    ("tava-baliklar", "Levrek"): "levrek-tava",
    ("tava-baliklar", "Barbun"): "barbun",
    ("tava-baliklar", "Palamut"): "palamut-tava",
    ("izgara-et", "Tavuk Şiş"): "tavuk-sis",
    ("izgara-et", "Tavuk Sote"): "tavuk-sote",
    ("izgara-et", "Tavuk Pirzola"): "tavuk-pirzola",
    ("izgara-et", "Kanat Izgara"): "kanat-izgara",
    ("izgara-et", "Piliç Sarma"): "pilic-sarma",
    ("izgara-et", "Köfte"): "kofte",
    ("izgara-et", "İnegöl Köfte"): "inegol-kofte",
    ("izgara-et", "Dana Bonfile"): "dana-bonfile",
    ("izgara-et", "Dana Antrikot"): "dana-antrikot",
    ("izgara-et", "Kuzu Şiş"): "kuzu-sis",
    ("izgara-et", "Kuzu Tandır"): "kuzu-tandir",
    ("izgara-et", "Kuzu Pirzola"): "kuzu-pirzola",
    ("izgara-et", "Çöp Şiş"): "cop-sis",
    ("izgara-et", "Çoban Kavurma"): "coban-kavurma",
    ("izgara-et", "Et Sote"): "et-sote",
    ("izgara-et", "Karışık Izgara"): "karisik-izgara",
    ("tatli-meyve", "Dondurmalı İrmik"): "dondurmali-irmik",
    ("tatli-meyve", "Fırında Helva"): "firinda-helva",
    ("tatli-meyve", "Mevsim Meyveleri"): "mevsim-meyveleri",
    ("mezeler", "Soğuk Meze"): "soguk-meze",
    ("mezeler", "Sıcak Pazı"): "sicak-pazi",
    ("ara-sicaklar", "Yunan Usulü Çıtır Kabak"): "yunan-usulu-kabak",
    ("ara-sicaklar", "Levrek Simit"): "levrek-simit",
    ("ara-sicaklar", "Balık Böreği"): "balik-boregi",
}

CATEGORY_FALLBACKS = {
    "mesrubatlar": "assets/foods/mevsim-meyveleri.jpg",
    "raki": "assets/category/raki.jpg",
    "saraplar": "assets/category/wine.jpg",
}

with open(os.path.join(BASE, "data", "menu.json"), encoding="utf-8") as f:
    data = json.load(f)

# Update restaurant logo and contact
data["restaurant"]["logo"] = "assets/logo.png"
data["contact"]["address"] = {
    "tr": "Yalova İzmit Karayolu Mevkii, Gazi Abdullah Erbaş Cad. Gazino No: 321/1A, Kılıçköy, Çiftlikköy, Yalova",
    "en": "Yalova-Izmit Highway, Gazi Abdullah Erbaş St. Gazino No: 321/1A, Kılıçköy, Çiftlikköy, Yalova"
}
data["contact"]["googleMaps"] = "https://maps.google.com/?q=Koca+Ustanın+Yeri+Yalova+Çiftlikköy"
data["social"]["googleMaps"] = data["contact"]["googleMaps"]

data["settings"]["footerNoteEn"] = "Alcohol prices may change on evenings with live music."

for cat in data["categories"]:
    items = cat.get("items") or []
    for sub in cat.get("subcategories") or []:
        items = items + sub.get("items", [])
    for item in (cat.get("items") or []):
        key = (cat["id"], item["name"])
        slug = IMAGE_SLUGS.get(key)
        if slug:
            item["image"] = f"assets/foods/{slug}.jpg"
    for sub in cat.get("subcategories") or []:
        for item in sub["items"]:
            pass  # wines don't have food images
    if cat["id"] in CATEGORY_FALLBACKS and cat.get("items"):
        for item in cat["items"]:
            if "image" not in item:
                item["image"] = CATEGORY_FALLBACKS[cat["id"]]

with open(os.path.join(BASE, "data", "menu.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("menu.json updated")
