# Greenhouse Agent Instructions

This document provides context and patterns for AI agents working in the Greenhouse codebase. Greenhouse is an Elixir-based blog engine/static site generator designed to replace `simple_blog_engine`. It utilizes a declarative data pipeline architecture powered by the `orchid` library.

## Project Architecture & Core Concepts

- **Data Pipeline Architecture**: The core build process is orchestrated as a Directed Acyclic Graph (DAG) using the `orchid` library. 
- **Recipes**: The workflow graph is defined as an `Orchid.Recipe`. The main build recipe is located in `lib/greenhouse/pipeline/recipe.ex`.
- **Steps**: Pipeline execution is divided into atomic steps. Steps can be module-based (implementing `Orchid.Step`) or function-based (2-arity functions).
  - You can find content loading steps in `lib/greenhouse/pipeline/content_steps.ex`.
  - Rendering and export steps: `Greenhouse.Pipeline.LayoutSteps` renders posts/pages HTML; `Greenhouse.Pipeline.MediaExportStep` copies raw files (images, PDFs) to output; `Greenhouse.Pipeline.IndexSteps` renders paginated index pages and taxonomy aggregations; `Greenhouse.Pipeline.AssetSteps` copies static assets (CSS, JS); `Greenhouse.Pipeline.DeployStep` pushes built output to a git remote.
  - `Greenhouse.Steps.MarkdownToHTML` converts Markdown to HTML via Pandoc (with bibliography support), producing `doc_struct` on each content item.
  - `Greenhouse.Pipeline.TaxonomyStep` extracts tags, series, and categories from posts.
  - `Greenhouse.Media.MediaLoader` uses `Orchid.Step.NestedStep` to compose image/PDF/SVG loading as a nested sub-recipe.
  - A step receives and returns data wrapped as Orchid parameters.
- **Orchid Knowledge Base**: This repository contains a detailed internal skill for Orchid workflows. **If you need to create or modify pipeline steps, recipes, hooks, or nested workflows, always refer to `.agent/skills/elixir-orchid-workflow/SKILL.md` first.**

## Key Components

- **Pipeline (`lib/greenhouse/pipeline/`)**: Contains recipes and steps that dictate the static generation workflow. The build recipe (`recipe.ex`) chains steps in this order: load posts/pages → load media → replace internal links → Markdown-to-HTML conversion → taxonomy extraction → layout rendering → media export → index/taxonomy page rendering → static asset copy → git deploy.
- **Content (`lib/greenhouse/content/`)**: Modules for parsing and loading raw source materials from the filesystem.
  - `FileDoc` — base struct (`id`, `created_at`, `updated_at`, `body`, `metadata`) for any parsed content file.
  - `Post` / `Page` — domain structs extending `FileDoc` with `title`, `route_path`, `doc_struct`, etc.
  - `PostsLoader` / `PagesLoader` — Orchid steps that discover and parse `.md` files from source directories.
- **Layout (`lib/greenhouse/layout/`)**: View helpers and UI components. Uses `phoenix_html` and `tailwind`. `View` renders EEx scaffold templates from `priv/layout/`.
- **Asset (`lib/greenhouse/asset/`)**: Media handling and loading.
  - `Media` — behaviour and structs for different media types (image, PDF, SVG/dot), each with `file_path`, `route_path`, and `file_type`.
  - `MediaLoader` — a nested Orchid recipe (`Orchid.Step.NestedStep`) that discovers images, PDFs, and SVGs, then merges them into a unified `media_map`.
- **Cite (`lib/greenhouse/cite/`)**: Replaces markdown links to internal resources/media with correctly resolved HTML links.
  - `Link` — canonical link conversion (`convert/1`).
  - `ContentReplacer` — bulk link rewriting across content maps.
- **Taxonomy (`lib/greenhouse/taxonomy/`)**: Builds relations for categories, tags, and series.
  - `Builder` — generic grouping logic (`posts_map_into_tags/1`, etc.).
  - `Tags` / `Categories` / `Series` — specialized taxonomy modules.
- **Theme/Render Engine (`lib/greenhouse/theme.ex`)**: A pluggable theming system. The rendering layer is entirely decoupled from the Orchid pipeline via the `Greenhouse.Theme` behaviour. Themes are configured dynamically via step options in `Greenhouse.Pipeline.LayoutSteps`.
  - `Greenhouse.Theme.Default` — base theme using EEx templates.
  - `Greenhouse.Theme.MobileFriendly` — responsive theme with Tailwind/DaisyUI, currently used in the production recipe.
  - Both use EEx templates (not LiveView/HEEx) to keep the engine lightweight. Pandoc-processed HTML is injected from `post.doc_struct.body`.
- **Bibliography (`lib/greenhouse/bibliography.ex`)**: Provides bibliography/citation support. Reads Pandoc metadata for `bibliography` and `csl` fields; defaults to Chinese national standard (GB7714) numeric style.
- **Storage (`lib/greenhouse/storage.ex`)**: ETS-backed key-value store implementing the `Orchid.Dehydration` contract. Used for checkpoint/recovery during long pipeline runs.
- **Monitor (`lib/greenhouse/monitor/`)**: Development-time live-reload subsystem.
  - `DevServer` — Plug-based static file server with SSE endpoint (`/sse`) for browser live-reload.
  - `Watcher` — GenServer wrapping `FileSystem` to watch source directories (`_posts/`, `img/`, `pdf/`, `src/`, `_bibs/`) and trigger full Orchid rebuilds on change.
  - `Broadcaster` — simple PubSub GenServer that fans out `{:reload, data}` messages to SSE-connected clients.
- **Orchid Extensions (`lib/orchid/`)**: The project extends the base `orchid` library with local helpers in the `Orchid` namespace (e.g., `Orchid.ParamFactory`, `Orchid.Steps.Helpers`, `Orchid.Visualizer`, `Orchid.TelemetryReporter`).
- **Helpers (`lib/greenhouse/helpers.ex`)**: Utility modules — `PathUtils` for cross-platform path normalization (Windows drive-letter downcasing), `FlatFiles` for recursive directory listing.
- **External Tool Integrations**:
  - `Pandox` (`lib/pandox.ex`) — wrapper around the Pandoc CLI; extracts args from front-matter metadata, manages Lua filters and CSL files from `priv/`.
  - `Lilypond` (`lib/lilypond.ex`) — wrapper around the LilyPond CLI for converting `.ly` music notation files to SVG.
- **Mix Tasks (`lib/mix/tasks/greenhouse/`)**: Custom Mix tasks.
  - `mix greenhouse.new_post` — scaffolds a new Markdown post with front-matter (title, tags, categories, series, date).

## Essential Commands

- **Dependencies**: `mix deps.get`
- **Testing**: `mix test`
- **Formatting**: `mix format`
- **Running the Demo**: `mix run demo_for_local.exs` (Note: This script has hardcoded paths to `D:/Blog/source` and is used to test the pipeline locally).
- **Creating a Post**: `mix greenhouse.new_post "Post Title" --tags a,b --categories misc`

## Conventions and Gotchas

- **Orchid Params**: Remember that Orchid step inputs and outputs aren't bare Elixir types; they are wrapped in `Orchid.Param`. When writing function steps, expect inputs like `%Orchid.Param{payload: data}` and return `{:ok, Orchid.Param.new(:name, :type, result)}` or use `Orchid.ParamFactory.to_param(result, :type)`.
- **NimbleOptions Validation**: Steps often validate their options using `NimbleOptions` (e.g., in `ContentSteps.load_posts/2`). Be sure to define schemas for any new step options.
- **Drop Native Orchid Opts**: Before validating step options with `NimbleOptions`, filter out Orchid's internal options by calling `Orchid.Steps.Helpers.drop_orchid_native(step_options)`.
- **Pluggable Themes**: When rendering HTML, the pipeline uses `Greenhouse.Pipeline.LayoutSteps`. Do not hardcode HTML rendering logic in pipeline steps. Instead, implement a module using the `Greenhouse.Theme` behaviour, and pass it to the step options (e.g., `theme: Greenhouse.Theme.MobileFriendly`). Both themes use EEx templates (not LiveView/HEEx). Pandoc-processed HTML is injected from `post.doc_struct.body`.
- **Routing and Links**: When generating routes or paths to save HTML on disk, use `Greenhouse.Cite.Link.convert/1` to ensure consistency. Use `Path.join(output_dir, rel_path)` instead of absolute filesystem overrides.
