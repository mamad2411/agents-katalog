---
alwaysApply: true
---
  actions: [storeUserPreferencesAction],
  providers: [userPreferencesProvider],
  schema: customSchema, // Your schema export
};
```

## Important Considerations

### 1. Database Access Pattern

* Always access the database through `runtime.databaseAdapter.db`
* Use repository classes to encapsulate database operations
* The database type is already properly typed from the runtime adapter

### 2. Shared Data Pattern

Without `agentId` in your tables:

* All agents can read and write the same data
* Use `userId` or other identifiers to scope data appropriately
* Consider data consistency across multiple agents

### 3. Type Safety

* Define interfaces for your domain types
* Map database rows to domain types in repository methods
* Handle both camelCase and snake_case field names

### 4. Error Handling

```typescript
try {
  const result = await repository.upsert(userId, preferences);
  return { success: true, data: result };
} catch (error) {
  console.error('Failed to store preferences:', error);
  return { 
    success: false, 
    error: error instanceof Error ? error.message : 'Unknown error' 
  };
}
```

## Example Flow

1. **User sends message**: "I prefer dark theme and Spanish language"
2. **Action triggered**:
   * LLM extracts: `{ theme: 'dark', language: 'es' }`
   * Repository stores in database
3. **Provider supplies data**:
   * On next interaction, provider fetches preferences
   * Agent context includes: "User Preferences: theme: dark, language: es"
4. **Multiple agents**: Any agent can access this user's preferences

## Summary

To add custom schema to an Eliza plugin:

1. **Define schema** without `agentId` for shared data
2. **Create repository** classes following Eliza's pattern
3. **Create actions** to write data using `parseKeyValueXml` for structure
4. **Create providers** to read data and supply to agent context
5. **Register everything** in your plugin configuration

Eliza handles the rest - migrations, database connections, and making your data available across all agents in the system.
