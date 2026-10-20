# GCP Digital Twin Agent System - Claude Instructions

## Project Overview

This project implements an intelligent agent system that leverages a digital twin of a GCP environment (represented in Neo4j) to provide proactive monitoring, predictive alerts, and task automation capabilities.

## Key Technologies

- **Neo4j**: Network Knowledge Graph for GCP digital twin representation
- **Qwen3 LLM**: Local model for agent reasoning
- **OAT Algorithm**: Offline Reinforcement Learning for agent training
- **MCP Protocol**: Multi-Agent Communication Protocol
- **GCP APIs**: Integration with Google Cloud Platform

## Project Structure

```
agent-seomax/
├── .taskmaster/          # Taskmaster project management
│   ├── tasks/           # Generated task files (after parse-prd)
│   ├── docs/            # Reference documentation
│   │   ├── prd.txt      # Product Requirements Document
│   │   ├── Implementation GCP-RL-LLM-NEO4J.md
│   │   ├── LLM Reinforcement Learning in Network Di.md
│   │   └── llm_training.md
│   └── config.json      # Taskmaster configuration
├── .cline/              # Cline rules and configuration
├── CLAUDE.md           # This file
├── .env.example        # API keys template
└── README.md           # Project documentation
```

## Implementation Phases

### Phase I: Environment Construction (Months 1-3)
- Neo4j schema for GCP resources
- Real-time data ingestion pipeline
- Basic graph visualization
- Digital twin simulation capabilities

### Phase II: Agent Training (Months 4-6)
- GEM-compliant environment API
- Historical data collection
- OAT algorithm implementation
- Offline RL training of Qwen3 model

### Phase III: Deployment (Months 7-12)
- Multi-agent orchestration framework
- MCP communication layer
- User interface development
- Continuous learning system

## Taskmaster Workflow

### Initial Setup (Completed)
- ✅ Taskmaster initialized for this directory
- ✅ PRD and implementation guides copied to `.taskmaster/docs/`
- ✅ Cline and Claude rule profiles configured
- ⚠️ Pending: API keys configuration for task generation

### Next Steps (After API Keys Setup)

1. **Configure API Keys**:
   ```bash
   # Copy template and add your keys
   cp .env.example .env
   # Edit .env with your ANTHROPIC_API_KEY and PERPLEXITY_API_KEY
   ```

2. **Generate Initial Tasks**:
   ```bash
   # Via MCP (if keys in mcp.json)
   task-master parse-prd .taskmaster/docs/prd.txt --num-tasks=12 --research
   
   # Or via CLI (if keys in .env)
   task-master parse-prd .taskmaster/docs/prd.txt --num-tasks=12
   ```

3. **Analyze & Expand Tasks**:
   ```bash
   task-master analyze-complexity --research
   task-master expand --all --research
   ```

4. **Start Development**:
   ```bash
   task-master next              # Get next available task
   task-master show <id>         # View task details
   task-master set-status --id=<id> --status=in-progress
   ```

## Development Guidelines

### Working with Digital Twin
- All GCP resources represented as Neo4j nodes
- Relationships define dependencies and connections
- Real-time sync maintains environment accuracy
- Historical states used for RL training

### Agent Architecture
- **Assistant/Planner**: User interaction orchestration
- **Query Agent**: Neo4j graph queries
- **Executor Agent**: Simulation and action execution

### Training Strategy
- Offline RL using OAT algorithm
- Experience sampling from historical data
- Reward models for successful predictions
- GEM framework for environment simulation

## Important Notes

- **Git Structure**: This directory is within the `mcp-examples` repo. Don't initialize new git repo here.
- **API Keys**: Required for taskmaster AI features (parse-prd, analyze-complexity, expand tasks)
- **Research Mode**: Use `--research` flag for Perplexity-enhanced task generation

## Reference Documentation

- **PRD**: `.taskmaster/docs/prd.txt` - Full product requirements
- **Implementation Guide**: `.taskmaster/docs/Implementation GCP-RL-LLM-NEO4J.md`
- **RL Theory**: `.taskmaster/docs/LLM Reinforcement Learning in Network Di.md`
- **Training Methods**: `.taskmaster/docs/llm_training.md`

## Commands Quick Reference

```bash
# Task Management
task-master list                              # List all tasks
task-master next                              # Get next task
task-master show <id>                        # View task details
task-master set-status --id=<id> --status=<status>

# Task Development
task-master expand --id=<id> --research      # Break down task
task-master update-subtask --id=<id> --prompt="notes"
task-master add-dependency --id=<id> --depends-on=<id>

# Project Analysis
task-master analyze-complexity --research
task-master complexity-report
task-master validate-dependencies
```

## MCP Integration

To use taskmaster via MCP (preferred method), add to parent repo's `.cline/mcp.json`:

```json
{
  "mcpServers": {
    "taskmaster-ai-local": {
      "command": "node",
      "args": ["/path/to/task-master/mcp-server/server.js"],
      "env": {
        "ANTHROPIC_API_KEY": "your_key_here",
        "PERPLEXITY_API_KEY": "your_key_here"
      }
    }
  }
}
