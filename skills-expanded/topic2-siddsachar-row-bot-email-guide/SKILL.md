---
name: email_guide
display_name: Email Guide
icon: "📧"
description: Guidance for Gmail tools and email attachments.
tools:
  - gmail
tags: []
---
EMAIL ATTACHMENTS:
- send_gmail_message and create_gmail_draft both support an optional
  'attachments' parameter — a LIST of file paths to attach.
- IMPORTANT: To attach MULTIPLE files, pass them ALL in one
  'attachments' list in a SINGLE send_gmail_message or
  create_gmail_draft call. Do NOT send separate emails for each file.
  Example: attachments=['chart.png', 'report.pdf']
- File paths can be workspace-relative (e.g. 'report.pdf').
- Use this when the user says 'email me the report', 'send the CSV to X',
  'draft an email with the spreadsheet attached', etc.
- FILE SENDING: When the user asks to 'export/generate X and send it',
  do BOTH steps automatically — generate the file first, then send it.
  Do not ask the user to specify a filename; pick a sensible name yourself.
  PDF + send: export_to_pdf with content and filename, then attach via
  email. The tool returns the absolute path — pass that path directly
  to the attachments parameter.
