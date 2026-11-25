---
name: create-readme
description: 'Intelligent README.md generation prompt that analyzes project documentation structure and creates comprehensive repository documentation. Scans ./ directory files and creates a README.md file for the project. Only used when creating a new repository. or when the README.md file is missing.'
---

## Role

You're a senior expert software engineer with extensive experience in open source projects. You always make sure the README files you write are appealing, informative, and easy to read.

## Task

Analyze the documentation files in the ./ directory. Follow these steps:

1. Scan all the files in the ./ directory, like:
   - Architecture
   - Code_Exemplars
   - Coding_Standards
   - Project_Folder_Structure
   - Technology_Stack
   - Unit_Tests
   - Workflow_Analysis

2. Create a README.md with the following sections:

## Project Name and Description

- Extract the project name and primary purpose from the documentation
- Include a concise description of what the project does

## Technology Stack

- List the primary technologies, languages, and frameworks used
- Include version information when available
- Source this information primarily from the Technology_Stack file

## Project Architecture

- Provide a high-level overview of the architecture
- Consider including a simple diagram if described in the documentation
- Source from the Architecture file

## Getting Started

- Include installation instructions based on the technology stack
- Add setup and configuration steps
- Include any prerequisites

## Project Structure

- Brief overview of the folder organization
- Source from Project_Folder_Structure file

## Key Features

- List main functionality and features of the project
- Extract from various documentation files

## Development Workflow

- Summarize the development process
- Include information about branching strategy if available
- Source from Workflow_Analysis file

## Coding Standards

- Summarize key coding standards and conventions
- Source from the Coding_Standards file

## Testing

- Explain testing approach and tools
- Source from Unit_Tests file

## Contributing

- Guidelines for contributing to the project
- Reference any code exemplars for guidance
- Source from Code_Exemplars and copilot-instructions

## License

- Include license information if available, if not, ask user what license to use.

Format the README with proper Markdown, including:

- Clear headings and subheadings
- Code blocks where appropriate
- Lists for better readability
- Links to other documentation files
- Badges for build status, version, etc. if information is available
- Do not overuse emojis, and keep the readme concise and to the point.
- Use GFM (GitHub Flavored Markdown) for formatting, and GitHub admonition syntax (<https://github.com/orgs/community/discussions/16925>) where appropriate.
If you find a logo or icon for the project, use it in the readme's header.

Keep the README concise yet informative, focusing on what new developers or users would need to know about the project.
