---
name: swpilotcli-read-drawing
description: Engineering drawing / hand-sketch interpretation protocol. MUST be executed before any feature modeling whenever the user provides an engineering drawing or hand-drawn sketch image. Enforces multi-view cross-reference and isometric priority to prevent geometric misinterpretation.
---

# swpilotcli-read-drawing

Structured protocol for interpreting engineering drawings and hand-drawn sketches before generating any SolidWorks modeling code.

## Trigger Condition

**Execute this protocol automatically** whenever the user provides:
- An engineering drawing (工程圖, 三視圖, 工程製圖)
- A hand-drawn sketch (手繪草圖, 草稿)
- Any dimensioned or undimensioned multi-view drawing

Do NOT skip this protocol and jump directly to code generation.

---

## Step 1：Identify Views Present

List all views found in the image:
- Front view（正視圖）
- Top view（俯視圖）
- Right/Left side view（右/左側視圖）
- Isometric / Pictorial view（等角圖）
- Section views, detail views, etc.

---

## Step 2：Isometric View Takes Priority

If an isometric (or pictorial) view is present:
- **Use it as the primary reference for overall geometry and shape**
- Describe the 3D shape based on the isometric view first
- Use orthographic views (front/top/side) for reading dimensions only

> Rationale: Isometric views directly show 3D form and prevent misreading orthographic projections.

---

## Step 3：Hidden Line (虛線) Cross-Reference

For every hidden line (dashed line) in any view:
- Identify which feature it represents
- Confirm it appears (as visible or hidden) in **at least one other view**
- State the correspondence explicitly before proceeding

Format:
```
正視圖虛線 A → 對應 [俯視圖 / 側視圖] 的 [特徵描述]
```

Do NOT infer a feature from a single view's hidden lines alone.

---

## Step 3b：Annotation & Geometry Interpretation Rules

Apply these rules before assigning any dimension to a feature:

**□N / ⌀N = the feature itself, not its inner cavity**
- □20 means the feature pointed to IS 20×20mm
- To indicate an internal hollow, a section view or explicit "內孔" annotation must be present
- Never infer hollow from □/⌀ annotation alone

**Do not assume hollow from hidden lines alone**
- Dashed lines in orthographic views represent hidden edges, not hollow walls
- A hollow feature requires section view evidence or an explicit annotation
- Default assumption: solid, unless proven otherwise

**Chain dimensions must be cross-referenced with isometric before assignment**
- For a chain a | b | c = total, verify what each segment refers to using the isometric view
- Do not assign chain segments to a feature without confirming via at least one other view

**Position must be verified across all three orthographic views**
- Front view → left/right position
- Side view → front/back position
- Top view → confirms both
- Never declare position from a single view

**Visual flush = geometric alignment, no dimension needed**
- If a feature appears flush/aligned with another feature's edge in any view, treat it as geometrically coincident
- Do not request a confirming dimension for visually obvious contact or alignment

**Isometric view is sufficient for reading position**
- If the isometric clearly shows a spatial relationship (e.g. column flush at back, feature offset to one side), treat this as confirmed positional evidence — no chain dimension required
- Do NOT retreat to "ambiguous / might be centered" when the isometric makes the position visually obvious
- Only flag position as ambiguous when the isometric itself is unclear or contradicts another view

---

## Step 4：Output Feature List

After completing Steps 1–3, output a structured feature list.

| # | Feature | Dimensions | Position | View Evidence |
|---|---------|------------|----------|---------------|
| 1 | Base plate | 40×40×10mm | Origin | Front+Top+Iso |
| 2 | Column | 20×20×73mm | X:10-30, Z:-20~-40 | Front+Side+Iso |
| … | … | … | … | … |

Rules:
- Every feature must have at least 2 views listed under "View Evidence"
- Position must state coordinate ranges, not just "centered" or "at back"
- Dimensions must be taken from dimensioned views only

---

## Step 5：Wait for Confirmation

After outputting the feature list:
1. Ask the user to confirm: **「以上理解正確嗎？」**
2. Do NOT generate any C# modeling code until the user confirms
3. If user corrects any item, update the feature list and re-confirm

---

## Notes

- This protocol replaces ad-hoc drawing interpretation
- If the drawing is ambiguous or a view is missing, state the ambiguity explicitly rather than assuming
- Dimensions shown in the drawing always override any calculated or estimated values
