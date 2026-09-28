import re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import p_home, p_main, p_docs
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
pages = {
  "index.html": p_home.page(), "pricing.html": p_main.pricing(), "faq.html": p_main.faq(),
  "signin.html": p_main.signin(), "about.html": p_docs.about(), "schools.html": p_docs.schools(),
  "contact.html": p_docs.contact(), "privacy.html": p_docs.privacy(), "terms.html": p_docs.terms(),
  "refunds.html": p_docs.refunds(), "404.html": p_docs.notfound(),
}
# 404 is served at any path, so every local link in it must be absolute.
def absolutize(html):
    return re.sub(r'(href|src)="(?!https?:|mailto:|#|/|data:)([^"]*)"', r'\1="/\2"', html)
pages["404.html"] = absolutize(pages["404.html"])
for name, html in pages.items():
    open(os.path.join(OUT, name), "w").write(html)
    print(name, len(html))


# ---- the same header and footer inside the app (between markers in app/index.html) ----
from common import NAV, FOOT, EMAIL
def _app_links(items, indent):
    out = []
    for h, t in items:
        href = "../" if h == "index.html" else "../" + h
        out.append(f'{indent}<a href="{href}">{t}</a>')
    return "\n".join(out)

APP_HEADER = f"""<!-- SITE-HEADER:START (written by tools/site-build/build.py; edit there) -->
<header class="sqc-head">
  <div class="sqc-wrap">
    <a class="sqc-brand" href="../" aria-label="Spelling Quest website"><img src="../img/sq-logo-horizontal.webp" alt="Spelling Quest" width="640" height="160"></a>
    <nav class="sqc-nav" aria-label="Website">
{_app_links(NAV, "      ")}
    </nav>
    <details class="sqc-menu">
      <summary aria-label="Open menu">Menu</summary>
      <div class="sqc-panel">
{_app_links(NAV + [("contact.html", "Contact")], "        ")}
      </div>
    </details>
  </div>
</header>
<!-- SITE-HEADER:END -->"""

APP_FOOTER = f"""<!-- SITE-FOOTER:START (written by tools/site-build/build.py; edit there) -->
<footer class="sqc-foot">
  <img class="sqc-mark" src="../img/sq-icon.webp" alt="" width="256" height="256" loading="lazy">
  <div class="sqc-name">Spelling Quest</div>
  <div class="sqc-tag">Follow the clue. Build the pattern. Reach the next star.</div>
  <nav class="sqc-links" aria-label="Footer">
{_app_links([x for x in FOOT if x[0] != "signin.html"], "    ")}
  </nav>
  <p>Questions? <a href="mailto:{EMAIL}">{EMAIL}</a></p>
  <p>Made by a parent, for families. &copy; 2026 Spelling Quest</p>
</footer>
<!-- SITE-FOOTER:END -->"""

import re as _re
_app = os.path.join(OUT, "app", "index.html")
_s = open(_app).read()
_s = _re.sub(r"<!-- SITE-HEADER:START.*?<!-- SITE-HEADER:END -->", lambda m: APP_HEADER, _s, flags=_re.S)
_s = _re.sub(r"<!-- SITE-FOOTER:START.*?<!-- SITE-FOOTER:END -->", lambda m: APP_FOOTER, _s, flags=_re.S)
open(_app, "w").write(_s)
print("app/index.html header+footer refreshed")
