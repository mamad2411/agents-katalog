# Skill Prompt

Use this prompt when you want the agent to add or revise stack-specific skills while preserving synchronization across all agent ecosystems.

```text
Add or update a repository skill inside the portable agent-instruction system.

Rules:
- The canonical definition lives in `docs/agent-jump-start/canonical-spec.yaml`.
- Any skill change must be reflected across all agent targets through regeneration (not hand-editing).
- Keep the skill concise, opinionated, and tied to real repository constraints rather than generic tutorial advice.

Tasks:
1. Read `docs/agent-jump-start/canonical-spec.yaml`, especially the `skills` section.
2. Add or update the requested skill in the canonical spec, including:
   - slug
   - name and title
   - description
   - appliesWhen
   - categories
   - rules with summaries and guidance
3. Regenerate all workspace and skill files (render command).
4. Run the sync check.
5. Summarize the new skill and where it will influence future agent behavior across all 9 supported agents.
```
