"""Builds the two language pages from index.html (the French page is the source).

index.html holds both languages; the <html lang> decides which one shows. This writes the search-engine head
(title, description, canonical, hreflang, Open Graph, JSON-LD) of each page and the English copy en/index.html,
so each language has its own URL. Run it after every change to index.html: python build.py
"""
import json
import re
from pathlib import Path

SITE = "https://dofight.github.io"
HERE = Path(__file__).parent
URLS = {"fr": f"{SITE}/", "en": f"{SITE}/en/"}
TEXT = {
    "fr": {
        "title": "Dofight · L'assistant de combat pour Dofus 3",
        "description": "Dofight : un panneau à côté de Dofus 3 qui te montre ce qui est dangereux chez les monstres "
        "autour de toi. Gratuit, open source, lecture de l'écran uniquement.",
        "locale": "fr_FR",
        "image_alt": "Dofight ouvert à côté d'un combat de Dofus 3",
    },
    "en": {
        "title": "Dofight · The fight assistant for Dofus 3",
        "description": "Dofight: a panel next to Dofus 3 that shows what makes the monsters around you dangerous. "
        "Free, open source, it only reads the screen.",
        "locale": "en_US",
        "image_alt": "Dofight open next to a Dofus 3 fight",
    },
}


def head(lang: str) -> str:
    t = TEXT[lang]
    other = "en" if lang == "fr" else "fr"
    app = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "Dofight",
        "description": t["description"],
        "url": URLS[lang],
        "image": f"{SITE}/images/og.jpg",
        "applicationCategory": "GameApplication",
        "operatingSystem": "Windows 10, Windows 11",
        "downloadUrl": "https://github.com/dofight/dofight/releases/latest",
        "license": "https://github.com/dofight/dofight/blob/main/LICENSE",
        "inLanguage": ["fr", "en"],
        "isAccessibleForFree": True,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
        "sameAs": ["https://github.com/dofight/dofight", "https://discord.gg/G8G4cyvpx6"],
    }
    esc = lambda s: s.replace("&", "&amp;").replace('"', "&quot;")
    return "\n".join([
        "<!-- seo: written by build.py -->",
        f"<title>{t['title']}</title>",
        f'<meta name="description" content="{esc(t["description"])}">',
        f'<link rel="canonical" href="{URLS[lang]}">',
        f'<link rel="alternate" hreflang="fr" href="{URLS["fr"]}">',
        f'<link rel="alternate" hreflang="en" href="{URLS["en"]}">',
        f'<link rel="alternate" hreflang="x-default" href="{URLS["fr"]}">',
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="Dofight">',
        f'<meta property="og:title" content="{esc(t["title"])}">',
        f'<meta property="og:description" content="{esc(t["description"])}">',
        f'<meta property="og:url" content="{URLS[lang]}">',
        f'<meta property="og:locale" content="{t["locale"]}">',
        f'<meta property="og:locale:alternate" content="{TEXT[other]["locale"]}">',
        f'<meta property="og:image" content="{SITE}/images/og.jpg">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{esc(t["image_alt"])}">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="theme-color" content="#1e2831">',
        '<meta name="google-site-verification" content="2zyhJK7FzVzOcl51zQkoh4fyFUQJCYZ-jEqQzTPVTx8">',  # Search Console
        f'<script type="application/ld+json">{json.dumps(app, ensure_ascii=False)}</script>',
        "<!-- /seo -->",
    ])


SEO = re.compile(r"<!-- seo: written by build.py -->.*?<!-- /seo -->", re.S)


def page(source: str, lang: str) -> str:
    out = SEO.sub(lambda _: head(lang), source)
    return re.sub(r'<html lang="\w+">', f'<html lang="{lang}">', out, count=1)


def main() -> None:
    source = (HERE / "index.html").read_text(encoding="utf-8")
    if not SEO.search(source):
        raise SystemExit("index.html has no <!-- seo --> block")
    (HERE / "index.html").write_text(page(source, "fr"), encoding="utf-8", newline="\n")
    (HERE / "en").mkdir(exist_ok=True)
    (HERE / "en" / "index.html").write_text(page(source, "en"), encoding="utf-8", newline="\n")
    print("index.html, en/index.html")


if __name__ == "__main__":
    main()
