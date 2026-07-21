"""Kullanici mesajindaki rakı ve meşrubat fiyatlarini uygular."""
import json
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "data" / "menu.json"
data = json.loads(p.read_text(encoding="utf-8"))

raki = next(c for c in data["categories"] if c["id"] == "raki")

for it in raki["items"]:
    if it["name"].startswith("Beylerbeyi ") and "Göbek" not in it["name"]:
        it["name"] = it["name"].replace("Beylerbeyi", "Beylerbeyi Göbek", 1)
        it["nameEn"] = it["nameEn"].replace("Beylerbeyi", "Beylerbeyi Göbek", 1)

by_name = {it["name"]: it for it in raki["items"]}

raki_prices = {
    "Beylerbeyi Göbek 20 cl": 1400,
    "Beylerbeyi Göbek 35 cl": 2300,
    "Beylerbeyi Göbek 50 cl": 3000,
    "Beylerbeyi Göbek 70 cl": 3800,
    "Beylerbeyi Göbek 100 cl": None,
    "Yeni Rakı 20 cl": 1100,
    "Yeni Rakı 35 cl": 1700,
    "Yeni Rakı 50 cl": 2200,
    "Yeni Rakı 70 cl": 2800,
    "Yeni Rakı Yeni Seri 20 cl": 1200,
    "Yeni Rakı Yeni Seri 35 cl": 1800,
    "Yeni Rakı Yeni Seri 50 cl": 2200,
    "Yeni Rakı Yeni Seri 70 cl": 3000,
    "Tekirdağ Rakısı Altın Seri 20 cl": 1300,
    "Tekirdağ Rakısı Altın Seri 35 cl": 2000,
    "Tekirdağ Rakısı Altın Seri 50 cl": 2600,
    "Tekirdağ Rakısı Altın Seri 70 cl": 3500,
}
for name, price in raki_prices.items():
    if name in by_name:
        by_name[name]["price"] = price

if "Yeni Rakı Yeni Seri 20 cl" not in by_name:
    idx = next(
        i for i, it in enumerate(raki["items"]) if it["name"] == "Yeni Rakı Yeni Seri 35 cl"
    )
    raki["items"].insert(
        idx,
        {
            "name": "Yeni Rakı Yeni Seri 20 cl",
            "nameEn": "Yeni Rakı Yeni Seri 20 cl",
            "price": 1200,
            "unit": None,
            "image": "assets/category/raki.jpg",
        },
    )

by_name = {it["name"]: it for it in raki["items"]}
for tr, en, pr in [
    ("Sarı Zeybek 3 Meşe 35 cl", "Sarı Zeybek 3 Meşe 35 cl", 2300),
    ("Sarı Zeybek 3 Meşe 50 cl", "Sarı Zeybek 3 Meşe 50 cl", 3200),
    ("Sarı Zeybek 3 Meşe 70 cl", "Sarı Zeybek 3 Meşe 70 cl", 4000),
    ("Sarı Zeybek 3 Meşe 100 cl", "Sarı Zeybek 3 Meşe 1 L", 5500),
]:
    if tr not in by_name:
        raki["items"].append(
            {
                "name": tr,
                "nameEn": en,
                "price": pr,
                "unit": None,
                "image": "assets/category/raki.jpg",
            }
        )
    else:
        by_name[tr]["price"] = pr

mes = next(c for c in data["categories"] if c["id"] == "mesrubatlar")


def find_sub(name):
    for sub in mes["subcategories"]:
        if sub["name"] == name:
            return sub
    return None


gazli = find_sub("Gazlı İçecekler")
for it in gazli["items"]:
    if it["name"] == "Kola":
        it["price"] = 100
    elif it["name"] == "Fanta":
        it["price"] = 100
    elif it["name"] == "Limonata":
        it["price"] = 150
    elif it["name"] == "Soda":
        it["price"] = 50

existing = {it["name"] for it in gazli["items"]}
for name, en, price in [
    ("Şalgam", "Turnip Juice", 100),
    ("Red Bull", "Red Bull", 200),
    ("Meyveli Soda", "Flavored Soda", 80),
]:
    if name not in existing:
        gazli["items"].append({"name": name, "nameEn": en, "price": price, "unit": None})

find_sub("Su & Ayran")["items"] = [
    {"name": "Küçük Su", "nameEn": "Small Water", "price": 25, "unit": None},
    {"name": "Büyük Su", "nameEn": "Large Water", "price": 50, "unit": None},
    {"name": "Maden Suyu", "nameEn": "Mineral Water", "price": None, "unit": None},
    {"name": "Ayran", "nameEn": "Ayran", "price": None, "unit": None},
]

for it in find_sub("Sıcak İçecekler")["items"]:
    if it["name"] == "Çay Bardak":
        it["price"] = 30
    elif it["name"] == "Çay Fincan":
        it["price"] = None
    elif it["name"] == "Türk Kahvesi":
        it["price"] = 80
    elif it["name"] == "Nescafe":
        it["price"] = 80

p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Guncellendi.")
