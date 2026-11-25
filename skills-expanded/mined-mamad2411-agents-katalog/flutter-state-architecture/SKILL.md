---
name: flutter-state-architecture
description: Arquitectura de estado de la app Flutter — separación UI/lógica/datos, estado de servidor vs estado de app, inmutabilidad, inyección de dependencias y testabilidad, con Riverpod (Notifier/AsyncNotifier) como referencia. Usar al decidir dónde vive un dato, al traer datos asíncronos a una pantalla, al escribir un notifier/provider o un repositorio, o cuando la lógica de negocio se está filtrando dentro de los widgets. La librería concreta la fija el CLAUDE.md del proyecto.
---

# Arquitectura de estado — Flutter

Separá tres capas y no las mezcles: **presentación** (widgets), **aplicación** (estado y casos
de uso) y **datos** (repositorios, DTOs, clientes de API). El widget muestra estado y emite
intenciones; nunca hace `http` ni contiene reglas de negocio.

> La elección de librería (Riverpod / Bloc / Provider) la fija el CLAUDE.md del proyecto. Los
> ejemplos usan **Riverpod** (Notifier/AsyncNotifier, verificado contra su doc v3). El patrón
> —capas, inmutabilidad, DI, testabilidad— vale igual con Bloc.

## 1. Estado de servidor vs estado de app

- **Estado de servidor**: datos que viven en el backend (agenda, ficha, catálogos). Se *cachean*,
  tienen carga/error/refresco. Modelalos como asíncronos (`AsyncValue`/`AsyncNotifier`), no como
  un `bool loading` + variable suelta.
- **Estado de app/UI**: filtros, pestaña activa, borrador de formulario. Vive en la capa de
  aplicación o, si es efímero del widget, en su `State`.
- No guardes copias del estado de servidor en variables locales que se desincronizan.

## 2. Notifier / AsyncNotifier

```dart
// Estado sincrónico de app
class FilterNotifier extends Notifier<AgendaFilter> {
  @override
  AgendaFilter build() => const AgendaFilter.today();
  void setRange(DateTimeRange r) => state = state.copyWith(range: r);
}
final filterProvider = NotifierProvider<FilterNotifier, AgendaFilter>(FilterNotifier.new);

// Estado de servidor (asíncrono): carga/dato/error los da AsyncValue
class AppointmentsNotifier extends AsyncNotifier<List<Appointment>> {
  @override
  Future<List<Appointment>> build() =>
      ref.watch(appointmentRepoProvider).findForDay(ref.watch(filterProvider).day);
}
final appointmentsProvider =
    AsyncNotifierProvider<AppointmentsNotifier, List<Appointment>>(AppointmentsNotifier.new);
```

En la UI, resolvé los tres casos con `when`, sin `bool` sueltos:

```dart
ref.watch(appointmentsProvider).when(
  data: (items) => AppointmentList(items: items),
  loading: () => const AppointmentsSkeleton(),
  error: (e, _) => ErrorRetry(onRetry: () => ref.invalidate(appointmentsProvider)),
);
```

## 3. Inmutabilidad

- El estado es inmutable: campos `final`, `copyWith` para derivar. Nunca mutes una lista/objeto
  en su lugar; asigná un objeto nuevo a `state` para que se notifique el cambio.
- Considerá clases de valor con igualdad por valor (p. ej. `freezed` o `==`/`hashCode` propios;
  verificá el paquete en pub.dev antes de citarlo).

## 4. Inyección de dependencias

- Repositorios y clientes se exponen como providers; los notifiers los obtienen con `ref.watch`/
  `ref.read`. Nada de `new Repo()` dentro de un widget o notifier.
- Esto permite reemplazar la dependencia por un doble en tests con `overrides`.

## 5. Testabilidad

- La lógica vive en notifiers/casos de uso testeables sin `WidgetTester`: creá un
  `ProviderContainer` con `overrides`, ejercé el notifier y comprobá el estado.
- Los widgets se prueban aparte (ver `flutter-testing`), inyectando el estado ya listo.
- Un notifier que no se puede testear sin levantar la UI está acoplado de más: sacá la lógica.

```dart
final container = ProviderContainer(overrides: [
  appointmentRepoProvider.overrideWithValue(FakeAppointmentRepo()),
]);
addTearDown(container.dispose);
```

## Anti-patrones
- `setState` moviendo datos de negocio dentro del widget.
- `AsyncValue` reemplazado por `bool isLoading` + `String? error` + `List data`.
- Notifier que hace `http` directo en vez de pasar por un repositorio.
- Mutar `state.list.add(x)` en lugar de `state = [...state, x]`.
- Un `Provider` global gigante con todo el estado de la app.

## Checklist
- [ ] Tres capas separadas; el widget no tiene reglas de negocio ni llamadas de red.
- [ ] Estado de servidor modelado como asíncrono con carga/dato/error explícitos.
- [ ] Estado inmutable con `copyWith`; se asigna objeto nuevo, no se muta.
- [ ] Dependencias inyectadas por provider y reemplazables en tests.
- [ ] Lógica testeada con `ProviderContainer` sin levantar la UI. Ver `unit-testing`.
