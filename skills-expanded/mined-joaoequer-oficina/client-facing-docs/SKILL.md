---
name: client-facing-docs
description: Writing client-facing technical documentation — architecture documents, proposals, project presentations — in plain language, jargon-free, with honest numbers and explicit pragmatic engineering principles. Use whenever the material will be read by a client or non-technical stakeholder - architecture doc, kickoff presentation, proposal, delivery report or closing email.
---

# Client-facing documentation

A document for a client is not a technical document with a nice cover. It is a different kind of writing.

## Principles

1. **Zero untranslated jargon.** "Monorepo" becomes "a single repository". "Multi-tenant" becomes "each company with its data isolated". "CI/CD" becomes "every change passes automated checks before going live". If a technical term must appear, a one-sentence explanation comes with it.
2. **Honest numbers.** Hours, deadlines and scope reflect the real contract — never a partial version that "presents better". A wrong number in presented material is the kind of thing that erodes trust and is very expensive to fix later.
3. **Document scope = contracted scope.** Future phases, product vision and commercial possibilities stay out of the MVP document (at most, a one-line note: "future evolutions depend on a new commercial cycle").
4. **Real team, real roles.** Only people actually allocated, each with their correct role. Double-check before sending.
5. **Explicit engineering principles.** A short section stating how the team decides: proven technology over trends, complexity only when the problem demands it, reversible decisions, honest deadlines. Clients understand and value it — and the document becomes an anchor when someone suggests the trend of the week.

## House formats

**Architecture/structure document (responsive HTML):**
- Sections: overview → what the system does → how it is organized (repos, modules) → team and roles → engineering principles → timeline/workstreams
- Flowing prose, tables only where comparison demands them
- No decorative Unicode borders and no emoji overload (they break rendering and age badly)

**Presentation (fullscreen HTML deck):**
- Keyboard (←/→) and click navigation, progress bar, slide counter
- One topic per slide, short sentences
- Export to PDF for distribution via WhatsApp/email (the PDF is what circulates; the HTML is what presents)
- **Mandatory final check**: deck numbers × contract numbers, before presenting

**Closing email (weekly/delivery):**
- What was done (verifiable facts), what comes next, items pending on the client
- Short: if it's longer than one screen, it became a report and nobody reads it

## Checklist before sending any material

- [ ] Numbers match the contract/execution plan
- [ ] Team and roles verified
- [ ] Jargon translated or eliminated
- [ ] Scope limited to what was contracted
- [ ] Rendering checked on the device the client will open it on (usually a phone)
