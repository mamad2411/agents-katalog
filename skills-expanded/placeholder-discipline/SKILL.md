---
name: placeholder-discipline
description: Moves floating text and objects into the layout's real title, body, and content placeholders so the deck inherits template styling automatically.
---

# Placeholder Discipline

## When to use

Use this skill when text and objects sit in free-floating boxes outside the layout placeholders. The tell-tale signs: titles that are manual text boxes rather than the title placeholder, body copy in a box that does not move when you change the layout, and content that keeps its own font and size no matter what the template says. Run this right after Master and Layout Mapper, once each slide is on the correct layout but the content still lives outside the placeholders.

## What it does

It moves content into the real placeholders the layout provides, so the slide inherits the template's title style, body style, bullet levels, and position. The result is a deck where the title is the title placeholder, the body is the body or content placeholder, and there are no rogue text boxes pretending to be structural elements.

## Method

A placeholder is a pre-positioned, pre-styled container defined on the layout. Content inside it inherits the template. Content in a plain text box does not. The job is to migrate content from boxes into placeholders.

1. **Identify the placeholders on each layout.** With the slide selected, open the Selection Pane (Home then Select then Selection Pane) to see every object. Placeholders are named "Title 1," "Content Placeholder 2," "Text Placeholder," and so on. Plain boxes are named "TextBox" or "Rectangle."

2. **Match each piece of content to a placeholder.** The slide's headline goes in the Title placeholder. The main body or bullets go in the Body or Content placeholder. A picture goes in the Picture placeholder. A caption goes in the Text placeholder on a caption layout.

3. **Move text into placeholders, not boxes onto placeholders.** Cut the text from the rogue box and paste it into the placeholder (click the placeholder's prompt text first, then paste as text so it adopts the placeholder's formatting). Do not drag the whole box on top of the placeholder; that leaves the box in place and the styling wrong.

4. **Clear direct formatting.** After pasting, select the text and clear formatting (Home then Clear All Formatting, or set font to the theme default) so the placeholder's real style shows. Then re-apply only the structural choices the template allows, such as bullet level.

5. **Use outline levels, not manual indents.** For bulleted content, use Tab and Shift-Tab to set the real outline level inside the placeholder. This pulls the correct indent, bullet glyph, and size from the layout instead of a hand-set indent.

6. **Delete the empty rogue boxes.** Once content is migrated, delete the now-empty text boxes and rectangles that were standing in for placeholders. Keep genuine non-placeholder graphics (a chart, a real diagram) where they belong.

7. **Restore missing placeholders.** If a layout's placeholder was deleted on a slide, use Home then Reset to bring back the layout's placeholders, then move content in.

## Inputs

- A deck that is already on the correct layouts (run Master and Layout Mapper first if not).
- The list of placeholders each layout provides, or access to the template.

## Output format

A per-slide migration list:

- Slide number.
- Each content item and the placeholder it should move into.
- Boxes to delete after migration.
- A "Reset needed" flag where a placeholder is missing.

Close with a one-line confirmation that titles are in Title placeholders and body copy is in Body or Content placeholders across the deck.

## Example

Input: slide 3 has a manual text box reading "Three forces are reshaping the market" at the top and three bullet boxes below.

Output:

- Move "Three forces are reshaping the market" into the Title placeholder, then Clear All Formatting so it adopts the template title style.
- Merge the three bullet boxes into the Content placeholder as three level-one bullets using Tab for sub-points.
- Delete the four empty boxes.
- Result: the slide now reads as a real Title and Content slide and will restyle automatically if the theme changes.
