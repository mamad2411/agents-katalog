# Domain Layer Memory

Apply this inside `ai-service/app/domains/`.

- Put reusable business behavior, schemas, and domain-specific validation here.
- Keep modules organized by product domain, not by technical layer.
- Avoid FastAPI-specific objects in domain services when plain Python types are enough.
- Domain outputs must remain explainable and non-diagnostic.
- For behavior changes, write or update domain-level tests that describe the contract.
