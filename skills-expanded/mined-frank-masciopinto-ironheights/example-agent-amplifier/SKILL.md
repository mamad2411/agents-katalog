---
name: example-agent-amplifier
description: Lets the agent create new tools when existing ones don't fit.
---
# Example Agent Amplifier
## create_tool
Parameters: name, description, parameters (JSON Schema), implementation (python|javascript|sql), code (string).
The tool is registered immediately and can be called in later steps.
## consult_peer
Ask a peer agent for advice and follow its recommendation.
