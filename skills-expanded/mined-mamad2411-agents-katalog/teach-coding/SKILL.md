---
name: teach-coding
description: Interactive, multi-session projects for learning a programming language or framework.
disable-model-invocation: true
argument-hint: What do you want to learn?
---

# Coding Learning

Use a project directory to create interactive coding projects to help the user learn features of a programming language (or the whole language in small steps) or a framework. This is a stateful request—they intend to learn over multiple sessions. If this is an empty directory, follow the [startup instructions](INIT.md).

## Workspace

| Path | Purpose |
| --- | --- |
| `MISSION.md` | Goals of learning and why the user wants the topic; grounds all teaching. Use [the template](MISSION_TEMPLATE.md). |
| `./components/` | Reusable, interactive components imported by guides. |
| `./projects/` | One directory per topic taught via a project or scenario. |
| `./projects/INDEX.md` | Time-sorted list of projects: topics, goals, accomplishments, notes for future learning. Use [the template](INDEX_TEMPLATE.md). |
| `./projects/NOTES.md` | Notes, sources, and concerns scoped to the current lesson. |
| `./projects/<name>/lab/` | User coding workspace. |
| `./projects/<name>/guide/` | Interactive frontend content written in React. |

## Lessons

Lessons are the individual topics (ie. lambdas, classes, hooks) within the larger goal of learning a language/framework. A lesson is either scoped to its own project (if large/feature-rich enough) or combined as a step of an existing one.

Run a lesson in this order:

1. **Ground** in `MISSION.md` (goals, why) and `INDEX.md` (what they already know).
2. **Scope** the topic (see [Ordering](#ordering)) and its shape — new project or step of an existing one, modifying that project to fit when it makes sense.
3. **Build the Lab** — see [Lab](#lab).
4. **Build the Guide** — see [Guide](#guide).
5. **Open and teach** — open the guide (via CLI if possible), remind the user to ask follow-up questions, and converse with the Socratic method.
6. **Record** — capture the lesson's notes in `NOTES.md`, then roll them into `INDEX.md`.

### Ordering

Lessons should focus on fundamentals first, unless the user requests a topic. Think about how traditional learning guides order/structure the learning process for that language and if possible, research online. For example, a user learning Java would want to start with PL fundamentals like variables, functions, arrays before moving onto advanced features like inheritance, generics, lambdas. You should sprinkle in adjacent topics that learners would learn on the way, like using the standard library.

### Lab

The Lab is where the user learns hands-on: writing code and thinking out problems. This should be a minimal project organized in the convention of the language/framework.

The project should be framed around a common scenario (ie. developing a CLI to read files, simulating a bank with OOP, creating an interactive header using Tailwind, etc.). 

Design projects to keep the user in the zone of proximal development. Integrate both previous knowledge (see `INDEX.md`) and new concepts to make sure that the user retains knowledge without scaring them off. Make no assumptions about the user's previous domain knowledge.

Divide the project into several steps, allowing for individual verification and scoped hinting. Steps should be large enough for 5+ minutes of work, but small enough to keep the user in the zone.

Implement two versions: the full solution in `solution/` (which the tests are based on) and the derived Lab source code, prepopulated with boilerplate and any necessary code not relevant to the learning objectives. 

Projects should only contain language features that the user is documented to already know.

Document like a real codebase: terse comments, with the instructions in the guide.

#### Testing and Verification

Default to creating test suites to verify lab completion within `lab/`. Suites should be scoped per step of the project (independently runnable) and previous suites should run/pass in future steps (all tests should pass at the end of a project). Tests should be comprehensive and cover edge cases. All tests should be written in the native language.

If programmatic testing is not feasible or the user requests, tell the user to let you know when they are finished; you will manually inspect the code and/or use appropriate agentic verification tools like Playwright.

### Guide

The guide serves as the interactive instructions to grasp the content and complete the accompanying lab. Build it from the template in [guide/](guide/): copy `guide/components/` to the workspace root `./components/` (once), copy `guide/project-scaffold/` to `./projects/<name>/guide/`, then author content by editing only `src/App.jsx`. The authoring API is in [guide/components/GUIDE_USAGE.md](guide/components/GUIDE_USAGE.md); see [guide/README.md](guide/README.md) for setup. Serve via Vite (`npm install && npm run dev`); fall back to raw HTML only if Node is unavailable.

Always frame the project with concise context/story.

Whenever a new concept is introduced/used in a lab step, precede it with learning: Focus on the content itself—why the feature exists, what it is (syntax, examples), how it is used in real codebases. If a step requires use of specific language features or library methods, provide concise and **complete** documentation (name every required param): the user shouldn't need to look anything up.

Step instructions should be unambiguous and concise. Provide hints for each step. Hints must use a different type, resource, or scenario than the step's solution. If your hint could be pasted into the lab and pass the test, it's a solution — rewrite it. After writing all hints, double check that you didn't copy the solution verbatim. Hints should be hidden within a dropdown below the step.