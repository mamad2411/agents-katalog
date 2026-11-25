---
name: embabeler
description: "Builds, extends and tests Embabel agents: goal-driven AI agents on the JVM with Java or Kotlin, Spring Boot, and Maven or Gradle. Creates a ready-to-run, tested project (Embabel 1.5.x on Spring Boot 4), explains how Embabel plans from @Agent/@Action/@AchievesGoal method signatures, and checks agent flows for planner problems with a test that reads Embabel's own agent model. Use whenever the user mentions Embabel, embabel-agent, @Agent or @Action or @AchievesGoal, GOAP agents on the JVM, or wants an AI agent with tools, typed LLM output, tests without an LLM, or an MCP-exposed agent in Java or Kotlin, even if they do not name the framework."
license: Apache-2.0
compatibility: "Needs Java 25 (21+ works with --java-version 21), Node.js 20+ and network access to Maven Central. An LLM API key is only needed to run an agent for real, never for the tests."
metadata:
  author: hadirsa
  version: "0.1.0"
  verified-with: "Embabel 1.5.2, Spring Boot 4.1.0"
---

# Embabeler

Embabel agents are Spring Boot applications where **the plan is inferred from method signatures**: each `@Action`'s parameter types are its preconditions and its return type is its effect, and the planner chains actions to reach the `@AchievesGoal` action. Most mistakes compile fine and then stall at runtime. This skill gives you a verified starting project, the conventions that avoid those stalls, and a checker for the ones the compiler cannot see.

Java and Kotlin are both supported, built with Maven (default) or Gradle (Kotlin DSL). The annotations and concepts are identical in both languages; the cookbook of pattern examples is Java.

Commands in this skill are written for Maven. In a Gradle project use the equivalents:

| Maven | Gradle |
|-------|--------|
| `./mvnw test` | `./gradlew test` |
| `./mvnw test -Dtest=BriefingAgentTest` | `./gradlew test --tests BriefingAgentTest` |
| `./mvnw spring-boot:run` | `./gradlew bootRun` |
| `./mvnw spring-boot:run -Dspring-boot.run.arguments='x "..." -p -r'` | `./gradlew bootRun --args='x "..." -p -r'` |
| `./mvnw -Pollama spring-boot:run` | `./gradlew -Pollama bootRun` |
| `embabel-agent.version` property in `pom.xml` | `embabelAgentVersion` value in `build.gradle.kts` |

## Prerequisites

- Java 25 (or 21+ with `--java-version 21`) and network access (Maven Central). Maven or Gradle comes from the project's wrapper.
- Node.js 20+ for the scripts (built-ins only, no `npm install`).
- A provider API key is needed only to run an agent against a real model. Tests never need one.

## Workflow

### 1. Establish the facts first

Embabel moves fast and its official templates lag its releases, so do not rely on memory or on a template's POM. Read `versions.json` for the verified combination (Embabel, Spring Boot, Java). When working in an existing project, read its `pom.xml` or `build.gradle.kts` and compare; the pairing matters because Embabel 1.5.x needs Spring Boot 4.x and fails at startup on 3.5.x. Details: [references/VERSIONS.md](references/VERSIONS.md).

### 2. Create or locate the project

New project: run the script from this skill's directory and pass the user's working directory as an absolute `--output-dir`, so the project lands in their workspace and not inside the skill folder.

```bash
node scripts/create-project.mjs <project-name> <java.package> --output-dir /absolute/path/to/workspace
```

Options: `--kotlin` (Kotlin sources instead of Java), `--gradle` (Gradle with the Kotlin DSL instead of Maven; use it when the user asks for Gradle or the workspace already builds with it), `--agent-name PascalCase` (default derived from the project name), `--with-cookbook` (adds compiled, tested Java examples of routing, conditions, states, domain tools, loops and human-in-the-loop; use it when the user wants to learn the patterns), `--latest` (newest Embabel release; run the tests straight away), `--dry-run`. Ask the user only for what you cannot infer: a project name and a package. The script refuses to overwrite a non-empty directory.

Existing project: do not regenerate. Read the code and `AGENTS.md`/`README.md`, follow the conventions already there, and use this skill's rules for anything new. If it has no plan check yet, add one (Java or Kotlin):

```bash
node scripts/add-plan-check.mjs /absolute/path/to/project <agents.base.package>
```

The project you get contains an agent (`UserInput -> BriefingRequest -> Facts -> Briefing`), domain types, a tool class, unit and integration tests, the plan check (`AgentPlanTest`), and its own `AGENTS.md` so later sessions follow the same conventions.

### 3. Design the flow before writing code

Write down the type chain and confirm it with the user when the request is vague. This takes a minute and prevents the most expensive class of bug.

| Step | Input types | Output type | LLM or code? | Temperature | Tools |
|------|-------------|-------------|--------------|-------------|-------|
| extractRequest | `UserInput` | `BriefingRequest` | LLM | 0.0 | none |
| ... | | | | | |

Rules of thumb: one record per concept (never a bare `String` as a flow type), the goal's return type is the contract with callers, put an LLM only where judgment is needed and plain Java everywhere else. Concepts: [references/CONCEPTS.md](references/CONCEPTS.md). Domain design: [references/DOMAIN-MODEL.md](references/DOMAIN-MODEL.md).

### 4. Test first, then implement

For each action, write the unit test before the code: it pins the prompt content, the temperature and the attached tools using `FakeOperationContext`, with no LLM involved. Then implement the action, then extend the integration test so the whole flow still reaches the goal. If an action can return `null` or is gated by a condition, also test the stuck path through `run(...)` and `AgentProcessStatusCode.STUCK`. Patterns and the API: [references/TEST.md](references/TEST.md).

Implementation references: actions, conditions, goals [ACTIONS.md](references/ACTIONS.md); calling models [PROMPTING.md](references/PROMPTING.md); tools [TOOLS.md](references/TOOLS.md); loops, states and human input [WORKFLOWS.md](references/WORKFLOWS.md).

### 5. Verify before claiming it works

From the project directory:

```bash
./mvnw test
```

It must pass. Besides the unit and integration tests it runs `AgentPlanTest`, which reads the agent model Embabel builds (so it understands Java and Kotlin exactly) and **fails** on a missing goal, a goal that can never be reached (dependency cycle or broken type chain), or a condition used in `pre` that no action declares in `post`. It prints warnings for ambiguous producers, unreachable actions and weak `String` flow types, and info notes such as inputs the caller must supply. Read that report; errors must be fixed, warnings deserve a decision.

For a quick look without a build, `node /path/to/embabeler/scripts/check-plan.mjs` runs a static version of the same rules on Java sources (not Kotlin). Use `--json` for machine-readable output and `--strict` to fail on warnings.

If the project's own tests fail only on startup with `ClassNotFoundException` for Spring AI classes, it is the Spring Boot version, not your code. See [references/PITFALLS.md](references/PITFALLS.md).

### 6. Run it for real (only if the user wants to)

This needs a provider key. Ask the user to export it in their shell; do not read, print or paste `.env`. Then `./mvnw spring-boot:run` opens a shell where `x "your request" -p -r` runs the agent and shows prompts and responses. To run one request without the interactive shell (for example from an agent's terminal), pass it as arguments: `./mvnw spring-boot:run -Dspring-boot.run.arguments='x "your request" -p -r'`. It prints the result and exits by itself (shutdown can take about a minute after the result); if the run fails, the build exits with code 1.

No provider key at hand? Ollama works through the same profile: `OPENAI_CUSTOM_BASE_URL=http://127.0.0.1:11434/v1`, any non-empty `OPENAI_CUSTOM_API_KEY`, and the model name in both `OPENAI_CUSTOM_MODELS` and `EMBABEL_MODELS_DEFAULT_LLM`. Small local models are slow on CPU and sometimes return malformed JSON on the first try; Embabel retries.

For a gateway or any OpenAI-compatible server, use the `openai-custom-models` profile (`OPENAI_CUSTOM_API_KEY`, `OPENAI_CUSTOM_BASE_URL` ending in `/v1`, and the model listed in `models`): [CONFIGURATION.md](references/CONFIGURATION.md#openai-compatible-endpoints). If calls fail with 5xx retries, check the endpoint with curl before touching the agent: [PITFALLS.md](references/PITFALLS.md#the-endpoint-is-down-and-the-agent-looks-stuck-r).

Invocation, MCP exposure and configuration: [references/INVOKING.md](references/INVOKING.md), [references/CONFIGURATION.md](references/CONFIGURATION.md).

## Rules that prevent the common failures

1. **Never invent Embabel APIs, imports or properties.** Names and packages differ from what memory suggests (`com.embabel.agent.api.annotation`, not `com.embabel.agent.annotation`). Take them from [references/PITFALLS.md](references/PITFALLS.md#imports-cheat-sheet), the cookbook, or the official sources below. If it is not there, say so and look it up.
2. **Never call a real LLM in a test.** Real calls are slow, flaky and cost money; the fakes exist so you never need to.
3. **Keep the type chain connected and unambiguous.** After changing any action signature, run `./mvnw test` and read the `AgentPlanTest` report. A disconnected chain produces no compile error.
4. **A condition used in `pre` must be declared in `post` on the action that produces its data**, or the gated action never runs.
5. **Use `run(...)`, not `invoke(...)`, when you need to know why a flow did not finish.** `invoke` turns a stuck process into an unhelpful `NullPointerException`.
6. **One Embabel version across all `com.embabel.agent` artifacts**, and Spring Boot 4.x with Embabel 1.5.x.
7. **Choose temperature per action** (0.0 extraction, about 0.2 factual, 0.7+ creative) and give every LLM-calling action a unit test.
8. **Expose to the LLM only what is safe.** `@LlmTool` methods are the only ones visible; prefer read-only tools and keep business rules in code.
9. **Configuration goes in `application.yml`** (and `application-<profile>.yml`), never a new `application.properties`: Spring would load both and the properties file silently wins.
10. **Secrets stay in the environment.** Never commit `.env`, never read or print its contents, never put keys in prompts or test data.
11. **The user reviews changes before they are committed.** Do not run `git commit` or `git push` unless asked.

## Looking things up

Order of trust: compiled code in this skill, then the official examples, then the versioned guide, then memory (last).

- Guide for the project's version: `https://docs.embabel.com/embabel-agent/guide/<version>/` (the unversioned URL returns 403).
- Working examples (Java and Kotlin): https://github.com/embabel/embabel-agent-examples
- Official templates: https://github.com/embabel/java-agent-template and https://github.com/embabel/kotlin-agent-template
- Official project creator: `uvx --from git+https://github.com/embabel/project-creator.git project-creator`
- Library docs through Context7, when available: `/embabel/embabel-agent`

## References

Load only what the task needs.

| File | Read it when |
|------|--------------|
| [CONCEPTS.md](references/CONCEPTS.md) | You are new to Embabel or a flow does not behave as expected |
| [ACTIONS.md](references/ACTIONS.md) | Writing agents, actions, goals, conditions, return types |
| [PROMPTING.md](references/PROMPTING.md) | Calling models, choosing temperature, typed output, personas |
| [TOOLS.md](references/TOOLS.md) | Giving the LLM tools, domain objects as tools, MCP |
| [DOMAIN-MODEL.md](references/DOMAIN-MODEL.md) | Designing the records that flow between actions |
| [WORKFLOWS.md](references/WORKFLOWS.md) | Loops, states, branching, retry-until-good, human input |
| [TEST.md](references/TEST.md) | Writing or debugging tests, stuck flows |
| [CONFIGURATION.md](references/CONFIGURATION.md) | Dependencies, providers, properties, secrets |
| [INVOKING.md](references/INVOKING.md) | Calling agents from code, the shell, MCP |
| [PITFALLS.md](references/PITFALLS.md) | Something fails and you need the cause; verified imports |
| [VERSIONS.md](references/VERSIONS.md) | Choosing or upgrading versions |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/create-project.mjs` | Generate a Java or Kotlin project from `assets/project-template` |
| `scripts/add-plan-check.mjs` | Add `AgentPlanCheck` + `AgentPlanTest` (from `assets/plan-check`) to an existing project |
| `scripts/check-plan.mjs` | Quick static plan checker for Java sources (no build) |
| `scripts/verify-scaffold.mjs` | Generate a project and run its real Maven or Gradle tests (the maintainers' gate) |
| `scripts/check-versions.mjs` | Report a newer Embabel release |
| `scripts/check-official-snippets.mjs` | Confirm snippets marked "official" still match the official repositories (network) |
| `scripts/sync-versions-in-docs.mjs` | Keep version tables in the docs in step with `versions.json` |

The compiled examples live in `examples/cookbook` and are copied into a project with `--with-cookbook`. Its `PitfallAgentsTest` (and `examples/pitfalls-kotlin` for Kotlin) shows the plan check catching deliberately broken agents.
