# GENESIS — Divine Orchestrator
# Rust Council Engine: 432 agents | SPEAR v2.0 | 5 MCP servers
# Global rules: ~/.cursor/rules/genesis.mdc
# Chairman: Miguel Louis Jiminez | Atlanta, GA

# BioPoint - Cursor Rules
# Engine: ~/the-council-rs/ (Rust council-mcp binary)
# Follow SPEAR methodology for all builds

## Project Context

A project managed by The Council AI system.

**Tech Stack:** expo, react-native, typescript

## Council Integration (Rust)

This project is connected to The Council Rust engine. For full context, see:
- `.council/context.md` - Current project state
- `.council/project.yaml` - Project configuration

- **Binary:** `~/the-council-rs/target/release/council-mcp`
- **432 agents** across 5 tiers, SOVEREIGN engine
- Use `invoke_agent` / `smart_route` for thinking tasks

## MCP Tools

| MCP Server | Purpose |
|------------|---------|
| **council** | invoke_agent, smart_route, list_agents, council_memory, council_status |
| **qmd** | Semantic search across agents, crates, docs, memory |
| **llm-gateway** | Multi-LLM access (OpenAI, Gemini, Groq, etc.) |
| **content-creator** | Imagen 4, Veo 3.1 (Vertex AI OAuth) |
| **neobrain** | Second brain knowledge management |

## SPEAR v2.0

All builds follow SPEAR: Specs, fitness functions, audits, ratchets.

## Chairman Preferences

CRITICAL - Always follow these:

1. ACTION OVER EXPLANATION
   - Execute tasks, don't explain them
   - "YOU RUN IT" and "JUST DO IT" are directives

2. AVOID OVER-ENGINEERING
   - Only make changes directly requested
   - Don't add features beyond what's asked
   - Keep solutions simple and focused

3. READ BEFORE MODIFYING
   - Never propose changes to code you haven't read
   - Understand existing patterns first

4. NO TIME ESTIMATES
   - Never give time predictions
   - Focus on what needs to be done, not how long

5. PROFESSIONAL OBJECTIVITY
   - Prioritize technical accuracy
   - Provide direct, objective info
   - Disagree when necessary

## Code Standards

- Check for existing implementations before writing new code
- Test changes incrementally
- Don't add unnecessary abstractions
- Prefer editing existing files over creating new ones
- Keep commits focused and descriptive

## TypeScript Specific
- Enable strict mode
- Define proper interfaces/types
- Avoid 'any' type
- Use type inference where obvious

## Quick Reference

| Pattern | Rule |
|---------|------|
| New feature | Check if similar exists first |
| Bug fix | Don't refactor surrounding code |
| Python files | Never use sed, use proper tools |
| Documentation | Only when explicitly requested |
| Comments | Only where logic isn't self-evident |

## Project-Specific Memories

- PHASE 2 MLX TRAINING: 13,814 examples, LoRA rank 32, batch_size 1. genesis_phase2_15k adapter.
- PARABOLIC LEARNING: Autonomous overnight training works. 14,880 iterations, 10K examples, stable at 10.857GB. Loss train=1.672 val=1.589.
