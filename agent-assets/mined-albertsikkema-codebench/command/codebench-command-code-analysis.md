---
description: "CB - Run code-index analysis (hotspots, coupling, errors, dead code)"
---

You are tasked with running a comprehensive automated code analysis on the codebase using the code-index MCP server tools.

## Evidence-Based Approach

This analysis uses tools classified by empirical evidence strength. See `.claude/library/best_practices/code-quality-evidence.md` for full details and citations.

| Tier | Label | Meaning | Action |
|------|-------|---------|--------|
| 1 | **[strong]** | Replicated peer-reviewed studies with controlled confounds | Flag prominently, prioritize fixes |
| 2 | **[moderate]** | Peer-reviewed but with known confounds (e.g., LOC correlation) | Flag as warnings, recommend review |
| 3 | **[practitioner]** | Widely accepted in practice, not empirically isolated | Flag for awareness, don't overweight |

**The LOC confound**: most code metrics correlate with lines of code (El Emam et al. 2001, Jay et al. 2009). A complex function may just be a long function. Keep this in mind when interpreting complexity, nesting, and coupling results -- they tell you WHERE to look, not that a bug exists.

## Scope

If the user specifies a file, directory, or module -- scope the analysis to that area. Otherwise, analyze the entire project.

## Steps

1. **Project overview:**
   - Run `get_project_summary()` to understand the codebase structure and key symbols.

2. **Run all analysis tools in parallel:**

   Launch these code-index MCP calls concurrently, grouped by evidence strength:

   **[strong] evidence -- highest-value signals:**

   | Tool | Purpose | Evidence |
   |------|---------|----------|
   | `find_hotspots()` | High-risk files (git churn x complexity) | Nagappan & Ball 2005 (89% accuracy), Tornhill & Borg 2022 (15x defect rate) |
   | `find_ownership_risks()` | Distributed ownership and bus-factor=1 files | Bird et al. 2011 (ownership is genuine signal, not proxy) |

   **[moderate] evidence -- useful signals with caveats:**

   | Tool | Purpose | Evidence |
   |------|---------|----------|
   | `find_circular_deps()` | Circular import chains | Zero false positives, clear architectural signal |
   | `analyze_coupling()` | Module coupling metrics (Ca, Ce, instability) | CBO validated (Chidamber-Kemerer 1994); Martin's framework less so (Al Dallal 2013) |
   | `find_unhandled_errors()` | Error handling gaps | High face validity, low false positive rate |
   | `find_duplicates()` | Copy-paste / structural duplication | Juergens et al. 2009 (52% inconsistent changes); but Bettenburg 2012 (only 1-3% cause defects) |
   | `find_cognitive_complexity()` | Functions hard to understand | Munoz Baron et al. 2020 (readability); NOT validated for defect prediction |
   | `find_testability_issues()` | Code that is hard to test well | Bruntink & van Deursen 2006 (WMC strongest predictor); NDSS 2022 (causal link to vulnerabilities) |
   | `find_bloated_functions()` | Oversized functions | Palomba et al. 2018 (smell-defect correlation, with size caveats) |
   | `find_deep_nesting()` | Deeply nested control flow | Hatton 1997; confounded with function length (El Emam 2001) |
   | `find_temporal_coupling()` | Hidden co-change dependencies | D'Ambros et al. 2009; Canfora et al. 2014 (64-93% defects in Granger-positive classes) |

   **[practitioner] evidence -- awareness signals:**

   | Tool | Purpose | Evidence |
   |------|---------|----------|
   | `find_dead_code()` | Potentially unused symbols | Standard practice; verify before removing |
   | `find_feature_envy()` | Methods using another class's data more than their own | Weaker evidence per Sharma & Spinellis 2018 |
   | `find_nested_loop_patterns()` | Performance-sensitive loop structures | Practitioner pattern, no dedicated study |

   If the user specified a scope, pass the relevant `file`, `file_or_module`, or `language` parameter where supported.

3. **Synthesize findings into a report:**

   Present the results organized by evidence strength and severity:

   ### Critical

   Issues with **[strong]** evidence backing or zero false positive rate:
   - Hotspot files: high churn + high complexity = where bugs concentrate (Tornhill & Borg: 15x defect rate, 124% more dev time)
   - Ownership risks: bus-factor=1 files or distributed ownership with no clear owner (Bird et al.: genuine predictor, not proxy)
   - Circular dependencies: deterministic detection, zero false positives, clear architectural problem

   ### High Priority

   Issues with **[moderate]** evidence and clear actionability:
   - Unhandled errors in critical paths: swallowed errors and unchecked returns are concrete bugs
   - Testability issues: code that is hard to test tends to be undertested, and undertested code has more bugs (NDSS 2022: fixing testability found 440 real vulnerabilities)
   - High cognitive complexity in hotspot files: the combination of [strong] hotspot + [moderate] complexity is a strong compound signal
   - Temporal coupling: unique signal (hidden dependencies no other method finds), but noisy -- only flag pairs with consistent co-change patterns

   ### Warnings

   Issues with **[moderate]** evidence or compound signals:
   - Highly coupled modules (hard to change independently)
   - Significant code duplication (maintainability risk, not a defect predictor)
   - Bloated functions and deep nesting (maintainability signals, confounded with LOC)

   ### Info

   Observations with **[practitioner]** evidence or low severity:
   - Dead code candidates (verify before removing -- may be used dynamically)
   - Feature envy (weaker evidence, may be design-appropriate)
   - Coupling metrics summary
   - Nested loop patterns (performance awareness)

4. **Actionable recommendations:**
   - Prioritize by evidence tier: [strong] findings first, then [moderate], then [practitioner]
   - For hotspot + ownership risk overlap: flag prominently -- these are the highest-value targets for refactoring or test investment
   - Suggest concrete next steps for the top issues
   - Reference specific files and line numbers
   - For testability issues: recommend specific test improvements, not just "add tests"
   - Remember Goodhart's Law: recommend fixing the underlying problem, not gaming the metric

## Output format

Keep the report concise and scannable. Use tables for metrics, bullet points for findings. Include the evidence tier tag ([strong], [moderate], [practitioner]) next to each finding so the reader knows how much weight to give it. Skip sections that have no findings -- don't include empty headings.

If everything looks clean, say so briefly -- don't invent problems.
