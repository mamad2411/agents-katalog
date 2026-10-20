# Claude Instructions

## On Startup
- Always read docs/PROJECT_NOTES.md first to understand the project context and current state.
- Always exclude the build/ directory from any code analysis or modifications.
- Always keep Swagger documentation up to date with any API changes.
- Always add a new line to the end of each file you modify.
- Always follow Effective Go guidelines for code style and conventions.
- Always group the consecutive var declarations, sorting them alphabetically within each group.
- Always use stretchr suite when writing tests.
- Do not create tests for cmd/ directory files.

## Project Commands
- Lint: `make lint`
- Test: `make test`
- Build: `make build`
- Goimports: `find ./ -type f -iname "*.go" -exec goimports -w {} \;`

## Important Files
- docs/PROJECT_NOTES.md - Contains project overview, goals, and current implementation status.
- docs/LOOP_STORE_ARCHITECTURE.md - Contains detailed architecture of the loop store component.
- README.md - Contains basic project information.
- Makefile - Contains build, test, and lint commands.
