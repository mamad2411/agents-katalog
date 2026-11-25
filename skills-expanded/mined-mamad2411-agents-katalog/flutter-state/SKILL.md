---
name: flutter-state
description: "State management en Flutter con Riverpod 3 y BLoC 9 (2026). Cubre StateNotifier, AsyncNotifier, FutureProvider, StreamProvider, BlocBuilder, Cubit, y cuándo elegir cada enfoque. Actívala al diseñar la arquitectura de estado, migrar de Provider a Riverpod, o implementar BLoC en apps enterprise."
---

# Flutter State Management

Guía de state management en Flutter 2026. **Riverpod 3 por defecto, BLoC 9 para enterprise.**

---

## Decisión

| Herramienta | Mejor para | Curva | Ejemplo Sputnik |
|-------------|-----------|-------|-----------------|
| **Riverpod 3** | Nuevos proyectos, equipos pequeños/medios | Media | App de órdenes con 3-5 pantallas |
| **BLoC 9** | Enterprise, equipos grandes, auditoría | Alta | App multi-módulo con 20+ pantallas |
| **Cubit** | Pantallas simples, lógica mínima | Baja | Formulario de login, settings |

---

## Riverpod 3

```dart
// providers/order_provider.dart
import 'package:riverpod_annotation/riverpod_annotation.dart';
part 'order_provider.g.dart';  // Generado por build_runner

// ✅ FutureProvider: datos async que se refrescan
@riverpod
Future<List<Order>> orderList(OrderListRef ref, {required String customerId}) async {
  final repository = ref.watch(orderRepositoryProvider);
  return repository.getByCustomer(customerId);
}

// ✅ Notifier: estado mutable con lógica
@riverpod
class CreateOrder extends _$CreateOrder {
  @override
  AsyncValue<Order?> build() => const AsyncData(null);

  Future<void> submit(CreateOrderInput input) async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      final repository = ref.read(orderRepositoryProvider);
      final order = await repository.create(input);
      ref.invalidate(orderListProvider);  // Refrescar lista
      return order;
    });
  }
}

// ✅ Provider simple (dependencias, repos)
@riverpod
OrderRepository orderRepository(OrderRepositoryRef ref) {
  return OrderRepository(ref.watch(httpClientProvider));
}
```

```dart
// Uso en widget
class OrdersListScreen extends ConsumerWidget {
  const OrdersListScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final ordersAsync = ref.watch(orderListProvider(customerId: 'CUST-001'));

    return switch (ordersAsync) {
      AsyncData(:final value) => ListView.builder(
          itemCount: value.length,
          itemBuilder: (_, i) => OrderCard(order: value[i]),
        ),
      AsyncError(:final error) => ErrorWidget(message: error.toString()),
      _ => const CircularProgressIndicator(),
    };
  }
}
```

---

## BLoC 9

```dart
// blocs/order/order_event.dart
sealed class OrderEvent {}
class LoadOrders extends OrderEvent {
  final String customerId;
  const LoadOrders(this.customerId);
}
class CreateOrder extends OrderEvent {
  final CreateOrderInput input;
  const CreateOrder(this.input);
}

// blocs/order/order_state.dart
sealed class OrderState {}
class OrderInitial extends OrderState {}
class OrderLoading extends OrderState {}
class OrdersLoaded extends OrderState {
  final List<Order> orders;
  const OrdersLoaded(this.orders);
}
class OrderError extends OrderState {
  final String message;
  const OrderError(this.message);
}

// blocs/order/order_bloc.dart
class OrderBloc extends Bloc<OrderEvent, OrderState> {
  final OrderRepository _repository;

  OrderBloc(this._repository) : super(OrderInitial()) {
    on<LoadOrders>(_onLoadOrders);
    on<CreateOrder>(_onCreateOrder);
  }

  Future<void> _onLoadOrders(LoadOrders event, Emitter<OrderState> emit) async {
    emit(OrderLoading());
    try {
      final orders = await _repository.getByCustomer(event.customerId);
      emit(OrdersLoaded(orders));
    } catch (e) {
      emit(OrderError(e.toString()));
    }
  }

  Future<void> _onCreateOrder(CreateOrder event, Emitter<OrderState> emit) async {
    emit(OrderLoading());
    try {
      await _repository.create(event.input);
      // Recargar lista
      add(LoadOrders(event.input.customerId));
    } catch (e) {
      emit(OrderError(e.toString()));
    }
  }
}
```

```dart
// Uso en widget con BlocBuilder
class OrdersListScreen extends StatelessWidget {
  const OrdersListScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<OrderBloc, OrderState>(
      builder: (context, state) => switch (state) {
        OrdersLoaded(:final orders) => ListView.builder(
            itemCount: orders.length,
            itemBuilder: (_, i) => OrderCard(order: orders[i]),
          ),
        OrderError(:final message) => ErrorWidget(message: message),
        _ => const CircularProgressIndicator(),
      },
    );
  }
}
```

---

## Cuándo cada uno

| Escenario | Riverpod | BLoC |
|-----------|----------|------|
| Pantalla simple con fetch | ✅ FutureProvider | ⚠️ Overkill |
| Formulario con submit | ✅ AsyncNotifier | ✅ Cubit |
| Módulo complejo (10+ eventos) | ⚠️ Lógica dispersa | ✅ Eventos + estados explícitos |
| Auditoría/trazabilidad | ❌ | ✅ Cada evento registrable |
| Equipo junior | ✅ Menos boilerplate | ❌ Curva alta |
| Equipo grande (5+ devs) | ⚠️ Libertad = inconsistencia | ✅ Estructura forzada |

---

## Checklist state

- [ ] Riverpod 3 por defecto, BLoC 9 para enterprise
- [ ] Estado async con `AsyncValue` (loading, data, error)
- [ ] Providers declarados con `@riverpod` (código generado)
- [ ] `ref.invalidate()` para refrescar datos después de mutación
- [ ] `ConsumerWidget`/`ConsumerStatefulWidget` para leer providers
- [ ] Sin `setState` para estado compartido entre pantallas
