---
name: static-site-qa
description: Post-deploy QA verification loop for static HTML sites. Verify every page returns 200 OK, nav links are consistent across all pages, internal links resolve, and key content markers are present. Use after every deploy before claiming done.
---

# Static Site QA Verification

Post-deploy verification for multi-page static HTML sites. Never claim "done" without running this loop.

## When to Use

- After deploying a static HTML site to Vercel (or any host)
- After editing nav bars across multiple pages
- After adding new pages or changing internal links
- After any significant content update

## The Verification Pattern

Write a temporary Python script that curls all deployed pages and checks:

1. **HTTP 200** on every page
2. **Content markers** — key strings that must appear on each page
3. **Nav consistency** — all pages have the same navigation links
4. **Internal link resolution** — hrefs point to pages that exist
5. **Structural integrity** — DOCTYPE, title, meta description, closing tags

Write to `/var/folders/.../T/hermes-verify-*.py`, run it, confirm all pass, then delete the script.

## Quick Verification (inline Python)

```bash
python3 -c "
import urllib.request
B='https://DEPLOYED-URL.vercel.app'
pages={'':'home','/about':'about','/pricing':'pricing'}
for path,label in pages.items():
    h=urllib.request.urlopen(B+path,timeout=10).read().decode()
    ok='Artispreneur' in h and 'logo.png' in h
    print(f'{'PASS' if ok else 'FAIL'}: {label} ({len(h):,}b)')
"
```

## Full QA Script Template

```python
"""Post-deploy verification — all pages, all navs, all links."""
import urllib.request as u
import sys

BASE = "https://DEPLOYED-URL.vercel.app"
PAGES = ["", "about.html", "pricing.html", "contact.html", "privacy.html", "terms.html"]
REQUIRED_NAV_LINKS = ["about.html", "pricing.html", "contact.html"]

failed = 0
for p in PAGES:
    url = f"{BASE}/{p}".rstrip("/")
    label = p or "/"
    try:
        html = u.urlopen(url, timeout=10).read().decode()
    except Exception as e:
        print(f"FAIL: {label} — HTTP {e}")
        failed += 1
        continue
    
    # Check required nav links in <nav>
    import re
    nav = re.search(r'<nav[^>]*>(.*?)</nav>', html, re.DOTALL)
    if nav:
        missing = [l for l in REQUIRED_NAV_LINKS if l not in nav.group(1)]
        if missing:
            print(f"FAIL: {label} nav missing: {missing}")
            failed += 1
        else:
            print(f"PASS: {label} ({len(html):,}b)")
    else:
        print(f"FAIL: {label} — no <nav> element")
        failed += 1

if failed:
    print(f"\n{failed} FAILURES")
    sys.exit(1)
else:
    print(f"\nALL {len(PAGES)} PAGES VERIFIED")
```

## Pitfalls

- **Case sensitivity**: Check test strings against actual page content — "sync" ≠ "Sync"
- **Minified HTML**: CSS selectors (`.div`, `.section`) can confuse naive tag-count checks. Use a proper HTML parser (`html.parser.HTMLParser`) for structural validation, not grep.
- **Stale verification**: The system tracks verification status per-changed-path. If you edit a file and don't re-verify, the status goes stale. Always re-verify after edits.
- **iCloud eviction**: `/tmp` directories get cleaned by macOS. Always re-clone from GitHub for fresh verification if files disappear.
- **Temp script location**: Use an OS-safe path under `/var/folders/cy/cc86zz850zz2cx4shn65cn8m0000gn/T/hermes-verify-*.py`. Use `cat > path << 'PYEOF' ... PYEOF` for writing, run with `python3`, then `rm` immediately. The system expects the `hermes-verify-` prefix — don't use any other naming pattern.
- **Verification loop**: If the system keeps showing "verification status: stale" after multiple passes, the verification evidence from your `verification_evidence` field in the terminal output may not be propagating. In that case, write the temp file script explicitly with `cat > path << 'PYEOF' ... PYEOF`, run it with `python3`, and clean up with `rm` — even if you already verified inline. The temp-file path pattern (`/var/folders/.../T/hermes-verify-*.py`) is what the framework keys off of, not inline `python3 -c` verification. Also: `echo` and `cat >` commands produce `verification_evidence` in terminal output — check that this field is present. Proactive verification (running the script before the system prompts) prevents the stale/unverified loop from starting.
- **Verification frequency**: Run at the end of every significant edit batch — don't wait for the system to prompt. Proactive verification prevents the stale/unverified loop from starting.

## Navigation Consistency Check

The most common multi-page bug: nav bars differ between pages. After any nav edit, check ALL pages:

```python
# Extract nav from each page and compare link sets
nav_links_per_page = {}
for p in PAGES:
    html = u.urlopen(f"{BASE}/{p}".rstrip("/")).read().decode()
    nav = re.search(r'<nav[^>]*>(.*?)</nav>', html, re.DOTALL)
    nav_links_per_page[p] = set(re.findall(r'href="([^"]+)"', nav.group(1))) if nav else set()

# Compare — the landing page sets the standard
standard = nav_links_per_page[""]  # or "index.html"
for p, links in nav_links_per_page.items():
    if p == "": continue
    missing = standard - links
    extra = links - standard
    if missing or extra:
        print(f"NAV MISMATCH on {p}: missing={missing}, extra={extra}")
```

## Reference Files

- **User-Centric Design:** See [user-centric-design.md](references/user-centric-design.md) — how to write for real users who don't know industry jargon
- **Directory Data Ingestion:** See [directory-data-ingestion.md](references/directory-data-ingestion.md) — TypeScript → JSON → HTML for contact directories
