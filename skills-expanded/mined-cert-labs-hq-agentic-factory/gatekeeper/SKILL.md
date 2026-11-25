# Skill: The Gatekeeper
**Description**: Validates the presence of mandatory project metadata before allowing any generative work.
**Triggers**: "make a spec", "implement", "create a plan"

## Instructions
Before performing any task, perform a **Metadata Audit**:
1.  **Check Identity**: Does this request have a defined Slice ID and Name?
2.  **Check Context**: Is there a linked `master_spec.md` section for this?
3.  **Check Quota**: Is there enough remaining token budget for the complexity of this task?

### Result
- **PASS**: "Gatekeeper Audit Successful. Proceeding to [Task]."
- **FAIL**: "Gatekeeper Audit Failed. Missing: [List missing items]. No spec will be generated until these are provided."