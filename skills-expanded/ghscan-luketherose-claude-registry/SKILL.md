---
name: ngrx-expert
description: "This skill should be used when the user designs, reviews, or refactors NgRx state management: store design, event-driven actions, pure reducers, memoised selectors, effects, facade pattern, state normalisation. Also use when deciding whether NgRx is the right choice or a simpler alternative (signals, services) is enough. Trigger phrases: \"NgRx store\", \"add an action\", \"reducer\", \"memoised selector\", \"effect\", \"should I use NgRx\". Do not use for general Angular component patterns (use angular-expert)."
---

# Ngrx Expert

Design, implement and refactor NgRx state management for predictability, maintainability and testability.

## When NgRx is appropriate

**Use NgRx when:**
- State shared between multiple components not hierarchically related
- Complex side effects (API calls, cache, WebSocket, localStorage)
- Need for time-travel debugging or undo/redo
- Team with well-defined state boundaries between features
- Data flows with many interdependent transformations

**NgRx is overkill when:**
- State local to a single component
- Parent-child communication via @Input/@Output
- Isolated feature with simple state
- The problem can be solved with a service + BehaviorSubject

**Recommended alternative before NgRx**:
```typescript
@Injectable({ providedIn: 'root' })
export class ItemStateService {
  private _items$ = new BehaviorSubject<Item[]>([]);
  items$ = this._items$.asObservable();

  loadItems() {
    this.itemApi.getAll().pipe(
      tap(items => this._items$.next(items))
    ).subscribe();
  }
}
```
Always evaluate this alternative before reaching for NgRx.

---

## Structure of an NgRx store for a feature

```
features/[feature-name]/store/
  [feature].actions.ts
  [feature].reducer.ts
  [feature].selectors.ts
  [feature].effects.ts
  [feature].facade.ts
  index.ts:               barrel export
```

---

## Actions: event-driven naming

Actions describe **what happened**, not what to do.

```typescript
// ✅ Correct — event-driven, with source tag
export const loadItemsRequested = createAction(
  '[Item List Page] Load Items Requested'
);
export const itemsLoadedSuccessfully = createAction(
  '[Item API] Items Loaded Successfully',
  props<{ items: Item[] }>()
);
export const itemsLoadFailed = createAction(
  '[Item API] Items Load Failed',
  props<{ error: string }>()
);

// ❌ Avoid — command-driven, generic, does not describe the source
export const loadItems = createAction('[Item] Load');
export const setItems = createAction('[Item] Set', props<{ data: any[] }>());
```

**Source tag convention**: `[Context] Event That Occurred`
- Components: `[Item List Page]`
- API/Effects: `[Item API]`
- Router: `[Router]`

---

## Reducers: pure and deterministic

Absolute rules:
- No side effects, no async calls, no direct mutations
- Same input → same output, always
- Use spread operator or `immer` (included in NgRx 9+)

```typescript
export interface ItemState {
  entities: { [id: number]: Item };
  ids: number[];
  loading: boolean;
  error: string | null;
  selectedId: number | null;
}

const initialState: ItemState = {
  entities: {}, ids: [], loading: false, error: null, selectedId: null
};

export const itemReducer = createReducer(
  initialState,
  on(ItemActions.loadItemsRequested, state => ({
    ...state, loading: true, error: null
  })),
  on(ItemActions.itemsLoadedSuccessfully, (state, { items }) => {
    const entities = items.reduce((acc, i) => ({ ...acc, [i.id]: i }), {});
    return { ...state, entities, ids: items.map(i => i.id), loading: false };
  }),
  on(ItemActions.itemsLoadFailed, (state, { error }) => ({
    ...state, loading: false, error
  }))
);
```

---

## Selectors: memoised and composable

```typescript
const selectItemState = createFeatureSelector<ItemState>('items');

export const selectItemIds = createSelector(selectItemState, s => s.ids);
export const selectItemEntities = createSelector(selectItemState, s => s.entities);
export const selectItemLoading = createSelector(selectItemState, s => s.loading);
export const selectItemError = createSelector(selectItemState, s => s.error);

// Derived selectors — automatically memoised
export const selectAllItems = createSelector(
  selectItemIds, selectItemEntities,
  (ids, entities) => ids.map(id => entities[id])
);

export const selectActiveItems = createSelector(
  selectAllItems,
  items => items.filter(i => i.isActive)
);

export const selectSelectedItem = createSelector(
  selectItemEntities, selectItemState,
  (entities, state) => state.selectedId ? entities[state.selectedId] : null
);
```

**Rule**: any derivation logic that appears in multiple components belongs in a selector.

---

## Effects: one effect = one side effect

```typescript
@Injectable()
export class ItemEffects {

  loadItems$ = createEffect(() =>
    this.actions$.pipe(
      ofType(ItemActions.loadItemsRequested),
      switchMap(() =>
        this.itemApi.getAll().pipe(
          map(items => ItemActions.itemsLoadedSuccessfully({ items })),
          catchError(error => of(ItemActions.itemsLoadFailed({ error: error.message })))
        )
      )
    )
  );

  constructor(
    private actions$: Actions,
    private itemApi: ItemApiService
  ) {}
}
```

**Flattening strategies in effects** → `rxjs-expert` § Flattening strategies is the source of truth for operator selection.

Summary for NgRx effects context:
- `switchMap` → search/query (cancels the previous request)
- `concatMap` → sequential operations dependent on order
- `mergeMap` → independent parallel operations
- `exhaustMap` → form submit (ignores new dispatches during the request)

---

## Facade Pattern: recommended

The facade isolates components from the store. Components are unaware of the internal structure of the store.

```typescript
@Injectable({ providedIn: 'root' })
export class ItemFacade {
  items$    = this.store.select(selectAllItems);
  loading$  = this.store.select(selectItemLoading);
  error$    = this.store.select(selectItemError);
  selected$ = this.store.select(selectSelectedItem);

  constructor(private store: Store) {}

  loadItems() {
    this.store.dispatch(ItemActions.loadItemsRequested());
  }

  selectItem(id: number) {
    this.store.dispatch(ItemActions.itemSelected({ id }));
  }
}
```

**Advantages of the facade**:
- Components do not change if the store structure changes
- Easily mockable in tests
- Clear and stable interface towards consumers

---

## State Normalisation

For lists of entities, use normalised structures:

```typescript
// ❌ Avoid — O(n) search and slow updates
interface BadState { items: Item[]; }

// ✅ Prefer — O(1) access, efficient updates
interface GoodState {
  entities: { [id: number]: Item };
  ids: number[];
}

// Even better: @ngrx/entity
const adapter = createEntityAdapter<Item>();
export const initialState = adapter.getInitialState({ loading: false, error: null });
// adapter.addMany(), adapter.updateOne(), adapter.removeOne() — all O(1)
```

---

## State Boundaries

- Each feature store manages only the data of its own feature
- Data shared between features → global store (root)
- Data local to a feature → feature store (featureState)
- Do not insert data from one feature into the global store without an explicit reason

---

## Testing

```typescript
// Reducer
it('sets loading=true on loadItemsRequested', () => {
  const state = itemReducer(initialState, ItemActions.loadItemsRequested());
  expect(state.loading).toBe(true);
});

// Selector
it('filters active items', () => {
  const items = [{ id: 1, isActive: true }, { id: 2, isActive: false }];
  expect(selectActiveItems.projector(items).length).toBe(1);
});

// Effect (with jasmine-marbles)
it('dispatches itemsLoaded on API success', () => {
  actions$ = hot('-a', { a: ItemActions.loadItemsRequested() });
  itemApi.getAll.mockReturnValue(cold('-b|', { b: mockItems }));
  const expected = cold('--c', { c: ItemActions.itemsLoadedSuccessfully({ items: mockItems }) });
  expect(effects.loadItems$).toBeObservable(expected);
});
```

---

## Constraints

- Do not use NgRx if a service with BehaviorSubject solves the problem
- Reducers must be pure: no side effects
- No HTTP calls in reducers or selectors, only in effects
- If using a facade, components do not access the store directly
- Always type state with explicit interfaces: zero `any`