# Cursor Rules for ve

Use `docs/AGENT.md` as the primary deep-context memory for this repository.

Keep these rules as non-negotiable guardrails:

1. Preserve architecture invariants:
   - Dual workspace model (`wksp_` and `alt_wksp_`) sharing one tempfile.
   - Current-line buffer discipline (`get_line()` -> edit `current_line_` -> `put_line()`).
2. Follow project style:
   - C++17, 4-space indentation, no tabs.
   - snake_case for methods/locals, PascalCase for types, trailing `_` for private members.
3. Always add/update tests for behavior changes:
   - Unit-style tests for data/logic behavior.
   - `TmuxDriver` integration tests for UI/keyflow behavior.
4. Run relevant verification before finishing:
   - Build and targeted tests at minimum.
5. When details are unclear, consult `AGENT.md` first, then source/tests as ground truth.
