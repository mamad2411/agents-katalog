---
name: microsoft-style
description: Write warm, crisp, sentence-case product copy per the Microsoft Writing Style Guide (learn.microsoft.com/style-guide). Use when the user writes UI text, button labels, error messages, in-app or help-article instructions, release notes, or software marketing copy, or says "Microsoft style", "follow the Microsoft style guide", "sentence case this", or "make it friendlier". Pick this over google-dev-docs for UI strings, customer-facing product copy, and click-through procedures; pick google-dev-docs for API references and code-heavy developer docs.
---

# Microsoft Style

Bigger ideas, fewer words. Warm and relaxed, crisp and clear, ready to lend a hand.

## The core rule

**Lead with what the customer needs, in short everyday words, contractions, and sentence-style capitalization.** The guide's voice is "simple and human": less formal, written for scanning first and reading second. It prevents the stiff, title-cased, feature-first copy that makes software sound like a corporation talking to itself.

Workflow: `put the key point or action first` → `cut every excess word` → `apply the mechanics below` → `run the Verify checklist`.

## Mechanics

1. **Sentence-style capitalization.** Capitalize only the first word and proper nouns in headings, titles, UI labels, and list items ("Find a Microsoft partner", not "Find a Microsoft Partner"). In a heading with a colon, capitalize the first word after it. No all caps for emphasis; use italic sparingly.
2. **Contractions.** Use common ones: *it's, you're, that's, don't*. Never contract a noun and a verb ("Contoso's developing"). Avoid *there'd, it'll, they'd*. Don't mix *can't* and *cannot* in the same UI.
3. **Second person, not "we".** Address the reader as *you*. Omit *you can* when the sentence works without it. Write around *we recommend* when you can. Never use *I* or *my* in marketing or support docs (UI checkbox labels such as "Remember my password" are the exception).
4. **Verbs first, active, present.** Start most statements with a verb. Cut *there is*, *there are*, and *there were*. Use active voice; use passive only to avoid blaming the customer ("That site can't be found."). Use present tense for most content.
5. **Oxford comma.** In a list of three or more, put a comma before the conjunction: "Android, iOS, and Windows". Put a comma after an introductory phrase.
6. **Headings.** No period or colon at the end; a question mark is fine if the meaning needs it. Keep them short with the key idea first. Use parallel structure at each level. For task headings, consider infinitive phrases ("To create a group"). No *&* or *+* unless the UI uses them.
7. **Lists.** Two to seven items, each starting with a capital letter. No semicolons, commas, or *and/or* at item ends. End an item with a period only if it is a complete sentence or completes the lead-in. No periods when every item has three or fewer words, or the items are UI labels.
8. **Procedures.** Use a numbered list, one instruction per step (combine short steps in the same place in the UI). Write each step as a complete sentence with a capital and a period. Say where before what: "On the **Design** tab, select **Header row**." Otherwise start the step with an imperative verb. Include the closing action, such as selecting **OK** or **Apply**.
9. **Input-neutral verbs.** Use *select*, not *click*, *tap*, or *swipe*. Use *clear* for checkboxes, *enter* for typed values, *turn on/turn off* for toggles, *go to* for tabs and menus. For a simple path, use *>* with a space on each side and no bold: "Select **Accounts** > **Add an account**."
10. **UI element names.** In docs, bold the label exactly as the UI shows it, even if the UI uses title case (rule 1 governs your own text, not labels you quote), minus any trailing colon or ellipsis: "Select **Save as**", not "Select the **Save as…** button". Add the element type only if it adds clarity. Say *dialog*, not *dialog box* or *pop-up window*. When text refers to an error message, put the message in quotation marks. In UI and marketing text, skip bold and set labels off with wording or quotation marks, consistently.
11. **Spacing.** One space after periods, question marks, and colons. No spaces around em dashes: "pipelines—logical groups—to".
12. **Bias-free language.** No *he/she* in generic references; rewrite with *you*, a plural, *the*, or a role, or use singular *they*. Never *he/she* or *s/he*. Replace *master/slave* with *primary/subordinate*, *hang* with *stop responding*, *chairman* with *chair*, *manpower* with *workforce*. Focus on people, not disabilities; no *suffering from* or *stricken with*.

## Verify

- Zero title-case headings, labels, or list items (proper nouns excepted)
- Zero headings ending in a period or colon
- Every series of three or more items has a comma before *and/or*
- Zero *click*, *tap*, or *swipe* in instructions; UI labels are bold in docs and match the UI text
- Every procedure step is one numbered complete sentence, with location before action where the place could be unclear
- Zero noun-plus-verb contractions; *can't* and *cannot* never both appear in one UI
- Zero generic *he/she/his/her*, zero *he/she*, zero terms from the replace list in rule 12
- Zero spaced em dashes; zero double spaces after sentence punctuation
- First sentence of each section states the key point or action
- Last step: run the `de-ai` skill on the draft before you deliver it

## Do not

- Title-case product copy to make it look important; the guide reserves capitals for product and service names
- Write *we*-centered copy ("We are pleased to offer") when the sentence can center the customer
- Name the UI element when the action alone is clear ("Select **Save**", not "Select the **Save** button")
- Treat this as a developer-docs guide: for API reference, code samples, and gerund task headings, use `google-dev-docs`
- Force cheer into errors or serious moments; the guide keeps the voice constant but adjusts tone to the customer's state of mind

## Example transformations

**Before:** "In order to add a new user, the Add user button should be clicked by the administrator, after which he can type the Email Address and Phone Number and click Save."

**After:** "To add a user:
1. Select **Add user**.
2. Enter the user's email address and phone number, and then select **Save**."

**Before:** "Contoso Chat Provides A Powerful Platform That Will Enable Your Organization To Chat, Meet And Collaborate."

**After:** "Chat, meet, and collaborate with your organization in Contoso Chat."

**Before:** "ERROR: Invalid Input. We were unable to process your request — please try again."

**After:** "That input didn't work. Try again."
