# Notes for agents

## Package management

Use Bun for everything. No npm, yarn, or pnpm.

## The resume

`/resume` is a real page, not a PDF viewer. `public/jaiden_dechon_resume.pdf` is
a build artifact printed from that page, kept at that path because external
links point at it.

- Content lives in `lib/data/resume.ts`. Editing the resume should be a change
  to that file and nothing else — the components under `components/resume/` are
  purely presentational.
- `bun run resume:pdf` regenerates the PDF. It boots its own dev server, so
  nothing needs to be running first.
- Pages are paginated by hand. The slice constants at the top of
  `pages/resume.vue` decide which entries land on which sheet. Sheets are fixed
  height and clip silently, so if content grows, adjust those slices — the
  generator measures every column and exits non-zero with the exact overflow
  rather than shipping a clipped page.
- Never hand-edit the PDF. A previous change patched it with `pypdf`; that work
  is lost the next time the page is printed.

### The PDF is not reproducible byte-for-byte

Regenerating produces a different file every run even when nothing has changed —
same byte count, identical text, identical images, but a different trailer ID
from Skia (Chromium's PDF writer). `bun run resume:pdf` will therefore always
leave `public/jaiden_dechon_resume.pdf` showing as modified in `git status`.

Confirm the content actually changed before committing it, otherwise the diff
carries a meaningless binary churn. Comparing extracted text is enough:

```bash
git show HEAD:public/jaiden_dechon_resume.pdf > /tmp/committed.pdf
pdftotext /tmp/committed.pdf - > /tmp/committed.txt
pdftotext public/jaiden_dechon_resume.pdf - > /tmp/current.txt
diff /tmp/committed.txt /tmp/current.txt
```

If that reports no difference, restore the committed copy with
`git checkout public/jaiden_dechon_resume.pdf` and leave it out of the commit.
