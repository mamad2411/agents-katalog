# Coding Guidelines

## Application Root

The application source directory belongs in `<app-root>/app/` directory

## Database

see rdbms.md

## Coding Language Specifications

Unless specified, use go for the application, and for light
scripting needs, unless specified otherwise, use nushell

`coding/languages/*.md` - general coding instructions for specific languages (go, bash, python, nushell, rust, etc.)

## CLI Built in help

When building, make sure to have `4sight --help` and support `--help` for all subcommands

show the help when missing required arguments.

help should list all the available subcommands, options, and arguments, but not usage

have a subcommand "usage" that shows the app/USAGE.md context if that file exists, else
the body part of the app/skill/SKILL.md file.
