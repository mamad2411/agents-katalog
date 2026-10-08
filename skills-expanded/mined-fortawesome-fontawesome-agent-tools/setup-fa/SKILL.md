---
name: setup-fa
description: Set up Font Awesome in a project from scratch, including Kit download and package configuration
user-invokable: true
args:
  - name: method
    description: "Preferred integration method: kit, npm, self-host, or auto (default: auto)"
    required: false
  - name: framework
    description: "Target framework if not auto-detected: react, vue, angular, ember, svelte, wordpress, html"
    required: false
---

Set up Font Awesome in a project from scratch. This skill handles everything from detecting the project type, through downloading a Kit or installing packages, to writing the initial integration code and creating `.font-awesome.md` so that `/add-icon` works immediately afterward.

Scripts referenced from `suggest-icon` are relative to `plugins/icons/skills/suggest-icon/`. Scripts referenced from `add-icon` are relative to `plugins/icons/skills/add-icon/`. Run them from their respective directories.

## Important: bare SVG markup

**Never generate Font Awesome SVG markup (raw `<svg>` elements) from your own knowledge or training data.** If a bare SVG is needed during setup (e.g., for verification), fetch it from the Font Awesome API using `fa icons --version <version> --name <icon> --svg-format html`. This requires the user to be logged in (`fa whoami`) or `FA_API_TOKEN` to be set.

## Pre-flight check

Before starting, check whether `.font-awesome.md` already exists in the project root. If it does, Font Awesome is already configured. Tell the user and ask if they want to reconfigure, update their setup, or if they had a different goal. Offer `/fa-help` if they have a question about their existing setup, or `/add-icon` if they want to start using icons.

## Tool selection

Run `command -v fa` to check whether the `fa` CLI is available on PATH.

The `fa kit` subcommand requires `fa` version 0.8.0 or newer. If the `fa kit` subcommand is needed, recommend the user upgrade `fa`, using instructions here: https://docs.fontawesome.com/web/use-with/fa-cli

- **If `fa` is found:** use it for Kit operations and version queries (it returns structured JSON). For kit operations (`fa kits` and `fa kit`), check auth first: run `fa whoami` to see if the user is logged in. If logged in, `fa kits` and `fa kit` will work directly. If not logged in but `FA_API_TOKEN` is set, they will also work. If neither, tell the user: "You need to be logged in to the Font Awesome CLI for kit operations. Run `fa login` in a separate terminal, then come back here and try again."
- **If `fa` is not found:** fall back to the Python scripts described below where applicable.
- Use `latest-version.py` to get the latest version.

## Steps

### 1. Detect the project type

**Use a subagent** (via the Agent tool with `subagent_type: "Explore"`) to determine:

- **Package manager** — look for `package.json` (npm/yarn/pnpm), `requirements.txt` / `pyproject.toml` (Python), `composer.json` (PHP), `Gemfile` (Ruby), or no package manager (static HTML).
- **Framework** — look for:
  - `react`, `react-dom`, `next`, `gatsby` in package.json → React
  - `vue`, `nuxt` in package.json → Vue
  - `angular.json` or `@angular/core` in package.json → Angular
  - `ember-cli` in package.json → Ember
  - `svelte` in package.json → Svelte
  - `wp-content/`, `functions.php`, `style.css` with WordPress theme headers → WordPress
  - `.html` files with no framework → static HTML
- **Existing Font Awesome traces** — check if Font Awesome is partially installed (old version, broken setup, etc.). Look for `@fortawesome` packages in `package.json`, Kit script tags in HTML, CDN links, or Font Awesome CSS/font files.
- **Icons already in use** — collect the set of Font Awesome icons the project already references, with the family and style for each where determinable. Look in class-based markup (`fa-solid fa-cart-shopping`, `fa-sharp fa-regular fa-user`), React/Vue imports (`faCartShopping` → `cart-shopping`), `<FontAwesomeIcon icon={...}>` / `icon={['far', 'cart-shopping']}` usages, sprite `<use href="...#icon-name">`, and `<fa-icon>` elements. This list drives the Kit-coverage check in step 4 — capture canonical icon names (kebab-case) and note the family-style when you can infer it.
- **License clues** — `fontawesome-pro` packages, Pro CDN URLs, or Kit config indicating Pro.
- **Project structure** — where HTML templates live, where CSS/JS entry points are, where components are defined.

If the user passed a `framework` argument, use that instead of auto-detecting.

The subagent should return a structured summary of what it found, including the list of icons already in use (with family-style where known).

### 2. Recommend an integration method

Based on the project type and any user preference (`method` argument), recommend one of these approaches. If the user specified a `method`, use that. Otherwise, follow this decision tree:

```
Has a Font Awesome account/Kit?
├── Yes → Kit (best experience, auto-subsetting, custom icons, easy updates)
│   ├── JS framework (React/Vue/Angular)? → Kit Package via npm (@awesome.me/kit-*)
│   ├── Static HTML / server-rendered? → Kit embed code (script tag or CSS link)
│   └── Desktop app? → Kit download (desktop)
└── No / Unknown
    └── Recommend signing up at https://fontawesome.com (free accounts available)
        then follow the Kit path above.
```

Always recommend creating a Font Awesome account and using a Kit — even for free-tier users. Kits provide the best experience (auto-subsetting, easy updates, custom icons) and a free account is all that's needed. Do not recommend third-party CDNs or other unofficial distribution methods.

**If the project already uses icons (from step 1), the chosen Kit should include them.** A Kit contains only a subset of all Font Awesome icons, so a Kit that omits icons the project already relies on will leave those icons broken. If the user has more than one Kit, guide them toward one whose subset and family styles cover the icons already in use. If they're creating a new Kit, mention that it needs to include those icons (and the family-styles they use). You'll verify the actual coverage once you have the Kit token, in step 4.

Present the recommendation to the user with a brief explanation of why. **Wait for the user to confirm before proceeding** — setup involves installing packages or modifying project files.

### 3. Fetch documentation for the chosen method

Use `WebFetch` to retrieve `https://docs.fontawesome.com/llms.txt` — this is an index of all available documentation pages with URLs and descriptions. Scan the index to find the setup page(s) most relevant to the chosen integration method and framework. Look for URLs containing keywords like `setup`, `use-kit`, `packages`, `host-yourself`, `use-with/react`, `use-with/vue`, `kit-download`, etc.

Then fetch the relevant page(s) using `WebFetch`. When fetching, use a prompt like: "Return the full content of this documentation page as Markdown. Preserve all headings, code blocks, and tables."

This ensures the instructions are current and version-accurate. Do not rely on training data alone for setup instructions — the docs are authoritative.

### 4. Execute the setup

Follow the path that matches the chosen method. Each path is documented in a separate reference file under `references/` (relative to this skill's directory). Read the appropriate file for detailed instructions.

| Method | Reference file |
|--------|---------------|
| Kit embed code (script tag or CSS link) | `references/path-a-kit-embed.md` |
| Kit package via npm (`@awesome.me/kit-*`) | `references/path-b-kit-npm.md` |
| Kit download (self-host or desktop) | `references/path-c-kit-download.md` |
| npm packages without a Kit (`@fortawesome/*`) | `references/path-d-npm-packages.md` |

After completing the path-specific steps, if the method involved installing npm packages (Paths B, D), read `references/path-f-framework-init.md` for framework-specific initialization code.

#### Verify the Kit covers the icons already in use

Once you have the Kit token (any Kit path: A, B, or C), and the project already used Font Awesome icons (collected in step 1), confirm the Kit's subset actually includes them. This requires the `fa` CLI and an authenticated session (`fa whoami`, or `FA_API_TOKEN` set).

1. Check each icon already in use with `fa kit icon --kit-token <TOKEN> <icon>`. This reports whether the icon is in the Kit and which family-styles it covers. For a small number of icons, check them individually; for many, you can list the Kit's contents with `fa kit icons --kit-token <TOKEN>` (paginated) and compare locally.
2. Confirm the family-styles the project uses are present with `fa kit family-styles --kit-token <TOKEN>` (paginated), or `fa kit family-style --kit-token <TOKEN> ...` to look up a single one.
3. If any in-use icon (or its family style) is **missing** from the Kit, warn the user explicitly. List exactly which icons are not covered and in which family styles, for example:

   > Your project uses `fa-thin fa-binoculars` and `fa-duotone fa-compass`, but this Kit doesn't include them: `binoculars` is missing the thin style, and `compass` isn't in the Kit at all. Those icons will not render. You can add them to your Kit at https://fontawesome.com/kits and re-run, choose a different Kit that includes them, or proceed and replace them with kit-available alternatives (try `/suggest-icon`).

   Let the user decide how to proceed before finishing setup. Do not silently configure a Kit that omits icons the project already depends on.

If the `fa` CLI isn't available or the user can't authenticate, note that you couldn't verify Kit coverage and that any icons missing from the Kit's subset won't render.

### 5. Verify the setup

Add a test icon to confirm everything is working:

1. Find a visible template or component in the project.
2. Add a simple icon (e.g., `fa-check` or `fa-font-awesome`) using the appropriate syntax for the integration method.
3. Tell the user to preview the page/app to confirm the icon renders.
4. If they report issues, refer back to the `llms.txt` index to find the relevant troubleshooting page (look for URLs containing `troubleshoot`) and fetch it to guide diagnosis.

### 6. Write `.font-awesome.md`

Create `.font-awesome.md` in the project root. Read `font-awesome-md-format.md` (in the `add-icon` skill directory, `plugins/icons/skills/add-icon/`) for the template and format to use. Populate it with everything discovered and configured during setup.

Tell the user: "I've written `.font-awesome.md` with your project's Font Awesome configuration. Commit this file so the team benefits and `/add-icon` works immediately."

### 7. Next steps

After setup is complete, tell the user what they can do next:

- **Add icons:** "Run `/add-icon <icon-name>` to add any Font Awesome icon to your code."
- **Find icons:** "Run `/suggest-icon <concept>` to find the right icon for your use case."
- **Get help:** "Run `/fa-help <question>` to get answers from the official Font Awesome docs."
