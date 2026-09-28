from common import *


def pricing():
    ld = [{
        "@context": "https://schema.org", "@type": "Product", "name": "Spelling Quest family access",
        "description": "Twelve months of Spelling Quest for every child in the household, on every device.",
        "brand": {"@type": "Brand", "name": "Spelling Quest"},
        "offers": {"@type": "Offer", "price": "40.00", "priceCurrency": "USD", "url": CHECKOUT,
                   "availability": "https://schema.org/InStock"},
    }]
    return head(path="pricing.html", title="Pricing: Spelling Quest",
                description="Seven free days with everything unlocked, no card and no account. Then $40 a year for every child in your family, on every device.",
                extra_ld=ld) + header("pricing.html") + f"""
<section class="hero">
  <div class="wrap grid">
    <div>
      <p class="eyebrow">7 free days</p>
      <h1>One purchase.<br><span class="hl">Every speller.</span></h1>
      <p class="lede">Try every sprint, every game and spelling bee prep for a full week before you spend
        anything. If it earns its place at your kitchen table, one price covers the whole family for
        twelve months.</p>
      <p class="note">The twelve months are twelve months, not a school year, so spelling bee season and
        summer practice keep working too.</p>
      <img class="side-scout" src="img/scout-cheering.webp" alt="" width="560" height="560">
    </div>
    <div class="card price-card">
      <span class="label-sm" style="color:var(--brand)">Family access</span>
      <div class="price">$40 <small>a year</small></div>
      <p class="mt-0">After your 7 free days. Renews yearly; cancel any time.</p>
      <ul class="ticks">
        <li><b>Every child</b> in your household, each with their own words and test day</li>
        <li><b>Every device</b> you use: the iPad, the phone, the old tablet. We don't count them</li>
        <li>Every daily sprint, fun spelling games and <b>spelling bee prep</b></li>
        <li>Progress that follows your family across devices</li>
      </ul>
      <div class="includes">
        <span class="label-sm">Your free week includes</span>
        <p>Everything unlocked. No card, no account, nothing to cancel.</p>
      </div>
      <a class="btn" href="{TRIAL}" style="width:100%">Start my 7 free days</a>
      <p class="fine center">Already know it's for you? <a href="{CHECKOUT}" rel="noopener">Buy a year now</a><br>
        Already a member? <a href="signin.html" data-signin>Sign in</a></p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Our family of apps</p>
      <h2>Already have one of <span class="hl">our other apps?</span></h2>
      <p class="lede">Spelling Quest is one of three apps we make for families. Each stands on its own,
        and if you already have one, the others cost less.</p>
    </div>
    <div class="grid-3">
      <div class="card offer">
        <span class="label-sm" style="color:var(--brand)">Add Spelling Quest</span>
        <div class="price" style="font-size:44px">$25 <small>a year</small></div>
        <p>You already have One Ayah At A Time or Muslim Kids Checklist.</p>
        <a class="btn-purple" href="{CHECKOUT_ADDON}" rel="noopener" style="width:100%">Add Spelling Quest</a>
      </div>
      <div class="card offer">
        <span class="label-sm" style="color:var(--brand)">Add the other two</span>
        <div class="price" style="font-size:44px">$49 <small>a year</small></div>
        <p>You already have one of our apps and want the other two.</p>
        <a class="btn-purple" href="{CHECKOUT_TWO}" rel="noopener" style="width:100%">Add both</a>
      </div>
      <div class="card offer">
        <span class="label-sm" style="color:var(--brand)">All three apps</span>
        <div class="price" style="font-size:44px">$89 <small>a year</small></div>
        <p>Starting fresh with Spelling Quest, One Ayah At A Time and Muslim Kids Checklist.</p>
        <a class="btn-purple" href="{CHECKOUT_THREE}" rel="noopener" style="width:100%">Get all three</a>
      </div>
    </div>
    <p class="note center mt-24">Meet the other two: <a href="https://oneayahatatime.github.io">One Ayah At A Time</a>,
      a gentle Qur'an memorization tracker, and <a href="https://muslimkidschecklist.github.io">Muslim Kids Checklist</a>,
      which turns the daily routine into something a child can run themselves.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">The small print, in plain words</p>
      <h2>No surprises.</h2>
    </div>
    <div class="grid-2" style="max-width:820px;margin:0 auto">
      <div class="glass"><h3>Renewal</h3><p>It renews once a year until you cancel. Cancel any time from
        the link in your purchase email; you keep full access to the end of the year you paid for.</p></div>
      <div class="glass"><h3>Checkout</h3><p>Payments go through Gumroad, who handle card details and sales
        tax. Your key arrives by email and works on every device.</p></div>
    </div>
    <p class="note center mt-24">Teaching a class or a group? <a href="schools.html">There's a page for that.</a>
      More questions? <a href="faq.html">Read the FAQ.</a></p>
  </div>
</section>

<section class="closing">
  <div class="wrap">
    <p class="statement">Try the whole quest. <span class="hl">Decide later.</span></p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn" href="{TRIAL}">Start my 7 free days</a>
    </div>
  </div>
</section>
""" + footer()


FAQ = [
    ("🚀", "Getting started", [
        ("What do I need to start?",
         "<p>This week's spelling list and a few minutes. Open Spelling Quest on any device with a web browser, "
         "tap <b>Begin my 7 free days</b>, add your child's nickname, and paste in the list. There's nothing to install "
         "and no account to create.</p>"),
        ("Which devices does it work on?",
         "<p>iPad, iPhone, Android phones and tablets, and laptops, in the web browser. On an iPad or iPhone you can "
         "add it to your Home Screen (Safari &rarr; Share &rarr; <b>Add to Home Screen</b>) so it opens full-screen "
         "like any other app.</p>"),
        ("Does it work offline?",
         "<p>Yes. Once it has loaded, practice keeps working without the internet. Progress catches up with your "
         "other devices the next time you're online.</p>"),
        ("What grades is it for?",
         "<p>Kindergarten through fifth grade: children who bring home a weekly spelling list. It adapts to the words "
         "you paste in, so it grows with them.</p>"),
    ]),
    ("📝", "The words", [
        ("What if the teacher's list is in a strange layout?",
         "<p>Paste it as it is. Any layout works, and just the words is fine.</p>"),
        ("Does my child need to practice every day of the week?",
         "<p>No. You tell Scout the test day, and the list becomes daily sprints across the nights before it. A short "
         "week never skips any of the practice; some nights simply get two short sprints. Every sprint stays open, "
         "so a child who misses a night can catch up whenever they like.</p>"),
        ("Can it help with a spelling bee?",
         "<p>Yes. Give it the long list and the date. It breaks the list into small weekly groups, and the words "
         "your child finds tricky keep coming back, week after week, until they're confident. Words they already "
         "know come back for a quick review near the end. Then it practices on a stage with judges, including how "
         "to ask for a repeat, a definition or a sentence. It gives hints, but never spells the word for them.</p>"),
        ("What is the Paper Power-Up?",
         "<p>Every day ends with a quick pencil-and-paper challenge instead of copying words out five times. Your "
         "child looks at the word and its tricky part, writes it from memory, then checks it and fixes only the "
         "part that needs another look.</p>"),
    ]),
    ("👧", "Children and progress", [
        ("I have more than one child. Do I need to buy it twice?",
         "<p>No. One purchase covers every child in your household. Each child gets their own words, their own "
         "stars and their own test day.</p>"),
        ("Will my children be compared with each other?",
         "<p>Never. There are no leaderboards, no rankings and no side-by-side scores. Each child only ever sees "
         "their own progress.</p>"),
        ("What happens when my child gets a word wrong?",
         "<p>A miss is a clue, not a verdict. Words your child finds tricky get extra practice in the Boss Battle, "
         "so time goes where it's needed, and you'll see them in the Grown-up Zone under "
         "<b>Words to revisit</b>.</p>"),
        ("Can I check my child's progress from my phone?",
         "<p>Yes. Open the Grown-up Zone (behind a grown-up PIN) on any of your devices to see which sprints each child "
         "has finished this week, their stars and streak, the words to revisit, earlier weeks and spelling bee progress. "
         "Progress follows your family across devices once you unlock with your key.</p>"),
        ("The voice sounds robotic. Can I fix it?",
         "<p>That's your device's basic built-in voice, and a better one is a free download. In the app, go to "
         "<b>Grown-ups &rarr; More &rarr; Voice</b> and it shows you exactly where to get one on iPhone, iPad and Android.</p>"),
    ]),
    ("💳", "Paying and your key", [
        ("How much is it?",
         "<p>Seven free days first, then <b>$40 a year</b> for the whole family, on every device. If you already "
         "have One Ayah At A Time or Muslim Kids Checklist, it's $25. <a href=\"pricing.html\">See all prices</a></p>"),
        ("Do I need a card for the free week?",
         "<p>No card and no account. If you do nothing, the free week simply ends. There's nothing to cancel.</p>"),
        ("How do I sign in on another device?",
         "<p>Use the key from your purchase email. Go to <a href=\"signin.html\">Sign in</a>, paste the key, and "
         "your family's progress follows you. It works on as many devices as your family uses.</p>"),
        ("My key isn't working.",
         "<p>Capitals and hyphens don't matter. If it still refuses, email "
         f"<a href=\"mailto:{EMAIL}\">{EMAIL}</a> with the key and the email you bought with, and it will be sorted out.</p>"),
        ("How do I cancel?",
         "<p>From the link in your purchase email, any time. You keep full access until the end of the twelve "
         "months you paid for. <a href=\"refunds.html\">Refund policy</a></p>"),
    ]),
    ("🔒", "Privacy", [
        ("What do you know about my child?",
         "<p>A nickname and a school grade. The nickname doesn't have to be a real name, and the app suggests it "
         "isn't one. No real names, birthdays, schools, photos or email addresses, ever.</p>"),
        ("Where is progress stored?",
         "<p>So progress can follow your family between devices, stars, finished days, the word list and the "
         "settings you chose are stored under a one-way fingerprint of your family code. It can't be traced back "
         "to a person. <a href=\"privacy.html\">Read the privacy page</a></p>"),
        ("Are there ads or tracking?",
         "<p>No advertising, no analytics and no third-party tracking of any kind.</p>"),
        ("Can I delete everything?",
         f"<p>Yes. Email <a href=\"mailto:{EMAIL}\">{EMAIL}</a> and one child, or your whole family, will be "
         "erased and you'll get a confirmation.</p>"),
    ]),
]


def faq():
    import re
    ld = [{
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a).replace("&rarr;", "→")}}
                       for _, _, qs in FAQ for q, a in qs],
    }]
    groups = ""
    for ico, name, qs in FAQ:
        items = "\n".join(f"""    <details class="q"><summary>{q}</summary><div class="a">{a}</div></details>""" for q, a in qs)
        groups += f"""
  <div class="faq-group">
    <h2><span class="hex" aria-hidden="true">{ico}</span>{name}</h2>
{items}
  </div>
"""
    return head(path="faq.html", title="Questions and answers: Spelling Quest",
                description="How Spelling Quest works, which devices it runs on, what it costs, and how it looks after your child's privacy.",
                extra_ld=ld) + header("faq.html") + f"""
<section class="page-hero">
  <div class="wrap">
    <img class="hero-scout" src="img/scout-thinking.webp" alt="" width="560" height="560">
    <p class="eyebrow">FAQ</p>
    <h1>Questions, <span class="hl">answered.</span></h1>
    <p class="lede">Short answers to what parents ask most. Can't find yours?
      <a href="contact.html">Write to us</a>. A real person reads every message.</p>
  </div>
</section>
<section class="section tight" style="padding-top:10px">
  <div class="wrap">{groups}
  </div>
</section>
<section class="closing" style="padding-top:30px">
  <div class="wrap">
    <p class="statement">The best answer is <span class="hl">a free week.</span></p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn" href="{TRIAL}">Start my 7 free days</a>
      <a class="btn-ghost" href="pricing.html">See pricing</a>
    </div>
  </div>
</section>
""" + footer()


def signin():
    return head(path="signin.html", title="Sign in: Spelling Quest",
                description="Open your family's Spelling Quest on any device with the key from your purchase email.",
                noindex=True) + header("signin.html") + f"""
<div class="wrap">
  <div class="signin-grid">
    <div class="signin-art">
      <!-- S1 stand-in: Scout pose 01, pointing toward the form. Swap for the honeycomb-door art if it's made. -->
      <img src="img/scout-pointing.webp" alt="Scout the Bee pointing to the sign-in box" width="560" height="560">
      <h1 style="font-size:clamp(30px,4vw,44px)">Your quest is <span class="hl">right where you left it.</span></h1>
      <p class="lede" style="max-width:440px;margin-left:auto;margin-right:auto">Stars, finished days and this week's
        words follow your family onto every device.</p>
    </div>

    <div class="card signin-card">
      <span class="label-sm" style="color:var(--brand)">Welcome back</span>
      <h2 style="font-size:30px;margin-bottom:6px">Pick up where you left off</h2>
      <p>Paste the key from your purchase email, or the access code you were given. No email address or
        password needed.</p>
      <form id="signin" autocomplete="off" novalidate>
        <label class="field" for="key">Your key or code</label>
        <input class="input" id="key" name="key" type="text" inputmode="text" autocapitalize="characters"
          spellcheck="false" placeholder="Paste your key or code" required>
        <button class="btn" type="submit">Open our quest</button>
        <p class="msg" id="msg" role="status" aria-live="polite"></p>
      </form>
      <p class="fine center">Capitals and hyphens don't matter. Lost your key? It's in your Gumroad receipt email,
        or <a href="contact.html">write to us</a>.</p>

      <div class="or">New to Spelling Quest?</div>
      <a class="btn-outline-ink" href="{TRIAL}">Start 7 free days</a>
      <p class="fine center">No card, no account. <a href="index.html">What is Spelling Quest?</a></p>
      <p class="fine center" id="already" hidden>This device is already set up. <a href="app/">Open the app</a></p>
    </div>
  </div>
</div>
<script>
(function () {{
  var f = document.getElementById('signin'), k = document.getElementById('key'), m = document.getElementById('msg');
  try {{ if (localStorage.getItem('spellingQuest.v1')) document.getElementById('already').hidden = false; }} catch (e) {{}}
  f.addEventListener('submit', function (e) {{
    e.preventDefault();
    var v = (k.value || '').trim();
    if (!v) {{ m.textContent = 'Paste your key or code first.'; k.focus(); return; }}
    m.textContent = 'Opening your quest…';
    /* The key goes to the app in the #hash, which browsers never send to a server.
       The app checks it exactly as its own key box does. */
    location.href = 'app/#key=' + encodeURIComponent(v);
  }});
}})();
</script>
""" + footer()
