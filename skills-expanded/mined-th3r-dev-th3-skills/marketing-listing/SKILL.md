---
name: marketing-listing
description: Write a marketplace service listing field by field in the platform's own layout (Fastwork: media, service name, description up to 2,000 characters, price and unit, tags, link to post, then each package's name, description up to 5,000 and price with unit), make its images with design's banner-design (service, work steps with a worked example, a work-sample template that shows Coming soon until there is real work), and check it with offer.py check. Use WHENEVER the user wants to "ลงขายงาน", "เขียนหน้า service", "ทำแพ็กเกจบน Fastwork", "เขียนรายละเอียดแพ็กเกจ", "รูปปกงาน", "service listing", "gig description", "package description", or pastes a screenshot of a listing form.
---

# Listing

The listing is filled in by hand, field by field, so the output mirrors the form: one block per
field, in the form's order, ready to paste. Field limits, units and rules: [references/listing.md](references/listing.md).

## Workflow

1. **Read the form.** If the user shows a screenshot, follow it exactly: field names, limits, unit
   options. Otherwise use the layout in listing.md.
2. **Write from the offer and the strategy note.** Package names, prices and units come from the
   offer TOON. Every number in the text must also be in the offer.
3. **Say what the buyer gets, not the stack:** what is included, where it runs (Cloud, Self-host on
   the client's machine), the support period, delivery days and revisions (the package form has no
   field for these, so they go in the description), what the client prepares, what is billed
   separately (domain, hosting, servers at cost).
4. **Plain characters:** no "·", "+" or dashes in anything pasted; "และ" or a space instead.
5. **Images** (1920 x 1080, 16:9) with `../design/banner-design/scripts/banner.py`, one spec with
   `pages`, in the brand's style, Thai fonts set in `fonts`:
   - **hook** (`hook`), always first: the image buyers see in search. One promise from the offer
     (a delivery time, a result), a three-line checklist true for every package, the starting price,
     and real work in a browser frame with the client label. Win the click; details come later.
     `flow` adds a strip of icons along the bottom (chat, brief, build, launch, support) so the way
     you work reads in one glance; keep it to the steps the process image shows
   - **service** (`stack`): the brand side with the starting price and support, the four parts of
     the service in buyer words, the hire call
   - **process** (`stairs`): the work steps, with one package as a worked example (days on each step).
     Give it a different style from the service image (light against dark) so the two never look alike
   - **showcase** (`showcase`): the work sample centred. `images` takes up to three screenshots
     of one project (the first large, the rest stacked beside it, each at its own proportions);
     `client` adds a label naming who the work was for. With no images it shows "Coming soon".
     Client screenshots are the client's: keep that spec and its images in the user's own folder,
     never in a public repo, and confirm the client agrees to being shown
   Set `"content_ratio": [4, 3]` in the spec: Fastwork's gallery shows a 4:3 centre crop of each
   16:9 image, except the first, which it shows as a square; give the hook page
   `"content_ratio": [1, 1]` and bench it with `--safe-ratio 1:1`. Bench the rest with `--safe-ratio 4:3`, and look at the `-safe.png`
   preview, which is what buyers see first.
   - **profile cover** (`orbit`), on the seller's profile rather than the service: the name, one
     tagline, and the seller's skills grouped into 6 to 8 capability nodes, with the platform's skill
     names under each. Keep the avatar's circle clear (`bench.py --clear`)
6. **Check:** `python3 scripts/offer.py check <offer.toon> <listing.md>`; fix every FAIL.
7. **Save** the listing and images where the user keeps their work (ask once), and tell them which
   image goes first.

## Output

`listing.md` in the platform's field layout, the images, and the offer TOON beside them.

## Done when

- `offer.py check` passes, and every image passes `bench.py`.
- A buyer reading only the first image knows what is sold, from what price, and how to hire.
