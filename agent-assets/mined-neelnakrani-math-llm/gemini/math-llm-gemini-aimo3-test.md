Project: Kaggle Competitions (focus: AIMO Progress Prize 3 and future math/ML comps)

Core Rules (always active):
- Always output a clear numbered PLAN first with estimated steps and token cost awareness.
- Prefer Tool-Integrated Reasoning (TIR) with SymPy/code execution for exact integer answers.
- Use self-consistency + majority voting on 8–16 samples unless specified.
- Never hallucinate answers — verify with code where possible.
- Output only clean, runnable Python. Log everything to experiments/.
- Token efficiency: Summarize previous iterations instead of repeating full history.
- For every experiment: create a timestamped folder in experiments/ with code, predictions, score, and lessons.