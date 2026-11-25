---
name: datasheet
description: Extract structured information from integrated circuit and component datasheets (PDF files or URLs) and generate consistent markdown summaries. Use when the user requests to extract, summarize, analyze, or document information from IC/component datasheets, or when they provide a datasheet and want structured documentation. Triggers on phrases like "extract this datasheet", "summarize this datasheet", "analyze [component name]", "document this IC", or when working with datasheets for hardware design.
---

# Datasheet

Extract focused, goal-oriented information from IC and component datasheets using a specialized autonomous agent.

## Overview

This skill delegates datasheet extraction to a specialized autonomous agent (`datasheet-agent`) that:
- Processes PDFs (local files) or URLs
- Extracts 2 goal-oriented sections:
  1. **Circuit Design Information**: Pinout, power requirements, logic levels, package (everything needed to wire the component)
  2. **Microcontroller Code Information**: Communication interface, initialization sequence, key registers, operating modes (everything needed to write firmware)
- Generates focused markdown files (~90-120 lines) in `datasheets/` directory
- Ensures 100% accuracy for critical information (pinouts, communication parameters, register addresses)
- Omits detailed electrical tables, timing diagrams, and application circuits available in original datasheet

**Context Efficiency**: The agent processes the datasheet in an isolated context. PDF content is loaded into the agent's context and discarded when the agent completes, keeping the main conversation clean and minimizing token usage.

## How to Use

When a user requests datasheet extraction:

1. **Identify the input**: User provides either:
   - Local PDF path: `/path/to/datasheet.pdf`
   - URL: `https://example.com/datasheet.pdf`

2. **Validate input**:
   - For local files: Verify the file exists and is accessible
   - For URLs: Confirm the URL is well-formed

3. **Delegate to agent**:
   - Use the Task tool to invoke the `datasheet-agent` subagent
   - Provide clear context about the datasheet source (path or URL)
   - Let the agent execute the full 6-step extraction workflow autonomously

   Example delegation:
   ```
   "I'm delegating this datasheet extraction to the datasheet-agent.
   Please process [URL/path], extract goal-oriented information focused on
   circuit design and microcontroller code development, and save the focused
   markdown output to the datasheets/ directory."
   ```

4. **Present results**: When the agent completes, show the user:
   - File location (e.g., `datasheets/74HC595.md`)
   - Component name and key characteristics
   - Brief summary of what was extracted
   - Any issues or notes from extraction (missing sections, ambiguities resolved, etc.)

## Agent Responsibilities

The `datasheet-agent` autonomously handles:
- **Step 1**: Receive and validate input (PDF path or URL)
- **Step 2**: Read datasheet using Read tool (PDF) or WebFetch (URL)
- **Step 3**: Extract 2 goal-oriented sections focused on circuit design and code development
- **Step 4**: Generate focused markdown file (~90-120 lines) with proper formatting
- **Step 5**: Verify completeness, accuracy, and focused scope
- **Step 6**: Return summary with file location and key component info

For full workflow details, see `.claude/agents/datasheet-agent.md`

## Example Invocations

User might say:
- "Extract this datasheet: https://www.ti.com/lit/ds/symlink/sn74hc595.pdf"
- "Summarize the ATmega328P datasheet for me"
- "I need documentation for this IC: /path/to/lm358.pdf"
- "Help me understand the 74HC595"
- "/datasheet https://example.com/datasheet.pdf"

## Reference Materials

- **Example output format**: See `references/example_output.md` for a complete example of expected markdown output
- **Agent workflow details**: See `../../.claude/agents/datasheet-agent.md` for complete extraction workflow

## Benefits of Agent-Based Architecture

- **Context efficiency**: PDF content stays in agent's isolated context, not main conversation
- **Clean conversation**: Main conversation only sees high-level progress and final summary
- **Token savings**: ~9,000+ tokens saved in main conversation for typical datasheet (PDF content discarded when agent completes)
- **Consistent output**: Agent follows same workflow every time, ensuring reliable results
- **Easy maintenance**: Update agent definition without changing skill interface
