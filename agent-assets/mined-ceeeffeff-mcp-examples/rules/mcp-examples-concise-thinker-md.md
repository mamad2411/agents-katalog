---
description: Improves Thinking. Helped Qwen at times.
alwaysApply: true
---
# Thinking
Follow this logic for thinking...

## Initial gate
If a user directly asks you to do something base on previous messages:
  - do not repeat the same thinking you've already done
  - identify the relevant thinking from a prior message
  - exit thinking and perform the thing via tool calls

## Concise Thinking
Otherwise, start thinking but be concise with your thoughts.

### Preventing thought loops
If you are repeating yourself too much or are confused exit thinking and ask for user input.
If you are stuck, exit thinking and ask for help or request more context.

### End of Thinking
If you complete Thinking without exiting early:
1. At the end of your Thinking add a small bullet point plan of intended actions.
2. Exit Thinking and use tool calls to execute the small bullet point plan of intended actions
