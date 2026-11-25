---
name: readable-speakerdeck
description: Fetches a SpeakerDeck slide deck by extracting the public PDF URL from the slide page (WebFetch), downloading it via curl, and running pdfvision — typically with --render on image-heavy pages so the slides can be read visually. Use when the URL is in the form speakerdeck.com/{user}/{slug}.
---

# SpeakerDeck Slide Reader

## Steps

### 1. Fetch page info with WebFetch

Use WebFetch to load the slide page and extract the PDF download URL.

- Form: `https://files.speakerdeck.com/presentations/{id}/{filename}.pdf`

### 2. Download the PDF

```bash
curl -L -o /tmp/slide.pdf "{PDF_URL}"
```

### 3. Extract the PDF contents

Prefer [pdfvision](https://github.com/yamadashy/pdfvision) — slide decks are often image-heavy, and pdfvision's density Overview surfaces the pages where `--render` is needed for multimodal review:

```bash
npx pdfvision /tmp/slide.pdf
npx pdfvision /tmp/slide.pdf --render -p {pages-with-low-coverage}
```

If only a Claude Code-style multimodal Read tool is available, `Read /tmp/slide.pdf` also works.
