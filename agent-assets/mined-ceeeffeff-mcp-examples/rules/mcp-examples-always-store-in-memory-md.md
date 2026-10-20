---
description: This rule ensures the Codebase memory is kept up-to-date.
alwaysApply: true
---
# Definitions
## Entities
Some examples of the type of entities this codebase :
* files
* directories
* classes
* objects
* scripts
* to-do items
* processes
And more that you might decide.

## Relations
Describes a relationship - edge between two nodes in the knowlege graph

## Observations
When you are working in this codebase you will:
* read and execute a lot of code
* traverse the directory tree
* learn about the user through interacting with them
* solve problems
* be unable to solve problems
Through this you should observe:
* patterns
* structure
* standards
* pitfalls
* issues
* definitions
* purpose of different entities
* the general setup and tech stack
* important areas of the code base
* files to ignore (check with a user if you think you've found a new file that needs ignoring)

# During Thinking
While doing the primary task thinking, also be attentive and identify any new Entities, Relations or Observations from the interaction describe them each as:
"Entity: Very short description..."
"Relation: Very short description..."
"Observation: Very short description..."

# After Thinking
After thinking, in addition to any other actions you want to do, use the Codebase Memory tools to update your memory knowledge graph step-by-step:
1. Create all of the entities identified during thinking
2. Connect related entities to eachother using relations identified during thinking (entities must have been created)
3. Store facts/observations about the entities identified during thinking as observations 

If at any point you need to clarify something it is **extremely** important you ask the user.

If an error occurs you might want to use the fix_codebase_memory tool if you think your calls were valid but the memory itself is corrupt.

