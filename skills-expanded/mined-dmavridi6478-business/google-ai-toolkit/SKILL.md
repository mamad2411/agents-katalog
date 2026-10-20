---
name: google-ai-toolkit
description: Directory of 11 free Google AI tools mapped to use case (Imagen/Nano Banana for images, Nano Banana Editing for image refinement, Veo for video, Gemini Live for live screen-share collaboration, Gemini in Google Sheets for spreadsheet analysis, Gems in Gemini for reusable task-specific assistants, Gemini Ask on YouTube for video Q&A, NotebookLM for research-to-learning, Google AI Studio for model/prompt testing, Firebase Studio for build-and-launch, Google App Builder for no/low-code apps), plus a 4-part usage guide (choose-the-right-tool map, 5 reusable prompt patterns, quality/safety checks, and a 4-step workflow blueprint). Use when picking a free Google AI tool for a specific job (image/video generation, spreadsheet work, live demos, research synthesis, prototyping, app-building), or when asked "what's the Google equivalent of X."
---

# Google AI Toolkit (Free)

Source: reviewed from an uploaded infographic — "Top 11 Free AI Tools
from Google" (smarterwithai.news). Tool names, use cases, and outputs are
as described in the source; verify current availability/pricing tier
before relying on any of them for client-facing work, since Google's free
tiers and tool names shift often (this space moves faster than most).
`notebooklm-skill` in this repo already vendors real automation for one
of the 11 (NotebookLM) — see that skill for actual working commands
rather than this entry's use-case description.

## The 11 tools, mapped to use case

| Tool | Best for | Output | Tip |
|---|---|---|---|
| **Imagen / Nano Banana** | Slides, thumbnails, quick concept art — images from short prompts | Still images, variations | Specify style + composition + lighting in one line |
| **Nano Banana (Editing)** | Refining/editing AI images into new variations — brand polish, iterations, compositing | Improved variants, edits | Say "keep same layout" + specify exactly what to change |
| **Veo (Video Gen)** | Explainers, b-roll concepts, storyboards — video clips/animations from text | Short clips, scenes | Define camera + scene + motion cues explicitly |
| **Gemini Live (Stream)** | Live AI chats with screen sharing — demos, workshops, stakeholder Q&A | Real-time answers + actions | Give it an agenda → decisions → next-steps structure |
| **Gemini in Google Sheets** | Spreadsheet text/formula/insight generation — analysis, cleanup, reporting | Formulas, summaries, patterns | Ask for "formula + explanation + edge cases," not just the formula |
| **Gems in Gemini** | Task-specific assistants built from files + instructions — repeatable workflows, team standards | Reusable expert agents | Define scope, inputs, and output format up front |
| **Gemini Ask on YouTube** | Chatting with a video for answers, chapters, key insights — fast learning, extracting takeaways | Summaries, timestamps, quotes | Ask for "3 takeaways + 5 quotes + a timeline" |
| **NotebookLM** | Turning sources into summaries, mind maps, quizzes, overviews — research to learning | Structured notes + Q&A | Upload 3-7 sources for higher coherence (see `notebooklm-skill` for real automation) |
| **Google AI Studio** | Testing models, tuning settings, comparing prompts side by side | Best-performing prompt recipes | Track temperature + system instructions per test |
| **Firebase Studio** | Quickly building and launching apps/websites with AI — MVPs, internal tools, prototypes | Deployed app + backend | Start from user stories + a data model, not a blank canvas |
| **Google App Builder** | No/low-code apps from prompts/templates — internal workflows, forms, dashboards | Working UI + logic | Start with fields, roles, and approval steps |

## A) Choose the right tool

Match the verb to the tool family, not the other way around:

- **Create** → Imagen, Veo, Nano Banana (Editing)
- **Learn** → NotebookLM, Gemini Ask on YouTube
- **Build** → Firebase Studio, Google App Builder, Gems in Gemini
- **Analyze** → Gemini in Google Sheets, Google AI Studio
- **Present** → Gemini Live, Imagen

## B) 5 reusable prompt patterns

Apply these to any of the 11 tools, not just one:

1. **Role + Goal + Constraints + Format** — the baseline structure for
   almost any prompt to any of these tools.
2. **Provide examples → ask for variant 1/2/3** — get several candidate
   outputs before picking one, rather than accepting the first result.
3. **Demand structure** — table / bullets / JSON, whichever the
   downstream use actually needs, stated explicitly rather than left to
   the tool's default formatting.
4. **Ask for a checklist → risks → assumptions** — surface what the
   output is assuming and what could go wrong, not just the output
   itself.
5. **Iterate: draft → critique → improve** — treat the first output as a
   draft to critique and refine, not a final answer.

## C) Quality & safety checks

- **Verify facts from sources** — NotebookLM citations when possible,
  rather than trusting an ungrounded generation.
- **Red-team prompts for edge cases** — check what breaks the output
  before shipping it, not after.
- **Sensitive data: never paste secrets** — API keys, credentials,
  customer PII don't belong in a prompt to a cloud AI tool.
- **Consistency: reuse a single style guide prompt** across a project
  instead of re-describing style/tone/constraints from scratch each time.

## D) Workflow blueprint

1. **Explore** — Google AI Studio: iterate on the prompt/model/settings
   until something works.
2. **Produce** — the tool-specific step (Sheets, Veo, Imagen, Firebase
   Studio, whichever matches the job).
3. **Package** — Sheets / Gemini Live / Assets: turn the raw output into
   something shareable or presentable.

Micro note from the source: save working prompts as reusable playbooks
rather than re-deriving them each time — the same discipline this repo's
`resume-prompt-kit` and `one-person-*` skills apply to their own prompt
sets.

## Related skills in this repo

- **notebooklm-skill**: The one tool in this table with real, working
  automation already vendored in this repo — use that skill's CLI
  commands instead of manually driving the NotebookLM web UI.
- **design-dev-resources**: Complementary free-tool directories (design
  assets, dev tools, AI prompt-discovery libraries) — this one is
  specifically Google's own free AI product line.
- **claude-code-tooling**: The Claude-Code-specific equivalent of this
  directory pattern — external tools worth knowing about, not skills to
  load.
- **ai-video-image-prompt-structure**: The 6-part prompt structure there
  generalizes this skill's "Role + Goal + Constraints + Format" pattern
  (B.1) specifically for image/video generation tools like Imagen/Veo.
