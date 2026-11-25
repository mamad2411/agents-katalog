---
name: google-workspace
description: "Create and edit Google Docs, Sheets, and Slides through the Google connectors. Use this whenever the user names a Google file type or shares a docs.google.com link, and for any follow-up change to a Google file made earlier in the chat, even when they just say \"change it\" or \"add a tab\"."
---

# Google Docs, Sheets, and Slides

This skill covers three jobs: picking the right connector, keeping edits in the same file, and using each Google API without trial and error.

## 1. Check the connectors before you start

Each connector does a different job:

| Connector | What it can do |
|---|---|
| Google Drive | Create files, upload and convert content, rename, read text, export, trash |
| Google Docs | Read a doc's structure and edit it in place |
| Google Sheets | Read cells and write values, formulas, and formatting in place |
| Google Slides | Read a deck and add or edit slides, shapes, text, and tables in place |

Drive can create all three file types. It can't edit a file after that. Without the matching editor connector, every change means a new file and a new link, and the user loses the link they already have.

Check the connectors before you start:

1. Check which Google tools are available in this conversation. On surfaces where tools are deferred, search for and load the editor tools you need first, such as "google sheets update". Tool names differ by surface, so use the names your surface lists. If a search returns nothing, list all available tools before deciding the connector is missing — the tool may exist under a different name.
2. If the editor tools are missing, tell the user. When you can list the conversation's connectors, say which case it is: a connector that is set up but turned off in this chat (ask them to turn it on in the chat's connector settings, then continue), or one that isn't connected at all (tell them which connector to add and what it enables).
3. With an editor connector missing, a request to create a new file continues with Drive. A change to an existing file stops and asks — see the missing-connector rule in section 2.
4. If the user asks only for a new file, create it with Drive. If the editor connector is off, add one line saying edits will need it.

Example: "I can create the sheet now. If you want changes later, turn on the Google Sheets connector in this chat first. Then I can edit this file, and the link will stay the same."

## 2. Rules for every file

- **A change goes in the same file.** "Change", "update", "fix", "add", and "switch it to" all mean the user wants the same file and link. Do not recreate the file to skip an edit.
- **A missing editor connector is a choice for the user, not a workaround for you.** When the user asks for a change to an existing file and the editor connector is missing, your whole reply is a short question, not a deliverable. Building the next-best thing feels helpful, but the user's file is still untouched and now there are two artifacts — the exact failure this skill exists to prevent. Lead with the fix: name the connector and say that with it on, the edit lands in their existing file and the link stays the same. You may offer an alternative — drafted text to paste, or a file to import by hand — but only as a named option, and build it only after the user picks it. Example reply, in full: "To add the slide to your deck directly, turn on the Google Slides connector in this chat and I'll do it — same deck, same link. Or I can draft the slide as a file you'd import by hand. Which do you prefer?"
- **Never trash a file the user didn't ask you to delete.** Drive can trash a file, but it can't restore one. The Docs, Sheets, and Slides connectors can't open a trashed file.
- **Read the file before you edit it.** Docs and Slides edits need current positions and object IDs. Sheets formatting needs the numeric `sheetId`.
- **Verify the result.** Read the file again after each edit. Use `get_values` for Sheets, `read_doc` for Docs, and `read_presentation` for Slides. Check the result before you report it. If the tool accepts the call, that does not mean the content is correct.
- **Build long requests with a script.** For index math, formula grids, or many formatting requests, write a script that prints the JSON, where you can run code. Then paste the JSON into the tool call — the tool takes inline arguments, not a file path.
- **Rename with Drive `update_file`.** A rename keeps the same link.
- **Share the link with each result.** Use the `viewUrl` from the Drive response. When you edit a file, say that the link stays the same.

## 3. Google Docs

### Create

Call Drive `create_file` with `contentMimeType: "text/html"` and the document as `textContent`. Drive converts `<h1>`, `<h2>`, `<p>`, `<ul>`, `<ol>`, `<b>`, `<i>`, and `<a>` into native Docs formatting. This is faster than building a doc with Docs edit requests.

### Edit

Use Docs `read_doc`, then `update_doc`.

- For a word or phrase, use `replaceAllText`. It needs no indexes.
- For a larger rewrite, replace one paragraph at a time. Read each paragraph's `startIndex` and `endIndex`. Delete `[start, end - 1]` to keep the paragraph's newline and style. Then call `insertText` at `start`.
- Order the requests from the highest index to the lowest. Then an edit can't shift the position of an edit later in the batch.
- Inserted text takes the style of the text before it. Reset bold and italic only on body text. Don't reset headings, because that removes their bold.
- To delete a whole paragraph, delete `[start, end]`.
- Use raw newlines in the text. Don't use escaped `\n`.
- Call `read_doc` again to check the edit.

## 4. Google Sheets

### Create

- **Blank sheet, then fill it:** create the file with Drive `create_file` and `contentMimeType: "application/vnd.google-apps.spreadsheet"`. Then fill it with Sheets `update_formulas`. Use this for models and anything with formulas.
- **Upload:** upload a CSV or an .xlsx built with the `xlsx` skill. Drive converts it. Use this for large data sets or many tabs. Then edit the result in place.

### Write

- `update_formulas` writes values and formulas. Send numbers as numbers, not text. Store percentages as fractions, such as `0.25` for 25%.
- Write formulas for every calculated cell. Do not write results you computed yourself. Formulas keep the sheet live when the user changes an input.
- Quote tab names that contain spaces or symbols: `'P&L'!F5`.
- In a spreadsheet you just created, the first tab's `sheetId` is `0`. For an existing file or other tabs, call `get_spreadsheet` with `fields: ["sheets.properties"]`. Do not use a subselection such as `sheets.properties(sheetId,title)`, because the tool rejects it. To set a new tab's `sheetId`, include it in `addSheet`.
- Format with `update_spreadsheet`. Use `repeatCell` for number formats, fonts, and fills. Use `updateBorders` and `updateDimensionProperties` for widths. Use `updateSheetProperties` for names and frozen rows. Ranges use 0-based indexes with exclusive end values. Colors use `red`, `green`, and `blue` values from 0 to 1, not hex.
- Send all formatting in one `update_spreadsheet` call.

### Verify

`get_values` returns the calculated, formatted values. Read the whole range you built. Look for `#REF!`, `#DIV/0!`, `#NAME?`, `#VALUE!`, and `#N/A`. Check that the totals match the expected numbers.

### Financial model conventions

These conventions come from the `xlsx` skill. Follow them unless the user or the file uses different ones.

- **Colors:** blue text for inputs, black for formulas, and green for links to another tab.
- **Number formats:** currency is `$#,##0;($#,##0);"-"`. Percentages are `0.0%`, stored as fractions. Multiples are `0.0x`. Years are text.
- **Structure:** put each assumption in its own labeled cell, and reference that cell in formulas. Use the same formula across each period in a row. Wrap division in `IFERROR`.
- **Inputs:** put a note near the top that says which cells are inputs.
- **Existing files:** follow the file's conventions. Write only in its input cells. Do not change its formulas.

### Function support

Sheets supports `XLOOKUP`, `FILTER`, `UNIQUE`, and `SORT`, so the `xlsx` skill's LibreOffice limits do not apply here. If the user may export the file to Excel, avoid Sheets-only functions such as `QUERY`, `ARRAYFORMULA`, `IMPORTRANGE`, and `GOOGLEFINANCE`.

## 5. Google Slides

### Create

Choose a method based on the deck.

- **A designed deck:** load the `pptx` skill, build a .pptx with it, and check it with that skill's QA steps. Then upload it with Drive `create_file` and let Drive convert it. You get the `pptx` skill's design tools and QA. Conversion can change fonts and spacing. Check the result with the QA steps below.
- **A few simple slides:** create a blank presentation with Drive `create_file` and `contentMimeType: "application/vnd.google-apps.presentation"`. Build the slides with `update_presentation`. The new deck starts with one title slide. Use it, or delete it with `deleteObject`.

### Edit

Use `read_presentation`, then `update_presentation`.

- Use a field mask with `read_presentation`. Example: `["slides(objectId,pageElements(objectId,size,transform,shape(shapeType,text)))"]`. A full read is very large.
- **Units:** the tool uses EMU. One inch equals 914400 EMU. The default 16:9 page is 9144000 x 5143500 EMU, or 10 x 5.625 in. Get the size from `pageSize` before you set positions.
- **Object IDs:** choose your own IDs when you create objects, such as `s3_title`. Each ID must be unique and 5 to 50 characters long. Use these IDs in later requests in the same batch.
- **Shapes:** use `createShape`, then `insertText`, then `updateTextStyle`. Font size uses `{magnitude, unit: "PT"}`. Use `updateShapeProperties` for fills and outlines.
- **Colors:** use `rgbColor` values from 0 to 1.
- **Simple edits:** use `replaceAllText` for text changes. Use `duplicateObject` to copy a slide. Use `updateSlidesPosition` to reorder slides.
- **Images:** `createImage` needs a public URL. If you have only a local image, use the .pptx upload method.
- **Charts:** use `createSheetsChart` to embed a chart from a Google Sheet. Do not use a chart image. An embedded chart stays linked to its data.
- **Text fit:** Slides does not shrink text to fit. Size each box for its text. If the text does not fit, use a smaller font or split the slide.

### Design

Load the `pptx` skill and use its Design Ideas and Avoid sections. If it is not available, the most important rules:

- Choose a palette that fits the topic. Use one dominant color and one accent.
- Vary the layouts. Give each slide a visual element, such as a chart, a large number, a shape, or an image.
- Use 36 to 44 pt titles and 14 to 16 pt body text. Left-align body text.
- Leave margins of at least 0.5 in and gaps of 0.3 to 0.5 in.
- Don't add accent lines under titles or decorative color bars.
- Use Google fonts, such as Arial, Roboto, Lato, Montserrat, or Merriweather.

### QA

1. Read the deck with a field mask. Check the text, slide order, and placeholder text.
2. Where you can run code, export the deck to PDF with Drive `download_file_content` and `exportMimeType: "application/pdf"`. Decode the base64 and render each page with `pdftoppm -jpeg -r 110`. Check the images for overflow, overlap, and low contrast. If you can't run code or the export fails, rely on step 1 and tell the user you couldn't check the layout.
3. Fix the problems and export the deck again to check the fixes.

## 6. Common failures

| Symptom | Cause | Fix |
|---|---|---|
| "No such tool available" | The tool is deferred, or the name is different on this surface | Search for and load the tool. Use the exact name your surface lists. |
| Permission denied on a file you created | The file is in the trash | Ask the user to restore it from Drive's trash. You can't restore it with the connectors. |
| Sheets `Invalid field` | The field mask uses a subselection | Use `sheets.properties` and filter the result yourself. |
| A heading loses its bold after an edit | A style reset was applied to the heading | Reset styles only on body text. |
| Edits land in the wrong place in a doc | The requests ran from the lowest index to the highest | Order the requests from the highest index to the lowest. |
| A Sheets formula shows text | The formula went to `update_values` | Use `update_formulas`. |
