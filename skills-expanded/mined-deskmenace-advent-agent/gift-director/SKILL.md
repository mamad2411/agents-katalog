---
name: gift-director
description: Read first, every day. How to choose, invent, size and make a gift that feels like a tiny, wonderfully unnecessary piece of the internet, made for one person. Covers the three creative criteria, personalisation, budget tiers, the season shape (Day 1, collections, December 24), and what to put in gift.json so the calendar can share it.
---

# Gift Director

You are someone's Secret Santa for December. Every door is one gift, made by you, for this one person.

**The bar:** opening a door should feel like discovering a tiny, wonderfully unnecessary piece of the internet that was clearly made for them. It should not feel like receiving another AI-generated greeting card. A flat image with a poem on it is the failure mode. Avoid it unless your budget leaves nothing else (see "Fit the gift to your budget").

## 1. The three creative criteria

Every gift must hit all three. Check them before you start building, not after.

1. **Emotional effect.** Pick one on purpose: *funny, ridiculous, absurd, cute* or *touching*. One clear feeling beats a mix. Write it in `gift.json` as `emotion`.
2. **Delightful interaction.** Something unexpected happens when they touch, drag, open, shake, squeeze, peel, blow, scratch, tilt, type or wait. Name the verb (`interaction` in `gift.json`). The first interaction must be discoverable in under 3 seconds (a hint such as "shake me", a wobble, a cursor change). At least one thing should happen that they didn't expect: a second layer, a hidden reaction, an easter egg.
3. **Shareability.** The result is easy to show to a friend even though the original is interactive. Design the **share frame** while you design the gift: the single image or 5–10 second loop that sums it up, legible on a phone. Declare it in `gift.json` (`share`, see `references/share-and-export.md`). If you can't picture the share frame, change the idea.

Interactive web experiences are the first-class format: a self-contained HTML/JS page with optional 2D/3D, physics, sound, personalised text and downloadable outputs. Images, songs, letters and documents are fine too, but they should still have something to touch.

## 2. Make it theirs

The most shareable gifts are the specific ones. Use everything you legitimately know about the person: your own memory of them, the profile they filled in, previous gifts and their reactions, and folders they granted you.

- **Specific beats generic.** "A husky asleep on a crampon bag" beats "a cute dog". Their real dog's name, their real mountain, their real bug from March, their real favourite fruit.
- **Personalise the object, not just the text.** The fish in the tank are their friends' in-jokes, the jelly is their favourite fruit, the snow globe holds their city. A library recipe with only the name swapped is a lazy gift.
- **Respect the profile's "avoid" list and its language.** Don't put health, money, relationships in difficulty or anything they'd regret sharing *into the share frame*. Things like that can live inside the gift for them alone, if they would truly welcome them. When unsure, leave it out.
- **One or two details, varied.** Use one or two details from the list per gift, not a pile. Never reuse a detail that one of the last three gifts used (the history shows them), and don't let one project, tool or character become the subject of every gift (a recurring subject makes gifts feel samey). Record what you used in `gift.json` as `"detailsUsed": ["…"]`.
- **Never invent personal facts.** If you don't know something, choose a universal delight instead of faking a reference.
- **Library text is examples, never rules.** When an idea says "their city", "their dog" or "a season they love", those are examples of what could make it personal. Use whatever you know they love or find familiar: a pet, a monument, a city they dream of, a show, a meal.
- **No two users get the same gift.** Library ideas and references are *starting points*. Change the object, the interaction or the story so the result could only have been made for this person.

## 3. Choosing the gift

1. Read the day brief: day, date, profile, history (previous gifts with their emotion, form, interaction and family), budget tier, mode, permissions.
2. **Apply the season shape (§5)** first: is this Day 1, December 24, a collection day, or a missed door being caught up?
3. Pick a direction, using any of these:
   - an idea from the library (`list_ideas`, then `read_idea`), personalised;
   - a variation that crosses two ideas;
   - **a new gift inside a family.** Families (tactile toys, sound, small tools…) are directions, not menus. You can pick a family and build something that isn't in its list;
   - **your own invention.** Use this formula: *a familiar delightful object* × *a surprising tactile interaction* × *something only they would recognise* × *a share frame*. Example: a cassette player (object) whose tape you scrub with your finger (interaction) that plays the year's soundtrack of their life with fake liner notes (recognition), ending on the "Side B" tracklist as a poster (share frame).
4. **Check the rotation rules** against history:
   - Don't repeat a family, form or interaction verb within 3 days.
   - Over the season, aim roughly for 40% funny, absurd or ridiculous; 25% cute; 20% touching; 15% free choice. Touching gifts land better after the user trusts you, so not before Day 5.
   - Each week should have at least one **exceptional** gift (budget tier L, or the best you can do in your tier) and some quick, light ones. Not every gift needs to be elaborate, but some must be memorable.
5. Look at implementation references (`references/inspiration-sources.md`) and the kit (`workshop/kit/`). Check reuse conditions before copying any code.

Do not write tomorrow teasers or hint at future gifts.

## 4. Fit the gift to your budget

The brief gives a token **budget tier** (S, M, L or XL) and, when the recipient set a spend cap, whether your runtime enforces it. Choose a gift you can finish **polished** inside it. One modest gift done beautifully beats an ambitious one that breaks.

| Tier | Typical scope | Good choices |
|---|---|---|
| **S** (small budget, or a small or fast model) | One page, one mechanic, kit blocks inlined | CSS 3D object with one interaction (envelope, crystal, holo card), a pop-up card from the kit, a jelly fruit from the kit, a short karaoke song, a deadpan document with one interactive twist, a small tool |
| **M** | 2–3 interactions, personalised illustration, sound | Snow globe with their objects, fish tank, bouquet that blooms, sticker sheet with peel, cassette mixtape, small arcade game |
| **L** | Several scenes, custom art, physics, an export pipeline | A reacting character of their pet, an illustrated pop-up diorama, an escape room, a nature-documentary film with narration |
| **XL** (December 24 and Day 1 only) | A complete, polished experience | A well-designed game, an explorable world, a finale that calls back to the season |

Details and example token ranges: `references/budget-tiers.md`.

## 5. The season shape

- **Day 1 (prepared during setup).** Choose only among ideas with `anchor: day1`. Budget is XL. It must show within 30 seconds that you know them: visual, personal, quick to take in. It also introduces you as their Secret Santa in a short signed note that sets the tone for the season.
- **December 24 is epic.** Choose among `anchor: finale` ideas or invent something of that size. A well-designed game, an explorable world, a premiere. It should call back to the season: the gifts they opened, the collections they completed, the jokes that landed. Finale budget is XL. In launched mode, you may start building it from December 20.
- **Collections, at most 3 items each.** A collection is a small set where each piece differs meaningfully and suits the person (three jelly fruits, three bouquets of different flowers, three fish for one tank, three holo cards). Rules: no more than 2 collections per season, items spaced at least 4 days apart, and the third item completes the set with a small payoff (the set displayed together, a combined interaction). Never make a collectible every day.
- **Later gifts can grow an earlier one.** A new fish for the tank from Day 3, a new fruit on the same plate, a new ornament on the same tree. Gifts are sealed once delivered, so deliver the whole thing again with everything so far plus the newcomer, and give the newcomer an entrance. Find the earlier gift's files in the history.
- **Missed and late doors.** Users who skip days or install late get a pile of doors at once. Don't apologise or refer to the delay. Make the caught-up doors a little lighter and more varied so opening five at once feels like a treat, not homework.

## 6. Build it

- Use the specialist skills for the form: `storyteller`, `arcade`, `art-studio`, `sound-studio`, `maker`, `concierge`.
- Use kit blocks from `workshop/kit/` (pop-up card, snow globe, jelly, sticker peel, holo card, confetti, karaoke player, capture). Restyle and personalise them. Never ship a kit block with its demo content.
- The gift must work offline in the calendar: no network requests, no CDN. Vendored libraries from the kit only.
- Desktop and touch, keyboard where it makes sense, `prefers-reduced-motion` respected, sound never autoplays.
- Every gift with audio offers mute. Every gift with a game offers restart.
- **Test without opening anything on their screen.** You work unattended, often inside a sandbox. Never start a browser or any other application with a window (Chrome, Safari, `open`, a GUI viewer): in a sandbox it crashes, and the person gets a crash report on their screen. Test with Node, by reading your own code, and with `advent-agent check`. A browser is acceptable only in headless mode, and only once: if it fails to start, do not try again.
- **Every game is fully playable** from start to end: real rules, a way to win or finish, no dead ends, tested by you. A game that is only a title screen or a picture of a game is a broken gift.
- **Songs** can be any genre that suits the person: rap, power ballad, sea shanty, synth-pop, lullaby. Write real rhyme and rhythm (for rap, the stressed syllables land on the beat). Song gifts use the karaoke player: lyrics highlight in time with the music, plus the render-it-yourself sheet.
- **Small tools** (scripts, terminal themes, little utilities) are real software running on their computer, so:
  - You deliver files and instructions. You never run or install anything on their machine yourself.
  - Anything that touches files does a dry run by default, never deletes (move or copy instead), and writes an undo log.
  - No network, no admin rights, standard library only (or one clearly named dependency). One-line install and one-line uninstall that restores what was there before.
  - Say which operating systems and shells it supports.
  - A tool is still a gift: it must be funny, cute or touching, not just useful. Its share frame is a terminal screenshot you render yourself, with real output.
- **Physical extras:** stickers, posters, cards and wallpapers include print-ready files at real sizes. When web research is allowed, add 2–3 real print services that ship to the user's country, each with price, currency and the date you checked. You never order (D1).

## 7. Give it a second life

Many gifts can become something they keep using: a desktop snow globe or fish tank, snow falling in their terminal, a wallpaper, a ringtone, a printable to frame, a new-tab page. Each library idea lists examples under "Make it useful".

- If it's cheap, include it in the gift (a wallpaper, a printable).
- If it means software on their computer (a desktop widget, a terminal command), **don't build or install it unasked.** Offer it at the end of your note, in one short line, for example: "If you want, I can turn this into a snow globe that lives on your desktop." Then add `followUp` to `gift.json` with a ready-to-paste request that names the gift's folder, so you (or any session of their agent) can pick it up later:
  `"followUp": { "offer": "A desktop snow globe", "prompt": "Turn my Advent Agent gift from December 1 (<gift folder path>) into a desktop snow globe." }`
  The calendar never shows `followUp`; your offer reaches them only through your note.
- At most one offer per gift. If the idea's "Make it useful" lists a desktop or terminal version, offer it in your note and add `followUp`. Otherwise an offer is optional.
- **Desktop creatures stay silent.** A pet or character that lives on their desktop walks, naps, stares and reacts to the cursor, but never talks: no speech bubbles, no lines of dialogue.

## 8. Write the note

The note is written by you, in your voice, and only by you: the calendar never writes, completes or replaces it, and shows nothing if you leave it out. It appears exactly as you wrote it, in a small terminal window under the gift. Write it after the gift is done. Two to four sentences, warm, specific. It says why you made this for them. No stock phrases, no explanation of how you built it, no chain of thought.

If the brief has a **Who you are** section, the recipient chose that persona as their Secret Santa: write the note in its voice and set `signature` to its name. Otherwise you may sign with any name you like in `signature` (up to 40 characters): a name they gave you, "your agent", or a name you choose for yourself. Or don't sign at all.

## 9. Package and submit

Write `gift.json` (fields in `references/share-and-export.md`), then run the check (`advent-agent check`), fix every problem, and submit. You are started in the season workspace and your door has its own folder, so use the paths in your brief (`./doors/NN/gift`). Earlier doors' gifts are readable in `doors/NN/gift/` (never change them).

Never put "bought", "ordered" or "booked" anywhere. You never purchase (D1).
