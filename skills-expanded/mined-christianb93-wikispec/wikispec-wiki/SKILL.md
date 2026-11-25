---
name: wikispec-wiki
description: This skills instructs the agent how to maintain the knowledge base in the wiki. Use it when you want to ingest documents or query the wiki
---

# LLM Wiki Schema

A knowledge base that helps humans and agents to maintain the code base, to understand designs, technical concepts, key features and key dependencies. 

## Overview

This wiki synthesizes knowledge built while working on the code in this software project. It focuses on key relations, concepts and facts and organizes for use by coding agents and human developers.

You maintain the wiki incrementally. When sources need to be ingested you read them, extract key concepts, and integrate them into the existing structure. The wiki becomes richer with every addition.

## Directory Structure

This wiki is part of the overall wikispec structure.


```
wikispec/             ← the wikispec root directory, located in the project root
├── changes/
│   ├── active/       ← changes currently in progress
│   └── archived/     ← completed and archived changes
└── wiki/             ← the wiki - these instructions focus on how to maintain this
    ├── <topic 1>/    ← documentation for one topic
    ├── .../
    ├── <topic n>/
    ├── log.md        ← append-only log of operations on the wiki
    └── index.md      ← index page
```

## Wiki topics

The wiki is organized in topics, that correspond to subdirectories of `wikispec/wiki`. You can use the `wikispec` CLI that exists in the path (no need to install) to understand which topics exist. Running

```
wikispecs topics 
```

returns a JSON structure with a list of all topics and their description.

## Operations

### Ingest a change

When a change needs to be a ingested, follow these steps.

1. **Understand the change**

  - locate specification, design and tasks for this change by running `wikispec files --change`. This will return a list of specification, design documents and tasks that describe the change
  - look at the tasks and design documents to determine which source files have been added or changed as part of this change
  - Read them. Understand the change 

2. **Determine impact on wiki**

  - run `wikispec topics` to get a list of existing topics and their descriptions
  - identify topics which could be impacted by this change, using your own judgement and the instructions printed by the `wikispec topics` tool
  - look at the files in the directory (pages) and identify which pages need to be updated or created


3. **Update or create pages.** 

   - Author changes to existing pages 
   - Add new pages as needed
   - feel free to restructure, split or remove pages if you feel that this makes it easier to capture the new and updated content in a clear and concise manner
   - you MUST follow the writing style guidelines below when changing or creating pages
   - add links (use Wikilink style `[[linked page]]`) where meaningful

4. **Update index.** 
    - Add entries to the index or update existing entries in `index.md` entry for each changed page or added page
    - each entry is a short summary of the page
    ```
    ## Topic: <topic>, page <page name as file name>
    Content:  <summary of page content, not more than five sentences, focus on key insights
    ```

5. **Log the ingest.** Append an entry to `log.md`:
   ```
   ## [2026-05-09] ingest | <change name>
   - New pages: <pages>
   - Updated pages: <pages>
   ```

### Writing guidelines

Focus on key facts - what would a developer need to know as a starting point to understand the codebase, its structure, the functionality of the systems and its architecture? The wiki is a starting point for building an understanding of the code, **not** a comprehensive reference full of details.

To add links between pages, use the wikilink syntax, i.e. `[[target page]]`. 

Unveil dependencies, structures and key decisions. Think about the things that are **not** obvious but important and document them. 

Bad habits:

- copy code into the wiki
- copy, replicate or reference individual requirements or test cases - the wiki should focus on the structure and behaviour of the code, not on tests or exact requirements


Good habits:

- be concise
- make sure to add references so that a developer can use wiki pages as starting point and dig deeper if required


Examples:

- instead of listing all packages that the project uses, explain which package manager we use and where its configuration is stored so that a developer can look up the details there
- instead of describing each field in an endpoint, explain what the endpoint does and which modules it invokes, this will allow a developer to quickly locate the code that contains the actual field list


### Query

You can query the wiki for information 

1. **Search the wiki.** Read `index.md` to find relevant pages.
2. **Synthesize.** Read relevant pages, identify connections, pull together an answer.
3. **Format answer.** Depending on the question:
   - Markdown explanation with citations
   - Comparison table
   - Concept map (markdown or description)
   - Slide deck (Marp) for presenting ideas


## Index and Log

### index.md

A catalog of everything in the wiki. Organized by category. Updated on every ingest.

**Format:**

```markdown

## Topic: <topic 1>, page <page name as file name>
Content:  <summary of page content, not more than five sentences, focus on key insights

## Topic: <topic 2>, page <page name as file name>
Content:  <summary of page content, not more than five sentences, focus on key insights
```



### log.md

An append-only record. Each entry is a single line (or a few for detailed ingests). Parseable with grep.

**Format:**

```markdown
# Log

## [2026-05-09] ingest | <change>
- Pages created: wiki/architectures/server.md, wiki/deployment/hosting.md
- Pages updated: wiki/architecture/layers.md

```
