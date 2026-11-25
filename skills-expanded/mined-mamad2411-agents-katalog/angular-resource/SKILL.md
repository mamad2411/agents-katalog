---
name: angular-resource
description: "ALWAYS use when working with Angular Resource, Angular 19 resource API, or new async data loading with signals."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# Angular Resource

**Version:** Angular 19+ (2025)
**Tags:** Resource, Async, Signals

**References:** [Resource API](https://angular.dev/guide/signals/resource)

## Best Practices

- Use resource for async data

```ts
import { resource } from '@angular/core/rxjs-interop';

@Component({})
export class MyComponent {
  private http = inject(HttpClient);
  
  users = resource({
    loader: () => this.http.get<User[]>('/api/users').toPromise()
  });
}
```

- Use with request

```ts
id = signal<string>('');

user = resource({
  request: () => ({ id: this.id() }),
  loader: ({ request }) => this.http.getUser(request.id).toPromise()
});
```
