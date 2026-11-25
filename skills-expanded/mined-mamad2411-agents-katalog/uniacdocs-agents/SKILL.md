# UniacDocs

The documentation for Uniac, a cloud deployment platform: the Mintlify project
behind docs.uniac.ai, and the only written copy of every public product fact.
The public `uniac` agent skill ([uniac-ai/agent-skills](https://github.com/uniac-ai/agent-skills))
compresses these pages and links to them; this repository holds nothing for
it, and Mintlify's generated `skill.md` is Mintlify's own.

## Ownership

- Product facts, examples, headings and links: the `.mdx` pages.
- Website navigation, redirects and theme: `docs.json`. Its groups provide
  navigation independently of the pages' links.
- The visual skin: `custom.css`, `logo/`, `favicon.png`.

The overview (`index.mdx`) and the resource pages own the platform model,
capabilities, lifecycle effects and limits. The composition and CLI pages own
YAML fields, commands, accepted values, defaults and output, and refer to the
resource pages for platform behavior: an interface omission or default is
stated as such, never as a platform restriction. The setup and quickstart
pages demonstrate those contracts and link to their owners. The CLI reference
states the CLI release it describes.

## Writing

State what the current release does. A limit appears only as a specification value, in the field table or command contract it constrains: an accepted value, a range, a quota or a requirement. Overviews, explanations and examples describe what works. Negative wording ("cannot", "no", "not supported", "does not") is reserved for a deliberate design constraint, such as a singleton's single replica or a volume's single holder. Pages name no feature the platform lacks and say nothing about future releases.

Write for a capable coding agent. Keep Uniac-specific facts: schema,
prerequisites, effects, limits, and behavior. Review document boundaries,
sections, and paragraphs before individual sentences. Each passage should
explain one concern coherently, with the context needed to understand it.
Judge each document against the outcome promised where readers enter it.
Then check its sentences, tables, and examples for directives and information
derivable from retained facts. Remove repeated explanations and constructed
procedures while preserving their independently useful premises. Operations
state their required inputs and effects, referencing the concepts that own
those inputs. The quickstart illustrates these contracts; missing prerequisites
or relationships are repaired in their owning page. Its example order applies
to its stated starting conditions, not to every task.

Describe what commands, files, and the platform do. A directive is justified
only by an essential user-experience requirement that the agent cannot infer
from those facts. State its concrete reason. First check whether the missing
knowledge is a prerequisite or side effect, and document that instead.
Permission, communication, and execution policies belong to the agent's
managing layer. Product confirmation controls are facts about the interface.

The overview develops the system model — including what runs and how reusable
definitions become running instances — before the composition format and the
CLI; a glossary or topic catalog does not establish those relationships. The
overview, composition and resource pages describe the system independently of
the CLI and link only to each other; links among the setup, quickstart and CLI
pages form no cycle. Resource pages distinguish required and optional
configuration from examples in a composition language. Keep topics normally
needed together in one page with sections; separate pages serve independently
useful questions. Brief restatement and cross-links between composition and
resource examples are useful when they let each page be understood in
context; full contracts still have one owner. Authentication owns credential
acquisition, renewal, selection, and status semantics; commands that use
credentials inherit that contract. Conditional requirements stay with the
operation that needs them, rather than becoming default setup steps.

Pages link each other by site route (`/cli/overview`, `/resources/service#public-endpoints`).
Use actual field names and established terms. Remove generic advice, invented
labels, failure stories, and repetition that does not help understanding.
Project-specific instructions belong in the customer's project; public
contracts remain here rather than copied into customer `AGENTS.md`.

## Verification and publication

Verify command and schema contracts against the released CLI, and platform
effects at the deployed implementation that applies them; schema acceptance
and CLI output do not establish runtime behavior. Keep output contracts
independent of display layout: the CLI pages own command arguments, flags,
defaults and parsing rules, and document actual release behavior in one place,
including reserved codes and limitations, rather than a general rule followed
by contradictory exceptions.

Run `mint validate` and `mint broken-links` (Node 20.17+) before opening a
pull request; CI runs both on every pull request and push to `main`. Pushes to
`main` deploy through the Mintlify GitHub app, whose "Mintlify Deployment"
check on the commit reports the result. Changes use a worktree and PR; the
Uniac engineering skills own that workflow.
