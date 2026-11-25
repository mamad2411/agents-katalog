---
name: camera-ready
description: Prepare and check the camera-ready version against the current ARR, ACL, ACLPUB and SemEval final-version rules (de-anonymization, acknowledgments, extra page, metadata, PDF checks).
disable-model-invocation: true
argument-hint: "[venue, e.g. 'ACL 2027 long']"
---

Turn the accepted paper into its final version and check it against the publication rules as they are published today. Every run fetches them.

`PK` means `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/paperkit.py`, run from the project root.

## 1. Fetch the rules

Read `venue`, `paper_type` and `stage` from `paper.config.json` and confirm them in one line (store corrections with `PK config-set`). If `stage` is `review`, ask whether the paper is accepted and the final version is due now.

```
PK guidelines camera-ready
```

For `venue` `semeval` fetch `camera-ready-semeval` instead: the SemEval paper requirements and system paper template plus ACLPUB's and the ACL template's guides. SemEval's own documents and the shared task's year page (ask for its URL; it wins) decide where they differ from ACLPUB. SemEval is not anonymous, so there is nothing to de-anonymize; check the title format and the final-version page limit in the fetched requirements.

For `acl-arr` it fetches the ARR author guide (camera-ready section), ACLPUB's final-version and formatting guides and the ACL template's `formatting.md`. On ⚠️ say what is missing. Read them in full. Then ask with AskUserQuestion, in one round: venue and paper type, the camera-ready deadline, whether the venue's own call names extra requirements (they override the general guides; ask for the text or URL), author names, order and affiliations as they should appear, and what goes in the acknowledgments (funding numbers). Ask again whenever a formatting rule leaves a choice the fetched guides do not settle.

## 2. Open promises

Collect open `report.md` items in category `Review`, especially changes promised in `rebuttal.md`, and the meta-review's requests in `reviews/meta.md`. Ask the user which are done; the rest are 🔴.

## 3. Check and prepare

Go through the fetched rules one by one. Typical points, to be confirmed against the fetched text rather than assumed:

- `\usepackage[review]{acl}` becomes `\usepackage[final]{acl}` (or the option the guides name), authors and affiliations filled in.
- Self-citations anonymized for review get their real form back; "anonymous" links (code, data) become the real URLs.
- Acknowledgments added where the guides allow.
- Page limit for the final version, and what does not count towards it.
- Limitations and ethics sections as required.
- PDF requirements: fonts embedded, no overfull lines into margins, PDF metadata, hyperlinks. Check them on the compiled PDF (`pdffonts` if available); when there is no fresh PDF, ask the user to compile.
- Bib: `PK sync` reports nothing unknown or unread; entries have venue and year.

Edit only what the user approves. Cite every rule by the identifier the fetched document uses (section heading, checklist question, issue code such as `H9`) and the document's URL as `PK guidelines` prints it. Rule violations and anything left open go to `report.md`, category `ACL-Compliance`.

Done when each rule in the fetched guides is marked met, fixed or open. Report in chat, each rule with identifier and document URL, what was changed, what is open, and the rules you could not check.
