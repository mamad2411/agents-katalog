# handwriting-grading

## Overview
Two-stage answer grading. Stage 1 involves a SymPy algebraic equivalence check. Stage 2 uses LLM conceptual grading to evaluate the concept, reasoning, and form scores. Final score is an aggregated weighted formula.

## Key Files
- `backend/sympy_validator.py` — Stage 1 SymPy algebraic equivalence check
- `backend/grading_service.py` — Stage 2 LLM conceptual grading (assumed)

## API / Interface
- `sympy_validator.validate_math_answer(user_text, reference_text)`

## Data Flow
1. Perform Stage 1 algebraic equivalence check via SymPy.
2. Perform Stage 2 conceptual grading via LLM (concept_score, reasoning_score, form_score).
3. Calculate final score: `final = algebraic*0.4 + concept*0.3 + reasoning*0.2 + form*0.1`.
4. Determine pass/fail based on a threshold of 0.85 (8.5/10).
5. Output structured grading result: `{grading_result: 'pass'|'needs_work', score, feedback, breakdown}`.

## Configuration
- Grading weights: algebraic (0.4), concept (0.3), reasoning (0.2), form (0.1).
- Pass threshold: 0.85 (8.5 out of 10).

## Error Handling
- Defaults to manual review if SymPy parsing completely fails.
- Fallback to partial scoring if LLM evaluation is unavailable.
