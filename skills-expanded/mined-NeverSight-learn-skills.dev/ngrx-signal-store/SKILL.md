---
name: ngrx-signal-store
description: Generates NgRx SignalStore code and provides guidance on state management with @ngrx/signals. Trigger when working with SignalStore, signalState, patchState, withState, withComputed, withMethods, withProps, withLinkedState, withEntities, withHooks, signalStoreFeature, withFeature, rxMethod, signalMethod, deepComputed, events plugin, or any @ngrx/signals import.
license: MIT
metadata:
  author: Community
  version: '1.0'
---

# NgRx SignalStore Developer Guidelines

**Package:** `@ngrx/signals`
**Install:** `ng add @ngrx/signals@latest`

When working with NgRx SignalStore, consult the following references based on the task:

- **SignalState**: Lightweight signal-based state for components/services (`signalState`, `patchState`, `DeepSignal`). Read [signalstate.md](references/signalstate.md)
- **SignalStore Core**: Creating stores with `signalStore`, `withState`, `withComputed`, `withMethods`, providing/injecting, protected state. Read [signalstore-core.md](references/signalstore-core.md)
- **Custom Store Properties**: Using `withProps` to add static properties, observables, and dependencies. Read [signalstore-core.md](references/signalstore-core.md)
- **Linked State**: Using `withLinkedState` for state slices that depend on other signals. Read [signalstore-core.md](references/signalstore-core.md)
- **Entity Management**: `withEntities`, entity updaters (`addEntity`, `updateEntity`, `removeEntities`, etc.), named collections, custom IDs, `entityConfig`. Read [entity-management.md](references/entity-management.md)
- **Private Store Members**: Using `_` prefix for private state, properties, and methods. Read [signalstore-advanced.md](references/signalstore-advanced.md)
- **Lifecycle Hooks**: `withHooks` for `onInit`/`onDestroy`, state tracking with `getState`/`watchState`. Read [signalstore-advanced.md](references/signalstore-advanced.md)
- **Custom Store Features**: `signalStoreFeature`, `withFeature`, creating reusable features with input constraints. Read [signalstore-advanced.md](references/signalstore-advanced.md)
- **Events Plugin**: Event-based state management with `event`, `eventGroup`, `withReducer`, `withEventHandlers`, `Dispatcher`, scoped events. Read [events.md](references/events.md)
- **RxJS Integration**: `rxMethod` for reactive side effects with RxJS operators. Read [rxjs-integration.md](references/rxjs-integration.md)
- **SignalMethod**: `signalMethod` for managing side effects without RxJS. Read [rxjs-integration.md](references/rxjs-integration.md)
- **DeepComputed**: `deepComputed` for creating `DeepSignal` from computed objects. Read [rxjs-integration.md](references/rxjs-integration.md)
- **Testing**: Testing stores in isolation, mocking dependencies, `unprotected` helper, testing `rxMethod`/`signalMethod`. Read [testing.md](references/testing.md)
- **FAQ**: Common patterns (class-based stores, getting store types, constructor injection). Read [faq.md](references/faq.md)
