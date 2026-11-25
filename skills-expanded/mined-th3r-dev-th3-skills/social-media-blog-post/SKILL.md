---
name: social-media-blog-post
description: Write title options, typed hooks and a blog post (Thai or English) about a topic or a piece of finished work, using only facts the user or the session supplied, and close with an "if you want ..." hook plus the user's hire or contact link. Thai is written with kien-thai, every draft gets a humanizer pass, and the post is checked against a TOON benchmark case with bench_post.py. Use WHENEVER the user says "ช่วยคิดหัวข้อ blog", "เขียนบล็อก", "เขียนโพสต์เล่าว่าทำยังไง", "blog post about this", "making-of post", "case study post", "hooks for a post", "titles for a post", or wants a post for Fastwork, LinkedIn or a personal blog.
---

# Blog post

A post about finished work earns trust when every claim can be checked. This sub-skill writes from a
facts list, in the reader's language, and lets a script decide whether the draft meets its brief.

References: [hooks and titles](references/hooks.md), [post shape](references/post-shape.md).

## Workflow

1. **Brief.** Topic, reader, goal, language, the CTA link. If the prompt is not in English, translate
   it to English first and keep both. Person and register for Thai: ask if not given; a prompt that
   says "จ้างผม" has already chosen ผม.
2. **Facts.** List what the post may say, each from the user, the session, the repo or a linked
   source. Numbers only from this list. Write it into a case file (step 7) as you go.
3. **Titles and hooks.** Five titles, then six hooks, one per type in [hooks.md](references/hooks.md).
   Each must be true from the facts; a hook that needs a fact you don't have is dropped.
4. **Outline, then draft.** Use the shape in [post-shape.md](references/post-shape.md): answer-first
   opening, numbered steps with the real commands and files, the failures and how they were fixed, the
   choice and why. A post is at most **2,000 characters** of shown text unless the user sets another
   limit; at that length four steps fit, six don't. Thai: load `kien-thai` and draft frame-first (or route through its Thai-native
   model script when one is running).
5. **Close.** The "if you want ..." hook, then "หากสนใจ" / "if you're interested" and the link. One CTA.
6. **Images.** One cover, one image per step, one closing image (the finished work). Hand the title,
   kicker and each step's title, caption and picture to [`../blog-cover`](../blog-cover/SKILL.md), and
   place each image under its heading.
7. **Review and bench.** `kien-thai` audit for Thai, then `humanizer`, then:

   ```
   python3 scripts/bench_post.py benchmarks/<case>.toon <post.md> --titles <titles.md>
   ```

   Fix every FAIL and re-run. A fact the bench flags is either added to the case with its source or
   cut from the post.

## Output

`titles.md` (titles first, then hooks), `post.<lang>.md`, the images from blog-cover, and a short
`RESULTS.md`: the bench lines, what failed and how it was fixed.

## Done when

- `bench_post.py` passes every rubric row.
- The kien-thai audit and the humanizer pass found nothing left to change.
- Every number and named source in the post appears in the case's facts.
