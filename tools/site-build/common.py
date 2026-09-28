"""Shared header, footer and <head> for the Spelling Quest website pages."""
import json

SITE = "https://spellingquest.github.io"
CSS_V = "5"
EMAIL = "spellingquest@gmail.com"
CHECKOUT = "https://spellingquest.gumroad.com/l/mlshxz"      # $40 family access
CHECKOUT_ADDON = "https://spellingquest.gumroad.com/l/xgcjen"  # $25 add Spelling Quest
CHECKOUT_TWO = "https://spellingquest.gumroad.com/l/miyhub"    # $49 add the other two
CHECKOUT_THREE = "https://spellingquest.gumroad.com/l/ihzywn"  # $89 all three
TRIAL = "app/#start=trial"

NAV = [
    ("index.html", "Home"),
    ("index.html#how", "How it works"),
    ("pricing.html", "Pricing"),
    ("faq.html", "FAQ"),
    ("schools.html", "Schools"),
    ("about.html", "About"),
]
FOOT = NAV + [
    ("contact.html", "Contact"),
    ("privacy.html", "Privacy"),
    ("terms.html", "Terms"),
    ("refunds.html", "Refunds"),
    ("signin.html", "Sign in"),
]


def head(*, path, title, description, extra_ld=None, noindex=False):
    url = f"{SITE}/" + ("" if path == "index.html" else path)
    ld = [{
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Spelling Quest",
        "url": f"{SITE}/",
        "logo": f"{SITE}/icon-512.png",
        "email": EMAIL,
    }]
    if extra_ld:
        ld += extra_ld
    ld_html = "\n".join(
        f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{description}">
{robots}<link rel="canonical" href="{url}">
<meta name="theme-color" content="#221252">
<link rel="icon" type="image/png" href="icon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">

<!-- Link preview (the card a texted or shared link shows). og:image MUST be an
     absolute URL; iMessage and some other scrapers fail silently on a relative one. -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="Spelling Quest">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{SITE}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Spelling Quest: their teacher's words, your child's learning path">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{SITE}/og.png">

<!-- Nunito for headings (approved 27 Sep 2026). Loaded without blocking the page. -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&display=swap"></noscript>
<link rel="stylesheet" href="site.css?v={CSS_V}">
{ld_html}
</head>
"""


def _is_current(href, current):
    return href == current


def header(current):
    links = "\n".join(
        f'      <a href="{h}"' + (' aria-current="page"' if _is_current(h, current) else "") + f">{t}</a>"
        for h, t in NAV)
    menu = "\n".join(
        f'        <a href="{h}"' + (' aria-current="page"' if _is_current(h, current) else "") + f">{t}</a>"
        for h, t in NAV + [("contact.html", "Contact"), ("signin.html", "Sign in")])
    return f"""<body>
<a class="skip" href="#main">Skip to the content</a>
<!-- Site header: identical on every page. If you change it, change it everywhere. -->
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Spelling Quest home">
      <img src="img/sq-logo-horizontal.webp" alt="Spelling Quest" width="640" height="160">
    </a>
    <nav class="nav" aria-label="Main">
{links}
    </nav>
    <div class="head-cta">
      <a class="signin" href="signin.html" data-signin""" + (' aria-current="page"' if current == 'signin.html' else '') + f""">Sign in</a>
      <a class="btn" href="{TRIAL}">Start free</a>
      <details class="menu">
        <summary aria-label="Open menu">Menu</summary>
        <div class="panel">
{menu}
        </div>
      </details>
    </div>
  </div>
</header>
<main id="main">
"""


def footer(*, root=False):
    links = "\n".join(f'    <a href="{h}">{t}</a>' for h, t in FOOT)
    # On the home page only: a phone that installed the app before 27 Sep 2026
    # has the site root saved as its Home Screen app. Launched from there, it
    # should open the app, not the website.
    root_js = """
  try {
    if (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone) {
      location.replace('app/' + location.hash);
    }
  } catch (e) {}""" if root else ""
    return f"""</main>

<!-- Site footer: identical on every page. -->
<footer class="site-foot">
  <div class="wrap">
    <img class="mark" src="img/sq-icon.webp" alt="" width="256" height="256" loading="lazy">
    <div class="name">Spelling Quest</div>
    <div class="tag">Follow the clue. Build the pattern. Reach the next star.</div>
    <nav class="foot-links" aria-label="Footer">
{links}
    </nav>
    <p class="mail">Questions? <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <p class="small">Made by a parent, for families. &copy; 2026 Spelling Quest</p>
  </div>
</footer>
<script>
(function () {{{root_js}
  /* This device already has Spelling Quest set up: offer the app, not a sign-in. */
  try {{
    if (localStorage.getItem('spellingQuest.v1')) {{
      document.querySelectorAll('[data-signin]').forEach(function (a) {{
        a.textContent = 'Open the app'; a.setAttribute('href', 'app/');
      }});
    }}
  }} catch (e) {{}}
}})();
</script>
</body>
</html>
"""
