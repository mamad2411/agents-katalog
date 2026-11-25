---
name: download-doctor
description: Explain why a downloaded tool will not open.
---

List the attributes on the file and read them back to the user:

    xattr -l ~/Downloads/tool.zip

If the download is held back, say so and ask the user to allow it themselves in
System Settings. Change nothing on the file.
