---
name: angular-reactive
description: "ALWAYS use when working with Angular Reactive programming, BehaviorSubject, Observable patterns, or reactive state management in Angular."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# Angular Reactive Programming

**Version:** Angular 21 (2025)
**Tags:** Reactive, Observables, RxJS, BehaviorSubject

**References:** [Reactive Guide](https://angular.io/guide/reactive) • [RxJS](https://rxjs.dev)

## Best Practices

- Use BehaviorSubject for state

```ts
@Injectable({ providedIn: 'root' })
export class StateService {
  private state = new BehaviorSubject<State>(initialState);
  state$ = this.state.asObservable();
  
  updateState(newState: Partial<State>) {
    this.state.next({ ...this.state.value, ...newState });
  }
}
```

- Use Observable in services

```ts
@Injectable({ providedIn: 'root' })
export class DataService {
  private http = inject(HttpClient);
  
  getData(): Observable<Data[]> {
    return this.http.get<Data[]>('/api/data');
  }
}
```

- Use async pipe

```ts
@Component({
  template: `
    @if (data$ | async; as data) {
      {{ data.name }}
    }
  `
})
export class MyComponent {
  data$ = this.service.getData();
}
```

- Use shareReplay for caching

```ts
data$ = this.http.get('/api/data').pipe(
  shareReplay(1)
);
```

- Use takeUntil for cleanup

```ts
@Component({})
export class MyComponent implements OnDestroy {
  private destroy$ = new Subject<void>();
  
  ngOnInit() {
    this.data$.pipe(takeUntil(this.destroy$)).subscribe();
  }
  
  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```
