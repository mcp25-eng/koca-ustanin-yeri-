"""Download accurate food images from Wikimedia Commons.

For each menu item we run one or more search queries against Wikimedia
Commons and keep the first landscape/portrait photo whose title matches the
expected keywords. Results are center-cropped to 600x600 JPEGs.

Run:  python scripts/download_food_images.py            # only missing
      python scripts/download_food_images.py --only key1 key2
      python scripts/download_food_images.py --force     # redownload all
"""
import argparse
import json
import time
import urllib.parse
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "foods"
UA = {"User-Agent": "KocaUstaniMenu/1.0 (restaurant digital menu; contact admin@kocaustaninyeri.local)"}

# key -> list of (query, [keywords that should appear in the file title]).
# The first candidate whose lowercased title contains any keyword wins;
# if none match, the first image result of the first query is used.
QUERIES = {
    # --- Mezeler ---
    "peynir": [("Feta cheese", ["feta", "cheese", "peynir"])],
    "kavun": [("Cantaloupe slices", ["melon", "cantaloupe", "kavun"])],
    "patlican-salata": [("Patlıcan salatası", ["patl", "eggplant", "aubergine"]),
                         ("Eggplant salad", ["eggplant", "aubergine", "salad"])],
    "soslu-patlican": [("Fried eggplant tomato sauce", ["eggplant", "aubergine", "patl"])],
    "haydari": [("Haydari meze", ["haydari"])],
    "acili-ezme": [("Ezme salad", ["ezme"]), ("Acılı ezme", ["ezme"]),
                    ("Turkish red pepper paste dip", ["ezme", "acuka", "muhammara"])],
    "havuc-tarator": [("Yoğurtlu havuç", ["havu", "yo\u011furt", "carrot"]),
                       ("Carrot yogurt dip meze", ["carrot", "yogurt", "yoghurt", "tarator"])],
    "zencefilli-cibez": [("Turkish meze plate", ["meze"])],
    "barbunya-pilaki": [("Barbunya pilaki", ["barbunya", "pilaki"]),
                         ("Borlotti beans stew", ["bean", "borlotti", "pilaki"])],
    "al-biber": [("Roasted pepper salad plate", ["pepper"]),
                  ("Marinated bell peppers dish", ["pepper", "capsicum"])],
    "tursu": [("Turşu pickles", ["tur", "pickle"]), ("Pickled vegetables jar", ["pickle"])],
    "cali-fasulye": [("Zeytinyağlı taze fasulye", ["fasulye", "bean"]),
                      ("Green beans olive oil", ["bean", "fasulye"])],
    "zeytinyagli-enginar": [("Zeytinyagli Enginar", ["enginar", "artichoke"]),
                             ("Artichoke hearts cooked dish", ["artichoke", "enginar"])],
    "fava": [("Fava dip plate", ["fava"]), ("Greek fava dish", ["fava"]),
              ("Yellow split pea puree meze", ["fava", "pea puree", "puree"])],
    "deniz-borulcesi": [("Samphire cooked dish", ["samphire", "salicornia", "glasswort"]),
                         ("Salicornia salad plate", ["salicornia", "samphire", "glasswort"])],
    "semizotu": [("Yoğurtlu semizotu", ["semizotu", "purslane"]),
                  ("Purslane yogurt dish", ["purslane", "semizotu"])],
    "midye-dolma": [("Midye dolma", ["midye", "mussel"]),
                     ("Stuffed mussels", ["mussel", "midye"])],
    "ahtapot": [("Octopus meze plate", ["octopus", "ahtapot"]),
                 ("Boiled octopus dish", ["octopus", "ahtapot"])],
    "lakerda": [("Lakerda", ["lakerda"])],
    "soslu-hamsi": [("Anchovy dish plate", ["anchov", "hamsi"]),
                     ("Marinated anchovies", ["anchov", "hamsi"])],
    "soya-soslu-uskumru": [("Grilled mackerel plate", ["mackerel", "uskumru"]),
                            ("Cooked mackerel fillet dish", ["mackerel", "fish"])],
    "kalamar-cibez": [("Calamari salad", ["calamari", "squid", "kalamar"])],
    "ciroz": [("Çiroz dried mackerel", ["ciroz", "\u00e7iroz", "mackerel"]),
               ("Dried fish meze", ["dried", "fish"])],
    "levrek-marin": [("Sea bass ceviche", ["ceviche", "bass", "levrek"]),
                      ("Fish carpaccio", ["carpaccio", "fish"])],
    "sogus-karides": [("Shrimp cocktail", ["shrimp", "prawn", "karides"]),
                       ("Boiled shrimp salad", ["shrimp", "prawn"])],
    "beyin-salata": [("Lamb brain salad", ["brain", "beyin"]),
                      ("Boiled brain dish", ["brain"])],
    "ciger": [("Arnavut ciğeri", ["ciger", "ci\u011fer", "liver"]),
               ("Fried liver dish", ["liver", "ciger"])],
    "feslegenli-levrek-marin": [("Fish carpaccio basil", ["carpaccio", "fish", "basil"]),
                                 ("Sea bass ceviche", ["ceviche", "bass"])],
    "patlican-tava": [("Fried eggplant slices", ["eggplant", "aubergine", "patl"])],
    "soguk-meze": [("Turkish meze plate", ["meze"]), ("Meze assortment", ["meze"])],
    "sicak-pazi": [("Sauteed spinach garlic plate", ["spinach", "chard", "greens"]),
                    ("Cooked leafy greens dish", ["greens", "spinach", "chard"])],
    # --- Ara Sıcaklar ---
    "kalamar-tava": [("Fried calamari rings", ["calamari", "squid", "kalamar"]),
                      ("Calamari fritti", ["calamari", "squid"])],
    "kalamar-izgara": [("Grilled squid plate", ["squid", "calamari"]),
                        ("Grilled calamari dish", ["squid", "calamari"])],
    "karides-guvec": [("Shrimp casserole", ["shrimp", "prawn", "g\u00fcve\u00e7", "saganaki"]),
                       ("Prawn saganaki dish", ["shrimp", "prawn"])],
    "tereyagli-karides": [("Shrimp butter garlic", ["shrimp", "prawn", "scampi"])],
    "jumbo-karides": [("Jumbo prawns grilled", ["prawn", "shrimp", "langoustine"])],
    "balik-mucver": [("Zucchini fritters mücver", ["mucver", "m\u00fccver", "fritter"]),
                      ("Fish cakes", ["fish cake", "fishcake"])],
    "balik-kokorec": [("Kokoreç", ["kokore"]), ("Grilled fish skewer", ["fish"])],
    "balik-kofte": [("Fish balls fried", ["fish", "ball", "k\u00f6fte", "kofte", "croquette"])],
    "pacanga-boregi": [("Paçanga böreği", ["pacanga", "pa\u00e7anga", "b\u00f6re"]),
                        ("Fried pastry rolls", ["borek", "b\u00f6re", "pastry"])],
    "sigara-boregi": [("Sigara böreği", ["sigara", "b\u00f6re", "borek"]),
                       ("Fried cheese rolls", ["borek", "b\u00f6re", "roll"])],
    "yaprak-ciger": [("Fried liver cubes dish", ["liver", "ciger"]),
                      ("Albanian liver", ["liver", "arnavut"])],
    "ahtapot-izgara": [("Grilled octopus tentacle plate", ["octopus", "ahtapot"]),
                        ("Grilled octopus dish", ["octopus"])],
    "pastirmali-humus": [("Hummus bowl", ["hummus", "humus"]),
                          ("Hummus with meat topping", ["hummus", "humus"])],
    "patates-tava": [("Bowl of french fries", ["fries", "chips"]),
                      ("French fried potatoes plate", ["fries", "chips", "potato"])],
    "yunan-usulu-kabak": [("Fried zucchini slices", ["zucchini", "courgette", "kabak"])],
    "levrek-simit": [("Grilled sea bass fillet plate", ["bass", "levrek", "sea bass"]),
                      ("Cooked sea bass dish", ["bass", "sea bass"])],
    "balik-boregi": [("Fried fish roll pastry", ["fish", "borek", "b\u00f6re", "pastry", "roll"]),
                      ("Fish spring roll", ["fish", "roll"])],
    # --- Salatalar ---
    "coban-salata": [("Çoban salatası", ["\u00e7oban", "coban", "shepherd"]),
                      ("Shepherd salad tomato cucumber", ["shepherd", "salad"])],
    "mevsim-salata": [("Mixed green salad plate", ["salad"])],
    "yesil-salata": [("Green salad lettuce", ["green salad", "lettuce", "salad"])],
    "gobek-salata": [("Iceberg lettuce salad bowl", ["iceberg", "salad"]),
                      ("Lettuce salad plate", ["lettuce", "salad"])],
    "gavurdagi-salata": [("Gavurdağı salatası", ["gavurda"]),
                          ("Tomato walnut salad", ["salad", "tomato"])],
    "sefin-salatasi": [("Chef salad plate", ["chef", "salad"]),
                        ("Composed salad plate", ["salad"])],
    # --- Izgara Balıklar ---
    "hamsi-izgara": [("Grilled anchovies plate", ["anchov", "hamsi"]),
                      ("Anchovies cooked dish", ["anchov", "hamsi"])],
    "sardalya-izgara": [("Grilled sardines plate", ["sardine", "sardalya"])],
    "cupra": [("Grilled dorada fish", ["dorada", "bream", "gilt"]),
               ("Cooked sea bream dish", ["bream", "fish", "dorada"]),
               ("Grilled fish plate lemon", ["fish", "grilled"])],
    "levrek-izgara": [("Grilled sea bass plate", ["bass", "levrek", "sea bass"])],
    "somon-izgara": [("Grilled salmon fillet plate", ["salmon", "somon"])],
    "cinekop": [("Fried bluefish plate", ["bluefish", "fish"]),
                 ("Grilled bluefish dish", ["bluefish", "fish"])],
    "sarikanat": [("Fried fish fillet plate", ["fish", "fried"]),
                   ("Grilled fish plate", ["fish", "grilled"])],
    "lufer": [("Grilled fish fillet plate", ["fish", "grilled", "bluefish"]),
               ("Cooked whole fish dish", ["fish", "cooked"])],
    "kofana": [("Grilled bluefish fillet", ["bluefish", "fish"]),
                ("Grilled fish plate", ["fish", "grilled"])],
    "kalkan": [("Cooked turbot fillet plate", ["turbot", "fish"]),
                ("Pan fried flatfish dish", ["fish", "flatfish", "turbot"]),
                ("Grilled white fish plate", ["fish", "grilled"])],
    "kilic-sis": [("Grilled swordfish skewers", ["swordfish", "kili\u00e7"]),
                   ("Grilled swordfish plate", ["swordfish"])],
    "akya": [("Grilled amberjack plate", ["amberjack", "leerfish", "fish"]),
              ("Grilled fish fillet plate", ["fish", "grilled"])],
    "lagos": [("Cooked grouper fillet plate", ["grouper", "fish"]),
               ("Grilled fish fillet dish", ["fish", "grilled"])],
    "deniz-levregi": [("Grilled sea bass whole plate", ["bass", "levrek", "sea bass"]),
                       ("Baked sea bass dish", ["bass", "sea bass"])],
    "deniz-cuprasi": [("Baked sea bream fish", ["bream", "dorada", "gilt"]),
                       ("Grilled fish plate lemon", ["fish", "grilled"])],
    "palamut-izgara": [("Grilled tuna steak plate", ["tuna", "bonito", "fish"]),
                        ("Grilled fish steak lemon", ["fish", "grilled"])],
    # --- Tava Balıklar ---
    "hamsi-tava": [("Fried anchovies plate", ["anchov", "hamsi", "fried"])],
    "sardalya-tava": [("Pan fried sardines Portuguese", ["sardine"]),
                       ("Fried sardines white plate", ["sardine", "fish"])],
    "istavrit": [("Fried horse mackerel plate", ["horse mackerel", "mackerel", "istavrit"]),
                  ("Deep fried mackerel dish", ["mackerel", "fish"])],
    "tekir": [("Pan fried red mullet", ["mullet", "tekir", "barbun"])],
    "mezgit": [("Fried whiting fish plate", ["whiting", "mezgit"]),
                ("Fried white fish fillet", ["fish", "fried", "whiting"])],
    "somon-tava": [("Pan seared salmon fillet plate", ["salmon", "somon"]),
                    ("Cooked salmon dish", ["salmon", "fish"])],
    "levrek-tava": [("Fried sea bass fillet plate", ["bass", "levrek", "sea bass"])],
    "barbun": [("Fried red mullet plate", ["mullet", "barbun"])],
    "palamut-tava": [("Seared tuna steak plate", ["tuna", "bonito", "fish"]),
                      ("Cooked fish steak dish", ["fish", "cooked", "steak"])],
    # --- Izgara Et ---
    "tavuk-sis": [("Chicken shish kebab", ["chicken", "shish", "\u015fi\u015f", "kebab"])],
    "tavuk-sote": [("Chicken saute vegetables", ["chicken", "saute", "sote"])],
    "tavuk-pirzola": [("Grilled chicken chops", ["chicken", "chop"])],
    "kanat-izgara": [("Grilled chicken wings", ["wing", "chicken"])],
    "pilic-sarma": [("Chicken wrap grilled", ["chicken", "roll", "wrap"])],
    "kofte": [("Turkish köfte grilled", ["k\u00f6fte", "kofte", "meatball"])],
    "inegol-kofte": [("İnegöl köfte", ["inegol", "ineg\u00f6l", "k\u00f6fte", "meatball"])],
    "dana-bonfile": [("Cooked beef tenderloin steak plate", ["tenderloin", "steak", "filet mignon"]),
                      ("Grilled beef steak dish", ["steak", "beef"])],
    "dana-antrikot": [("Grilled steak plate", ["steak", "ribeye", "entrecote"]),
                       ("Cooked beef steak dish", ["steak", "beef"])],
    "kuzu-sis": [("Lamb shish kebab", ["lamb", "shish", "\u015fi\u015f", "kebab"])],
    "kuzu-tandir": [("Lamb tandır", ["tandir", "tand\u0131r", "lamb"]),
                     ("Roast lamb", ["lamb", "roast"])],
    "kuzu-pirzola": [("Grilled lamb chops", ["lamb", "chop", "pirzola"])],
    "cop-sis": [("Çöp şiş kebab", ["\u00e7\u00f6p", "cop sis", "shish", "kebab"]),
                 ("Small lamb skewers", ["skewer", "kebab", "lamb"])],
    "coban-kavurma": [("Kavurma meat", ["kavurma", "roast", "saute"])],
    "et-sote": [("Beef saute vegetables", ["saute", "sote", "beef", "meat"])],
    "karisik-izgara": [("Mixed grill meat platter", ["mixed grill", "grill", "kebab"])],
    # --- Tatlı & Meyve ---
    "dondurmali-irmik": [("Semolina halva ice cream", ["semolina", "irmik", "halva"]),
                          ("İrmik helvası", ["irmik", "helva", "semolina"])],
    "firinda-helva": [("Halva dessert", ["halva", "helva"])],
    "mevsim-meyveleri": [("Fruit platter", ["fruit", "platter", "meyve"])],
}


def fetch_json(url):
    req = urllib.request.Request(url, headers=UA)
    return json.loads(urllib.request.urlopen(req, timeout=25).read())


def commons_file_url(title, width=700):
    """Return the scaled thumbnail URL for an exact File: title."""
    if not title.startswith("File:"):
        title = "File:" + title
    params = urllib.parse.urlencode({
        "action": "query", "format": "json", "titles": title,
        "prop": "imageinfo", "iiprop": "url", "iiurlwidth": width,
    })
    data = fetch_json("https://commons.wikimedia.org/w/api.php?" + params)
    for pg in data.get("query", {}).get("pages", {}).values():
        ii = (pg.get("imageinfo") or [{}])[0]
        return ii.get("thumburl") or ii.get("url")
    return None


# key -> exact Commons file title (overrides search when set)
DIRECT = {
    "al-biber": "Padron peppers roasted w salt and olive oil (5968334695).jpg",
    "sicak-pazi": "Acelga a la crema (tallos).jpg",
    "palamut-izgara": "Atún ojael 5.JPG",
    "palamut-tava": "Awesome tuna steak.jpg",
    "istavrit": "Fish and chips in Turkey.jpg",
}


def commons_search(query, limit=8):
    params = urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": query, "gsrlimit": limit, "gsrnamespace": 6,
        "prop": "imageinfo", "iiprop": "url|mime", "iiurlwidth": 700,
    })
    data = fetch_json("https://commons.wikimedia.org/w/api.php?" + params)
    pages = data.get("query", {}).get("pages", {})
    results = []
    for pg in sorted(pages.values(), key=lambda p: p.get("index", 999)):
        ii = (pg.get("imageinfo") or [{}])[0]
        title = pg.get("title", "")
        low = title.lower()
        if not (low.endswith(".jpg") or low.endswith(".jpeg") or low.endswith(".png")):
            continue
        thumb = ii.get("thumburl")
        if thumb:
            results.append((title, thumb))
    return results


BLACKLIST = [
    "manuscript", "gallica", "bnf", "drawing", "painting", "map", "coat of arms",
    "stamp", "banknote", "logo", "poster", "portrait", "statue", "book", "page",
    "illustration", "century", "1808", "diagram", "chart", "label", "sign",
    "engraving", "woodcut", "miniature", "fresco", "icon", "sculpture", "cover",
    "market", "aquarium", "underwater", "reef", "swimming", "live specimen",
    "museum", "drawing of", "seal of", "flag", "mercado", "secos", "dried",
    "drying", "seco ", "specimen", "taxidermy", "fishing", "aquarel", "stuffed animal",
    ".djvu", ".pdf", ".svg", ".tif", "manual", "fish-culture", "1897", "1898", "1899",
    "wdl", "world digital", "threshing", "harvest", "plant", "growing", "field",
    "frittata", "teishoku", "tonjiru", "soup", "kenkey", "tartare", "tartar",
]
FOOD_WORDS = [
    "dish", "plate", "meze", "food", "salad", "grill", "fried", "cooked", "restaurant",
    "kebab", "meal", "cuisine", "served", "recipe", "plated", "bowl", "appetizer",
    "starter", "roast", "steak", "fillet", "fresh", "seafood",
]


def score(title, keywords):
    low = title.lower()
    if any(b in low for b in BLACKLIST):
        return -1
    s = 0
    if any(k.lower() in low for k in keywords):
        s += 3
    if any(w in low for w in FOOD_WORDS):
        s += 1
    return s


def pick(candidates_by_query):
    """candidates_by_query: list of (keywords, [(title, url), ...]).

    Prefer earlier queries; within a query, pick the highest scoring candidate
    that isn't blacklisted. Fall back to first non-blacklisted image overall.
    """
    for keywords, results in candidates_by_query:
        best = None
        best_s = 0
        for idx, (title, url) in enumerate(results):
            sc = score(title, keywords)
            if sc < 0:
                continue
            # earlier results get a tiny boost so ties keep search ranking
            sc_adj = sc * 10 - idx
            if best is None or sc_adj > best_s:
                best, best_s = (url, title), sc_adj
        if best and best_s >= 30:  # required at least one keyword match
            return best
    # relaxed: any non-blacklisted result, keyword match preferred
    for keywords, results in candidates_by_query:
        for title, url in results:
            if score(title, keywords) >= 0:
                return url, title
    return None, None


def save_square(url, path):
    data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()
    img = Image.open(BytesIO(data)).convert("RGB")
    side = min(img.size)
    left = (img.size[0] - side) // 2
    top = (img.size[1] - side) // 2
    img = img.crop((left, top, left + side, top + side)).resize((600, 600), Image.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "JPEG", quality=88)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    keys = args.only if args.only else list(QUERIES.keys())
    log = []
    for key in keys:
        if key not in QUERIES:
            print(f"SKIP {key}: no query defined")
            continue
        out_path = OUT / f"{key}.jpg"
        if key in DIRECT:
            try:
                url = commons_file_url(DIRECT[key])
                save_square(url, out_path)
                print(f"OK   {key}  <- (direct) {DIRECT[key]}")
                log.append((key, "OK-direct", DIRECT[key]))
            except Exception as exc:
                print(f"FAIL {key} (direct): {exc}")
                log.append((key, "DIRECT FAIL", DIRECT[key]))
            time.sleep(0.3)
            continue
        cand = []
        for query, keywords in QUERIES[key]:
            try:
                cand.append((keywords, commons_search(query)))
            except Exception as exc:
                cand.append((keywords, []))
                print(f"  search error {key} <{query}>: {exc}")
            time.sleep(0.4)
        url, title = pick(cand)
        if not url:
            print(f"FAIL {key}: no result")
            log.append((key, "NO RESULT", ""))
            continue
        try:
            save_square(url, out_path)
            print(f"OK   {key}  <- {title}")
            log.append((key, "OK", title))
        except Exception as exc:
            print(f"FAIL {key}: {exc}")
            log.append((key, "DL FAIL", title))
        time.sleep(0.3)

    (ROOT / "scripts" / "download_log.txt").write_text(
        "\n".join(f"{s}\t{k}\t{t}" for k, s, t in log), encoding="utf-8")


if __name__ == "__main__":
    main()
