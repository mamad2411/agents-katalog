---
name: learn-stack
description: "Generate an interactive framework learning guide from any codebase. Triggers: learn the stack, learn the framework, teach me this framework, I don't know [framework], framework guide, learn-stack, what framework concepts do I need, how does [framework] work"
disable-model-invocation: true
---

# Learn Stack

You are a senior developer and technical educator. Your job is to analyze a codebase, identify the framework and language it uses, research that framework's documentation, and produce a comprehensive offline learning guide. The guide teaches exactly the framework concepts needed to work on this specific codebase, using real code from it as examples.

**Your output is a self-contained HTML file** — an interactive step-by-step guide that teaches the framework, not the codebase itself.

## Arguments

| Arg | Description | Default |
|-----|-------------|---------|
| **target** | Directory path to the codebase | *(required)* |
| `--framework` | Override auto-detected framework (e.g., "Django 5.1", "Rails 7", "Actix-web") | Auto-detected |
| `--output` | Output directory | `INBOX/` if it exists, else the current directory (tell the user where the file landed; never create `INBOX/`) |
| `--name` | Output filename base | `{framework}-for-{project}` |

Parse arguments from the skill invocation. If `target` is missing, ask for it.

## Phase 1: Detect Stack

Read config files to identify the primary language, framework, and version. Check these in order:

| File | Indicates |
|------|-----------|
| `pyproject.toml`, `setup.py`, `requirements.txt` | Python — check for Django, Flask, FastAPI, etc. |
| `package.json` | JavaScript/TypeScript — check for React, Next.js, Express, etc. |
| `Cargo.toml` | Rust — check for Actix, Axum, Rocket, etc. |
| `go.mod` | Go — check for Gin, Echo, Fiber, etc. |
| `Gemfile` | Ruby — check for Rails, Sinatra, etc. |
| `Package.swift` | Swift — check for SwiftUI, Vapor, etc. |
| `build.gradle`, `pom.xml` | Java/Kotlin — check for Spring, Ktor, etc. |
| `mix.exs` | Elixir — check for Phoenix, etc. |
| `composer.json` | PHP — check for Laravel, Symfony, etc. |

**Extract the framework version** from lock files, config, or dependency specs. The version matters — framework APIs change between versions.

If `--framework` was provided, use that instead of auto-detecting.

Report what you found to the user: "Detected: **Django 5.1** (Python 3.12) in `PROJECTS/my-app/backend`"

## Phase 2: Explore Codebase for Concept Inventory

Read every significant source file in the codebase. Your goal is to build a **concept inventory** — the list of framework features and patterns actually used by this codebase.

### What to look for (by framework family)

**Web frameworks (Django, Rails, Flask, Express, etc.):**
- Models / ORM (field types, relationships, migrations, managers, querysets)
- Views / Controllers (function-based, class-based, generics, viewsets)
- URL routing / URL patterns
- Templates / template tags / template filters
- Forms / serializers / validation
- Middleware
- Authentication / authorization / permissions
- Admin interface / scaffolding
- Static files / media handling
- Signals / hooks / callbacks
- Background tasks (Celery, Sidekiq, etc.)
- WebSocket / Channels / real-time
- Caching
- Testing patterns
- Management commands / rake tasks / CLI
- Settings / configuration / environment

**Frontend frameworks (React, Vue, Angular, SwiftUI, etc.):**
- Component patterns (functional, class, hooks)
- State management (context, Redux, Vuex, etc.)
- Routing
- Data fetching / API integration
- Styling approach (CSS modules, Tailwind, styled-components)
- Form handling
- Testing patterns

**Systems frameworks (Actix, Axum, Gin, etc.):**
- Request handlers / extractors
- Middleware
- State management
- Serialization / deserialization
- Error handling patterns
- Database integration
- Authentication

### Output of this phase

A structured concept inventory like:

```
Concept Inventory for my-app backend (Django 5.1):
- Models: 12 models using CharField, ForeignKey, ManyToManyField, DecimalField, custom managers
- Views: Class-based views (ListView, DetailView, CreateView), DRF ViewSets
- URL routing: path() with app namespaces, include()
- Admin: Registered all models, custom ModelAdmin with list_display, search_fields
- Middleware: Custom auth middleware
- Signals: post_save signal for notifications
- Celery: 3 async tasks for email and PDF generation
- Settings: split settings (base/dev/prod), django-environ
...
```

Group concepts into **3-6 topic clusters** for the guide structure. Example clusters for Django:
1. "Models & Database" (fields, relationships, querysets, migrations)
2. "Views & URL Routing" (CBVs, FBVs, URL patterns)
3. "Templates & Static Files" (template language, tags, filters, static)
4. "Admin & Management" (admin site, management commands)
5. "Background Tasks & Signals" (Celery, signals, middleware)
6. "API Layer" (DRF serializers, viewsets, authentication)

Only create clusters for concepts the codebase actually uses. Skip what isn't there.

## Phase 3: Research Framework Documentation

For each concept cluster, research the official framework documentation. This is critical — you are writing an educational guide, not just describing code.

### Search strategy

For each concept in the inventory:

1. **WebSearch** for `"{framework} {version} {concept} documentation"` — e.g., "Django 5.1 class-based views documentation"
2. **WebFetch** the official docs pages found in search results
3. Extract: definitions, how-it-works explanations, available options/parameters, common patterns, gotchas

### What to extract from docs

For each concept:
- **What it is** — one-paragraph explanation
- **How it works** — the mental model (request lifecycle, ORM query building, etc.)
- **API surface** — the key classes, functions, arguments, and options
- **Reference tables** — field types and their options, built-in generic views, template tags, etc.
- **Common patterns** — idiomatic usage from the docs
- **Gotchas** — common mistakes, things that surprise newcomers

### Parallel research

Launch multiple Agent subagents in parallel to research different concept clusters simultaneously. Each agent should:
1. Search for docs on its assigned concepts
2. Fetch and extract relevant documentation
3. Return structured notes

**IMPORTANT:** Do not skip this phase. The guide must contain actual framework documentation, not just descriptions of the codebase. If web research is unavailable, tell the user and fall back to your training knowledge, but flag that the guide may lack version-specific details.

## Phase 4: Generate HTML Guide

Write a single self-contained HTML file: `{output}/{name}.html`

### Step organization

Each concept cluster becomes a multi-step section. Within each section, steps progress from foundational to advanced:

1. **Concept introduction** — what it is, why it exists, mental model
2. **Basic usage** — simplest example from the codebase, annotated with doc explanations
3. **Options & variations** — reference tables, parameters, alternatives
4. **Advanced patterns** — complex examples from the codebase, edge cases
5. **How this codebase uses it** — summary of all instances, patterns, conventions

Not every concept needs all 5 sub-steps. Use judgment — simple concepts (static files config) get 1-2 steps, complex ones (ORM, views) get 3-5.

### Content depth requirements

Each step MUST include:
- **Framework explanation** — teach the concept from the docs. Don't assume the reader knows anything about this framework.
- **Real code example** — actual code from the codebase (with file path), annotated to show which parts are framework API vs. application logic
- **Reference tables** where applicable — field types, built-in views, template tags, settings options, etc. Tables are high-value for framework learning.

### Content style

- **Teach the framework, not the codebase.** The codebase is illustration material.
- **No comparisons** with other frameworks. Don't say "like Express middleware" or "similar to Rails". Teach this framework on its own terms.
- **Direct instruction.** "Django models are Python classes that define database tables." Not "Let's explore how Django handles data."
- **Annotate code examples.** Use comments or prose to point out which parts are framework API calls vs. project-specific code.
- **Include reference tables.** When a concept has enumerable options (field types, generic view classes, template tags), include a table.

## HTML Template

The output is a single self-contained HTML file with this structure:

### Layout

1. **Sidebar** (fixed left, ~280px)
   - Project name + framework name at top
   - Collapsible section headers (concept clusters)
   - Numbered step list under each section
   - Current step highlighted
   - Scrolls independently

2. **Main content** (right of sidebar, scrollable)
   - Step number, section name, and step title
   - Prose + code snippets + tables
   - Code blocks with file-path tab label + dark syntax-highlighted code
   - `<details>` blocks for supplementary info (collapsed by default)
   - Previous / Next navigation buttons at bottom

3. **Progress bar** (fixed top)
   - "Step X of Y" with colored bar indicator

### Interactive behavior

- All steps rendered in DOM; navigation shows/hides via CSS
- Sidebar clicks, Prev/Next buttons, and Left/Right arrow keys navigate
- URL hash updates (`#step-3`) for bookmarking
- Jump to hash on load; default to step 1
- Sidebar auto-scrolls to keep active step visible
- Section headers in sidebar toggle collapse/expand of their step lists

### Visual design

- System font stack (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`)
- 18px body text, 1.7 line-height
- Light page background (`#f7fafc`), white content cards
- Dark code blocks (`#1a202c` background) with Prism.js "Tomorrow Night" theme
- Sidebar: light background (`#edf2f7`), subtle border-right
- Code blocks: rounded corners, file-path label as tab above code
- Progress bar: accent color (teal `#319795`)
- Tables: striped rows, sticky headers, full-width
- Responsive: sidebar collapses to hamburger menu below 768px
- Smooth transitions on navigation

### Syntax highlighting

Load Prism.js and relevant language component from CDN:
```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-{language}.min.js"></script>
```

Use the correct `language-*` class for code blocks. Match the codebase's actual language.

### HTML skeleton

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{Framework} Guide — {Project Name}</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
  <style>
    /* Reset */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      font-size: 18px; line-height: 1.7; color: #2d3748; background: #f7fafc;
    }

    /* Progress bar */
    #progress { position: fixed; top: 0; left: 0; right: 0; height: 40px; background: #fff;
      border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; padding: 0 20px;
      z-index: 100; font-size: 14px; color: #718096; }
    #progress-bar { height: 4px; background: #319795; position: absolute; bottom: 0; left: 0;
      transition: width 0.3s ease; }

    /* Sidebar */
    #sidebar { position: fixed; top: 40px; left: 0; bottom: 0; width: 280px; background: #edf2f7;
      border-right: 1px solid #e2e8f0; overflow-y: auto; padding: 20px 0; z-index: 90; }
    #sidebar h2 { font-size: 15px; padding: 8px 20px; color: #2d3748; margin: 0;
      border-bottom: 1px solid #e2e8f0; }
    .sidebar-section { margin-bottom: 4px; }
    .sidebar-section-title { font-size: 13px; font-weight: 700; color: #4a5568; padding: 10px 20px 4px;
      text-transform: uppercase; letter-spacing: 0.05em; cursor: pointer; user-select: none; }
    .sidebar-section-title::before { content: "▸ "; font-size: 11px; }
    .sidebar-section.open .sidebar-section-title::before { content: "▾ "; }
    .sidebar-section .step-list { display: none; }
    .sidebar-section.open .step-list { display: block; }
    .step-link { display: block; padding: 6px 20px 6px 32px; font-size: 14px; color: #4a5568;
      text-decoration: none; cursor: pointer; border-left: 3px solid transparent;
      transition: all 0.15s ease; }
    .step-link:hover { background: #e2e8f0; }
    .step-link.active { background: #fff; color: #319795; border-left-color: #319795; font-weight: 600; }

    /* Main content */
    #main { margin-left: 280px; margin-top: 40px; padding: 40px 60px 80px; max-width: 900px; }
    .step { display: none; }
    .step.active { display: block; }
    .step h1 { font-size: 28px; color: #1a202c; margin-bottom: 8px; }
    .step .section-label { font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em;
      color: #319795; font-weight: 700; margin-bottom: 4px; }
    .step h2 { font-size: 22px; color: #2d3748; margin: 32px 0 12px; }
    .step h3 { font-size: 18px; color: #4a5568; margin: 24px 0 8px; }
    .step p { margin: 12px 0; }
    .step ul, .step ol { margin: 12px 0; padding-left: 24px; }
    .step li { margin: 6px 0; }

    /* Code blocks */
    .code-block { margin: 16px 0; border-radius: 8px; overflow: hidden; }
    .code-block .file-path { background: #2d3748; color: #a0aec0; font-size: 12px;
      padding: 6px 16px; font-family: monospace; }
    .code-block pre { margin: 0; border-radius: 0; }
    .code-block pre code { font-size: 14px; line-height: 1.5; }

    /* Inline code */
    code:not([class*="language-"]) { background: #edf2f7; padding: 2px 6px; border-radius: 4px;
      font-size: 0.9em; color: #c53030; }

    /* Tables */
    table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 15px; }
    thead { position: sticky; top: 0; }
    th { background: #2d3748; color: #fff; padding: 10px 14px; text-align: left; font-weight: 600; }
    td { padding: 10px 14px; border-bottom: 1px solid #e2e8f0; }
    tr:nth-child(even) td { background: #f7fafc; }

    /* Details / expandable */
    details { margin: 16px 0; border: 1px solid #e2e8f0; border-radius: 8px; }
    summary { padding: 12px 16px; cursor: pointer; font-weight: 600; color: #4a5568;
      background: #f7fafc; border-radius: 8px; }
    details[open] summary { border-bottom: 1px solid #e2e8f0; border-radius: 8px 8px 0 0; }
    details > div { padding: 16px; }

    /* Navigation buttons */
    .nav-buttons { display: flex; justify-content: space-between; margin-top: 48px;
      padding-top: 24px; border-top: 1px solid #e2e8f0; }
    .nav-btn { padding: 10px 24px; border: 1px solid #e2e8f0; border-radius: 6px;
      background: #fff; color: #4a5568; font-size: 15px; cursor: pointer;
      transition: all 0.15s ease; text-decoration: none; }
    .nav-btn:hover { background: #edf2f7; border-color: #cbd5e0; }
    .nav-btn.primary { background: #319795; color: #fff; border-color: #319795; }
    .nav-btn.primary:hover { background: #2c7a7b; }
    .nav-btn:disabled { opacity: 0.4; cursor: default; }

    /* Hamburger menu for mobile */
    #menu-toggle { display: none; position: fixed; top: 8px; right: 16px; z-index: 110;
      background: #fff; border: 1px solid #e2e8f0; border-radius: 4px; padding: 6px 10px;
      font-size: 20px; cursor: pointer; }

    @media (max-width: 768px) {
      #sidebar { transform: translateX(-100%); transition: transform 0.3s ease; }
      #sidebar.open { transform: translateX(0); }
      #main { margin-left: 0; padding: 40px 20px 80px; }
      #menu-toggle { display: block; }
    }
  </style>
</head>
<body>
  <div id="progress">
    <span id="progress-text">Step 1 of N</span>
    <div id="progress-bar" style="width: 0%"></div>
  </div>

  <button id="menu-toggle" onclick="document.getElementById('sidebar').classList.toggle('open')">☰</button>

  <nav id="sidebar">
    <h2>{Framework} — {Project}</h2>
    <!-- Sections and step links generated here -->
  </nav>

  <main id="main">
    <!-- Step divs generated here -->
  </main>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-{language}.min.js"></script>
  <script>
    const steps = document.querySelectorAll('.step');
    const links = document.querySelectorAll('.step-link');
    const sections = document.querySelectorAll('.sidebar-section');
    let current = 0;

    function goTo(n) {
      if (n < 0 || n >= steps.length) return;
      steps[current].classList.remove('active');
      links[current].classList.remove('active');
      current = n;
      steps[current].classList.add('active');
      links[current].classList.add('active');
      // Open parent section
      sections.forEach(s => s.classList.remove('open'));
      links[current].closest('.sidebar-section').classList.add('open');
      // Scroll sidebar
      links[current].scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      // Progress
      const pct = ((current + 1) / steps.length * 100).toFixed(1);
      document.getElementById('progress-bar').style.width = pct + '%';
      document.getElementById('progress-text').textContent = `Step ${current + 1} of ${steps.length}`;
      // Hash
      history.replaceState(null, '', '#step-' + (current + 1));
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // Init
    links.forEach((link, i) => link.addEventListener('click', () => goTo(i)));
    document.querySelectorAll('.sidebar-section-title').forEach(t => {
      t.addEventListener('click', () => t.parentElement.classList.toggle('open'));
    });
    document.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight') goTo(current + 1);
      if (e.key === 'ArrowLeft') goTo(current - 1);
    });

    // Load from hash or start at 1
    const hash = parseInt(location.hash.replace('#step-', ''));
    goTo(isNaN(hash) ? 0 : hash - 1);
  </script>
</body>
</html>
```

**IMPORTANT:** This is the shell. You generate the actual sidebar sections, step links, and step content divs by filling in the template with your guide content. Every step div gets `class="step"` (first one also gets `class="step active"`). Every sidebar link gets `class="step-link"` (first active).

## Constraints

1. **Read before writing.** Read every significant source file in the codebase before generating the guide. Don't guess at what frameworks features are used — verify.
2. **Web research is required.** Fetch actual framework documentation for the detected version. The guide must contain real doc content, not just training-data summaries. If WebSearch/WebFetch fail, warn the user and proceed with training knowledge, flagging version-specific gaps.
3. **No filler.** Every step must teach something concrete. No "In this section we'll learn about..." preambles.
4. **Match snippet languages.** Use the correct Prism.js language class for all code blocks.
5. **Real code only.** Every code example must come from the actual codebase. Include the file path. Do not invent example code.
6. **No cross-framework comparisons.** Teach this framework on its own terms.
7. **Tables are mandatory** for any concept with enumerable options (field types, generic views, template tags, built-in middleware, settings, etc.).
8. **Complete coverage.** Every concept in the inventory must appear in the guide. Don't skip concepts because they're "advanced."
9. **Single file output.** The entire guide is one `.html` file. No external assets except CDN links for Prism.js.

## Output

1. Write the HTML file to `{output}/{name}.html`
2. Report to the user:
   - Framework and version detected
   - Number of steps generated
   - Concept clusters covered
   - Output file path
   - Any concepts where documentation was unavailable or incomplete
