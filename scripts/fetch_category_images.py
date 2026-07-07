"""Download professional category images for rakı and wine."""
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "category"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def save_square(url: str, path: Path) -> None:
    data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()
    img = Image.open(BytesIO(data)).convert("RGB")
    side = min(img.size)
    left = (img.size[0] - side) // 2
    top = (img.size[1] - side) // 2
    img = img.crop((left, top, left + side, top + side))
    img = img.resize((600, 600), Image.LANCZOS)
    img.save(path, "JPEG", quality=92)
    print(f"OK {path.name} ({len(data)} bytes)")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    wine_urls = [
        "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=800&q=85",
    ]

    raki_urls = [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Tastingouzo.jpg/500px-Tastingouzo.jpg",
    ]

    for url in wine_urls:
        try:
            save_square(url, OUT / "wine.jpg")
            break
        except Exception as exc:
            print(f"wine fail: {exc}")

    for url in raki_urls:
        try:
            save_square(url, OUT / "raki.jpg")
            break
        except Exception as exc:
            print(f"raki fail {url[:60]}: {exc}")


if __name__ == "__main__":
    main()
