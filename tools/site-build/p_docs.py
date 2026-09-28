from common import *


def hero(eyebrow, title_html, lede, scout=None):
    scout_img = (f'<img class="hero-scout" src="img/scout-{scout}.webp" alt="" width="560" height="560">\n    '
                 if scout else '')
    return f"""
<section class="page-hero">
  <div class="wrap">
    {scout_img}<p class="eyebrow">{eyebrow}</p>
    <h1>{title_html}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>
"""


def cta_band(line_html):
    return f"""
<section class="closing" style="padding-top:10px">
  <div class="wrap">
    <p class="statement" style="font-size:clamp(28px,4vw,42px)">{line_html}</p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn" href="{TRIAL}">Start my 7 free days</a>
      <a class="btn-ghost" href="pricing.html">See pricing</a>
    </div>
  </div>
</section>
"""


def about():
    return head(path="about.html", title="About: Spelling Quest",
                description="Spelling Quest turns the weekly spelling list into daily sprints, spread over however many nights your child actually has, so they can get on with it themselves and you get your evening back.") + header("about.html") + hero(
        "About Spelling Quest", 'Made by a parent, <span class="hl">for families.</span>',
        "Spelling Quest turns the weekly spelling list into seven short goes, about ten minutes a day, so a child can get on with it largely by themselves, and a parent gets their evening back.") + f"""
<div class="wrap">
  <section class="founder" aria-labelledby="why">
    <div class="founder-photo">
      <div class="frame"><img src="img/kathryn.webp" alt="Kathryn, founder of Spelling Quest" width="360" height="360"></div>
      <img class="founder-scout" src="img/scout-waving.webp" alt="" width="560" height="560" loading="lazy">
    </div>
    <div class="founder-story">
      <p class="eyebrow">Why I built this</p>
      <h2 id="why">It started at <span class="hl">my kitchen table.</span></h2>
      <p>Every week my kids came home with a spelling list, and every week we did the same thing. Copy the
        words out. Call them out loud. Hope they stuck until test day. It sort of worked, but it didn't feel
        like learning, and it definitely didn't feel fun, for them or for me.</p>
      <p>The spelling apps my kids enjoyed had their own word lists, so practice turned into new work on words
        that weren't even their focus that week. And the drills we did at home taught them to memorize a word
        until Friday, not to understand it. I wanted them to know <em>why</em> <b>light</b> and <b>night</b> are
        spelled the same way, so the next <b>igh</b> word they meet isn't a mystery. Learn the pattern once, and
        it keeps helping with words they haven't even seen yet.</p>
      <p>So I built something for us. Their teacher's words, nothing extra. Games that are genuinely fun but
        always practice spelling. Patterns and rules explained in plain language. And a route they can follow
        on their own, so they feel capable and proud, and I'm not the one calling out words at 7 p.m.</p>
      <p>I kept thinking about the parents I know who grew up speaking another language. Helping with English
        spelling is hard when the rules feel like a mystery to you too. Spelling Quest says each word out loud,
        shows the pattern and walks your child through it, so you can support them without having to be the
        spelling teacher.</p>
      <p>Then came the spelling bee. A list of hundreds of words is overwhelming for anyone, let alone a
        young speller. Breaking it into small groups, a few focus areas at a time, turned “I can’t learn all
        of these” into “I can do this week’s.”</p>
      <p>Spelling Quest is what my own kids practice with now. I hope it brings your family what it brought
        mine: a child who thinks <span class="hl-ink">“I can figure words out,”</span> and a calmer evening
        for everyone.</p>
      <p class="signoff">Kathryn, founder</p>
    </div>
  </section>

  <article class="card doc">
    <p class="updated">Last updated 27 September 2026</p>

    <h2>Who it is for</h2>
    <p>Children in elementary school who bring home a spelling list every week, and anyone helping them
      with it. One purchase covers every child in your family, each with their own words, their own
      stars and their own test day.</p>

    <h2>How it works</h2>
    <ul>
      <li>Paste in the list the teacher sent. Any layout; just the words is fine.</li>
      <li>The app works out the pattern, writes a memory trick, splits the words into chunks and builds
        a practice route around <b>your child's test day</b> and the number of nights they actually have.
        A Friday test works exactly like a Monday one, and four nights works as well as seven.</li>
      <li>Scout turns the list into <b>daily sprints</b>: meet the words · sound out &amp; build · missing letters ·
        spelling bee · fun spelling games · a boss battle on the tricky words · the champion quiz and a badge.
        A short week never skips any of it; some nights simply get two short sprints.</li>
      <li>Every day ends with a <b>Paper Power-Up</b>, not copying a word out five times, which mostly
        feels like a punishment. Your child looks at the word and its tricky part, writes it from memory,
        then checks it and fixes only the part that needs another look. Writing by hand is still how spelling
        sticks; this is the version that teaches while it does.</li>
    </ul>

    <h2>Spelling bees too</h2>
    <p>Give it a long list and a date. It breaks the list into small weekly groups, and the words your
      child finds tricky keep coming back, week after week, until they're confident. Words they already know
      come back for review in the last two weeks, and it practices on a stage with judges. It gives hints, but
      never spells the word for them.</p>

    <h2>It follows them between devices</h2>
    <p>Stars and finished days move with your family code, so a child can start on the iPad and carry on
      with a phone, and you can check whether the homework is done without being in the room.</p>

    <h2>Our other apps</h2>
    <p>Spelling Quest is one of three we make for families. Each one stands on its own, and if you have
      one already the others cost less.</p>
    <ul>
      <li><a href="https://oneayahatatime.github.io">One Ayah At A Time</a>: a gentle Qur'an memorization
        tracker, with a shelf and certificates for each child.</li>
      <li><a href="https://muslimkidschecklist.github.io">Muslim Kids Checklist</a>: turns the daily
        routine into something a child can run themselves.</li>
    </ul>
    <p>Already have one of them? Add Spelling Quest for <b>$25 a year</b>, or add both others for
      <b>$49</b>. Starting fresh and want all three? <b>$89 a year</b> for the whole family.
      <a href="pricing.html">See pricing</a></p>

    <h2>Try it first</h2>
    <p>Seven free days, everything unlocked, no card and no account. After that it is
      <b>$40 a year</b> for the whole family: twelve months, not just term time, so the summer
      keeps working too.</p>
  </article>
</div>
""" + cta_band('Their teacher\'s words. <span class="hl">Your child\'s learning path.</span>') + footer()


def schools():
    return head(path="schools.html", title="Schools, classrooms and tutors: Spelling Quest",
                description="Spelling Quest for classrooms, intervention groups and tutors: every child gets their own words and test day, and nothing is ranked or compared.") + header("schools.html") + hero(
        "Schools, classrooms &amp; tutors", 'The same quest, <span class="hl">for a whole group.</span>',
        "Spelling lists don't only come home in a backpack; somebody set them in the first place. The same daily-sprint route works just as well for a class, a small group, or a tutor working one-to-one.") + f"""
<div class="wrap">
  <article class="card doc">
    <p class="updated">Last updated 21 August 2026</p>
    <p>We are a small family business. This started as something we built for our own household, and
      hearing from teachers has been one of the nicest surprises since. If you are bringing this to a
      classroom, an intervention group, or a tutoring practice, we would love to hear from you.
      <a href="mailto:{EMAIL}">Write to us</a> and we will work with you directly.</p>

    <h2>How it works for a group today</h2>
    <p>Every child gets their own words, their own stars and their own test day. One child's list is
      never tangled up with another's, and nothing is ranked or compared: there is no leaderboard
      and no class scoreboard anywhere in the app.</p>
    <p>Because you paste in whichever list you already set, it fits the words you are already teaching.
      It does not ask you to adopt somebody else's curriculum, and it does not care whether your test
      day is Friday or Tuesday. A teacher can set up a shared device for a group, or point families to
      install it at home and practice there. Either way the pace stays personal.</p>

    <h2>Spelling bees</h2>
    <p>If your school runs a bee, give the app a long list and the date. It breaks the list into small
      weekly groups, and the words each child finds tricky keep coming back until they're confident. Words
      they already know come back for review near the end, and it practices on a stage with judges, including
      how to ask for a repeat, a definition, and the word in a sentence. It gives hints, but never spells the
      word for them.</p>

    <h2>What we do not have yet</h2>
    <p>We would rather be straight with you than let a page oversell it: there is no teacher
      dashboard, no way to push a list out to a whole class at once, and no way to see everyone's
      progress at a glance. What exists today is the same daily-sprint route a family uses, used by more
      people.</p>
    <p>If a class needs its own arrangement, such as more than one household on a single license or a whole
      year group, <a href="mailto:{EMAIL}">get in touch</a> and we will work it out with you, rather than make
      you guess at a pricing page.</p>

    <h2>What guides anything we build for classrooms</h2>
    <p>If we do build teacher-facing features, these are the lines we will not cross:</p>
    <ul>
      <li><b>No rankings.</b> A teacher might see that a class is practicing. Never a leaderboard of who
        is ahead.</li>
      <li><b>No child's tricky words on display.</b> The words a child finds tricky stay between
        that child and the app.</li>
      <li><b>No red flags.</b> A tricky word is a clue, not a verdict, and a quiet week is not
        something that surfaces as a warning to an adult in charge.</li>
      <li><b>Nothing travels further than it has to.</b> The app asks for a nickname, never a real name,
        and never an email address. That same care would extend to anything built for a class.</li>
    </ul>
    <p>Gentle support for a class should never become surveillance or comparison. We would rather move
      slowly and get this right than turn spelling practice into a scoreboard.</p>

    <h2>Try it with your class</h2>
    <p>Seven free days, everything unlocked, no card and no account. Set it up on as many devices as
      your group needs and see whether it fits before anyone commits to anything.</p>
  </article>
</div>
""" + cta_band('Every child\'s own words. <span class="hl">No scoreboard.</span>') + footer()


def contact():
    return head(path="contact.html", title="Contact: Spelling Quest",
                description="Get in touch with Spelling Quest. A real person reads every message, usually within a day.") + header("contact.html") + hero(
        "Contact", 'A real person <span class="hl">reads these.</span>',
        "Usually within a day, or two if it lands on a weekend.", scout="pencil") + f"""
<div class="wrap">
  <div class="grid-2" style="max-width:980px;margin:0 auto 30px">
    <div class="card">
      <div class="hex" aria-hidden="true">✉️</div>
      <h2 style="font-size:26px">Email us</h2>
      <p><a href="mailto:{EMAIL}" style="font-size:20px">{EMAIL}</a></p>
      <h3 style="font-size:18px;margin-top:18px">Worth including</h3>
      <ul class="ticks">
        <li>What device you are on: iPad, iPhone, Android tablet, laptop</li>
        <li>What you expected to happen, and what happened instead</li>
        <li>A screenshot if you can. It usually saves a whole round of questions.</li>
      </ul>
    </div>
    <div class="card">
      <div class="hex white" aria-hidden="true"><img class="ui-ic" src="img/ui/icon-tip.webp" alt="" width="160" height="160" loading="lazy"></div>
      <h2 style="font-size:26px">Before you write, two quick ones</h2>
      <h3 style="font-size:18px">The voice sounds robotic.</h3>
      <p>That is your device's basic voice, and a better one is a free download. In the app:
        <b>Grown-ups &rarr; More &rarr; Voice</b>, and it shows you exactly where to go for iPhone, iPad and Android.</p>
      <h3 style="font-size:18px">Your key isn't working.</h3>
      <p>Capitals and hyphens don't matter. If it still refuses, send the key and the email you bought
        with, and it will be sorted out.</p>
      <p class="mb-0">More answers in the <a href="faq.html">FAQ</a>.</p>
    </div>
  </div>
  <div class="glass center" style="max-width:980px;margin:0 auto 80px">
    <h3>Teaching a class or running a group?</h3>
    <p class="mb-0">There's <a href="schools.html">a page for that</a>, and we'd genuinely like to hear from you.</p>
  </div>
</div>
""" + footer()


def privacy():
    return head(path="privacy.html", title="Privacy: Spelling Quest",
                description="No accounts, no email addresses, and never your child's real name, school or birthday. How Spelling Quest handles children's data.") + header("privacy.html") + hero(
        "Privacy", 'Built for children, <span class="hl">private by design.</span>',
        "No accounts, no email addresses, and we never ask for your child's name, school or birthday.") + f"""
<div class="wrap">
  <article class="card doc">
    <p class="updated">Last updated 9 September 2026</p>
    <div class="summary-box">
      <span class="label-sm">The short version</span>
      <p>A nickname and a grade are all the app asks a child for. Progress is stored under a one-way
        fingerprint that can't be traced to a person. No ads, no analytics, no tracking. Email us and
        we'll erase everything.</p>
    </div>
    <nav class="jump" aria-label="On this page">
      <a href="#asks">What we ask</a><a href="#stored">What is stored</a><a href="#never">Never collected</a>
      <a href="#email">Your email</a><a href="#delete">Deleting</a><a href="#children">Children's privacy</a>
    </nav>

    <h2 id="asks">What the app asks a child for</h2>
    <p>A nickname and a school grade. That's it. The nickname doesn't have to be a real name and the app
      suggests it isn't one. There is no sign-up, no password and no profile.</p>

    <h2 id="stored">What is stored, and where</h2>
    <p>So that progress can follow your family between devices, this much is kept on a server:</p>
    <ul>
      <li>The nickname, and the grade, test day and avatar you chose</li>
      <li>Stars, streak and badges</li>
      <li>Which days are finished</li>
      <li>The word list you pasted in</li>
    </ul>
    <p>Which words your child found tricky is worked out on their device and never sent anywhere.</p>
    <p>It is filed under a fingerprint of your family code: a one-way scramble that cannot be
      turned back into the code. There is no name, no email and no address attached to it, so the records
      cannot be traced to a person.</p>

    <h2 id="never">What is never collected</h2>
    <p>Email addresses inside the app, real names, birthdays, schools, locations, photos, contacts, or
      anything about a child's device. There is no advertising, no analytics and no third-party tracking
      of any kind.</p>

    <h2 id="email">Your email, when you buy</h2>
    <p>If you buy, Gumroad collects your email to send your key and receipt, and I may email
      you about the app. That is a parent's address, given by a parent, never a child's. You can
      unsubscribe from any of those emails.</p>

    <h2 id="delete">Removing a child, and deleting for good</h2>
    <p>Removing a child in <b>Grown-ups &rarr; Kids</b> takes them out of the app on every device in your
      family, and it can't be undone from inside the app. On the server their record is marked as removed
      rather than wiped: the nickname, word list and progress stay in place, unused, so that a child
      removed by mistake can be put back by hand.</p>
    <p>If you want it gone for good, one child or your whole family, email
      <a href="mailto:{EMAIL}">{EMAIL}</a> and I'll erase it and confirm.</p>

    <h2 id="children">Children's privacy</h2>
    <p>The app is designed so that a child cannot hand over personal information even if they try:
      there is nowhere to type it. Parents buy, parents set it up. If you believe any personal information
      about a child has reached me, write to me and I will delete it.</p>
  </article>
</div>
""" + footer()


def terms():
    return head(path="terms.html", title="Terms: Spelling Quest",
                description="Plain-English terms for Spelling Quest: what you're buying, what it costs, the free week and fair use.") + header("terms.html") + hero(
        "Terms", 'Plain English, <span class="hl">no lawyer needed.</span>',
        "You shouldn't need a lawyer to buy a spelling app.") + f"""
<div class="wrap">
  <article class="card doc">
    <p class="updated">Last updated 17 August 2026</p>
    <nav class="jump" aria-label="On this page">
      <a href="#buying">What you're buying</a><a href="#costs">What it costs</a><a href="#free">The free week</a>
      <a href="#fair">Fair use</a><a href="#promise">What I can promise</a><a href="#payments">Payments</a>
    </nav>

    <h2 id="buying">What you're buying</h2>
    <p>Access to Spelling Quest for twelve months, for everyone in your household: every child, and
      <b>as many devices as your family actually uses</b>. The iPad, the phone in your bag, the old tablet
      in the kitchen. We don't count them.</p>

    <h2 id="costs">What it costs</h2>
    <ul>
      <li><b>$40 a year</b> for Spelling Quest.</li>
      <li><b>$25</b> to add it if you already have One Ayah At A Time or Muslim Kids Checklist.</li>
      <li><b>$49</b> to add the other two if you already have one of them.</li>
      <li><b>$89</b> for all three, if you do not have any of them yet.</li>
    </ul>
    <p>It renews once a year on its own until you cancel. You can cancel any time from the shop, and
      you keep full access until the end of the year you have paid for.</p>

    <h2 id="free">The free week</h2>
    <p>Seven days, everything unlocked, no card and no account. Nothing to cancel: if you do nothing,
      it simply stops.</p>

    <h2 id="fair">Fair use</h2>
    <p>One household, one key. Please don't post it publicly or pass it round a class; keys that turn up
      in public get switched off. We'd rather trust you than count your devices.</p>

    <h2 id="promise">What I can and can't promise</h2>
    <p>I'll keep it working and fix things when they break. I can't promise it will never be
      unavailable, and I can't promise a particular result in a spelling test. It's practice, not magic.
      Nothing here takes away rights you have under the consumer law where you live.</p>

    <h2 id="payments">Payments</h2>
    <p>Payments are handled by <b>Gumroad</b>, who are the merchant of record. They take care of
      card details and sales tax, and their name is what appears on your statement.</p>
  </article>
</div>
""" + footer()


def refunds():
    return head(path="refunds.html", title="Refunds: Spelling Quest",
                description="Spelling Quest's refund policy: a free week first, refunds for renewals you didn't mean to pay and for anything that won't work.") + header("refunds.html") + hero(
        "Refunds", 'Fair, <span class="hl">and in plain words.</span>',
        "There's a free week, fully unlocked, with no card, so you can find out whether your child will actually use this before any money changes hands.") + f"""
<div class="wrap">
  <article class="card doc">
    <p class="updated">Last updated 17 August 2026</p>
    <div class="summary-box">
      <span class="label-sm">The short version</span>
      <p>Use the free week to decide. After that, a renewal you meant to cancel, or an app that won't work
        for you, gets refunded. Cancelling never cuts off early.</p>
    </div>

    <h2>The policy</h2>
    <p>Because there is a full seven-day free trial before any money changes
      hands, I don't generally refund a purchase after the fact; that's what the free week is for.</p>
    <p>Two exceptions, and I mean them:</p>
    <ul>
      <li><b>A renewal you didn't mean to pay.</b> If you meant to cancel and it slipped past you, tell me
        and I'll refund it.</li>
      <li><b>Something is broken.</b> If the app won't work for you and I can't fix it, I refund you in
        full, whenever that happens. I would rather sort the problem than keep money from someone who
        couldn't use the thing.</li>
    </ul>
    <p>Refunds go back to the card or account you paid with, through Gumroad, and usually appear within
      a few business days.</p>
    <p>Nothing on this page limits any stronger consumer rights you may have where you live.</p>

    <h2>If you cancel</h2>
    <p>You keep full access until the <b>end of the twelve months you have already paid for</b>. Nothing
      cuts off early, and cancelling only means "don't bill me again."</p>
    <p>The app checks your key quietly about once a month, so nothing happens the instant anything
      changes. If the check can't reach the internet at all, your child carries on regardless. A
      network problem has never been a reason to lock a family out.</p>
    <p>Cancel any time from the link in your purchase email. You don't have to ask me.</p>

    <h2>Charged twice, or something odd</h2>
    <p>Write to <a href="mailto:{EMAIL}">{EMAIL}</a> with the receipt and
      I'll refund the duplicate the same day I see it.</p>
  </article>
</div>
""" + footer()


def notfound():
    return head(path="404.html", title="Page not found: Spelling Quest",
                description="That page wandered off.", noindex=True) + header("") + f"""
<section class="closing">
  <div class="wrap">
    <img class="hero-scout" src="img/scout-thinking.webp" alt="" width="560" height="560">
    <p class="statement">That page <span class="hl">flew off.</span></p>
    <p class="lede">Let's get you back on the path.</p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn" href="/">Go to the home page</a>
      <a class="btn-ghost" href="/app/">Open the app</a>
    </div>
  </div>
</section>
""" + footer()
