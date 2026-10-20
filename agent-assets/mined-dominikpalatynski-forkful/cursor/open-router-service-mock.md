---
alwaysApply: false
---
# Mocking OpenRouterService.generate() for GenerationRecipeService Tests

## Overview

Simple guide for mocking the `OpenRouterService.generate()` method output when testing `GenerationRecipeService`. Focus on **what it returns**, not how it works internally.

## 1. Basic Setup

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { GenerationRecipeService } from './generation-recipe.service';
import type { OpenRouterService } from './openrouter.service';

describe('GenerationRecipeService', () => {
  let mockOpenRouterService: OpenRouterService;
  let generationService: GenerationRecipeService;

  beforeEach(() => {
    vi.resetAllMocks();

    // Mock just the generate method - that's it!
    mockOpenRouterService = {
      generate: vi.fn(),
    } as unknown as OpenRouterService;

    generationService = new GenerationRecipeService(
      mockSupabase, // your mocked Supabase
      mockOpenRouterService
    );
  });
});
```

## 2. Mock Success Response

```typescript
it('should handle successful recipe generation', async () => {
  const mockRecipe = {
    name: 'Pasta Carbonara',
    description: 'Classic Italian pasta',
    ingredients: [
      { content: '400g pasta', position: 1 },
      { content: '200g bacon', position: 2 },
    ],
    steps: [
      { content: 'Boil pasta', position: 1 },
      { content: 'Fry bacon', position: 2 },
    ],
  };

  // Mock the generate() method to return this recipe
  vi.mocked(mockOpenRouterService.generate).mockResolvedValueOnce({
    raw: {}, // You don't care about this
    json: mockRecipe, // This is what matters
  });

  // Now test your GenerationRecipeService...
  const result = await generationService.generateRecipeFromText(
    'Make pasta',
    'user-123'
  );

  expect(result.name).toBe('Pasta Carbonara');
});
```

## 3. Mock Error Response

```typescript
it('should handle OpenRouter errors', async () => {
  const error = new Error('API Error');

  // Mock the generate() method to throw an error
  vi.mocked(mockOpenRouterService.generate).mockRejectedValueOnce(error);

  // Test that your service handles it properly
  await expect(
    generationService.generateRecipeFromText('Make pasta', 'user-123')
  ).rejects.toThrow('API Error');
});
```

## 4. Mock Invalid Recipe Response

```typescript
it('should handle invalid recipe structure', async () => {
  // Mock generate() returning incomplete data
  vi.mocked(mockOpenRouterService.generate).mockResolvedValueOnce({
    raw: {},
    json: {
      name: 'Incomplete Recipe',
      // Missing required fields
    },
  });

  await expect(
    generationService.generateRecipeFromText('Make recipe', 'user-123')
  ).rejects.toThrow('Failed to validate recipe');
});
```

## 5. Quick Reference

```typescript
// Success
vi.mocked(mockOpenRouterService.generate).mockResolvedValueOnce({
  raw: {},
  json: { name: '...', description: '...', ingredients: [...], steps: [...] }
});

// Error
vi.mocked(mockOpenRouterService.generate).mockRejectedValueOnce(
  new Error('message')
);

// Reset all mocks between tests
vi.resetAllMocks();
```

That's it! You only care about the output of `.generate()`, not how it gets there.
