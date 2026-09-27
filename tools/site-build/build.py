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
