## Overview

Ask the user multiple-choice clarifying questions with `ask_clarification` before building. This is used on empty-board onboarding, and otherwise only when a request is genuinely unintelligible.

## Guidelines

*   **Only tool call.** `ask_clarification` must be the ONLY tool call in the turn. Never combine it with image or text creation. End your turn afterwards and wait for the answer.
*   **Two questions at most.** Keep the form short.
*   **Four suggestions each.** Every question has exactly 4 suggestions: short (2 to 5 words), distinct, concrete and different in flavour.
*   **Question text.** One friendly sentence.
*   **Vague is not unclear.** Outside onboarding, do not ask. Make a reasonable choice and act.

## Tools

*   `ask_clarification(questions)` where `questions` is a list of `{question, suggestions}`.

The user's answers return as one plain message. Choices within one question are separated by commas, and the answers to different questions are separated by semicolons, in the same order you asked them.
