---
name: litig-matter-workspace
version: 1.0.0
description: Set up the folder and document workspace structure for a litigation matter — pleadings, discovery, correspondence, and research.
author: matrixx0070
tags: [litigation, workspace, file-organization, discovery, case-management]
capabilities: []
---

## When to use
Use this right after a matter is opened, before documents start arriving, so everything lands in a predictable place. Use it to create a consistent folder tree that every team member can navigate without asking. A good structure pays off most during discovery and trial prep, when volume spikes.

**Not for:** capturing case facts (see litig-matter-intake) or writing status entries (see litig-matter-update).

## Method
1. Create the top-level matter folder named with the matter number and short caption.
2. Add core subfolders: Pleadings, Discovery, Correspondence, Research, Motions, and Admin.
3. Split Discovery into Propounded, Received, and Productions, with a privilege-log subfolder. **Decision point:** if the matter involves substantial ESI, add a dedicated ESI/native-files folder and note the review platform.
4. Establish a naming convention: date-prefixed, party-tagged, versioned.
5. Seed an index or README in the root that maps the tree and the naming rules.
6. Set access so privileged and work-product folders are restricted appropriately. **Decision point:** if outside co-counsel or a client will have access, segregate privileged material into a restricted subfolder.
7. ATTORNEY-ESCALATION gate: before any drafted pleading, motion, or letter leaves the workspace, route it to the supervising attorney for review and signature.

## Example
> A new employment case opens. You create "2025-0142 Doe v. Acme" with Pleadings, Discovery (Propounded/Received/Productions/Privilege-Log), Correspondence, Research, Motions, and Admin, add an ESI folder for the email collection, seed a README with the naming convention, and restrict the Privilege-Log folder.

## Pitfalls
- **Flat dumping ground:** without subfolders, discovery volume becomes unsearchable fast.
- **Inconsistent naming:** ad-hoc filenames break sorting and version tracking.
- **Privilege bleed:** privileged and work-product files stored alongside producible material risk inadvertent disclosure.
- **No index:** a tree nobody documented is a tree nobody trusts.

## Output format
```
<matter#> <short caption>/
  Pleadings/
  Motions/
  Discovery/
    Propounded/  Received/  Productions/  Privilege-Log/  [ESI/]
  Correspondence/
  Research/
  Admin/
  README (tree map + naming convention)
```

## Reference
Discovery organization tracks the FRCP framework: initial disclosures (FRCP 26(a)), interrogatories (33), requests for production (34), requests for admission (36), and depositions (30). Keep propounded and received discovery separate, and maintain a running privilege log per FRCP 26(b)(5) describing withheld documents without revealing protected content. For ESI, preserve native files and metadata and agree production format early (often via a FRCP 26(f) conference and ESI protocol). A date-first naming convention (YYYY-MM-DD_party_doctype_vNN) keeps chronology intact. Clawback agreements under FRE 502(d) reduce inadvertent-waiver risk. Structures and local rules vary by jurisdiction; confirm the specifics with the supervising attorney.
