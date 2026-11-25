---
name: vantoan252003_mozi
description: vantoan252003 mozi
---

# GoMove Client App — Master Architecture Guide

> **AI Agent: Read this file first before touching any code.**
> This is the single source of truth for the entire project.

---

## 1. Project Overview

**GoMove** is a Flutter client application for ride-hailing and food delivery
(similar to Grab / Be App). This repository contains **only the customer-facing
client**. Driver app, merchant app, and Java backend live in separate repos.

**Core user flows:**
- Book a motorbike / car ride with live driver tracking
- Order food from nearby restaurants with live delivery tracking
- Manage wallet, vouchers, notifications, and profile

---

## 2. Tech Stack

| Concern              | Library / Tool                          |
|----------------------|-----------------------------------------|
| Framework            | Flutter ≥ 3.22, Dart ≥ 3.4              |
| State Management     | `flutter_bloc` + Cubit                  |
| Dependency Injection | `get_it` + `injectable`                 |
| Navigation           | `go_router` ≥ 13                        |
| HTTP Client          | `dio` + `retrofit`                      |
| WebSocket / Realtime | `socket_io_client`                      |
| Maps                 | `google_maps_flutter` + `flutter_polyline_points` |
| Location / GPS       | `geolocator` + `geocoding`              |
| Local Storage        | `hive_flutter` (cache) + `flutter_secure_storage` (tokens) |
| Push Notifications   | `firebase_messaging` + `flutter_local_notifications` |
| Payment Deep Links   | `url_launcher` (MoMo / ZaloPay)         |
| Functional           | `dartz` (Either<Failure, T>)            |
| Image Loading        | `cached_network_image`                  |
| Animations           | `lottie` + `shimmer`                    |
| Connectivity         | `connectivity_plus`                     |
| Permissions          | `permission_handler`                    |
| Code Generation      | `build_runner` + `injectable_generator` + `retrofit_generator` + `hive_generator` |
| Testing              | `bloc_test` + `mockito` + `flutter_test` |

---

## 3. Clean Architecture — Layer Rules

```
┌──────────────────────────────────────────────────────────────┐
│  PRESENTATION LAYER                                          │
│  ├── Pages        (StatelessWidget / StatefulWidget)         │
│  ├── Widgets      (reusable UI components)                   │
│  └── BLoC / Cubit (state management)                         │
│                                                              │
│  ✅ Can import: domain/entities, domain/usecases             │
│  ❌ Cannot import: data/models, data/datasources             │
└─────────────────────────┬────────────────────────────────────┘
                          │ calls UseCase.call()
┌─────────────────────────▼────────────────────────────────────┐
│  DOMAIN LAYER  (Pure Dart — zero Flutter imports)            │
│  ├── Entities     (immutable plain Dart objects)             │
│  ├── Repository   (abstract interfaces only)                 │
│  └── UseCases     (one public call() method each)            │
│                                                              │
│  ✅ Can import: core/errors (Failure types), dartz           │
│  ❌ Cannot import: anything Flutter, data layer, services    │
└─────────────────────────┬────────────────────────────────────┘
                          │ implements interface
┌─────────────────────────▼────────────────────────────────────┐
│  DATA LAYER                                                  │
│  ├── Models        (Entity subclasses with fromJson/toJson)  │
│  ├── RemoteDataSource  (Dio / Retrofit API calls)            │
│  ├── LocalDataSource   (Hive / SecureStorage)                │
│  └── RepositoryImpl    (catches exceptions → returns Failure)│
│                                                              │
│  ✅ Can import: domain layer (to implement it)               │
│  ✅ Can import: core/network, core/storage, core/errors      │
│  ❌ Cannot import: presentation layer                        │
└──────────────────────────────────────────────────────────────┘
```

---

## 4. Data Flow

```
Widget
  └─▶ BLoC/Cubit.add(Event) / cubit.method()
        └─▶ UseCase.call(params)
              └─▶ Repository interface.method()
                    └─▶ RepositoryImpl  (try / catch)
                          ├─▶ RemoteDataSource.apiCall()  ──▶ Dio ──▶ Backend API
                          └─▶ LocalDataSource.read()      ──▶ Hive / SecureStorage
                    ◀── Either<Failure, Model>
              ◀── Either<Failure, Entity>       (Model extends Entity, so same object)
        ◀── Either<Failure, Entity>
  ◀── BLoC emits new State  (ErrorState or LoadedState)
```

---

## 5. Directory Map

```
lib/
├── core/                  Infrastructure — shared by all features
│   ├── config/            Environment variables, flavors
│   ├── constants/         API endpoints, route names, Hive keys, socket events
│   ├── di/                GetIt + Injectable setup
│   │   └── modules/       @Module classes for 3rd-party singletons
│   ├── errors/            Failure hierarchy + Exception hierarchy
│   ├── network/           Dio factory, interceptors
│   │   └── interceptors/  Auth, Logging, Error interceptors
│   ├── router/            go_router config + route guards
│   ├── services/          Long-lived singleton services (NOT usecases)
│   │   ├── location/      GPS tracking, permission, geocoding
│   │   ├── socket/        Socket.IO connection manager
│   │   ├── notification/  FCM + local notifications
│   │   └── permission/    permission_handler wrapper
│   ├── storage/           Hive + SecureStorage wrappers
│   ├── theme/             Colors, typography, dimensions, ThemeData
│   └── utils/             Pure utility functions
│
├── features/              Business features (each self-contained)
│   ├── onboarding/
│   ├── auth/
│   ├── home/
│   ├── map/               Google Maps, Places search, routing
│   ├── ride/              Book ride, estimate, driver tracking
│   ├── food/              Restaurants, menu, cart, checkout
│   ├── tracking/          Realtime order tracking (shared)
│   ├── voucher/
│   ├── wallet/            Balance, top-up, payment methods
│   ├── profile/           User info, saved addresses
│   ├── notification/
│   ├── order_history/
│   ├── rating/
│   └── settings/
│
└── shared/                Reusable UI building blocks
    ├── widgets/           Pure UI components (no BLoC injected)
    ├── extensions/        Dart extension methods
    └── mixins/            Flutter StatefulWidget mixins

assets/
├── fonts/                 BeVietnamPro (Regular/Medium/SemiBold/Bold)
├── images/                PNG/JPG assets
├── icons/                 SVG icons
└── animations/            Lottie JSON files

test/
└── features/              Mirror of lib/features structure
```

---

## 6. Mandatory Rules for AI Agents

### 6.1 Layer Imports
```
FORBIDDEN:
  presentation/ → import 'package:.../data/...'
  domain/       → import 'package:flutter/...'
  domain/       → import 'package:.../data/...'

REQUIRED:
  Each UseCase has exactly ONE public method named call()
  RepositoryImpl must be the ONLY place that catches Exceptions
  All repository methods return Future<Either<Failure, T>>
```

### 6.2 Error Handling Contract
```
DataSource layer  → throws  Exception subclasses  (ServerException, CacheException...)
Repository layer  → catches Exception, returns Left(Failure)
UseCase layer     → NEVER try/catch, just returns Either
BLoC/Cubit layer  → fold() on Either, emit error state or success state
```

### 6.3 Naming Conventions
```
Files:        snake_case.dart
Classes:      PascalCase
BLoC files:   <name>_bloc.dart  +  <name>_event.dart  +  <name>_state.dart
Cubit files:  <name>_cubit.dart +  <name>_state.dart
UseCase:      <verb>_<noun>_usecase.dart  (class: VerbNounUseCase)
Model:        <name>_model.dart  (extends matching Entity)
DataSource:   <name>_remote_datasource.dart  /  <name>_local_datasource.dart
Repository:   <name>_repository.dart (abstract) / <name>_repository_impl.dart
```

### 6.4 State Management Choice
```
Use BLoC when:  multiple event types, complex transitions, ride/auth flows
Use Cubit when: simple load/error/loaded pattern, forms, lists
```

### 6.5 Hardcoding Forbidden
```
❌ Colors hardcoded   → ✅ use AppColors.xxx
❌ Font sizes         → ✅ use AppTypography.xxx
❌ API strings        → ✅ use ApiConstants.xxx
❌ Route strings      → ✅ use RouteConstants.xxx
❌ Hive key strings   → ✅ use HiveConstants.xxx
❌ Socket event names → ✅ use SocketEvents.xxx
❌ Tokens in Hive/SharedPrefs → ✅ use FlutterSecureStorage only
```

### 6.6 Services vs UseCases
```
Service  = long-lived singleton managed by DI, holds state (e.g. GPS stream, socket conn)
UseCase  = stateless, created fresh per use, calls Repository or Service

Services live in: core/services/
UseCases live in: features/<name>/domain/usecases/
```

### 6.7 CartCubit is Global
```
CartCubit is provided at MaterialApp level (not inside a single route).
When user adds an item from a different restaurant:
  → emit CartRestaurantConflict state
  → UI shows "Clear cart?" dialog
  → on confirm: clearCart() then addItem()
Cart state is persisted to Hive (cartBox) to survive app restart.
```

### 6.8 Code Generation
```
After adding @injectable, @singleton, @LazySingleton, @RestApi, @HiveType annotations:
  flutter pub run build_runner build --delete-conflicting-outputs
Generated files (*.g.dart, *.config.dart, *.freezed.dart) are gitignored.
```

---

## 7. Realtime Architecture

```
LocationService (GPS stream)
  ├── StreamSubscription managed per screen lifecycle
  └── Provides Stream<LocationEntity> to LocationBloc

SocketService (singleton)
  ├── connect(token)   → authenticate on WS handshake
  ├── disconnect()
  ├── joinRoom(orderId)
  ├── leaveRoom(orderId)
  ├── emit(event, data)
  └── on<T>(event)     → Stream<T>
        ├── consumed by TrackingBloc (driver location, status)
        └── consumed by NotificationCubit (new notification events)

NotificationService (singleton)
  ├── FCM background: handled by Firebase directly
  ├── FCM foreground: shows local notification via flutter_local_notifications
  └── tap payload → NavigationService.go(deepLink)
```

---

## 8. Feature Dependency Graph

```
auth ──────────────────────────────► home
                                       │
               ┌───────────────────────┼──────────────────┐
               ▼                       ▼                  ▼
             ride                    food              wallet
               │                       │
          map ◄┴───────────────────────┘
               │
           tracking  ◄──── shared by ride + food
               │
            rating  ◄──── triggered on order completion
               │
        order_history
```
