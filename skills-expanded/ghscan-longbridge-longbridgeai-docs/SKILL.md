---
sidebar_position: 2
title: "Skill System"
---

## What It Is

A Skill is a **dynamic context management and capability extension mechanism** for Agents: it packages a domain's methodology, rules, and tool combinations into a reusable capability package that the Agent loads on demand — avoiding a bloated context from stuffing everything into the System Prompt, and improving response quality and execution efficiency.

In one sentence: **the System Prompt is the Agent's personality; Skills are the professional skills the Agent can pick up whenever needed.**

## Three Ways to Create

![Skills page empty state: the "Create Skill" entry, with support for dragging Skill files directly onto the page](./images/02-1-Skill%E9%A6%96%E9%A1%B5.png)

| Method | When to Use |
|------|---------|
| Create and edit manually (create an empty Skill) | Build your own methodology from scratch |
| Upload a Skill archive | Import your team's existing Skill assets |
| Search GitHub Skills online and import | Reuse mature community Skills |

The creation flow has two steps: **① upload/search/create empty → ② name and describe → publish**.

**Step 1**: upload is the default, supporting `.zip` or `.skill` files (must contain a `SKILL.md`); the "Other creation methods" section below lets you switch to **Search Skill** or **Create Empty Skill**:

![Create Skill step 1: upload .zip/.skill, or switch to Search Skill / Create Empty Skill](./images/02-2-%E5%88%9B%E5%BB%BASkill%E4%B8%8A%E4%BC%A0.png)

Choosing "Search Skill" lets you **search community Skills on GitHub online**, retrieving by keyword (e.g. the superpowers series); click to import:

![Search GitHub Skills: keyword search for community Skills, showing name, author, and description](./images/02-3-%E6%90%9C%E7%B4%A2GitHubSkill.png)

**Step 2**: name and describe — the system automatically extracts the name and description from the uploaded/imported files, which you can edit manually; confirm and click "Publish":

![Name your Skill: name, description, source URL, and tool mounting; confirm and publish](./images/02-4-%E5%91%BD%E5%90%8D%E4%B8%8E%E5%8F%91%E5%B8%83.png)

- **Naming rules**: lowercase letters, digits, and hyphens only, up to 64 characters
- **Description**: describe the functionality and applicable scenarios precisely (so the model can judge when to invoke it); **line breaks are not supported**
- Skills imported from GitHub automatically record their **source URL**; you can also mount tools to the Skill at this step

## Skill Details & Editing

After publishing you land on the Skill detail page:

![Skill detail page: user-invocable switch, tools, file browser, and SKILL.md content preview](./images/02-5-Skill%E8%AF%A6%E6%83%85.png)

- **User-invocable**: a switch; when on, users can trigger the Skill directly by typing `/` in a conversation
- **Tools**: view/add the tools mounted to the Skill; tools already added are preserved when the Skill is updated
- **File browser**: view the list of files inside the Skill, with support for creating files/folders and adding files to supplement assets
- **Content preview**: select a file (such as `SKILL.md`) to preview the rendered result; click "Edit" to enter edit mode

Edit mode provides **Editor/Preview** tabs; the top of `SKILL.md` is frontmatter (`name`, `description`), and the body is the Skill's methodology content — click "Save File" to apply changes:

![Editing SKILL.md: editor/preview toggle, frontmatter (name/description) + body](./images/02-6-%E7%BC%96%E8%BE%91SKILLmd.png)

## Three Ways to Use

### Fixed Skills (Agentic Chat / Chatflow / Workflow)

Mount the Skill to the Agent, which then **automatically decides** whether to invoke it based on the task context and executes the relevant capability at the right stage.

- Typical scenario: earnings report analysis — the Agent automatically loads the earnings analysis Skill when it receives an earnings-related question

Two mounting points:

**① Agentic Chat**: in the "Skills" section of the Agent configuration page (below the knowledge base), click "+ Add Skill" to mount:

![Agentic Chat configuration page: mounting a Skill in the Skills section](./images/02-9-AgenticChat%E6%8C%82%E8%BD%BDSkill.png)

**② Agent node in Chatflow / Workflow**: in the "Skills" section of the node editing panel, click `+` to add (alongside the tool list, with the same support for variable injection):

![Agent node editing panel: the add entry in the Skills section](./images/02-10-Agent%E8%8A%82%E7%82%B9%E6%8C%82%E8%BD%BDSkill.png)

Both places share the same selection dialog: it lists your **custom Skills** and **official built-in Skills** with an "Official" tag, and you can also create a Skill directly from the dialog:

![Select Skill dialog: custom and official Skills, with direct creation supported](./images/02-11-%E9%80%89%E6%8B%A9Skill%E5%BC%B9%E7%AA%97.png)

### Dynamic Skills (Agent node in Chatflow)

Instead of being hard-coded at configuration time, the Skill is **passed in dynamically at runtime by the frontend via the Start node**.

- Typical scenario: strategy analysis — when the user manually selects a strategy, the frontend passes in the corresponding Skill, and the Agent invokes that Skill during execution to complete the task

### Manual Trigger in Conversation (User-Invocable)

With "**User-invocable**" enabled on the Skill detail page, the user can **type `/` in a conversation with the Agent to bring up the Skill selection popover**, which shows the Skill name, description, and Skill tags; selecting one triggers that Skill directly in the current turn:

![Typing / in the chat input brings up the Skill selection popover; the selected Skill fires directly in this turn](./images/02-7-%E5%AF%B9%E8%AF%9D%E4%B8%AD%E8%A7%A6%E5%8F%91Skill.png)

- Difference from the first two methods: those let the Agent/flow decide when to use a Skill, while this one is **explicitly specified by the user** — suited to cases where "the user knows exactly which specialized task to run"
- How **clearly the Skill's description is written** directly affects how efficiently users can choose in the popover; see naming and description guidelines in Step 2 of the creation flow above

After selecting a Skill, you can **append specific instructions and send them together** (e.g. `/superpowers-brainstorm help me list possible analysis angles for Google`): the Skill appears as a tag in the message bubble, and the Agent **executes and outputs following the methodology/template structure defined by that Skill** — in the screenshot below, the answer strictly follows the Goal / Constraints / Known context / Risks framework defined in the Skill:

![Skill execution result: Skill tag in the message + appended instruction, with the answer structured per the Skill template](./images/02-8-Skill%E6%89%A7%E8%A1%8C%E6%95%88%E6%9E%9C.png)

## Official Built-in Skills

The platform provides high-quality official Skills, available on **Pro and above plans**.

## Notes

1. **Quantity scales with plan**: custom Skill limits are Starter 3 / Pro 20 / Premium 100; delete or upgrade when over the limit — see [Workspace & Plans](../plans)
2. Skill content follows the same principles as prompts: conclusions first, actionable rules, positive and negative examples attached; see [Prompt Writing Tips](../../tutorials/prompt-writing)
3. Before using community Skills imported from GitHub in customer-facing Agents, review their content yourself against the [Compliance Requirements](../../compliance/index)

## Related Reading

- [Agent Node Documentation](../nodes/agent) — where Skills are mounted
