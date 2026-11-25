---
name: find-ubiquitous-language
description: |
  Analyze the codebase to discover and extract the ubiquitous language.
  Identify domain terms, their definitions, and how consistently they are used.
---

## Find Ubiquitous Language Skill

Analyze the codebase to extract the ubiquitous language — the shared vocabulary between developers and domain experts that should be consistently reflected in the code.

### Analysis Flow

1. **Scan the domain layer**: Read domain models, entities, value objects, aggregates, services, and events to identify key domain terms.

2. **Scan supporting layers**: Check application services, API endpoints, database schemas, and documentation for additional terms and potential inconsistencies.

3. **Build the glossary**: For each discovered term, record:
   - **Term**: The canonical name
   - **Definition**: What it means in the business domain
   - **Code locations**: Where it appears (classes, methods, variables, tables)
   - **Aliases/Inconsistencies**: Alternative names used for the same concept (e.g., `User` vs `Account` vs `Customer` for the same entity)

4. **Identify problems**:
   - **Synonyms**: Multiple names for the same concept
   - **Homonyms**: Same name used for different concepts in different contexts
   - **Missing terms**: Business concepts that exist implicitly but have no explicit representation in code
   - **Technical leakage**: Domain terms polluted with technical jargon

5. **Output format**:

   ```
   ## Ubiquitous Language: <project name>

   ### Glossary

   | Term        | Definition                     | Code Locations          | Issues        |
   |-------------|--------------------------------|-------------------------|---------------|
   | Order       | A customer's purchase request  | `src/domain/Order.ts`   | —             |
   | Customer    | A registered buyer             | `src/domain/User.ts`    | Called "User" in code |
   | ...         | ...                            | ...                     | ...           |

   ### Inconsistencies

   #### 1. <Issue title>
   - **Concept**: The business concept involved
   - **Variants found**: List of different names used
   - **Recommendation**: Which term to standardize on and why

   ### Missing Terms
   - <Business concepts that should be explicit in code but aren't>
   ```

### Guidelines

- Focus on domain-meaningful terms, not generic programming terms.
- When in doubt about the business meaning, note the ambiguity rather than guessing.
- Do NOT make changes. This skill only produces the analysis.
