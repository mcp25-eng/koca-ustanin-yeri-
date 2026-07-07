import re
import urllib.parse
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

for term in ["ouzo", "raki", "pastis", "anise drink", "turkish drink"]:
    q = urllib.parse.quote(term)
    url = f"https://pixabay.com/images/search/{q}/"
    html = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20).read().decode("utf-8", "ignore")
    ids = re.findall(r"/photos/[^\"']+-(\d+)/", html)
    cdn = re.findall(r"https://cdn\.pixabay\.com/photo/[^\"'\s>]+\.jpg", html)
    print(term, "ids", ids[:5], "cdn", len(cdn))
    for c in cdn[:3]:
        print(" ", c)
