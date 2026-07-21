import json
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "data" / "menu.json"
data = json.loads(p.read_text(encoding="utf-8"))
cur = data["settings"]["currency"]
print("showPrices:", data["settings"]["showPrices"])
print()

for cat in data["categories"]:
    name = cat["name"]
    items = []
    if "items" in cat:
        for it in cat["items"]:
            items.append(dict(it))
    if "subcategories" in cat:
        for sub in cat["subcategories"]:
            for it in sub["items"]:
                row = dict(it)
                row["_sub"] = sub["name"]
                items.append(row)
    priced = [it for it in items if it.get("price") is not None]
    unpriced = [it for it in items if it.get("price") is None]
    if not items:
        continue
    print(f"=== {name} — fiyatli {len(priced)} / {len(items)} ===")
    for it in priced:
        unit = it.get("unit")
        u = f" / {unit}" if unit else ""
        sub = f" ({it['_sub']})" if "_sub" in it else ""
        print(f"  • {it['name']}{sub}: {it['price']}{cur}{u}")
    if unpriced:
        print("  [fiyatsiz]")
        for it in unpriced:
            sub = f" ({it['_sub']})" if "_sub" in it else ""
            print(f"    - {it['name']}{sub}")
    print()
