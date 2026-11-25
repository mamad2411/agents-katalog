---
name: taste-brief
description: >-
  Doctrine « anti-slop » de tasteskill 2.5 (Leonxlnx, MIT), partie savoir uniquement, sans
  script : règles de maison, plan de page par type de commerce, liste des « jamais ». Utiliser en
  Cowork/chat pour rédiger un brief de site vitrine, relire une maquette ou une page, ou juger si
  une page a l'air « faite par une IA ». L'exécution (construction, vérification navigateur) se
  fait dans Claude Code avec le skill taste-cockpit.
---

# taste-brief — la doctrine, sans l'outillage

Extrait fidèle du skill tasteskill 2.5 (Leon Lin, MIT). Aucun script ici : ce fichier sert à
**penser et juger** une page vitrine. Pour construire et vérifier, le skill `taste-cockpit`
(Claude Code) applique les mêmes règles avec devis et GO humain.

La barre : figma.com et x.ai — une page qui dit ce qu'elle vend, montre la vraie chose à chaque
écran, et a l'air faite pour ce client, ni d'un gabarit ni d'une œuvre d'art.

## House rules

These nine win over everything else in this skill.

1. **No caption or description under any image, render or visual.** Licence credits go in one
   footer line.
2. **Every visual renders, never an empty ground,** at 1440, 1024, 768 and 390.
3. **One section per screen:** the hero alone on the first screen, every section exactly one or
   two screens tall at 1440x900, no second section heading peeking in. The one exception is a
   live `photo-chapters` section, three or four screens, set by the moment.
4. **Equal left and right content edges.**
5. **Hover micro-animations:** a linked card lifts 2px, a photo zooms 1.02-1.03 inside its frame,
   buttons step on hover and press on click, underlines draw, card loops cycle in 2.5-4 s, repeat
   and restart on hover. The motion layer does it; never strip or override it. No tilt, carousels
   or timed tabs. Every hero enters once on load (`data-enter`), and every page carries one dealt
   moment, two on a long page (the gate holds both).
6. **More and better real photographs where they fit;** nicer backgrounds; better heroes, layouts
   and fonts.
7. **Real full-colour icons** (a known product's real icon, never a drawn one); small diagram
   visuals in cards (a hub with branches; one input, a main processor, three parallel lanes;
   pulses running along the lines).
8. **The big award-site scenes and creative moments are part of the skill:** every page deals its
   moments (photo- and type-led off tech), but shader effects and scenes only where the trade has a
   technical subject (tech, AI, developer tools, gaming, fintech, hardware), never on a local cafe,
   bakery, guesthouse or shop: those get photographs.
9. **Addresses:** street and district only (no street given: the district), no house number, postcode or coordinates; no register
   or VAT numbers; no phone in a real format; contacts on `.example`.

## 1. The kind of business decides everything

Write the kind on the plan's first line and declare it on the page: the page type on
`<html data-type>` and `<meta name="page-type">` (the same value), and `<meta name="site-kind">`;
a place adds `<meta name="page-kind" content="place">`. The dealers take the last column
((outil Claude Code), (outil Claude Code)), the hero dealer the page type; (outil Claude Code) reads
the metas.

| Brief | page type | site-kind | kind |
|---|---|---|---|
| App, SaaS, AI, developer tool, fintech or banking app, a studio selling its own software | software | software | software |
| A game, a studio launching its game | software | gaming | gaming |
| Hardware or a tech device (a drone, a robot arm, a keyboard) | product | tech | tech |
| Any other physical product or brand (a chair, a bike, coffee beans sold online) | product | other | product |
| People are hired: clinic, law firm, agency, creative studio, trade | service | other | service |
| People come to it: cafe, bar, bakery, restaurant, guesthouse, small hotel, shop, florist, bike shop, gym, local studio | place | other | place |

A maker that also opens its door or teaches (a ceramics studio, a bakery with a web shop) is a
**place**; its web shop becomes the goods section. It is a product only when nothing happens at the door.

"Tech" below means site-kind software, gaming or tech; "other" is everything else. Effects,
scenes, loops, counts, CSS grounds, dark pages and dark heroes are tech only. An other page is
photographs, flat colour, type, real icons, the hero's entrance, its dealt moment (photo- or
type-led, `moments.md`) and the hover layer.

## 2. The page plan by kind

The full plans, deal lists and section order: `references/sections.md`.

- **Place** (a cafe, bakery, guesthouse, shop). Photographs lead: 12 to 20 on the full page, 8 to
  12 compact, under 8 frames the 3-screen short page, whatever the trade; no client photographs:
  the draft path and a live search (`photos.md`), then count; the palette dealt by trade. The hero
  a photograph whenever a frame fits (a remote place: its region's landscape), the visit block on
  screen two, the offer, the place, orders or booking.
  **Variety without effects** (`sections.md` section 4): the offer and the place deal different
  compositions, never two sections round one picture; one type moment (the address or name set large); one main action a screen; list text 16px. Flat grounds, square
  photographs, one button style, the phone bar, the dealt moments; no effect, ground, loop,
  fragment, diagram or tab.
- **Product and service** (site-kind other). Photographs lead: the product, the people, the rooms,
  the work, two or more a screen on a product page. Real icons for the tools a studio uses; one
  still diagram at most; flat grounds and one brand band. No shader effect, print, grain, gradient,
  scene or loop (the dealt moments only); WebGL only for a product render the brief asks for. **A
  physical product with no photographs is shown in photographs:** stand-ins of the same kind of
  thing from (outil Claude Code), each listed in the report, on the full product page; a render
  (`assets/objects/product-render`, stills) only when the brief asks for 3D or a render; never a
  drawing, mood stock or a set of props (`sections.md`, Product).
- **Every product page** (photographed, in stand-ins or rendered on a 3D ask, hardware too; the bar is Figure and 1X;
  `sections.md`, Product): the product **big** where it stands
  whole (most of its frame, or on the ground at anchor scale), never mid-size in a grey rounded
  panel on a grey ground; **a different picture each section**, never one view twice; **every headline promise pictured** (a family bike shows the child bench); dealt
  compositions, no structure twice, one contrasting ground; the **swatch changes the picture**,
  every colour shown once; **no fact twice**; buttons step and press (rule 5).
- **Tech** (software, gaming, hardware). The client's own subject leads at true size. Software: its
  own UI as live HTML showing what it works on (a code-review tool: a red and green diff with its
  Accept action) in one `app-frame`, never a generic dashboard or only fragments on panels; cards:
  fragments on lit panels, pulsing diagrams, real icons. Hardware: its photographs, else stand-in
  photographs of its kind (a render only when the brief asks for 3D), never a split hero of only
  an order form or a drawn SVG. A game: its name in the h1, a launch line, its world as full-bleed
  key art (else its name set large over stand-in photographs of its setting), an effect never in
  its place (`sections.md`, Gaming). **60 to 80 words a screen** outside UI mocks (`copy.md`). By
  deal: **one effect** (a shader ground in the hero or the one `[data-visual]` frame, a WebGL
  part, an object or one big scene) and **one or two moments** in their own sections; four live
  WebGL contexts at most; no card moves with the scroll (`effects-usage.md`).
- **One object never carries the page.** The product or hero object whole leads the hero and **two more sections at
  most**; another kind of visual the brief supports carries the rest (`sections.md` section 1,
  its table): a game's world and crew; hardware's use at the bench, its parts close up; a still
  diagram card, a type moment, a context photograph where the trade allows.
- **The client's own assets get slots.** A trailer, key art, screenshots, CAD renders or a motion
  video the brief names each get a frame that reads finished now (a real `<video>` with a stand-in
  poster, a play control only when there is a page or file to play, three to five stand-in
  photographs of the world, a CAD frame), named in a comment for the client's file, never empty
  (`sections-library.md`, client-slots).

## 6. Never

- A card, row or tile that fades in on scroll; a fade-in on every section; parallax on text;
  scroll-jacking; random blinking.
- Stock photographs passed off as the client's product, people or place (a stand-in is listed in
  the report as one, never shown with another maker's name or logo); a product page that never
  shows the product.
- A drawn look-alike of a real logo; invented reviews, quotes, customers or figures.
- Violet or lavender in the page's own design: accent, ground, gradient, effect colour or tint (a
  real third-party logo keeps its own colours, `icons.md`).
- Copying a reference site's code, copy, pictures or signature effect.
- Deleting or editing the kit's own files (`assets/`, `scripts/`) to clear a check: a check that
  flags a kit file is reported, and the page is checked again after any change.


## Comment s'en servir en Cowork
1. **Brief** : écrire le type de commerce (section 1), ce qui est vendu, qui achète, l'action
   principale unique, et le matériel réel disponible (logo, photos, prix, adresse, horaires).
2. **Plan** : une ligne par section — id, idée unique, image et sa nature, 1 ou 2 écrans.
3. **Revue** : passer la page aux neuf règles de maison puis à la liste des « jamais » ; nommer
   chaque écart avec la règle enfreinte, rien d'autre.
4. Tout ce qui exige un navigateur, une photo du web ou un script → Claude Code, `taste-cockpit`,
   sur devis.
