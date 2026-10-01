# Spelling Bee games: new artwork for ChatGPT

Spelling Quest's bee screen now has four games, and Bug Bop uses 20 bug pictures. Each game card shows an emoji until its icon file is uploaded. When a file with the exact name below goes into `img/ui/`, the app picks it up on its own, with no code change.

## How to use this
1. Paste the **style prompt** into ChatGPT once at the start of a new chat.
2. Then paste each **item prompt** one at a time, so you get one image per message.
3. Save each image with the file name shown, as a square PNG with a transparent background.
4. Send me the images and I'll convert them to the app's format (160×160 WebP) and upload them. Or upload them to `img/ui/` yourself as `.webp`.

---

## Style prompt (paste first)

> I'm making icons for a children's spelling app called Spelling Quest. Its mascot is Scout, a friendly cartoon bee. Please match this style exactly for every icon I ask for:
>
> - Glossy cartoon "sticker" icon with a thick dark navy outline (#2b2350) around every shape
> - Soft gradients and one bright highlight, like a shiny sticker
> - Main colours: honey gold (#ffc93c), warm yellow (#ffe08a), soft purple (#7c5cff and #c9a7ff), with pink (#ff9ec7), sky blue (#7cc8ff) and mint green (#8fe3a3) as accents
> - One simple object, centred, filling about 85% of the square, readable at 56 pixels
> - Transparent background, no shadow on the ground, no frame, no text or letters anywhere
> - Friendly and calm for ages 5 to 11, nothing scary
> - Square, 1024 × 1024
>
> Reply "ready" and I'll send the icons one at a time.

---

## Needed now: the four game icons

### 1. Spin & Spell: `icon-spin-spell`
> A round prize wheel seen from the front, with 8 slices in honey gold, pink, sky blue, mint green and purple. Each slice has a simple pattern (stripes, polka dots, zigzag, checks, waves). It has a small navy pointer triangle at the top and a tiny bee in the centre hub. No pictures, letters or numbers on the slices.

### 2. Save the Flower: `icon-thirsty-flower`
> A droopy, slightly wilted sunflower in a small terracotta pot. Its head tilts down and its petals are a little faded. Beside it, a small sky-blue watering can is tipped toward it, with three water drops falling. The flower should look thirsty but hopeful, with a small worried face, never sad or dead.

### 3. Memory Match: `icon-memory-match`
> A sky-blue card with a purple speaker horn on it, next to a playing card that is face down, honey gold with a small cartoon bee on it. The two cards lean together like a pair.

### 4. Bug Bop: `icon-bug-bop`
> A cheerful red ladybug on a small patch of green grass, holding up a small blank white sign. A soft purple toy mallet hovers above, about to give it a gentle "bop", with little star sparkles. Playful, not violent.

---

## Needed now: 20 bugs for Bug Bop

In Bug Bop, each bug crawls around its card and turns to face the way it's walking. So these must all be drawn **from directly above (top-down), with the head pointing straight up** to the top of the picture. Save each one as `bug-<name>` (for example `bug-ladybug`). Until a bug's file is uploaded, the game shows an emoji in its place.

Add this to each bug prompt:
> Draw it from directly above, top-down view, head pointing straight up to the top of the image, legs visible on both sides, centred, filling about 80% of the square. Cute, round and friendly with big shiny eyes, never creepy. Same sticker style as before, transparent background, no text.

| File name | Prompt |
|---|---|
| `bug-ladybug` | A round red ladybug with black spots |
| `bug-caterpillar` | A plump green caterpillar with soft yellow stripes |
| `bug-grasshopper` | A bright green grasshopper with long back legs |
| `bug-ant` | A friendly red-brown ant |
| `bug-stag-beetle` | A shiny dark-blue stag beetle with small rounded pincers |
| `bug-snail` | A snail with a swirly pink-and-gold shell |
| `bug-butterfly` | A butterfly with purple and gold wings, open flat |
| `bug-dragonfly` | A dragonfly with see-through sky-blue wings, open flat |
| `bug-firefly` | A firefly with a softly glowing yellow tail |
| `bug-cricket` | A brown cricket with long antennae |
| `bug-inchworm` | A tiny lime-green inchworm, gently curved |
| `bug-roly-poly` | A grey-blue roly-poly (pill bug) with banded segments |
| `bug-bumblebee` | A fuzzy round bumblebee with black and orange stripes. It must look different from Scout, so no gold, no sparkles |
| `bug-moth` | A soft cream moth with fluffy antennae and brown wing spots |
| `bug-praying-mantis` | A green praying mantis with folded arms, cute not scary |
| `bug-cicada` | A green-and-brown cicada with clear veined wings |
| `bug-jewel-beetle` | A beetle with a shiny rainbow-green shell |
| `bug-weevil` | A little brown weevil with a long nose |
| `bug-water-strider` | A slim water strider with long thin legs spread out |
| `bug-katydid` | A leaf-green katydid shaped a bit like a leaf |

---

## Optional extras (only if you'd like them later)

These would need a small code change to use. Tell me if you make them.

### Badges, to match the existing badge style: round patch with a purple border
Save as `badge-<name>`:
- `badge-green-thumb`: a sunflower in full bloom in a pot, with sparkles (for bringing the flower to full bloom)
- `badge-bug-bopper`: the ladybug from Bug Bop wearing a tiny gold crown (for bopping every word)
- `badge-memory-master`: two matching cards with a gold star between them (for all pairs with no extra tries)
- `badge-wheel-whiz`: the patterned prize wheel with a gold ribbon (for spinning every word on today's list)

Add this line for badges:
> Make it a round badge patch: a circle with a thick purple (#7c5cff) border and a white inner ring, with the object inside on a soft pale-yellow background.

### Flower growth set for Save the Flower
The game draws its own flower now. If you'd prefer hand-drawn art, make five pictures of the **same** sunflower in the **same** pot, from the same angle. Name them `flower-stage-0` to `flower-stage-4`:
- 0: wilted, head hanging down, faded brownish petals
- 1: starting to lift, a little colour back
- 2: halfway up, mostly yellow
- 3: almost upright, bright yellow, a small smile
- 4: full bloom, upright, big smile, sparkles and a tiny bee visiting

> Keep the pot, the angle and the size identical in all five, so they line up when swapped.
