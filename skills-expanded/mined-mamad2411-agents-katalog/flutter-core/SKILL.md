---
name: flutter-core
description: "Guía principal de Flutter 3.44 y Dart 3.12 (2026). Cubre widgets, composición, stateful/stateless, hot reload, temas, navegación básica, null safety, records, patterns y fundamentos del framework. Actívala para cualquier tarea Flutter: nuevas pantallas, diseño de widgets, o migración de versiones. Las sub-skills del kit profundizan en dominios específicos."
---

# Flutter Core Guide

Guía canónica de Flutter 3.44 + Dart 3.12 (Mayo 2026). Stack móvil del equipo Sputnik: Flutter + SQL Server + .NET 10.

---

## Versiones

| Versión | Fecha | Novedades clave |
|---------|-------|-----------------|
| Flutter 3.44 | Mayo 2026 | Agentic Hot Reload, GenUI preview, Swift Package Manager default, Vulkan para Impeller |
| Dart 3.12 | Mayo 2026 | Private named parameters, primary constructors (experimental) |

---

## Widgets — Composición sobre herencia

```dart
// ✅ StatelessWidget (no tiene estado mutable)
class OrderCard extends StatelessWidget {
  final Order order;
  final VoidCallback? onCancel;

  const OrderCard({super.key, required this.order, this.onCancel});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Orden #${order.orderNumber}',
                style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 8),
            Text('Estado: ${order.status}'),
            Text('Total: \$${order.totalAmount.toStringAsFixed(2)}'),
            if (onCancel != null)
              TextButton(
                onPressed: onCancel,
                child: const Text('Cancelar'),
              ),
          ],
        ),
      ),
    );
  }
}

// ✅ StatefulWidget (tiene estado mutable)
class OrderForm extends StatefulWidget {
  const OrderForm({super.key});

  @override
  State<OrderForm> createState() => _OrderFormState();
}

class _OrderFormState extends State<OrderForm> {
  final _formKey = GlobalKey<FormState>();
  String _customerId = '';
  double _amount = 0;
  String _currency = 'MXN';
  bool _isSubmitting = false;

  Future<void> _handleSubmit() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isSubmitting = true);
    try {
      await createOrder(_customerId, _amount, _currency);
    } finally {
      setState(() => _isSubmitting = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(children: [
        TextFormField(
          decoration: const InputDecoration(labelText: 'ID del Cliente'),
          validator: (v) => v == null || v.isEmpty ? 'Requerido' : null,
          onChanged: (v) => _customerId = v,
        ),
        TextFormField(
          decoration: const InputDecoration(labelText: 'Monto'),
          keyboardType: TextInputType.number,
          validator: (v) {
            if (v == null) return 'Requerido';
            final n = double.tryParse(v);
            if (n == null || n <= 0) return 'Debe ser positivo';
            return null;
          },
          onChanged: (v) => _amount = double.tryParse(v) ?? 0,
        ),
        DropdownButtonFormField<String>(
          value: _currency,
          items: const [
            DropdownMenuItem(value: 'MXN', child: Text('MXN')),
            DropdownMenuItem(value: 'USD', child: Text('USD')),
          ],
          onChanged: (v) => setState(() => _currency = v!),
        ),
        const SizedBox(height: 16),
        ElevatedButton(
          onPressed: _isSubmitting ? null : _handleSubmit,
          child: Text(_isSubmitting ? 'Creando...' : 'Crear Orden'),
        ),
      ]),
    );
  }
}
```

---

## Dart 3.12 — Novedades

```dart
// ✅ Private named parameters (Dart 3.12) — parámetros nombrados privados
class OrderService {
  final String _apiKey;
  final Duration _timeout;

  // El guion bajo en named parameter: solo visible dentro de la librería
  const OrderService({required String apiKey, this._timeout = const Duration(seconds: 30)})
      : _apiKey = apiKey;
}

// ✅ Primary constructors (experimental en Dart 3.12)
// class OrderRepository(Database db);

// ✅ Records (Dart 3.0+)
(double amount, String currency) parsePrice(String input) {
  final parts = input.split(' ');
  return (double.parse(parts[0]), parts[1]);
}
final (amount, currency) = parsePrice('150.00 MXN');

// ✅ Patterns (Dart 3.0+)
switch (order.status) {
  case 'pending' || 'confirmed' => return true;  // Puede cancelar
  case 'shipped' || 'delivered' => return false;  // No puede
  _ => return false;
}

// ✅ Sealed classes (Dart 3.0+)
sealed class OrderState {}
class Loading extends OrderState {}
class Loaded extends OrderState {
  final List<Order> orders;
  const Loaded(this.orders);
}
class Error extends OrderState {
  final String message;
  const Error(this.message);
}
```

---

## Widgets clave

```dart
// ✅ ListView.builder (listas grandes, construye bajo demanda)
ListView.builder(
  itemCount: orders.length,
  itemBuilder: (context, index) => OrderCard(order: orders[index]),
)

// ✅ GridView (catálogo de productos)
GridView.builder(
  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
    crossAxisCount: 2,
    childAspectRatio: 0.75,
  ),
  itemCount: products.length,
  itemBuilder: (context, index) => ProductCard(product: products[index]),
)

// ✅ SingleChildScrollView (pantallas con contenido fijo)
SingleChildScrollView(
  child: Column(children: [
    OrderHeader(order: order),
    OrderItems(items: order.items),
    OrderTotal(total: order.total),
  ]),
)

// ✅ Stack + Positioned (overlays, badges)
Stack(
  children: [
    const Icon(Icons.shopping_cart),
    Positioned(
      right: 0,
      top: 0,
      child: Container(
        padding: const EdgeInsets.all(2),
        decoration: const BoxDecoration(color: Colors.red, shape: BoxShape.circle),
        child: Text('$count', style: const TextStyle(fontSize: 10)),
      ),
    ),
  ],
)
```

---

## Temas — Material 3

```dart
MaterialApp(
  theme: ThemeData(
    useMaterial3: true,
    colorSchemeSeed: Colors.blue,
    brightness: Brightness.light,
  ),
  darkTheme: ThemeData(
    useMaterial3: true,
    colorSchemeSeed: Colors.blue,
    brightness: Brightness.dark,
  ),
  home: const OrdersPage(),
);
```

---

## Estructura de proyecto

```
lib/
├── main.dart                     # Entry point + MaterialApp
├── config/
│   ├── theme.dart                # ThemeData
│   └── routes.dart               # GoRouter config
├── modules/
│   └── orders/
│       ├── models/
│       │   └── order.dart        # Modelos de datos
│       ├── repositories/
│       │   └── order_repository.dart  # Acceso a API
│       ├── providers/
│       │   └── order_provider.dart    # Riverpod/BLoC
│       ├── screens/
│       │   ├── orders_list_screen.dart
│       │   ├── order_detail_screen.dart
│       │   └── create_order_screen.dart
│       └── widgets/
│           ├── order_card.dart
│           └── order_form.dart
├── shared/
│   ├── widgets/
│   │   ├── loading_indicator.dart
│   │   └── error_widget.dart
│   └── utils/
│       ├── http_client.dart
│       └── formatters.dart
└── gen/                          # Código generado (build_runner)
    └── ...
```

---

## Reglas de oro

1. **`const` en todo widget que no dependa de estado.** Reduce rebuilds.
2. **`ListView.builder` sobre `ListView` para listas largas.** Construye solo lo visible.
3. **`StatefulWidget` solo cuando realmente hay estado mutable.**
4. **Extraer widgets grandes en widgets más pequeños.** Facilita lectura y optimiza rebuilds.
5. **`Form` + `TextFormField` para formularios.** Validación built-in.
6. **`GoRouter` para navegación.** Soporta deep links en móvil y web.
7. **`Riverpod` para state management (default 2026).** BLoC para enterprise.
8. **Null safety siempre.** Dart 3.x es sound null safe.

---

## Sub-skills del kit

| Skill | Cuándo cargarla |
|-------|-----------------|
| `flutter-state` | Riverpod 3, BLoC 9, Cubit, state management |
| `flutter-ui` | Material 3, temas, responsive, formularios avanzados, animaciones |
| `flutter-navigation` | GoRouter v17, deep linking, nested navigation, guards |
| `flutter-networking` | Dio, http, REST, WebSocket, caching |
| `flutter-storage` | SQLite (Drift), SharedPreferences, SecureStorage, Hive |
| `flutter-performance` | const widgets, RepaintBoundary, lazy loading, DevTools |
| `flutter-deployment` | App stores, Codemagic, versionado, code signing |

---

## Stack recomendado

| Propósito | Herramienta |
|-----------|-------------|
| State management | Riverpod 3 (default) o BLoC 9 (enterprise) |
| HTTP | Dio |
| Navegación | GoRouter |
| DB local | Drift (SQLite) |
| CI/CD | Codemagic |
