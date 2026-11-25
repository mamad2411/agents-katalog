---
name: namoo-quickshare
description: "Upload HTML/Markdown/SVG/Mermaid content to QuickShare and return a shareable link. Triggers: share this, upload to QuickShare, get a link, 分享, 上传, 生成分享链接, share HTML, quickshare, make this a link, 把这个分享出去, 发个链接, 带密码分享. NOT for: editing existing pages, managing page lists, or deleting pages."
allowed-tools:
  - Bash
  - Read
---

# namoo-quickshare

Upload a file or inline content to QuickShare, return the shareable URL.

## Output Contract

After a successful share, output exactly:

```
https://quickshare.namooca.com/view/abc123
```

If password-protected, append:

```
Password: 482910
```

If the env vars are missing, tell the user to add `QUICKSHARE_URL` and `QUICKSHARE_API_KEY` to `~/.zshrc`.

## Execution

Use the script — do not rewrite curl from prose.

```bash
# File share
bash ~/.agents/skills/namoo-quickshare/scripts/share.sh /path/to/file.html

# With options
bash ~/.agents/skills/namoo-quickshare/scripts/share.sh file.html --title "My Page" --protected

# Inline content (pipe)
echo '<h1>Hello</h1>' | bash ~/.agents/skills/namoo-quickshare/scripts/share.sh

# Markdown with explicit type
bash ~/.agents/skills/namoo-quickshare/scripts/share.sh README.md --type markdown
```

### Options

| Flag | Effect |
|------|--------|
| `--title "text"` | Set page title |
| `--protected` | Generate a 6-digit password for the page |
| `--type html\|markdown\|svg\|mermaid` | Override auto-detection |

### Flow

1. Read the file path from user (or inline content from context)
2. If user says "带密码" / "with password" / "protected", add `--protected`
3. Run the script with appropriate flags
4. Output the URL (and password if present)

## References

- [API Reference](references/api.md) — endpoint details, error codes, content type mapping
