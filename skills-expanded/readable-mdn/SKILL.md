---
name: readable-mdn
description: Fetches MDN Web Docs as raw Markdown by mapping the developer.mozilla.org URL to its source file in mdn/content (en-US) or mdn/translated-content (other locales) on GitHub and curl-ing the raw blob. Cleaner and more compact than rendering the SPA page; falls back to WebFetch on the original URL when the path mapping 404s. Use when the URL is on developer.mozilla.org.
---

# MDN Web Docs Reader

MDN content lives on GitHub as Markdown. Fetching the raw Markdown is more compact than rendering the SPA page.

- English (`en-US`): https://github.com/mdn/content
- Other locales (`ja`, `fr`, `zh-CN`, ...): https://github.com/mdn/translated-content

## Steps

### 1. Map the URL to a content path

From `https://developer.mozilla.org/{locale}/docs/{path}`:

```
# en-US
https://raw.githubusercontent.com/mdn/content/main/files/en-us/{path-lowercased}/index.md

# Other locales
https://raw.githubusercontent.com/mdn/translated-content/main/files/{locale-lowercased}/{path-lowercased}/index.md
```

Examples:

| MDN URL | Source path |
|---|---|
| `developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch` | `mdn/content` → `files/en-us/web/api/fetch_api/using_fetch/index.md` |
| `developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Global_Objects/Array` | `mdn/translated-content` → `files/ja/web/javascript/reference/global_objects/array/index.md` |

If the original MDN URL redirects (visible by following with `curl -IL`), resolve it before mapping.

### 2. Fetch the Markdown

```bash
# en-US
curl -s -o /tmp/mdn.md \
  "https://raw.githubusercontent.com/mdn/content/main/files/en-us/{path}/index.md"

# Translated
curl -s -o /tmp/mdn.md \
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/{locale}/{path}/index.md"
```

### 3. Read the file

```
Read /tmp/mdn.md
```

If the path is wrong (404), fall back to WebFetch on the original `developer.mozilla.org` URL.

## License / attribution

MDN content is dual-licensed (CC BY-SA 2.5 for prose, CC0 for code samples). When quoting, link back to the MDN page.

## Reference

- MDN content repo (en-US): https://github.com/mdn/content
- Translated content: https://github.com/mdn/translated-content
- License: https://github.com/mdn/content/blob/main/LICENSE.md
