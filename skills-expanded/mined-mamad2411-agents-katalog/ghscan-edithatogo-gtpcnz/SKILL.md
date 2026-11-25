# Substack rich content skill

Use this skill when packaging a Substack-ready post.

## Supported content patterns

- Hero image or thumbnail.
- Image block with alt text and native caption. For API-written drafts, use Substack's caption-capable image node with caption content inside the image node. Do not simulate captions with a separate italic paragraph.
- Inline hyperlinks where the source is relevant.
- Button/callout link for dashboard, report, model card or appendix.
- Divider between main post, optional deep dive and sources.
- Table if readable on mobile.
- Card-style fallback if a table is too wide.
- Simple formula or LaTeX when it helps a general reader.

## Formula rules

- Use formulae only for simple mechanisms.
- Explain every formula immediately in plain English.
- Do not introduce equations that imply calibration.

Example:

```text
Practice margin on one extra visit = scheduled payment - marginal cost
```

Plain English: if the payment for the extra visit is below the cost of delivering it, the practice loses money on that extra care.

## Done means

- Thumbnail exists or is specified.
- Every image has alt text and caption.
- API audit confirms image captions are stored natively, not as ordinary body paragraphs.
- Tables are preserved or converted with rationale.
- Source links are inline where relevant.
- Formulae are explained.
