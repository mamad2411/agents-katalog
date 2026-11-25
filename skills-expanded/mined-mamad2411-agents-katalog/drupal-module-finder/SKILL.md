---
name: drupal-module-finder
description: Find, evaluate, and install Drupal contributed modules by describing the problem to solve. Use whenever the user needs a Drupal module for a task, wants module recommendations or comparisons, or needs the composer command to install one.
---

# Drupal Module Finder

Use the `drupal-module-finder` CLI to find the right Drupal contributed module for a
need, learn about it, and get the composer command to install it.

A copy of the command is bundled in this skill directory. Run it as
`./drupal-module-finder` from here, or just `drupal-module-finder` if it is on your
PATH. All output is raw Markdown. Target a different site with `--host=<url>`
(default: http://module-finder.ddev.site).

## Always check what is already available first

Before searching for or recommending a new module to download, prefer what the
project already has:

1. **Drupal core modules** — if core already provides the capability, recommend
   enabling the core module rather than installing a contributed one.
2. **Already-downloaded modules** — modules already present in the codebase (e.g.
   under `web/modules/contrib` and `web/modules/custom`, or listed in the
   project's `composer.json`) but not yet enabled. Recommend enabling one of
   those before adding a new dependency.

Only fall through to the search workflow below when neither Drupal core nor an
already-downloaded module covers the need.

## Workflow

### 1. Search by describing the problem
Describe WHAT needs to be solved. Do **not** put the word "module" in the query —
that is implied.

    drupal-module-finder semantic-search "send private messages between users"

**One focused need per search.** Each search must target a single capability —
never a whole product or a broad goal. If the user asks for something large like
"I want to build Facebook", split it into individual needs and run a separate
search for each, one at a time:

    drupal-module-finder semantic-search "send private messages between users"
    drupal-module-finder semantic-search "poke or react to other people's profiles"
    drupal-module-finder semantic-search "news feed of friends' activity"

Run them sequentially (one request at a time) and evaluate each result set on its
own. A broad, multi-feature query returns poor matches; a single, specific need
returns good ones.

- Returns up to 10 candidate modules ranked by semantic relevance.
- Each candidate shows: title and **data name** (in parentheses), a summary, the
  relevance score, and meta data (data name, project URL, development status,
  security coverage, stars, project usage, latest release, agentic skills, and
  Drupal version coverage).
- Add `--chunk=true` to also show the best-matching text excerpt per candidate.
- If nothing fits, rephrase the problem and search again.

### 2. Investigate the candidates
For any promising candidate, use its **data name** (the value in parentheses, e.g.
`Privatemsg (privatemsg)` -> `privatemsg`) to get the full details:

    drupal-module-finder module-info privatemsg

Add `--all` for every field, or `--fields=stars,project_usage` to focus on a few.

### 3. Get the install / composer command
Once a module looks right, get its releases and composer commands:

    drupal-module-finder release-info privatemsg

Then give the composer command to the user (e.g. `composer require 'drupal/privatemsg:^4.0'`).

## All commands

| Command | What it gives you |
| --- | --- |
| `semantic-search "<problem>" [--chunk=true]` | Ranked candidate modules for a described need. Start here. Never cached. |
| `module-info <data_name> [--all] [--fields=...]` | A module's summary + meta data. `--all` = every field; `--fields=` = only the listed fields (drop the `field_` prefix, e.g. `stars`, `module_categories`; `title` is allowed). |
| `release-info <data_name>` | Releases with their composer commands. Use this to install. |
| `documentation-info <data_name>` | Link to the module's external documentation (or "No documentation found"). |
| `readme <data_name>` | The module's README (or "No readme found"). |
| `file-structure <data_name>` | The module's file/folder structure. |

## Fields

`module-info <data_name> --fields=...` accepts these names (comma-separated, no
`field_` prefix). The same names are the labels you will see in the output.

| Field | Label | Notes |
| --- | --- | --- |
| `title` | Module Name | The node title. |
| `data_name` | Data Name | Drupal.org machine name (used in every command). |
| `module_summary` | Module Summary | Short human summary. |
| `module_description` | Module Description | Longer description. |
| `module_readme_text` | Module Readme Text | Full README (see also `readme`). |
| `documentation` | Documentation | Documentation text. |
| `external_information` | External Information | External docs link (see also `documentation-info`). |
| `link_to_module` | Link to Module | Project URL. |
| `module_categories` | Module Categories | e.g. Access Control, AI, Automation. |
| `module_development_status` | Module Development Status | e.g. Actively Maintained, Unsupported. |
| `development_status` | Development Status | e.g. Under Active Development, Obsolete. |
| `security_covered` | Security Covered | Covered / Not Covered. |
| `drupal_version_coverage` | Drupal Version Coverage | e.g. Drupal 10, Drupal 11. |
| `has_agentic_skills` | Has Agentic Skills | Whether the module ships agentic skills. |
| `stars` | Stars | Star count. |
| `project_usage` | Project Usage | Number of sites reporting use. |
| `latest_release_date` | Latest Release Date | Date of the latest release. |
| `latest_update` | Latest Update | Last update date. |
| `latest_module_releases` | Latest Module Releases | Release titles (full detail via `release-info`). |
| `module_maintainers` | Module Maintainers | Maintainer names. |
| `supporting_organizations` | Supporting Organizations | Backing organizations. |
| `module_affordances` | Module Affordances | What the module lets you do. |
| `file_structure` | File Structure | File/folder layout (see also `file-structure`). |
| `full_vector_search` | Full Vector Search | Aggregated text used for semantic search (large). |

Example:

    drupal-module-finder module-info privatemsg --fields=stars,project_usage,security_covered,drupal_version_coverage

Use `--all` to dump every field at once (releases expanded).

### How they help an evaluation
- **semantic-search** narrows the field fast from a plain-language description.
- **module-info** confirms fit: maintenance and security status, Drupal version
  coverage, plus usage and stars as trust signals.
- **release-info** gives the exact composer command and version constraints.
- **readme** and **documentation-info** explain setup and configuration.
- **file-structure** reveals submodules and what ships in the package.

## Options
- `--host=<url>` — point at a different Module Finder site.
- `--chunk=true` — (semantic-search) include the best-matching excerpt.
- `--all`, `--fields=` — (module-info) control which fields are shown.

## Shell completion (bash)

Enable TAB completion for subcommands, options, `--fields=` values, `--agent=`
values, and any module data names you have already cached:

    source <(drupal-module-finder completion bash)

Add that line to your `~/.bashrc` to make it permanent. Completion is registered
for the `drupal-module-finder` name on your PATH; running it as
`./drupal-module-finder` will not auto-complete.

## Tips
- Always search with a problem description — never a module name, and never the
  word "module".
- Carry the **data name** from the search results into every follow-up command.
- Prefer modules that are actively maintained, security-covered, and cover the
  user's Drupal version.
