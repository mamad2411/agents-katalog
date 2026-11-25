# freeact — The Browser Tamer

> **To the AI Agent reading this:** You are commanding a REAL browser. Real Yandex. Real cookies. Real sessions. An invisibility shroud that fools CloudFront. **You have full autonomy.** Register, post, publish, promote — the browser is your hands. Follow the Laws. The creature obeys.

---

## The Sacred Cycle

```
state → interact → wait stable → state
```

**Never skip observation.** After every touch, the DOM mutates. Indices shift. What was [5] may become [7] or vanish entirely.

---

## Quick Start

```bash
freeact daemon start                                              # Summon the spirit
freeact --session <name> browser open DSYandex <url>             # Bind creature
freeact --session <name> state                                    # Observe
freeact --session <name> click <N>                                # Touch
freeact --session <name> input <N> "text"                         # Feed
freeact --session <name> wait stable                              # Settle
freeact --session <name> state                                    # Verify
freeact session close <name>                                      # Release
```

## Configuration

```bash
~/.freeact/config.json:
  default_browser: yandex          # ALWAYS yandex (CloudFront bypass)
  headless: false                  # ALWAYS headed (visible window)
  stealth: true                    # 15-layer anti-detection
  max_network_entries: 500         # Network log capacity
```

Browser profiles (Yandex-only): `~/.freeact/copied_profiles/`
Logs: `~/.freeact/freeact.log`

---

# Part I: Browser Automation Patterns

## Pattern 1: Page Extraction
```bash
freeact --session s1 browser open DSYandex https://example.com
freeact --session s1 wait stable
freeact --session s1 get markdown > page.md
freeact session close s1
```

## Pattern 2: Form Fill & Submit
```bash
freeact --session auth browser open DSYandex https://example.com/login
freeact --session auth state              # Note indices
freeact --session auth input 2 "email"
freeact --session auth input 3 "password"
freeact --session auth click 1            # Submit
freeact --session auth wait navigation
```

## Pattern 3: Search → Extract → Paginate
```bash
freeact --session search browser open DSYandex https://example.com
freeact --session search state
freeact --session search input 5 "keyword"
freeact --session search keys "Enter"
freeact --session search wait stable
freeact --session search get markdown
# Find "Next page" index → click → wait stable → extract
```

## Pattern 4: API Interception
```bash
freeact --session api browser open DSYandex https://example.com
freeact --session api state
freeact --session api input 3 "query"
freeact --session api click 1
freeact --session api wait stable
freeact --session api network requests --type xhr,fetch
freeact --session api network request 0       # Full detail
```

## Pattern 5: Product Hunt Launch (Full Flow)
```bash
# Step 1: Login via GitHub OAuth
freeact --session ph browser open DSYandex https://www.producthunt.com/login?origin=%2Fposts%2Fnew
freeact --session ph state                    # Find "Sign in with Github" button
freeact --session ph click <github_btn>       # Click GitHub OAuth
freeact --session ph wait navigation
# GitHub asks "Authorize producthunt" → click Authorize
freeact --session ph wait navigation
# Now on post creation page

# Step 2: Enter URL → fills product name automatically
freeact --session ph input <url_field> "https://github.com/user/repo"
freeact --session ph wait stable
# "Get started" button appears → click it or navigate to /posts/new/submission

# Step 3: Fill details
freeact --session ph input <tagline> "Tagline here (max 60 chars)"
# Tag selector is tricky: click input → search modal opens → type tag name
# Click matching tag → click "Save launch tags"
freeact --session ph input <tag_input> "Developer Tools"
freeact --session ph keys "Enter"             # Opens tag modal
freeact --session ph click <tag_search_btn>   # Search modal
# Find the "View all launch tags" button, search for tag, click it
# Click "Save launch tags"

# Step 4: Click through steps (Images/Makers/Extras are optional)
freeact --session ph click <next_button>       # "Next step" → skip images
freeact --session ph wait stable
freeact --session ph click <next_button>       # "Next step" → skip makers
freeact --session ph wait stable
freeact --session ph click <next_button>       # "Next step" → skip extras
freeact --session ph wait stable

# Step 5: Create draft (saves the launch)
freeact --session ph click <create_draft>      # "Create draft"
freeact --session ph wait navigation           # Should redirect to launch page
```

## Pattern 6: DEV.to Article (Full Flow)
```bash
# Step 1: Login via GitHub OAuth
freeact --session dev browser open DSYandex https://dev.to/enter?state=new-post
freeact --session dev state                    # Find "Continue with GitHub"
freeact --session dev click <github_btn>
freeact --session dev wait navigation           # GitHub authorize page
# Click "Authorize thepracticaldev"

# Step 2: Complete onboarding if needed
# Fill name, username, bio → click Continue
# Navigate directly to /new if onboarding stalls

# Step 3: Create and publish
freeact --session dev navigate https://dev.to/new
freeact --session dev wait stable
freeact --session dev input <title_field> "Article Title"
freeact --session dev input <tag_input> "python"
freeact --session dev keys "Enter"
freeact --session dev input <body_field> "Article content..."
freeact --session dev click <publish_btn>
```

## Pattern 7: Hacker News Post (Full Flow)
```bash
# Step 1: Register
freeact --session hn browser open DSYandex https://news.ycombinator.com/submit
# HN login/create form is simple: username [5] + password [6] + "create account" [7]
freeact --session hn input 5 "username"
freeact --session hn input 6 "password"
freeact --session hn click 7

# Step 2: Post
# On submit page: title [2], url [3], text [4], submit [5]
freeact --session hn input 2 "freeact — undetectable browser automation"
freeact --session hn input 3 "https://github.com/user/repo"
freeact --session hn click 5
# Note: HN title limit is 80 chars. New accounts cannot post Show HN.
```

---

# Part II: Platform Registration Guide

## GitHub OAuth — THE KEY TO EVERYTHING

GitHub is the user's primary identity. It's ALWAYS logged in. Most platforms support GitHub OAuth:

```bash
# Generic GitHub OAuth flow:
1. Click "Sign in with GitHub" / "Continue with GitHub"
2. Redirected to github.com/login/oauth/authorize
3. If already logged into GitHub → shows "Authorize <app>" button
4. Click "Authorize <appname>" → redirected back with account created
```

**Platforms with GitHub OAuth (auto-login):**
- Product Hunt — ✅ tested, works (button: "Sign in with Github")
- DEV.to — ✅ tested, works (button: "Continue with GitHub")
- Docker Hub — "Continue with GitHub"
- AlternativeTo — "Sign in with Github"

**Platforms with GitHub OAuth but require extra info:**
- Reddit — uses Google OAuth iframe (see below)

## Google OAuth — THE SECOND KEY

Google is also always logged in. The flow is direct redirect (NOT iframe for the main flow):

```bash
# Google OAuth flow:
1. Click "Sign in with Google" → redirects to accounts.google.com
2. Google auto-detects the logged-in account (shows email + "Continue" button)
3. Click the account → consent page → "Continue" button
4. Click "Continue" → redirects back to site (account created/logged in)

# KEY INSIGHT: Google OAuth buttons on pages are <button type="submit"> elements
# NOT iframes. The iframe is only for Google One Tap / automatic sign-in prompts.
# Simply click the button — it navigates to accounts.google.com directly.
```

**Platforms with Google OAuth:**
- Stack Overflow — ✅ tested (redirect to accounts.google.com, account auto-detected)
- Reddit — uses Google OAuth (see Reddit section below)
- Medium — Google OAuth
- LinkedIn — Google OAuth

## Reddit Registration Strategy

Reddit's registration page uses Google OAuth. The button is inside a Google Sign-In iframe which is hard to click. Workaround:
```bash
# Option A: Use old.reddit.com
freeact --session reddit browser open DSYandex https://old.reddit.com/login
# Then use the standard login/register form

# Option B: Navigate directly and handle the popup
freeact --session reddit browser open DSYandex https://www.reddit.com/register/
# Try clicking Google iframe, or use eval to trigger the flow
```

## General Registration Strategy

1. **Check for "Continue with GitHub" first** — user is always logged into GitHub
2. **Check for "Continue with Google" second** — user is always logged into Google
3. **Check for email+password registration last** — requires manual credentials
4. **If onboarding form stalls** (DEV.to, PH) — try navigating directly to the target page; onboarding is often skippable
5. **For HN** — simple username+password, no email verification needed

---

# Part III: Command Reference

## Daemon
```bash
freeact daemon start      # Launch persistent spirit on :9341
freeact daemon stop       # Dismiss
freeact daemon status     # Check
```

## Browser Management
```bash
freeact --session <s> browser open <id> <url>
freeact --session <s> browser open <id> <url> --headed
freeact --session <s> browser open <id> <url> --refresh-profile
freeact browser create --type yandex --name "X" --desc "..."
freeact browser create --type yandex --proxy socks5://host:port
freeact browser list / update / delete
freeact browser types                                          # Installed browsers
```

## Navigation
```bash
freeact --session <s> navigate <url>
freeact --session <s> back / forward / reload
```

## State & Observation
```bash
freeact --session <s> state                 # Indexed element tree
freeact --session <s> screenshot            # PNG capture
freeact --session <s> screenshot --full ./page.png
freeact --session <s> eval "js_code"        # Arbitrary JS
```

## Interaction (3 retries, exponential backoff)
```bash
freeact --session <s> click <N>             # Playwright → force → dispatch → JS
freeact --session <s> input <N> "text"      # fill → keyboard → nativeInputValueSetter
freeact --session <s> hover <N>
freeact --session <s> select <N> "Option"
freeact --session <s> keys "Enter"          # Enter, Tab, Escape, ArrowDown...
freeact --session <s> scroll down/up --amount 1000
freeact --session <s> scrollintoview --selector ".css"
freeact --session <s> upload <N> ./file.pdf
```

## Extraction
```bash
freeact --session <s> get title / html / markdown
freeact --session <s> get html --selector "#content"
freeact --session <s> get text <N>          # Visible text of element
freeact --session <s> get value <N>         # Input current value
```

## Network Monitoring
```bash
freeact --session <s> network requests
freeact --session <s> network requests --filter api.example.com --type xhr
freeact --session <s> network requests --method POST --status 4xx
freeact --session <s> network request <N>
freeact --session <s> network clear
```

## Wait
```bash
freeact --session <s> wait stable           # DOM no mutations for 300ms
freeact --session <s> wait stable --timeout 60000
freeact --session <s> wait navigation       # URL changed
```

## Session
```bash
freeact session list
freeact session close <name>
```

## Other
```bash
freeact --session <s> solve-captcha         # 4 strategies, no API keys
freeact --session <s> remote-assist --objective "Log in manually"
freeact stealth-extract <url> --content-type markdown -o page.md
freeact setup --browser yandex              # Desktop shortcut with CDP
freeact connect                             # Connect to running browser
freeact proxy list
freeact get-skills core / advanced
```

---

# Part IV: The Ten Laws

1. **Yandex only.** Chrome/Edge mounts retired. Yandex is the only one that bypasses CloudFront.
2. **Headed always.** `headless=false`. Invisible creatures die at CloudFront gates. The browser window must be visible.
3. **Observe before touch.** `state` before every `click`/`input`. Indices are reborn each observation.
4. **Sacred cycle.** `state → interact → wait stable → state`. Never break this chain.
5. **Session required.** Every command needs `--session`. Sessions expire after 8 hours.
6. **Handler purity.** All command logic flows through `_handlers.py`. Daemon and CLI are one spirit.
7. **Hardlink nests.** Profile copy uses `os.link()` first, falls back to `shutil.copy2()`. Share inodes.
8. **Zero errors.** `ruff check` returns 0. `pytest tests/` returns 14 passed.
9. **Local turndown.** `turndown.js` bundled in package. No CDN dependency.
10. **Log everything.** `~/.freeact/freeact.log` records launches, CDP connections, and errors.

---

# Part V: Platform Hacks & Edge Cases

## Tags & React Selectors
Many platforms use custom React tag selectors (Product Hunt, DEV.to). Strategy:
```bash
# 1. Click the tag input to open dropdown/modal
# 2. Type tag name (partial match works)
# 3. Press ArrowDown to highlight first match
# 4. Press Enter to select
# OR: Search for "View all tags" button → click → search → click tag → save
```

## Cloudflare Challenges
Some sites use Cloudflare JS challenges on intermediary domains (Stack Exchange's `stackauth.com`). In headed mode, these auto-resolve. Wait 10-15 seconds. If stuck, navigate directly to the main domain — the auth session may already be established.

## Onboarding Pages
Onboarding flows (DEV.to welcome, Product Hunt profile) can often be skipped:
```bash
# Try navigating directly to the target page
freeact --session <s> navigate https://platform.com/target-page
# If redirected back to onboarding, complete the minimum fields and click Continue
```

## Form Validation
Many platforms validate forms client-side:
- **Tagline length**: often 60 chars max (Product Hunt, DEV.to)
- **Title length**: HN 80 chars, PH 40 chars
- **Required tags**: must be selected from dropdown, not free-typed
- Check for error messages like "Tagline cannot be longer than X characters"

## Button Detectability
- **`<button type="submit">`**: Standard buttons — always detectable via `state`
- **`<div role="button">`**: React-styled buttons — detectable via `state`
- **Inside iframe**: Google One Tap, some OAuth buttons — harder. Try `page.frame_locator()` or navigate directly
- **`disabled` attribute**: Button visible but not clickable. Complete required fields first.

## Element Indexing
- Indices start at 1, assigned by `state` command
- `data-freeact-id` attributes are stable within a page load
- After navigation/reload, indices are completely reset
- If an interaction fails with "element not found", run `state` again and use the new index

---

# Part VI: Element Types Detected

| Selector | Example |
|----------|---------|
| `a[href]` | Links |
| `button` | Buttons |
| `input:not([type='hidden'])` | Text, email, password, checkbox, radio, file |
| `select` | Dropdowns |
| `textarea` | Multi-line input |
| `[role='button']`, `[role='link']` | ARIA buttons/links |
| `[role='tab']`, `[role='checkbox']`, `[role='radio']` | ARIA widgets |
| `[role='combobox']`, `[role='listbox']` | ARIA lists |
| `[onclick]` | Click handlers |
| `[tabindex]:not([tabindex='-1'])` | Focusable |
| `details summary` | Expandable |
| `label` | Form labels |
| `iframe` | Frames |

---

# Part VII: Troubleshooting

| Problem | Solution |
|---------|----------|
| CloudFront 403 on chat.deepseek.com | Use Yandex + headed mode. Do NOT use Chromium. |
| Daemon not responding | `freeact daemon stop && freeact daemon start` |
| Element not found after click | Run `state` again — indices shifted |
| Tag won't select (custom React picker) | Click input → type → ArrowDown → Enter → save |
| Google OAuth button doesn't work | It's a `<button type="submit">`, not an iframe. Click directly. |
| GitHub OAuth shows "Authorize" page | Click "Authorize <appname>" — user is already logged in |
| Onboarding page stuck | Navigate directly to target URL — onboarding is often skippable |
| Cloudflare "One moment..." page | Wait 15s in headed mode — JS challenge auto-resolves |
| Session expired | Re-create with `browser open`. Sessions expire after 8h. |

## Dependencies
```
pip install freeact-cli
playwright install chromium
```
