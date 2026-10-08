# Agent Guidelines for timetracker

## Code Requirements
- All functions must have comments - concise but complete
- Avoid external dependencies when possible
- Write tests first (TDD approach)
- Keep code simple and readable

## Project Structure
- Source: `~/go/src/timetracker/`
- Binary: `~/go/bin/timetracker`
- Config: `~/.config/timetracker.json`
- Data: OneDrive folder (configured in config)

## Commands
- CLI: add, list, weekly, edit, delete, accounts
- TUI: vim-style navigation, pop out to $EDITOR for editing
- Use urfave/cli for CLI framework

## Testing
- Run tests: `go test ./...`
- All packages should have _test.go files
- Test behavior, not implementation details