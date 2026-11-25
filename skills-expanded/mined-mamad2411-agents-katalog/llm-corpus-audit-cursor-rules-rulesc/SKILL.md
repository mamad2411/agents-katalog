---
description: 
globs: 
alwaysApply: true
---
# Project Guiding Principles

## 1. Target Audience: Linguists with Limited Programming Experience

*   **Primary Consideration:** This project is designed for linguists who may not have extensive programming experience. All development, documentation, and communication should reflect this.
*   **Clarity in Code:**
    *   Write Python code that is as clear, readable, and straightforward as possible.
    *   Prefer simpler programming constructs over complex ones if they achieve the same result effectively.
    *   Comment code generously, especially explaining the "why" behind non-obvious logic.
*   **Accessible Documentation:**
    *   Ensure all setup instructions, usage guides, and explanations of technical steps are detailed, easy to follow, and avoid unnecessary jargon.
    *   The main `README.md` should be particularly clear and guide the user through the project.
*   **Simplified Explanations:** When discussing technical aspects, aim for explanations that are understandable to someone without a deep programming background.

## 2. Environment Management

*   **Conda Environment:** Consistently use the `llm-corpus-audit` conda virtual environment for all project work.
    *   Activation: `conda activate llm-corpus-audit`
    *   Ensure all required packages are listed in `requirements.txt` and installed within this environment.

## 3. Planning and Documentation

*   **Centralized Plan:** The primary project plan, workflow, and documentation are consolidated in the main `README.md` file in the project root.
*   **Adherence to Plan:** Strive to follow the steps and milestones outlined in the `README.md`.
*   **Keep README Updated:** Crucially, if the plan, scope, methodology, or deliverables change, the `README.md` must be updated promptly to reflect these changes. It serves as the single source of truth for the project's state and direction.

## 4. Development Workflow

*   **Iterative Approach:** Employ an incremental development process:
    1.  **Small Steps:** Break down tasks into the smallest manageable and testable units.
    2.  **Implement:** Code the small unit of functionality.
    3.  **Test:** Thoroughly test the new code to ensure it works as expected and doesn't break existing functionality. This can involve running scripts, checking outputs, or simple manual checks for initial stages.
    4.  **Continue:** Once tested and verified, move to the next small step.
*   **Benefits:** This approach helps in early bug detection, makes debugging easier, and provides a steady sense of progress.

## 5. Communication (AI Assistant Guidelines)

*   **Acknowledge Audience:** Remember the target audience (linguists with limited programming experience) in all explanations and code suggestions.
*   **Clarity and Simplicity:** Prioritize clear and simple explanations over overly technical ones.
*   **Step-by-Step:** When providing instructions or suggesting code, break it down into logical, easy-to-follow steps.
*   **Assume Less:** Do not assume deep knowledge of programming concepts or specific tools without prior confirmation.
