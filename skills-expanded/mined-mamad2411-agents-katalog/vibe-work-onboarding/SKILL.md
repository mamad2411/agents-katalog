Onboarding — Discover Vibe Work

When to use

Activate when the user onboards on Work mode or asks "what is Work", "what can you do" or clicks "Setup and Discover what Work can do" from the home page, or is redirected from the welcome modal.

Flow

Run this whole onboarding sequence as one continuous assistant turn. Do not stop after any explanatory text and wait for a normal chat reply. The only allowed pauses for user input are the programmatic callback cards created by askEnableConnector, askEnableSkill, and askUserQuestion. When a callback returns, immediately continue with the next step in the same flow.

User-facing text is mandatory. The first visible assistant output must be the welcome text from Step 1, not a thought and not a tool call. Before every run_typescript call in this flow, emit a short visible assistant text chunk that explains what the next action is for. Do not put these explanations inside TypeScript. Never show connector, Skill, or task-choice cards without first explaining them in plain language. Translate all user-facing text into the language used by the user.

Do not inspect connector README files, saved JSON files, or the filesystem to discover connectors during onboarding. Use only listAvailableConnectors({}) for connector discovery. Do not say "let me read" or "let me inspect" before the welcome message.

Programmatic functions

These functions are available from run_typescript. When this skill says to call one, execute TypeScript and await the function; do not merely mention the function name in assistant text.

````typescript
const { connectors } = await listAvailableConnectors({});

const { connectedConnectorIds, deniedConnectorIds } =
  await askEnableConnector({ connectorIds });

const { enabledSkillIds, deniedSkillIds } =
  await askEnableSkill({ skillIds });

const [selectedTask] = await askUserQuestion({
  questions: [
    {
      question: "What would you like to try first?",
      options: [
        "Deep research on a topic",
        "Summarize my unread emails and draft responses",
        "Brief me for my next meeting",
      ],
    },
  ],
});
````

Step 1: Welcome

Emit this visible message as normal assistant text before any TypeScript or file/tool inspection, then continue directly to connector setup without waiting for a reply:

"Welcome to Work mode. I can help with longer tasks across your tools, like summarizing inboxes, drafting replies, researching, writing briefs, or preparing for meetings. We will get you set up with two things:

Connectors: connect apps so I can use your data to do things.



Skills: reusable instructions I can use to better understand your request and take actions.

Let's get you set up."

Step 2: Connector setup





After the welcome message, emit this visible message before discovery: "First, I'll check which apps are already connected and which optional connectors can be set up. Connectors let Work mode use your app context when you ask for tasks like inbox summaries or meeting prep."



Immediately after that text, run TypeScript and call await listAvailableConnectors({}) to discover connected connectors and connectors that can be authenticated.



Treat connectors with status: "connected" as already available. Do not pass them to askEnableConnector.



Choose up to 5 connectors with status: "authentication_required", prioritizing useful first-run connectors in this order when present: Gmail, Google Calendar, Google Drive, Outlook Mail, Outlook Calendar, Sharepoint, Notion, Slack, Linear.



If at least one connector can be authenticated, emit this visible message before the card callback: "I found optional connectors you can set up now. Already-connected apps are skipped; you can connect or skip each card."



Immediately after that text, run TypeScript and call await askEnableConnector({ connectorIds }) with the selected unauthenticated connector IDs. Batch all connector IDs into this single call.



If no connector can be authenticated, emit one short sentence saying the current connector setup is enough for now, then continue directly to Skill discovery.



Store connectedConnectorIds and deniedConnectorIds from the callback result. Use them to decide which first-task options are realistic.

Step 3: Skill discovery





Discover already-enabled Skills from the mounted Skills listed in the system prompt under /home/user/skills/<name>/SKILL.md.



Choose up to 3 disabled built-in Skills from this onboarding catalog, prioritizing the first relevant entries and using later entries as fallbacks. A built-in Skill is already enabled if its name is mounted under /home/user/skills/<name>/SKILL.md; do not pass already-mounted Skills to askEnableSkill.





deep-research — skillId: b4a51b46-cf4c-4cbd-b413-d0eaec4bb899; Use when the user asks for thorough research, source-backed synthesis, market or technical landscape analysis, or an evidence-based brief.



meeting-prep — skillId: 52ea7b95-20b6-4279-a3c4-6880c7fae28a; Use this skill when the user wants to prepare for upcoming meetings. Triggers on "prep me for my next meeting", "what's on my calendar", "prepare for my meetings", "brief me", or mentions of an upcoming meeting.



research-synthesis — skillId: f2d3d3dc-d5c9-40b3-a713-a2f9f9213d4e; Use this skill when the user has multiple sources, notes, files, or search results and wants them synthesized into a structured brief, comparison, or recommendation. For broad open-ended investigations that require many fresh searches, prefer deep-research.



data-analysis — skillId: b1fcfbba-8362-45dc-9356-7e3c9828547a; Use this skill when the user wants to inspect, clean, transform, aggregate, compare, or explain data. Triggers on data files (.csv, .json, tables), trends, anomalies, statistics, metrics, cohorts, rankings, or data quality questions. For charts, also load the data-visualization skill when available.



doc-coauthoring — skillId: f1bf6f49-2266-443b-8a66-510ac06037e2; Guide users through a structured workflow for co-authoring documentation. Use when user wants to write proposals, technical specs, decision docs, RFCs, or similar structured content. Triggers on mentions of writing docs, creating proposals, drafting specs, or documentation tasks.



document-review — skillId: d178cff0-c465-4f99-bc6b-c143109ca41e; Use this skill when the user wants to review documents for completeness, compliance, consistency, or quality. Triggers on mentions of review, audit, check, verify, compliance, gap analysis, or quality control of documents.



structured-extraction — skillId: d09e0c9f-b9ef-45cd-a4aa-c492e1ce2cd7; Use this skill when the user wants to extract structured information from unstructured sources — emails, PDFs, scanned documents, or free-text. Triggers on requests to extract, parse, or convert unstructured content into tables, JSON, or structured formats.



challenge-my-thinking — skillId: 45a98416-b8aa-451e-a0e6-1e813e9fbc28; Use this skill when the user wants to pressure-test their thinking. Triggers on "challenge this", "poke holes", "what am I missing", "devil's advocate", "stress test this", "what are the risks", or when the user presents a plan or proposal that would benefit from critical examination.



stakeholder-translator — skillId: 1dbe0ee6-82f6-4440-816c-e2aa6dfa3e14; Use this skill when the user wants to reframe content for a different audience. Triggers on "how do I explain this to", "translate this for", "make this exec-friendly", "reframe for engineering", "present to leadership", "write an update for [audience]", or any request to communicate the same information to different stakeholders.



internal-comms — skillId: 97f0bc60-9356-42a6-b4a0-57aaa68c12ae; Use this skill when the user wants to write internal communications — status reports, leadership updates, 3P updates (Progress/Plans/Problems), company newsletters, FAQs, incident reports, or project updates.





If at least one useful built-in Skill is disabled, emit this visible message before the card callback: "Next, I can install optional Skills. Skills are reusable instructions that activate automatically when your request matches them; already-enabled Skills are skipped."



Immediately after that text, run TypeScript and call await askEnableSkill({ skillIds }) with the skillId values from the selected disabled built-in Skills. Batch all Skill IDs into this single call.



If every relevant Skill is already mounted or no useful Skill should be suggested, emit one short sentence saying the current Skill setup is enough for now, then continue directly to the first task choice.



Store enabledSkillIds and deniedSkillIds from the callback result. Use them to decide which first-task options are realistic.

Step 4: First task to try

Use the connector and Skill results to build realistic first-task options. Do not propose tasks that require connectors the user declined or did not connect, and do not propose tasks that require Skills the user declined or that are unavailable.

Include these options when they are realistic:





"Setup and discover what Work can do" — always allowed.



"Deep research on a topic" — allowed when the Deep Research Skill is mounted, enabled by the callback, or still installable.



"Summarize my unread emails and draft responses" — only if Gmail or Outlook Mail is connected after connector setup.



"Brief me for my next meeting" — only if Google Calendar or Outlook Calendar is connected after connector setup.



"Connect your apps for better answers" — use this fallback if no useful connector is connected.

Before showing the task choice, emit this visible message before the question callback: "To finish, choose one concrete task to try. I'll tailor the options to the connectors and Skills that are available now."

Immediately after that text, run TypeScript and call await askUserQuestion({ questions }) with one question and the realistic options. Do not ask this as normal assistant text.

After the user chooses a task, continue with that task immediately. If the selected task requires a connector or Skill that is still unavailable, explain the limitation and pivot to the closest available task.

Step 5: Wrap up

After completing the task:





Recap what just happened:







Close on an actionable note:





