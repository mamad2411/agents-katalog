---
name: conv2pdf
description: Convert and edit the files of the user's computer with the Conv2pdf tools. Use when the user asks to turn a Word, Excel, PowerPoint, OpenDocument, Pages, image, HEIC, EPUB, PostScript, XPS, Markdown or HTML file, or a web page at an address, into a PDF, to turn a PDF into a Word document or into images, or to merge, split, extract pages from, rotate, number, watermark, compress, password-protect or unlock PDFs, for one file or for a whole folder.
license: MIT
compatibility: Needs the Conv2pdf MCP server (npm package conv2pdf-mcp, Node.js 22 or later) and a Conv2pdf API key.
---

# Conv2pdf

The Conv2pdf tools convert and edit files that are on the user's computer. A tool takes the path of a file, sends the file to Conv2pdf and writes the result next to it. This skill tells which tool to call, in which order, and what a call costs.

## Before the first call

- **The files leave the computer.** A file given to a tool is uploaded to Conv2pdf, on OVHcloud servers in France, and deleted there once the result is on disk. Say so once, before the first file, when the user said the document is confidential or when it is of a kind that usually is: a contract, a payslip, a medical or an identity document. Otherwise do not ask for each file.
- **Each call counts.** A conversion uses one unit of the quota of the API key. The Dev plan has 300 units in all, valid for 12 months and not renewed. `get_quota` is free, and every result carries the quota as it stands after the call.
- **Give absolute paths.** A relative path is read from the working directory of the server, which may not be the folder the user is in. `~` is the home folder.
- **No Conv2pdf tool in the list** means the MCP server is not installed: point the user to https://github.com/conv2pdf/mcp#installation.

## Which tool

| The user wants | Tool | To know |
|---|---|---|
| A PDF from a Word, Excel, PowerPoint, OpenDocument, Pages, RTF, TXT or CSV file, from a PNG, JPG, WebP, GIF, TIFF or HEIC image, from an EPUB book, a PostScript or EPS file, an XPS or OXPS file, a Markdown file or an HTML file | `convert_to_pdf` | One file per call. The converter is chosen from the extension |
| A PDF of a web page, from its address | `convert_url_to_pdf` | A public page only: it is opened without a session, so nothing behind a login. Give `output_path`, since there is no input file to write next to |
| A JPG from an iPhone HEIC photo | `convert_heic_to_jpg` | |
| An editable Word document from a PDF | `convert_pdf_to_word` | Only a PDF with real text. A scan is refused, and counted |
| The pages of a PDF as images | `convert_pdf_to_images` | One ZIP of PNG or JPG files at 150 DPI, 100 pages at most |
| One PDF out of several | `merge_pdfs` | In the order of the list. 2 files per call on the Dev plan, up to 20 on paid plans |
| Some pages of a PDF, in a new PDF | `extract_pdf_pages` | Pages as `1-5,7,10-12`, in the order written. One call per file to produce |
| Every page of a PDF in its own file | `split_pdf` | One ZIP of single-page PDFs, 200 pages at most. A one-page PDF is refused, and counted |
| Pages turned the right way | `rotate_pdf` | Every page, by 90, 180 or 270 degrees clockwise |
| Page numbers | `add_page_numbers` | "3 / 12" or "3", at the bottom |
| A text stamped across the pages | `add_watermark` | 50 characters at most, Latin letters, digits and punctuation |
| A smaller PDF | `compress_pdf` | `low` is 72 DPI, `medium` 150, `high` 300. Default: `medium` |
| A PDF that asks for a password | `protect_pdf` | Password of 6 to 64 characters. Can also forbid printing or copying |
| The password or the restrictions removed | `unlock_pdf` | With the password the user knows: it does not find a forgotten one. No password is needed for a PDF that opens freely but forbids printing or copying |

Conv2pdf converts neither Numbers spreadsheets nor Keynote presentations: ask the user to export them from the application, with File > Export To > PDF. It has no OCR either: a scanned PDF does not become a Word document here.

## Several steps

When a request takes several tools, keep this order: merge, then extract or rotate, then number or watermark, then compress, and protect last.

- **Protect last.** A tool that opens a protected PDF with `password` writes a result that has no password. To edit a protected PDF and keep it protected, do the edit with `password`, then call `protect_pdf` on the result: two units.
- **Unlock before merging.** `merge_pdfs` takes no password: a protected PDF goes through `unlock_pdf` first.
- **Several images in one PDF.** Convert each image with `convert_to_pdf`, then merge the PDFs.
- **Merging on the Dev plan.** With 2 files per call, merging n PDFs takes n - 1 calls: merge the first two, then the result with the third, and so on.
- **Count the calls first.** When a request takes more than a few calls, tell the user how many units it will use before starting.
- **Intermediate files stay on disk.** Give the last step an `output_path` with the name the user expects, say which file is the final one, and offer to delete the intermediate files you created.

## A whole folder

- Call `get_quota` first and compare what is left with the number of calls. When it does not fit, say so before starting, not halfway.
- Run the calls one after the other. The API accepts 20 conversions per minute for a key. The server waits by itself when the API asks to slow down; when a call comes back with a delay, wait that long and go on.
- A file may weigh 10 MB on the Dev plan and 200 MB on paid plans. A file that is too large is refused on arrival, and not counted.

## Results

- A result gives `output_path` and `size_bytes`: tell the user where the file is.
- Nothing is overwritten. `report.docx` gives `report.pdf`, a PDF tool adds a suffix, as in `report-compressed.pdf`, and a name that is taken becomes `report (2).pdf`. A tool refuses an `output_path` that already exists, before converting anything.
- After `compress_pdf`, compare `size_bytes` with the size of the original. Compression lowers the resolution of the images, so a PDF made of text barely shrinks. When the gain is small, say so; ask before trying a lower quality, since each try counts.

## Refusals

A refusal comes back as a sentence that says what to change. Read it before calling again.

- **A refused setting is free.** A page range that does not exist, a password that is too short, a rotation that is not allowed: fix the argument and call again.
- **A refusal that follows the reading of the file is counted.** A scanned PDF given to `convert_pdf_to_word`, an unreadable file, a document with too many pages: calling again with the same file uses another unit for the same answer. Report it instead.
- **A failure on the side of Conv2pdf is not counted.** Try once more, then report it.
- **A password that is missing or wrong.** Ask the user for it. Never guess one.
- **No API key.** In Claude Code with the Conv2pdf plugin, the key is the "Conv2pdf API key" option of the plugin: `/plugin configure conv2pdf@conv2pdf`, or `/plugin`, Installed tab, conv2pdf, Configure options. Elsewhere it is the `CONV2PDF_API_KEY` variable in the configuration of the MCP server. The user sets it there: never ask for the key in the conversation.

## Passwords

Use the password the user gives to `protect_pdf`. When the user asks for one to be chosen, give it back in the answer: `unlock_pdf` cannot recover it.
