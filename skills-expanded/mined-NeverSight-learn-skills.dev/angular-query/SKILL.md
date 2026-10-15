---
name: angular-query
description: "ALWAYS use when working with TanStack Query (Angular Query) for server state management, data fetching, caching, or mutations in Angular applications."
metadata:
  version: 5.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# @tanstack/angular-query-experimental

**Version:** 5.x (2025)
**Tags:** Data Fetching, Server State, Caching, TanStack Query

**References:** [Docs](https://tanstack.com/query/latest/docs/framework/angular/overview) • [GitHub](https://github.com/TanStack/query) • [npm](https://www.npmjs.com/package/@tanstack/angular-query-experimental)

## API Changes

This section documents version-specific API changes.

- NEW: Angular Query v5 — Signal-based API for TanStack Query [source](https://tanstack.com/query/latest/docs/framework/angular/overview)

- NEW: `injectQuery` — Signal-based query injection

- NEW: `injectMutation` — Signal-based mutation injection

- NEW: Query options pattern — Service-based query configuration

- NEW: DevTools integration — Angular Query DevTools for debugging

## Best Practices

- Install and setup

```bash
npm install @tanstack/angular-query-experimental
```

```ts
import { provideHttpClient } from '@angular/common/http';
import { provideTanStackQuery } from '@tanstack/angular-query-experimental';
import { QueryClient } from '@tanstack/query-core';

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(),
    provideTanStackQuery(new QueryClient())
  ]
};
```

- Use injectQuery for data fetching

```ts
import { injectQuery } from '@tanstack/angular-query-experimental';

@Component({})
export class TodosComponent {
  private http = inject(HttpClient);
  
  query = injectQuery(() => ({
    queryKey: ['todos'],
    queryFn: () => lastValueFrom(this.http.get<Todo[]>('/api/todos'))
  }));
}
```

- Use in templates with signals

```ts
@Component({
  template: `
    @if (query.isPending()) {
      Loading...
    } @else if (query.isError()) {
      Error: {{ query.error().message }}
    } @else {
      @for (todo of query.data(); track todo.id) {
        {{ todo.title }}
      }
    }
  `
})
export class TodosComponent {
  query = injectQuery(() => ({ ... }));
}
```

- Use mutations for data modification

```ts
import { injectMutation, injectQueryClient } from '@tanstack/angular-query-experimental';

@Component({})
export class AddTodoComponent {
  private http = inject(HttpClient);
  private queryClient = injectQueryClient();
  
  mutation = injectMutation(() => ({
    mutationFn: (newTodo: string) => 
      lastValueFrom(this.http.post('/api/todos', { title: newTodo })),
    onSuccess: () => {
      this.queryClient.invalidateQueries({ queryKey: ['todos'] });
    }
  }));
  
  addTodo(title: string) {
    this.mutation.mutate(title);
  }
}
```

- Use query options for reusable queries

```ts
@Injectable({ providedIn: 'root' })
export class TodoService {
  private http = inject(HttpClient);
  
  getTodoOptions = (id: number) => queryOptions({
    queryKey: ['todo', id],
    queryFn: () => lastValueFrom(this.http.get(`/api/todos/${id}`))
  });
}

@Component({})
export class TodoComponent {
  private todoService = inject(TodoService);
  
  todo = this.todoService.getTodoOptions(1);
}
```

- Handle loading and error states

```ts
query = injectQuery(() => ({
  queryKey: ['todos'],
  queryFn: () => fetchTodos(),
  retry: 3,
  staleTime: 1000 * 60 * 5, // 5 minutes
  refetchOnWindowFocus: false
}));
```

- Use invalidation for cache updates

```ts
mutation = injectMutation(() => ({
  mutationFn: createTodo,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['todos'] });
  }
}));
```

- Use optimistic updates

```ts
mutation = injectMutation(() => ({
  mutationFn: updateTodo,
  onMutate: async (newTodo) => {
    await queryClient.cancelQueries({ queryKey: ['todos'] });
    const previousTodos = queryClient.getQueryData(['todos']);
    queryClient.setQueryData(['todos'], (old: Todo[]) => [...old, newTodo]);
    return { previousTodos };
  },
  onError: (err, newTodo, context) => {
    queryClient.setQueryData(['todos'], context.previousTodos);
  }
}));
```
