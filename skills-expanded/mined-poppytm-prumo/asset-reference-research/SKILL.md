# Game-Asset Reference Research

## Purpose
Gather legally usable game-asset references and placeholders with complete licensing metadata: need-driven source sweeps across open repositories, per-asset license matrices, placeholder-to-final mapping, and attribution packs that keep builds shippable without infringing copyright.

## Use when
- A game vertical slice, prototype, or milestone needs sprites, models, audio, fonts, or UI kits before final art exists.
- Replacing grey-box placeholders with licensed references while preserving dimensions, pivots, and anchor points.
- Auditing an asset folder for unknown licenses, missing attribution, or non-commercial clauses in a commercial build.
- Preparing a shipped asset manifest with author, source URL, license, and modification notes per file.

## Do not use when
- Final production art is commissioned in-house and no external references enter the build; the art pipeline owns that work.
- The task is engine code, tooling, or protocol design with no asset sourcing involved.
- Reference material is for internal mood boards only and will never ship; a lightweight link list suffices without license matrices.

## Required context
- Asset brief listing each need with type, count, target resolution or poly budget, style anchors, and placeholder dimensions.
- Commercial status of the project, which decides whether non-commercial licenses are usable at all.
- Trusted source list, for example OpenGameArt, Kenney.nl, Poly Pizza, Unsplash, and Freesound, plus any blocked sources.
- Attribution format required by the shipping build, such as CREDITS.md plus in-game credits screen.

## Procedure
1. **Freeze the brief**: record each asset need with type, quantity, technical budget such as 512-pixel sprites or 5k-triangle models, style anchors from 3 approved references, and the placeholder slot it fills. Needs without budgets are returned for clarification, never researched vaguely.
2. **Sweep trusted sources first**: search OpenGameArt, Kenney.nl, Poly Pizza, Unsplash, and Freesound in that order, logging source URL, author, stated license, and file hash per candidate. Candidates from untrusted re-upload aggregators are quarantined pending origin proof.
3. **Build the license matrix**: classify every candidate as approved, conditional, or forbidden. CC0 and CC-BY 4.0 are approved for commercial builds, CC-BY-SA 4.0 is conditional on share-alike compatibility review, and any NC, ND, unknown, or ripped-game-content license is forbidden for commercial shipment.
4. **Map placeholders to finals**: pair each grey-box placeholder with its replacement, verifying pivots, tile sizes, loop points for audio, and font glyph coverage for the shipping locales pt-BR and en-US. Mismatches resize the brief, never silent stretching at import.
5. **Ship the attribution pack**: emit CREDITS.md entries plus in-game credits lines with title, author, source URL, license identifier, and modification notes, and store source archives with hashes under `assets/vendor/` so any file can be re-verified later.
6. **Verify the research**: run `scripts/verify.sh`, confirm 100% of shipped assets carry license proof, zero forbidden licenses in commercial paths, and placeholder coverage at 100% of briefed needs before handoff.

## Decision rules
- **No proof, no ship**: an asset without recorded author, source URL, and license identifier never enters the build.
- **NC and ND are forbidden commercially**: non-commercial and no-derivatives terms disqualify candidates for commercial builds without exception or legal waiver on file.
- **Ripped content is rejected**: assets extracted from commercial games are forbidden regardless of uploader claims.
- **Placeholders are explicit**: every grey box is registered in the brief with its replacement status; orphan placeholders fail verification.
- **Hashes pin everything**: vendor archives carry SHA-256 hashes; a re-downloaded file with a different hash is treated as a new candidate.

## Evidence required
- Research specification following `templates/asset-reference-research-spec.md` with brief, matrix, and mapping.
- License matrix covering every shipped asset with author, source, license, and modification notes.
- Attribution pack as CREDITS.md entries plus credits-screen lines, with vendor archive hashes.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Licensed reference set mapped one-to-one onto briefed placeholder slots.
- Complete license matrix with zero forbidden entries in commercial paths.
- Attribution pack and vendor archives enabling future re-verification.

## Stop conditions
- 100% of briefed needs mapped with 100% of shipped assets carrying license proof.
- Zero forbidden licenses present in commercial build paths.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to the producer if a briefed need has no licensable candidate within budget, so scope, style, or commissioned art can be decided.
- Escalate to legal counsel if a high-value asset carries ambiguous licensing, conflicting uploader claims, or share-alike obligations affecting proprietary code.
