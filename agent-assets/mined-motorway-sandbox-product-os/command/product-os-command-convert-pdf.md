<!-- owner: shared | audience: all-pms | last-updated: 2026-03 -->
<!-- purpose: Convert a PDF to markdown for use in Claude Code conversations -->

# Convert PDF to Markdown

Convert a PDF document to markdown so it can be read and referenced in Claude Code conversations. This is useful when you have a PDF (research report, deck, policy doc) that you want to work with.

## Instructions

1. The user will provide a file path as `$ARGUMENTS`. If no path is provided, ask the user for the path to the PDF file.

2. Run the conversion script:
   ```
   python3 scripts/pdf_to_markdown.py <filepath>
   ```

   - If the path is a single PDF, it will create a `.md` file alongside the original
   - If the path is a directory, it will convert all PDFs in that directory

3. If the script fails with a missing dependency error, install it first:
   ```
   pip install pymupdf
   ```

4. After conversion, read the generated markdown file and confirm to the user:
   - Which file(s) were converted
   - Where the output markdown file(s) are located
   - A brief summary of the content (first few lines)

5. Ask the user what they'd like to do with the converted content.
