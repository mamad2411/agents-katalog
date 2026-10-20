# P3IF Project Rules

## Directory Structure
- Core framework is in `src/p3if/core/`
- Thin orchestrator examples are in `src/p3if/orchestrators/`
- Visualization modules are in `src/p3if/visualization/`
- Shared utilities are in `src/p3if/utils/`
- Data management is in `src/p3if/data/`
- Test suite is in `tests/`
- Domain data files are in `data/`
- Documentation is in `docs/`
- Web portal is in `website/`

## Code Style
- Follow PEP 8 for Python code style
- Use docstrings for all public functions, classes, and methods
- Keep lines under 100 characters
- Use 4 spaces for indentation (no tabs)

## Imports
- Import order: standard library, third-party packages, local modules
- Use absolute imports from the package root
- Example: `from p3if.core.models import Property`

## Documentation
- All code should have appropriate documentation
- Update docs when making changes to functionality
- Keep documentation in sync with code changes
- Reference docs are in Markdown format

## Script Paths
- All scripts should be invoked from the project root
- Example: `python scripts/run_all.py`
- Do not use relative imports that reach outside of a package

## Version Control
- Use semantic versioning for releases
- Provide descriptive commit messages
- Reference issue numbers when applicable

## Testing
- Write tests for new functionality
- Run tests before submitting changes
- Tests should be independent and deterministic
- Use pytest for testing
- **NEVER USE MOCK METHODS OR MOCK CLASSES**
- **ALWAYS USE REAL P3IF METHODS AND CLASSES**
- For external dependencies (matplotlib, PIL, etc.), use pytest.skip if unavailable
- All tests must use real P3IF framework instances

## Error Handling
- Use appropriate error handling and provide helpful error messages
- Log errors in a standardized format
- Fail gracefully when possible

## Real Methods Only
- NEVER create mock classes or mock methods
- NEVER use unittest.mock.patch or MagicMock for P3IF components
- ALWAYS use real P3IF classes: P3IFFramework, P3IFCore, Property, Process, Perspective
- ALWAYS use real P3IF methods for all operations
- If P3IF modules are unavailable, fix import paths - do not create mocks
- External dependencies (matplotlib, PIL) should be required or tests skipped

## Visualization Standards
- Maintain consistent styling across visualizations
- Follow the color scheme defined in documentation
- Support accessibility requirements
- Include legends and explanatory text 