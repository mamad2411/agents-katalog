---
name: ace-tech-20-year-service-certificate
en_name: "Ace Tech — 20-Year Service Certificate"
description: "一份为 Ace Tech 打造的精美印刷级20周年服务证书：横向A4布局，奶油色纸面，海军蓝与金色配色，装饰性内联SVG角标，双线金色边框，衬线大标题，签名/日期栏位。"
en_description: "A polished, print-ready 20-year service anniversary certificate: landscape A4 with a cream paper surface, navy-and-gold color scheme, decorative corner ornaments, a double hairline gold border, a large serif heading, and signature/date lines."
category: certificate
tags: ["certificate", "service award", "anniversary", "print", "corporate"]
od:
  mode: template
  surface: web
  preview:
    type: html
    entry: example.html
  design_system:
    requires: false
  example_prompt: "Design a polished, print-ready 20-year service anniversary certificate: landscape A4 orientation, cream paper with a subtle radial highlight, navy (#142b45) and gold (#ae8950) color scheme, a thin double-rule gold border inset from the edges, decorative inline-SVG corner ornaments in gold, a large serif '20 Years of Service' heading, an italic 'presented with appreciation to' intro line, a recipient name underline, a short gratitude paragraph, an inline SVG brand mark above the heading, and a CEO signature/date footer. No clipart, no gradients standing in for real design, no emoji. Use — placeholders for recipient name."
---

# Ace Tech — 20-Year Service Certificate

1. Create a landscape A4 sheet (`297mm × 210mm` via `@page { size: A4 landscape }`) centered on a warm gray (`#e9e7e1`) page background. The certificate body uses a cream paper color (`#fbf8f0`) with a subtle radial gradient highlight toward the center and a soft drop shadow so the sheet edge reads clearly on screen.
2. Add two concentric 1px solid gold borders inset from the edges — an outer border in the primary gold (`#ae8950`) and an inner border slightly further in in a lighter gold (`#d9c39b`). These are the only framing lines; no thick frame, no rounded-corner card chrome.
3. Place decorative inline-SVG corner ornaments at all four corners in the gold color — a small geometric line-and-dot motif, flipped via `scaleX(-1)` / `scaleY(-1)` as needed to mirror into each corner.
4. Add a large translucent serif numeral "20" as a watermark behind the content (very low opacity navy, e.g. `3.5%`), positioned in the bottom-right area, so it reads as a background texture rather than foreground content.
5. At the top of the content area, place an inline-SVG brand mark (a hexagonal shape with a stylized initial) in gold alongside a small uppercase tracked brand name ("Ace Tech") in navy, center-aligned.
6. Below the brand, add a small gold uppercase eyebrow line ("With gratitude and admiration"), then the main heading "20 Years of Service" in a large serif font (Georgia or similar) at `clamp(34px, 5vw, 57px)`, navy color, centered.
7. Insert a decorative divider rule: a horizontal gold line on each side of a small rotated diamond mark, all in gold, centered.
8. Below the divider, add an italic serif intro line ("Presented with appreciation to"), followed by a recipient name area as a blank underline in gold, with a small uppercase "Honored team member" label beneath it.
9. Add a short appreciation paragraph in neutral ink color, centered, at a comfortable reading size (~14px), expressing gratitude for 20 years of service.
10. At the bottom, place a signature footer with two columns: a left column for the CEO's name in a script/cursive font with a name-and-title line below, and a right column for the date — both separated by thin gold rules.
11. Include `@media print` rules so the certificate renders at exactly `297mm × 210mm` with no padding/shadow and `print-color-adjust: exact` for faithful color reproduction.
12. Ensure the layout is responsive: on narrow screens (< 700px), switch to auto aspect-ratio, reduce padding, and wrap the footer columns. All sizing uses `clamp()` or percentage-based values for smooth scaling.
13. Ask the user for the recipient's real name and the signing executive's name and title before finalizing — keep honest `—` placeholders for anything not provided rather than inventing a name.
