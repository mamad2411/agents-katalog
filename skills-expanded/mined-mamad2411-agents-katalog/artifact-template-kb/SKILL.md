---
name: artifact-template-kb
description: "Create an image using the KB 청년 위시리스트 슬라이드 비주얼 template and its retained reference file. Use when the user selects this template, names KB 청년 위시리스트 슬라이드 비주얼, or explicitly invokes $artifact-template-kb. KB AI Challenge 청년 위시리스트 발표용 인포그래픽과 피규어 이미지를 일관된 레이아웃과 색상으로 생성합니다."
---

# KB 청년 위시리스트 슬라이드 비주얼

Create an image from this template. Keep the reference file unchanged.

## Workflow

1. Read `artifact-template.json` and resolve its paths relative to this skill directory.
2. Invoke $imagegen with the retained PNG as a reference image and the user's requested content as the edit or generation brief.
3. Treat the user's prompt and available sources as the content input. Do not invent factual claims merely to fill the composition.
4. Preserve the reference's visual language unless the user explicitly requests a deviation.
5. Visually inspect the generated image for fidelity and defects, then return the final image.

## Fidelity

Preserve the reference image's composition, visual hierarchy, palette, typography, material treatment, lighting, and recurring brand elements.

User instructions control requested content and explicit deviations. The retained reference controls layout and formatting where the user has not requested a change.
