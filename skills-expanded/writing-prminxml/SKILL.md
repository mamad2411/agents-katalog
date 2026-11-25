---
name: writing-prminxml
description: How to use the PRM-in-XML tool, information about the PRM-in-XML format for RISC OS documentation. Use when reading, writing, editing or reviewing API documentation for RISC OS, or when asked to create PRM-in-XML (or PRMinXML) documents. PRM-in-XML should be used for interface and external documentation.
metadata:
  author: gerph@gerph.org
license: MIT
allowed-tools: Bash(riscos-prminxml:*) Bash(host-open:*)
---
# PRM-in-XML

## Summary

PRM-in-XML defines documents in the style of the Programmer's Reference Manual
as XML. Those documents can then be converted to HTML and other output formats,
and are intended to remain machine-readable.

PRM-in-XML should be used for API and interface documentation. If asked to
create API or interface documentation, use PRM-in-XML by default.
Repository and implementation details should not use PRM-in-XML unless
explicitly requested; use Markdown for those instead. If asked to create a
`README.md`, always create Markdown.

## Tools

* Create a skeleton document: `riscos-prminxml -f skeleton -o <document>.xml`
* Convert a document to HTML: `riscos-prminxml -f html5+xml -O <directory> <document>.xml`
* Lint a document: `riscos-prminxml -f lint <document>.xml`
* Build an indexed manual set: `riscos-prminxml -f index index.xml`
* Help on the tool itself: `riscos-prminxml --help`

Never write HTML output to the same directory as the source XML with `-O`;
that would overwrite source files.
Create the output directory before using `-O`; the converter expects it to
exist already.

## Agent workflow

When using this skill:

1. Decide whether the task is PRM-in-XML at all.
2. Choose the smallest useful document shape for the request.
3. Read only the focused reference files needed for the task.
4. Edit or create the XML.
5. Lint the changed document or indexed set.
6. Build HTML output to confirm the structure renders correctly.
7. If the user wants to inspect the result, open it with `host-open`.

After creating or editing a PRM-in-XML document, always lint it and then build
the HTML version to confirm that the syntax and structure are correct.

Show the user generated documentation with `host-open output/html` or another
relevant built output directory once the result is ready.

## Core rules

* Write PRM documentation as authoritative user-facing guidance.
* Explain what the documented tool, interface, or workflow does, how it is
  used, and what constraints users must follow.
* Do not frame PRM documentation as a report about repository state, wrapper
  source, shipped help, or what another document currently says, unless the
  subject itself is repository layout or source format.
* When a limitation or special case matters, document it directly as supported
  behaviour or a workflow boundary.
* For component or interface documents, ensure the `Overview` section explains
  why the component exists and how it relates to other components.
* For component or interface documents, ensure the `Technical Details` section
  explains how the component is used and what its interfaces mean.
* For multi-file manuals, do not force every chapter into the same heading
  template. Workflow, reference, and appendix chapters may use different
  structures when that makes the manual clearer.
* Appendix chapters may begin with `Overview`, but do not need an `Examples`
  section unless worked examples materially improve the appendix.
* When creating a multi-file manual set intended to read as a book, prefer an
  indexed collection with a local `index.xml`, front matter, and a `Makefile`
  that can build both per-chapter HTML and the indexed collection.
* The metadata section should be updated with each major change. Populate the
  visible author or maintainer details with the user's full name where the
  document format expects that information.
* When converting an existing document set into PRM-in-XML, preserve the
  original document history and authorship in `<history>` where the source
  material provides it; the conversion revision should not erase earlier
  protocol or manual releases.
* When a converted source has substantial rationale or background material,
  prefer separate `Introduction` and `Overview` sections rather than forcing
  everything into `Introduction and Overview`.
* Canonical conversions should retain not just the final interface reference
  facts, but also important rationale, motivating examples, and workflow
  guidance from the original document when those explain how the interface is
  intended to be used.

## Routing

Read the focused reference file that matches the task:

* Document shape, chapter structure, prose rules, basic XML skeleton,
  paragraphs, lists, examples, cross-references, inline elements, and entities:
  [references/document-structure.md](references/document-structure.md)
* SWI, service, system-variable, VDU, star-command, and `<reference>` details:
  [references/definitions-and-references.md](references/definitions-and-references.md)
* Indexed manual sets, `index.xml`, metadata, and local `Makefile` patterns:
  [references/indexed-manual-sets.md](references/indexed-manual-sets.md)
* BNF, table elements, common lint failures, conversion guidance, and quick
  reference material:
  [references/tables-and-troubleshooting.md](references/tables-and-troubleshooting.md)
* Existing-document review for accuracy or publication readiness:
  [references/documentation-review.md](references/documentation-review.md)
* Publishing PRM-in-XML output through GitHub Actions:
  [references/github-ci.md](references/github-ci.md)

Prefer reading only the references needed for the current task rather than
loading the entire reference set.

## Primary source documents

The PRM-in-XML XML format is described in:
`/riscos-resources/Install/Tools/Linux/riscos-prminxml-resources/docs/PRMinXML.txt`

General authoring guidance is in:
`/riscos-resources/Install/Tools/Linux/riscos-prminxml-resources/docs/HowTo.md`

The DTD used by PRM-in-XML 1.03 is:
`/riscos-resources/Install/Tools/Linux/riscos-prminxml-resources/gerph/103/prm.dtd`

## Validation

For single-document work, the normal validation loop is:

* `riscos-prminxml -f lint <file>.xml`
* `riscos-prminxml -f html5+xml -O <output-dir> <file>.xml`

For indexed manual sets, lint and build the index as well:

* `riscos-prminxml --lint -f index -L <log-dir> index.xml`
* `riscos-prminxml -f index -L <log-dir> index.xml`
