# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

"today" - A Rust CLI application for managing daily tasks. The application allows users to create, track, and manage their daily tasks from the command line with a rolling task management system where uncompleted tasks carry forward to the next day.

## Development Setup

This is a Rust project chosen specifically for creating standalone binaries with no runtime dependencies.

### Why Rust?
- Compiles to single static binary with zero dependencies
- Excellent cross-platform compilation (`cargo build --target`)
- Fast compilation and execution
- Rich CLI ecosystem (`clap`, `serde`, `chrono`)
- Memory safe with no garbage collector

### Prerequisites
- Rust toolchain (rustc, cargo) - install via [rustup.rs](https://rustup.rs/)

### Quick Start
```bash
git clone <repo>
cd today
cargo build --release
./target/release/today --help
```

## Commands

### Build and Development
- `cargo build` - Build the project in debug mode
- `cargo build --release` - Build optimized release version
- `cargo run` - Run the application in development
- `cargo run -- [args]` - Run with command line arguments

### Testing and Quality
- `cargo test` - Run all tests
- `cargo test [test_name]` - Run specific test
- `cargo clippy` - Run Rust linter for code quality
- `cargo fmt` - Format code according to Rust standards

### Documentation
- `cargo doc` - Generate documentation
- `cargo doc --open` - Generate and open documentation in browser

## CLI Commands

### Basic Task Management
- `today list` - Display all current tasks for today
- `today task 'task description'` - Add a new task with description
- `today done <task_id>` - Mark a task as completed by its ID

### Status Management
- `today working <task_id>` - Mark task as currently in progress
- `today block <task_id> "reason"` - Mark task as blocked with reason
- `today unblock <task_id>` - Remove blocker from task

### Standup & Reporting
- `today standup` - Generate standup report (yesterday completed, today in progress, blockers)
- `today yesterday` - Show tasks completed yesterday
- `today summary [days]` - Show summary of past tasks (defaults to 7 days)
- `today week` - Weekly summary for retrospectives
- `today stats` - Basic productivity statistics

### Organization
- `today priority <task_id> <high|medium|low>` - Set task priority
- `today tag <task_id> <tag>` - Add tags like "bug", "feature", "meeting"
- `today archive [days]` - Archive old completed tasks (default 30 days)

## Task Data Structure

Each task contains:
- Unique ID (for referencing in commands)
- Task description
- Status (pending, working, blocked, completed)
- Priority (high, medium, low)
- Tags (array of strings like "bug", "feature", "meeting")
- Date created
- Date started (when marked as working)
- Date completed (when marked as done)
- Date due/scheduled (optional)
- Blocker reason (when blocked)
- Archived flag (for old completed tasks)

## Rolling Task Behavior

Uncompleted tasks automatically roll forward to the next day, ensuring nothing is forgotten.

## Standup Integration

The `today standup` command generates a formatted report perfect for daily standups:
- **Yesterday**: Tasks completed in the last 24 hours
- **Today**: Tasks currently marked as "working" or high-priority pending tasks
- **Blockers**: Any tasks marked as blocked with their reasons

This enables quick, accurate standup reporting without manual tracking.

## Data Storage

Uses JSON file storage with atomic writes:
- Data location: `~/.local/data/today.json`
- Human-readable format for easy debugging and backups
- Atomic file operations (temp file + rename) for crash safety
- Appropriate for personal task management scale
- Simple serialization with `serde_json`

## Architecture

CLI task management application with the following components:

- **Command Parser**: Handle CLI arguments and subcommands with multiple categories
- **Storage Layer**: JSON file operations with atomic writes
- **Task Operations**: CRUD operations with status management, priorities, and tags
- **Standup Generator**: Automated daily standup report generation
- **Display/Formatting**: Clean output formatting for lists, summaries, and reports
- **Date Management**: Handle task rolling, archiving, and time-based filtering
- **Statistics**: Basic productivity tracking and reporting

Key dependencies:
- `clap` - Command line argument parsing
- `serde` + `serde_json` - JSON serialization/deserialization
- `chrono` - Date and time handling
- `colored` - Terminal color output for better UX