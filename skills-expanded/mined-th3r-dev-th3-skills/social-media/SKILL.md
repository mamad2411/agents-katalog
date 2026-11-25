---
name: social-media
description: >-
  Social and blog content toolkit, one skill with sub-skills. (1) blog-post: turn a topic or a piece of
  finished work into title options, typed hooks and a post in Thai or English, grounded only in facts the
  user or the session supplied, closing with an "if you want ..." hook and the user's hire or contact link;
  (2) blog-cover: render the post's cover (1200 x 630 OG card and 1920 x 1080) through design's
  banner-design engine and bench it for crop, contrast and phone width. Use WHENEVER the user wants a blog
  post, article, case study, making-of, social post or post cover ("ช่วยคิดหัวข้อ blog", "เขียนบล็อก",
  "เขียนโพสต์เล่าเบื้องหลัง", "ทำปกบทความ", "write a blog post about this", "blog cover", "OG image",
  "post for Fastwork / LinkedIn"), wants hooks or titles for a post, or wants a post benchmarked against a
  case. Read the sub-skill's SKILL.md before acting.
---

# social-media: sub-skills

| When the work is… | Read | Scripts |
|---|---|---|
| titles, hooks, a blog post or making-of, Thai or English | [`blog-post/SKILL.md`](blog-post/SKILL.md) | `scripts/bench_post.py` (post vs a TOON case) |
| the cover for that post, an OG image, a 16:9 post image | [`blog-cover/SKILL.md`](blog-cover/SKILL.md) | `../design/banner-design/scripts/banner.py` (`cover` layout), `bench.py` |

They chain: `blog-post` writes the title and kicker, `blog-cover` sets them on the cover.

## Rules every sub-skill keeps

- **Facts come from the user, the session or a source you can link.** No invented numbers, clients,
  results or first-person experience. When a fact is missing, ask or leave it out.
- **Translate the prompt to English first** when it is in another language, and keep both versions
  in the benchmark case, so the brief can be reviewed by anyone.
- **Thai prose is written with the `kien-thai` skill** (register, person deixis, the seven frames).
  Every prose deliverable then gets a `humanizer` pass. If either skill is not installed, say so and
  apply its rules from memory rather than skipping the review.
- **Drafting is not publishing.** Writing a post never posts it, sends it or changes an account.
- **A check the author didn't run decides done:** `bench_post.py` for the post, `bench.py` for the cover.

## Benchmarks

Cases live in [`benchmarks/`](benchmarks/) as TOON files: the original prompt, its English
translation, the facts the post may cite, and a rubric table whose ids map to checks in
`scripts/bench_post.py`. Edit the case to change what is measured; a rubric id with no check fails.
The worked case is [banner-making-of](examples/banner-making-of/RESULTS.md).
