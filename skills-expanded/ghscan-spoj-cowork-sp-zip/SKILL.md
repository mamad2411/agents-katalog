---
name: sharepoint-folder-zip
description: Use when you need many files from a SharePoint folder at once, e.g. to search, compare or read a whole folder tree with shell tools.
---

# SharePoint folder zip

1. Call `zip_folder` with the folder's browser URL or sharing link. Narrow large folders with `include`, `exclude`, `modified_since` or `max_file_mb`.
2. Pull the zip from the returned OneDrive path (`Cowork/zips/...`) into the sandbox, unzip it, and use shell tools freely.
3. Check `skipped` in the result; those files are not in the zip.
4. The zip is a read-only snapshot. To change a file, write it directly to SharePoint; `MANIFEST.tsv` maps each zipped path to its SharePoint item id, eTag and web URL.
5. Call `zip_folder` again for a fresh snapshot; it replaces the previous zip of the same folder.
