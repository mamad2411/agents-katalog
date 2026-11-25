---
name: review-ddd
description: |
  Review code base from the viewpoint of Domain Driven Design (DDD) specialist.
  Evaluate how core business logics are well organized in terms of DDD principle.
---

## DDD Review Skill

Review the codebase from a Domain-Driven Design perspective. Evaluate the structural health of domain modeling and identify areas for improvement.

### Review Flow

1. **Discover the domain**: Read source code, directory structure, and documentation to understand the business domain and its boundaries.

2. **Evaluate DDD alignment**: Assess the codebase against the following dimensions:
   - **Bounded Contexts**: Are domain boundaries clearly defined? Is there proper separation between contexts?
   - **Aggregates**: Are aggregate roots correctly identified? Are consistency boundaries appropriate?
   - **Entities & Value Objects**: Are entities and value objects properly distinguished? Are value objects immutable?
   - **Domain Services**: Is business logic placed in the right layer? Are domain services used appropriately (not as a dumping ground)?
   - **Repositories**: Do repositories abstract persistence correctly? Are they defined per aggregate?
   - **Domain Events**: Are important state changes captured as domain events?
   - **Ubiquitous Language**: Does the code reflect the business language consistently?

3. **Identify issues**: For each issue found, report:
   - **What**: The specific DDD violation or weakness
   - **Where**: File paths and code locations
   - **Why it matters**: Impact on maintainability, correctness, or team communication
   - **Suggestion**: Concrete steps to improve

4. **Output format**:

   ```
   ## DDD Review: <project or module name>

   ### Summary
   <Brief overall assessment — 2-3 sentences>

   ### Scores
   | Dimension              | Score (1-5) | Notes                  |
   |------------------------|-------------|------------------------|
   | Bounded Contexts       | ...         | ...                    |
   | Aggregates             | ...         | ...                    |
   | Entities & Value Objects| ...        | ...                    |
   | Domain Services        | ...         | ...                    |
   | Repositories           | ...         | ...                    |
   | Domain Events          | ...         | ...                    |
   | Ubiquitous Language    | ...         | ...                    |

   ### Issues

   #### 1. <Issue title>
   - **What**: ...
   - **Where**: ...
   - **Why it matters**: ...
   - **Suggestion**: ...

   ### Strengths
   - <What the codebase does well from a DDD perspective>
   ```

### Guidelines

- Focus on structural and modeling issues, not code style or formatting.
- Be specific — reference actual files, classes, and functions.
- If the project is small or does not have a complex domain, note that and adjust expectations accordingly.
- Do NOT make changes. This skill only produces the review report.
