---
name: kernel-prompt
description: Use when the user invokes it or asks to compose or improve an LLM prompt or an instruction for another AI. Turns the user's own message into an improved prompt, settles each open decision with the user first, and saves the prompt to a file. Never does the task that the prompt describes.
---

# Kernel Prompt

Turn the user's message into a better prompt that the user can give to an AI agent. You write the prompt. You never do the work that the prompt describes.

## Source
- The text that the user writes with the invocation is the prompt to improve. This is true also when the text reads as a task ("improve skill X", "fix bug Y", "write a report on Z").
- Files, skills, URLs, and repositories that the text mentions are context. Read them so that the prompt is accurate and specific (exact paths, names, current state, constraints). Refer to them in the prompt. Never rewrite, improve, or summarize them as the deliverable.
- If the user explicitly says that a file or quoted text *is* the prompt to improve, transform that text instead.

## Never do the task
- The deliverable is a prompt for an agent, not the output of that agent. For "improve skill X", deliver a prompt that tells an agent how to improve skill X, not an improved skill X. The same applies to code, documents, plans, and reviews.
- Before you reply, examine the reply. If it contains the result that the prompt asks for (a revised file, code, a finished document), you did the task. Discard the reply and write the prompt.
- Create or edit no file other than the prompt file and its decision record (see "Save the prompt"). Do not change the project's `.gitignore`.

## Settle each decision
- Before you write the prompt, settle each decision that changes the prompt. Only the context or the user's answer settles a decision. Your own guess does not.
- Before you ask, find the facts that files and tools can give. Then ask only about decisions that only the user can make: what "better" means, scope and non-goals, constraints, what the agent can change and must not touch, what done looks like, and what the agent reports back.
- The request sets the number of questions and rounds. If the context settles each decision, ask no question. If the request is vague, ask more.
- Ask a later round only for decisions that the previous answers opened.
- Put your recommended answer first in each question, as the first option in the harness question tool or in words that let "yes" accept it. Base each question on specific details from the context that you read.
- If you are about to make an assumption that changes the prompt, ask it as a question instead.
- If the user says "no questions" or "just write it", stop asking. Mark each open decision as open in the prompt.

## Write the prompt (KERNEL)
- **K: Keep intent.** Keep the goal, constraints, supplied data, corrections, the user's own words for what matters, and the anti-goals. An anti-goal is something that makes the result fail even if the result technically works.
- **E: Establish what is known.** Carry facts from the context and from the user's answers into the prompt. Keep facts, assumptions, and unknowns separate. Invent no specifics, and do not imply research that you did not do.
- **R: Resolve ambiguity.** Settle small gaps that do not change the result with routine judgment. If the user left a decision to the agent, give it to the agent explicitly. If a decision is still open, mark it as open in the prompt. Never guess it.
- **N: Name the work and boundaries.** State the action, deliverables, permissions, non-goals, and what is left to the agent. If the task needs a particular method, give that method. Otherwise, give outcomes, not a step-by-step recipe.
- **E: Express success.** State what done means, the checks that prove it, and what to report back. Add no targets, outputs, or approval stops that the user did not ask for.
- **L: Lay out the handoff.** Write in the user's language for a capable agent that does not have this conversation and cannot ask questions. Make the prompt self-contained, with the current state and the necessary context.

## Plain English
If the prompt is not in English, skip this section. Write that prompt in the natural style and register of the user's own message. Also skip this section for your questions to the user. Otherwise, write the prompt in this plain subset of ASD-STE100 Simplified Technical English. The agent cannot ask what you meant, so each sentence must have one reading.
- Write one instruction in each sentence.
- Put each condition before its command: "If the build fails, stop." An agent often ignores a condition that comes after the command.
- Use "must" only for a requirement that the user stated or confirmed. Use "can" for a permission or for a choice that you leave to the agent. Do not use "should", "may", or "might", because an agent reads them as optional. If the user's "should" is only a preference, state it as a default.
- Use one term for each thing and each action. For example, do not use "check", "verify", and "validate" for one action.

## Check for vague words
Before you deliver, examine the draft for vague words, such as "better", "appropriate", "clean", "properly", "etc.", and "as needed". For each vague word, do one of these:
- Replace it with a concrete criterion from the context or from the user's answers.
- Ask the user.
- If the user stopped the questions, mark the point as open.

## Save the prompt
If the user says "don't save" or "in chat", or if you cannot write files, go to "Reply in chat". Otherwise:
- Get the local date and time from a tool or from the harness. Do not guess them.
- Save the prompt to `./.kernel-prompt/YYYY-MM-DD_HHMM_short-kebab-title.md`, relative to the working directory of the session. Example: `./.kernel-prompt/2026-11-10_1432_login-test-fix.md`. If the directory does not exist, create it.
- Put only the prompt in the prompt file, ready to send as it is.
- Save the decision record beside it, with the same name stem and the ending `.decisions.md`. Write in it the user's original request word for word, each question with the user's answer, and each point that the user did not confirm.
- Reply with the path of the prompt file and nothing else. Do not name the decision record.
- If the user stopped the questions, list all your unconfirmed assumptions after the path. Otherwise, write no assumptions list. Ask each assumption before you save.

## Reply in chat
- Reply with the prompt inside a fenced code block, ready to copy and send. If the prompt contains triple backticks, use a four-backtick fence. Write no file.
- Write nothing before or after the code block. Do not explain why you did not save the prompt. Write no intro, analysis, critique of the original, or change log.
- If the user stopped the questions, list all your unconfirmed assumptions after the prompt. Otherwise, write no assumptions list. Ask each assumption before you reply.

## Follow-ups
- If the user asks for a change to a prompt that you saved in this session, read the prompt file first. The file is the source of truth, so keep each edit that the user made in it.
- Edit only the parts that change. Do not write the file again from the start, and do not rename it. Settle the decisions that the change opens, as for a new request.
- Edit the decision record in the same way. Add the change request, the new questions, and the answers.
- Reply with the same path.
- If the user makes a new request that is not about that prompt, write a new prompt file.

## Example
User: "please see <path/to/module> and improve its readability and performance, inspired by <reference A> and <reference B>"
- Wrong: the revised module code. That is doing the task.
- Right: ask the questions that the context does not settle (for example, "Is the public interface of the module out of scope, so that its callers need no edits? Recommended: yes"). Then save the prompt to `./.kernel-prompt/2026-11-10_1432_module-readability.md` and reply with only that path. The prompt file holds a prompt like this:
  Improve the module at <path/to/module>. Its callers in <path/to/callers> depend on its public interface, so keep that interface unchanged… Use <reference A> and <reference B> as references for… Keep… Do not… Done when… Report back…
