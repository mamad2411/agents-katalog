---
name: present-data
description: Render complex information (reports, research, plans, tables, sources) as styled HTML files in a tmp/ directory instead of plain terminal output. Use when presenting data that benefits from rich formatting like tables, links, and images beyond what markdown supports.
---



When presenting information to the user that is using the harness, if the information can be presented with mere words/paragraphs, continue to do so as you normall would. If the information is some sort of report, research, plan, or anything that includes elements like tables, lists, sources, etc, use HTML. create a "tmp" folder in the current directory. If that directory is not in .gitignore, add it there. Afterwards, write an html file in there that contains your data. Keep the style simple, but readable. Make sure you add simple, basic support for dark and light mode using the css media query.

This will allow you to include things in html that you couldn't in markdown, like source-links for claims, images for reference, etc. Feel free to use these if necessary.

