from common import *

LD = [{
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Spelling Quest",
    "applicationCategory": "EducationalApplication",
    "operatingSystem": "Web browser (iPad, iPhone, Android, laptop)",
    "description": "Spelling practice built from the list your child brought home this week. It finds the patterns, builds a short daily route to test day, and brings tricky words back until they stick.",
    "url": f"{SITE}/",
    "offers": {"@type": "Offer", "price": "40.00", "priceCurrency": "USD",
               "description": "Twelve months for the whole family, every device. Seven free days first."},
}]

def page():
    return head(
        path="index.html",
        title="Spelling Quest: their teacher's words, your child's learning path",
        description="Paste the spelling list from your child's backpack. Spelling Quest finds the patterns, builds a short daily route to test day, and brings tricky words back until they stick. 7 free days.",
        extra_ld=LD,
    ) + header("index.html") + f"""
<section class="hero">
  <div class="wrap grid">
    <div>
      <p class="eyebrow">For the list in the backpack</p>
      <h1>Their teacher's words.<br><span class="hl">Your child's learning path.</span></h1>
      <p class="lede">Start with the spelling list your child brings home. Spelling Quest finds the patterns,
        practices the tricky words, and builds a short daily route to test day that your child can
        follow by themselves.</p>
      <div class="btn-row">
        <a class="btn" href="{TRIAL}">Start my 7 free days</a>
        <a class="btn-ghost" href="#how">See how it works</a>
      </div>
      <p class="reassure">Free for 7 days, then $40 a year for the whole family. No card, no account.<br>
        Already a member? <a href="signin.html" data-signin>Sign in</a></p>
    </div>
    <div class="hero-art">
      <div class="halo" aria-hidden="true"></div>
      <!-- ART SLOT home-hero: replace with the approved Scout game-map illustration (SQ Website Image Plan, H1). -->
      <img src="img/sq-badge.webp" alt="The Spelling Quest badge: a bee flying toward a gold star above a row of honeycomb letter tiles" width="720" height="720" fetchpriority="high">
    </div>
  </div>
</section>

<section class="section tight">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Sound familiar?</p>
      <h2>Spelling homework shouldn't take over <span class="hl">the whole evening.</span></h2>
    </div>
    <div class="familiar">
      <div class="glass"><div class="ico" aria-hidden="true">🕖</div><div>
        <h3>It's 7 p.m. and you're calling out words.</h3>
        <p>Again. From a crumpled list, between dinner and bath time.</p></div></div>
      <div class="glass"><div class="ico" aria-hidden="true">✍️</div><div>
        <h3>“Write each word five times.”</h3>
        <p>It fills the page. It doesn't always fill the memory.</p></div></div>
      <div class="glass"><div class="ico" aria-hidden="true">📅</div><div>
        <h3>Right on Monday. Gone by Friday.</h3>
        <p>The words were practiced. They just didn't stick until test day.</p></div></div>
      <div class="glass"><div class="ico" aria-hidden="true">🎲</div><div>
        <h3>Fun spelling apps, wrong words.</h3>
        <p>Lovely games. Just not the list your child actually has this week.</p></div></div>
    </div>
  </div>
</section>

<section class="section tight center">
  <div class="wrap narrow">
    <p class="statement">Paste the list. <span class="hl">Get the week back.</span></p>
    <p class="lede">The words come from the teacher. The practice path comes from Spelling Quest.</p>
  </div>
</section>

<section class="section" id="how">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">How it works</p>
      <h2>Three steps from backpack <span class="hl">to confident.</span></h2>
    </div>
    <div class="grid-3 steps">
      <div class="card step">
        <div class="num" aria-hidden="true">1</div>
        <h3>Paste this week's list</h3>
        <p>Any layout the teacher sent. Just the words is fine. Tell it the test day and how many
          nights your child has.</p>
      </div>
      <div class="card step">
        <div class="num" aria-hidden="true">2</div>
        <h3>It builds the route</h3>
        <p>Spelling Quest finds the patterns, splits words into chunks, writes a memory trick and spreads
          seven short stages across the nights you actually have.</p>
      </div>
      <div class="card step">
        <div class="num" aria-hidden="true">3</div>
        <h3>They play, you step back</h3>
        <p>About ten minutes a day, largely on their own. You can check what's done from your own phone,
          without being in the room.</p>
      </div>
    </div>

    <div class="card center mt-40 narrow">
      <span class="label-sm" style="color:var(--brand)">Spelling Quest notices things like this</span>
      <div class="pattern-demo" aria-label="Example words with shared letter patterns highlighted">
        <span class="tile">l<mark>igh</mark>t</span><span class="tile">n<mark>igh</mark>t</span>
        <span class="tile p2">pl<mark>ay</mark></span><span class="tile p2">st<mark>ay</mark></span>
        <span class="tile p3">r<mark>ai</mark>n</span><span class="tile p3">tr<mark>ai</mark>n</span>
      </div>
      <p class="mb-0"><b>light</b> and <b>night</b> share <b>igh</b>, <b>play</b> and <b>stay</b> share <b>ay</b>,
        and <b>rain</b> and <b>train</b> share <b>ai</b>. Connecting words through shared patterns makes the list
        feel less random, and easier to practice.</p>
      <p class="demo-caption mt-24 mb-0">Example list. Not a real child's or teacher's data.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">The quest</p>
      <h2>Seven short stages, <span class="hl">one confident speller.</span></h2>
      <p class="lede">Each stage practices the same words a different way, from first look to spelling them
        from memory. A short week never drops a stage; some nights simply get two short goes.</p>
    </div>
    <div class="stages">
      <div class="stage s1"><div class="em" aria-hidden="true">👋</div><div class="n">Stage 1</div><h3>Meet the Words</h3><p>Read them aloud and learn the pattern</p></div>
      <div class="stage s2"><div class="em" aria-hidden="true">🧩</div><div class="n">Stage 2</div><h3>Sound &amp; Build</h3><p>Hear it, build it from chunks</p></div>
      <div class="stage s3"><div class="em" aria-hidden="true">✏️</div><div class="n">Stage 3</div><h3>Missing Letters</h3><p>Fill in the gaps</p></div>
      <div class="stage s4"><div class="em" aria-hidden="true">🐝</div><div class="n">Stage 4</div><h3>Spelling Bee</h3><p>Type the whole word from memory</p></div>
      <div class="stage s5"><div class="em" aria-hidden="true">🎮</div><div class="n">Stage 5</div><h3>Arcade</h3><p>Three silly games, all spelling</p></div>
      <div class="stage s6"><div class="em" aria-hidden="true">⚔️</div><div class="n">Stage 6</div><h3>Boss Battle</h3><p>Take on the tricky words</p></div>
      <div class="stage s7"><div class="em" aria-hidden="true">🏆</div><div class="n">Stage 7</div><h3>Champion Quiz</h3><p>The big one, and a badge</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">A miss is a clue</p>
      <h2>Practice that teaches, <span class="hl">not just repeats.</span></h2>
    </div>
    <div class="compare">
      <div class="old">
        <span class="label-sm">The usual way</span>
        <h3>Drill it and hope</h3>
        <ul>
          <li>Copy each word five times</li>
          <li>The same practice for every word</li>
          <li>A wrong answer is just wrong</li>
          <li>A grown-up calls out every word</li>
        </ul>
      </div>
      <div class="new">
        <span class="label-sm">With Spelling Quest</span>
        <h3>Notice, build, remember</h3>
        <ul>
          <li>Look, say, cover, write, check, and fix only what needs fixing</li>
          <li>Words that need another look keep coming back</li>
          <li>A miss becomes a clue for what to practice next</li>
          <li>Your child follows the route by themselves</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">What's inside</p>
      <h2>Everything the week needs, <span class="hl">nothing it doesn't.</span></h2>
    </div>
    <div class="grid-3">
      <div class="card"><div class="hex" aria-hidden="true">👧</div><h3>Every child, their own words</h3>
        <p>One purchase covers the whole family. Each child gets their own list, their own stars and their own test day.</p></div>
      <div class="card"><div class="hex white" aria-hidden="true">📝</div><h3>Paper Power-Up</h3>
        <p>Every day ends with a short handwriting routine: look, say, cover, write, check. Writing by hand, done in a way that teaches.</p></div>
      <div class="card"><div class="hex violet" aria-hidden="true">🎤</div><h3>Spelling bee prep</h3>
        <p>Give it a long list and a date. It spreads the words across the weeks and practices on a stage with judges. It hints; it never spells the word for them.</p></div>
      <div class="card"><div class="hex" aria-hidden="true">📱</div><h3>Every device you own</h3>
        <p>Start on the iPad, carry on with a phone. Stars and finished days follow your family code across every device.</p></div>
      <div class="card"><div class="hex white" aria-hidden="true">🔁</div><h3>Tricky words, handled</h3>
        <p>Words that caught them out get their own Boss Battle, so practice goes where it's needed instead of the same drill for every word.</p></div>
      <div class="card"><div class="hex violet" aria-hidden="true">🛡️</div><h3>Private by design</h3>
        <p>Nicknames only, never real names. No ads, no tracking, no email address inside the app.
          <a href="privacy.html">How we handle data</a></p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="scout">
      <div class="scout-art">
        <!-- ART SLOT scout-intro: replace with the approved Scout pose (SQ Website Image Plan, H4). -->
        <div class="placeholder" role="img" aria-label="Scout the Bee">🐝</div>
      </div>
      <div>
        <p class="eyebrow plain">Meet Scout</p>
        <h2>A friendly guide, <span class="hl">not a know‑it‑all.</span></h2>
        <p class="lede">The little bee on our badge has a name, and a job: flying ahead from a brand-new list
          to a confident speller. Scout's way of seeing things runs through the whole app. A miss is a clue,
          the tricky part can be found, and every word can be figured out.</p>
        <div class="quotes" aria-label="How Scout sees it">
          <div class="quote">“Let’s see what these words have in common.”</div>
          <div class="quote">“That miss gave us a clue.”</div>
          <div class="quote">“You know more about this word than you did one minute ago.”</div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section tight">
  <div class="wrap">
    <div class="trust">
      <span>No ads</span><span>No tracking</span><span>Nicknames, never real names</span>
      <span>No leaderboards</span><span>Delete everything any time</span>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">One simple price</p>
      <h2>One purchase. <span class="hl">Every speller.</span></h2>
    </div>
    <div class="card price-card center">
      <div class="price">$40 <small>a year</small></div>
      <p class="mt-0">For the whole family, after 7 free days.</p>
      <ul class="ticks" style="text-align:left">
        <li>Every child in your household</li>
        <li>Every device you use, as many as you like</li>
        <li>All seven stages, the arcade and spelling bee prep</li>
        <li>Twelve months, summer included</li>
      </ul>
      <a class="btn" href="{TRIAL}" style="width:100%">Start my 7 free days</a>
      <p class="fine">No card, no account. If you do nothing, the free week simply ends.
        <a href="pricing.html">See pricing and bundles</a></p>
    </div>
  </div>
</section>

<section class="closing">
  <div class="wrap">
    <p class="statement">Help them think, <span class="hl">“I can figure words out.”</span></p>
    <p class="lede narrow">And give yourself the evening back.</p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn" href="{TRIAL}">Start my 7 free days</a>
      <a class="btn-ghost" href="signin.html" data-signin>Sign in</a>
    </div>
  </div>
</section>
""" + footer(root=True)
