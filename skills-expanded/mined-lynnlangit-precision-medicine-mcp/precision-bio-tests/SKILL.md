---
name: precision-bio-tests
description: >
  Expert guide for testing bioinformatics MCP servers.
  Covers pytest, DRY_RUN modes, and PatientOne simulation scenarios.
---

# Precision Bio-Testing

This skill provides guidelines for validating the complex biological and clinical logic in this repository.

## Automated Testing Strategy

### 1. Unit Testing (`pytest`)

Tests live in two locations:
- **Project-root tests:** `tests/unit/mcp-[server]/` (e.g., `tests/unit/mcp-spatialtools/`)
- **Server-local tests:** `servers/mcp-[name]/tests/` (e.g., `servers/mcp-perturbation/tests/`)

Both patterns are in active use. Check both locations when looking for existing coverage.

### 2. The `.fn` Testing Pattern

**FastMCP Pattern**: Never call `@mcp.tool()` decorated functions directly. Always use the `.fn` attribute to bypass the MCP protocol layer:

```python
result = await server.perturbation_predict.fn(gene="BRCA1", cell_type="T-cell")
```

This pattern is used across 9 test files in the project. Always follow it when writing new tests.

### 3. DRY_RUN Mode

Always test both modes:
- `DRY_RUN=True` (default) — returns synthetic/simulated data, no real bio tools needed
- `DRY_RUN=False` — exercises real logic (monkeypatch external dependencies in CI)

### 4. Bioinformatics Fixtures

Some test suites use fixture files (e.g., `tests/unit/mcp-multiomics/fixtures/` contains sample CSV files). Large datasets should be mocked or referenced from `data/patient-data/`.

## The PatientOne Scenario

The gold standard for integration testing is the **PatientOne** workflow (`docs/reference/testing/patient-one/`):
- **Phase 1**: Clinical (Epic)
- **Phase 2**: Multi-omics
- **Phase 3**: Spatial
- **Phase 4**: Imaging
- **Phase 5**: Final integrated recommendation

## Manual Testing (Prompts)

For browser-based or chat-based testing:
- Use the templates in `docs/reference/testing/quick-test-prompts.md`
- Verify the "Clinical Interpretation" matches the expected biological signal (e.g., GZMB/IFNG upregulation in immunotherapy)

## Testing Checklist

- [ ] Tool discovery via MCP protocol works
- [ ] `.fn` pattern used for all tool function calls in tests
- [ ] Both DRY_RUN=True and DRY_RUN=False paths covered
- [ ] Memory usage remains within 4Gi during heavy bioinformatics processing
- [ ] Error messages are informative for clinicians, not just developers

---

**Use this skill when:**
- Adding new tools to an MCP server
- Running regression tests on patient data pipelines
- Validating a new server's "production-ready" status
