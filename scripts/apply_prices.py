"""Fiyat listesinden menu.json guncelleme (sadece net yazili fiyatlar)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENU = ROOT / "data" / "menu.json"

# (kategori_id, urun_adi) -> fiyat; unit menu.json'da zaten varsa korunur
PRICES = {
    # Mezeler
    ("mezeler", "Peynir"): 150,
    ("mezeler", "Kavun"): 150,
    ("mezeler", "Patlıcan Salata"): 200,
    ("mezeler", "Soslu Patlıcan"): 200,
    ("mezeler", "Haydari"): 200,
    ("mezeler", "Acılı Ezme"): 200,
    ("mezeler", "Havuç Tarator"): 200,
    ("mezeler", "Barbunya Pilaki"): 200,
    ("mezeler", "Al Biber"): 200,
    ("mezeler", "Zeytinyağlı Enginar"): 250,
    ("mezeler", "Fava"): 200,
    ("mezeler", "Deniz Börülcesi"): 200,
    ("mezeler", "Semizotu"): 200,
    ("mezeler", "Midye Dolma"): 300,
    ("mezeler", "Lakerda"): 350,
    # Ara sicaklar
    ("ara-sicaklar", "Kalamar Tava"): 300,
    ("ara-sicaklar", "Karides Güveç"): 300,
    ("ara-sicaklar", "Tereyağlı Karides"): 300,
    ("ara-sicaklar", "Jumbo Karides"): 250,
    ("ara-sicaklar", "Balık Köfte"): 100,
    ("ara-sicaklar", "Paçanga Böreği"): 200,
    ("ara-sicaklar", "Sigara Böreği"): 150,
    ("ara-sicaklar", "Yaprak Ciğer"): 750,
    ("ara-sicaklar", "Ahtapot Izgara"): 900,
    ("ara-sicaklar", "Pastırmalı Humus"): 350,
    ("ara-sicaklar", "Patates Tava"): 200,
    # Salatalar
    ("salatalar", "Çoban Salata"): 200,
    ("salatalar", "Mevsim Salata"): 200,
    ("salatalar", "Yeşil Salata"): 200,
    ("salatalar", "Göbek Salata"): 250,
    ("salatalar", "Gavurdağı Salata"): 250,
    # Izgara balik
    ("izgara-baliklar", "Çupra"): 700,
    ("izgara-baliklar", "Levrek"): 750,
    ("izgara-baliklar", "Deniz Levreği"): 1800,
    ("izgara-baliklar", "Deniz Çuprası"): 1800,
    # Tava balik
    ("tava-baliklar", "Somon"): 700,
    # Izgara et
    ("izgara-et", "Tavuk Şiş"): 400,
    ("izgara-et", "Tavuk Sote"): 450,
    ("izgara-et", "Tavuk Pirzola"): 400,
    ("izgara-et", "Köfte"): 450,
    ("izgara-et", "Dana Bonfile"): 1000,
    ("izgara-et", "Dana Antrikot"): 900,
    ("izgara-et", "Kuzu Şiş"): 750,
    ("izgara-et", "Kuzu Pirzola"): 600,
    ("izgara-et", "Çoban Kavurma"): 800,
    ("izgara-et", "Et Sote"): 800,
    ("izgara-et", "Karışık Izgara"): 1200,
    # Tatli & icecek
    ("tatli-meyve", "Mevsim Meyveleri"): 200,
    ("mesrubatlar", "Meyve Suları"): 100,
    ("mesrubatlar", "Nescafe"): 70,
    ("mesrubatlar", "Çay Bardak"): 30,
    ("mesrubatlar", "Çay Fincan"): 50,
    ("mesrubatlar", "Türk Kahvesi"): 70,
    # Raki
    ("raki", "Yeni Rakı Duble"): 400,
    ("raki", "Yeni Rakı Tek"): 250,
    ("raki", "Yeni Rakı 20 cl"): 1000,
    ("raki", "Yeni Rakı 35 cl"): 1600,
    ("raki", "Yeni Rakı 50 cl"): 2100,
    ("raki", "Yeni Rakı 70 cl"): 2500,
    ("raki", "Yeni Rakı Yeni Seri 35 cl"): 1650,
    ("raki", "Yeni Rakı Yeni Seri 50 cl"): 2100,
    ("raki", "Yeni Rakı Yeni Seri 70 cl"): 2600,
    ("raki", "Beylerbeyi 20 cl"): 1300,
    ("raki", "Beylerbeyi 35 cl"): 2000,
    ("raki", "Beylerbeyi 50 cl"): 2300,
    ("raki", "Beylerbeyi 70 cl"): 3000,
    ("raki", "Beylerbeyi 100 cl"): 4500,
    ("raki", "Tekirdağ Rakısı Altın Seri 20 cl"): 1100,
    ("raki", "Tekirdağ Rakısı Altın Seri 35 cl"): 1600,
    ("raki", "Tekirdağ Rakısı Altın Seri 50 cl"): 2200,
    ("raki", "Tekirdağ Rakısı Altın Seri 70 cl"): 2800,
}

WINE_PRICES = {
    ("Buzbağ Klasik", "Öküzgözü - Boğazkere"): 1400,
    ("Buzbağ", "Emir - Narince"): 1200,
    ("Leona Blush", "Leona Blush"): 1200,
}


def apply():
    data = json.loads(MENU.read_text(encoding="utf-8"))
    data["settings"]["showPrices"] = True
    updated = 0

    for cat in data["categories"]:
        cid = cat["id"]
        if "items" in cat:
            for item in cat["items"]:
                key = (cid, item["name"])
                if key in PRICES:
                    item["price"] = PRICES[key]
                    updated += 1
        if "subcategories" in cat:
            for sub in cat["subcategories"]:
                for item in sub["items"]:
                    key = (cid, item["name"])
                    if key in PRICES:
                        item["price"] = PRICES[key]
                        updated += 1
                    wine_key = (item["name"], item["nameEn"])
                    if wine_key in WINE_PRICES:
                        item["price"] = WINE_PRICES[wine_key]
                        updated += 1

    MENU.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Guncellenen urun: {updated}")


if __name__ == "__main__":
    apply()
