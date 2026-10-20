---
alwaysApply: false
---

# API Hooks Rules

## Fetch Functions
Create async fetch functions with proper error handling:

```typescript
async function deleteRecipe(recipeId: string): Promise<void> {
  const response = await fetch(`/api/recipes/${recipeId}`, { method: "DELETE" });
  if (!response.ok) {
    if (response.status === 404) throw new Error("Recipe not found");
    if (response.status === 403) throw new Error("You don't have permission to delete this recipe");
    throw new Error("Failed to delete recipe");
  }
}
```

## Mutation Hooks
Handle all side effects (toasts, redirects, query invalidation) inside hooks:

```typescript
export function useDeleteRecipe(recipeId: string) {
  const mutation = useMutation({
    mutationFn: deleteRecipe,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["recipes"] });
      queryClient.invalidateQueries({ queryKey: ["recipe"] });
      queryClient.invalidateQueries({ queryKey: ["tags"] });

      toast.success("Przepis został pomyślnie usunięty!", {
        duration: 1500,
        onAutoClose: () => {
          closeDialog();
          window.location.href = "/recipes";
        },
      });
    },
    onError: (error: Error) => {
      toast.error(`Błąd podczas usuwania przepisu: ${error.message}`);
    },
  }, queryClient);

  return {
    mutate: mutation.mutate,
    mutateAsync: mutation.mutateAsync,
    isPending: mutation.isPending,
    isError: mutation.isError,
    error: mutation.error as Error | null,
    isSuccess: mutation.isSuccess,
    reset: mutation.reset,
  } as const;
}
```

## Query Hooks
Configure caching and return consistent interfaces:

```typescript
export function useRecipeDetail(recipeId: string) {
  const { data: recipe, isLoading, isError, error, refetch } = useQuery<RecipeDetailDto>({
    queryKey: ["recipe", recipeId],
    queryFn: () => fetchRecipeById(recipeId),
    refetchOnWindowFocus: false,
    staleTime: 5 * 60 * 1000,
  }, queryClient);

  return { recipe, isLoading, isError, error: error as Error | null, refetch } as const;
}
```

## Key Principles

### Separation of Concerns
- **Hooks**: Business logic, API calls, error handling, side effects (toasts/redirects)
- **Components**: UI rendering, hook calls, state-based rendering

### Patterns
- **Naming**: `use[Action][Entity]`, `fetch[Entity]By[Identifier]`
- **Query Keys**: `["entity", id]` or `["entity", "sub-entity", id]`
- **Caching**: 5min staleTime for details, invalidate related queries on mutations
- **Toasts**: Polish messages, `onAutoClose` for navigation/dialog management
- **Navigation**: `window.location.href` for redirects after mutations
