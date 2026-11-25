---
name: gradient-fill
description: "Apply blue-purple-navy gradients to selected PowerPoint shapes or text and optionally remove their outlines without rasterizing content. Use for gradient fills or title emphasis. 図形・文字のグラデーションと輪郭線の除去に使用。"
license: MIT
---

# Gradient Fill

1. Identify the selected shapes or text runs and clarify whether the request
   concerns the shape background or the letters. A shape containing text is not
   automatically a request to change both.
2. Preserve position, size, wording, font, and unrelated objects. Keep the output
   editable. Use supported application controls before considering XML editing.
3. Follow the user's palette or deck theme. If unspecified, use stops `0070C0`
   at 0%, `7030A0` at 55%, and `1F3864` at 100%. Default to a linear
   left-to-right gradient; use a radial gradient only if requested.
4. Apply to the selected shape fill or selected text runs only. Remove outlines
   for that target unless the user requests preserving them. Do not remove the
   whole shape's border when only the letters are selected.
5. If low-level editing is necessary and available, use the DrawingML namespace
   `http://schemas.openxmlformats.org/drawingml/2006/main`. Replace mutually
   exclusive fill elements only on the target properties, preserve schema order,
   and represent a removed line with `a:ln` containing `a:noFill`.
   Avoid rewriting all text-run properties or overwriting inherited formatting.
6. Check actual rendering and readability against the background, especially for
   text gradients. Prefer solid emphasis when the gradient reduces readability.
   If text gradients or partial text selection are unsupported, explain this and
   offer a supported alternative; do not silently flatten the text into an image.
7. Report the target scope, palette, gradient direction, and any unverified result.
