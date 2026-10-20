---
applyTo: "**/+(commands|queries)/*.+(command|query).ts"
---

# Commands and Queries Instructions

## Overview
Commands and Queries are the foundation of the CQRS (Command Query Responsibility Segregation) pattern in this application. They serve as data transfer objects (DTOs) that carry information between different layers of the application.

**CRITICAL REQUIREMENTS**:
- Commands handle state-changing operations (POST, PUT, DELETE)
- Queries handle data retrieval operations (GET)
- All commands and queries must have a unique type identifier
- Use TypeScript interfaces for payload structure
- Follow consistent naming conventions

## Command Structure

### Basic Command Pattern
Commands represent intentions to change application state:

```typescript
import { Command } from "@tshio/command-bus";

export const CREATE_USER_COMMAND_TYPE = "users/CREATE_USER";

export interface CreateUserCommandPayload {
  firstName: string;
  lastName: string;
  email: string;
  role?: string;
}

export class CreateUserCommand implements Command<CreateUserCommandPayload> {
  public type: string = CREATE_USER_COMMAND_TYPE;

  constructor(public payload: CreateUserCommandPayload) {}
}
```

### Command Naming Conventions
- **Type constant**: `FEATURE_ACTION_COMMAND_TYPE` pattern
- **Interface**: `{Action}CommandPayload` 
- **Class**: `{Action}Command`
- **File**: `{action}.command.ts`

By {action}, we mean a verb that describes the operation, e.g., CreateUser, UpdateOrder, DeleteProduct.

Examples:
```typescript
// User management commands
export const CREATE_USER_COMMAND_TYPE = "users/CREATE_USER";
export const UPDATE_USER_COMMAND_TYPE = "users/UPDATE_USER";
export const DELETE_USER_COMMAND_TYPE = "users/DELETE_USER";
export const ACTIVATE_USER_COMMAND_TYPE = "users/ACTIVATE_USER";

// Order management commands  
export const CREATE_ORDER_COMMAND_TYPE = "orders/CREATE_ORDER";
export const PROCESS_ORDER_COMMAND_TYPE = "orders/PROCESS_ORDER";
export const CANCEL_ORDER_COMMAND_TYPE = "orders/CANCEL_ORDER";
```

### Command Payload Patterns

#### Create Commands
```typescript
// create-user.command.ts
export const CREATE_USER_COMMAND_TYPE = "users/CREATE_USER";

export interface CreateUserCommandPayload {
  firstName: string;
  lastName: string;
  email: string;
  role: UserRole;
  preferences?: UserPreferences;
}

export class CreateUserCommand implements Command<CreateUserCommandPayload> {
  public type: string = CREATE_USER_COMMAND_TYPE;

  constructor(public payload: CreateUserCommandPayload) {}
}
```

#### Update Commands
```typescript
// update-user.command.ts
export const UPDATE_USER_COMMAND_TYPE = "users/UPDATE_USER";

export interface UpdateUserCommandPayload {
  id: string;                    // Always required for updates
  firstName?: string;            // Optional fields for partial updates
  lastName?: string;
  email?: string;
  status?: UserStatus;
  updatedBy: string;             // Audit information
}

export class UpdateUserCommand implements Command<UpdateUserCommandPayload> {
  public type: string = UPDATE_USER_COMMAND_TYPE;

  constructor(public payload: UpdateUserCommandPayload) {}
}
```

#### Delete Commands
```typescript
// delete-user.command.ts
export const DELETE_USER_COMMAND_TYPE = "users/DELETE_USER";

export interface DeleteUserCommandPayload {
  id: string;
  deletedBy: string;             // Audit information
  reason?: string;               // Optional deletion reason
}

export class DeleteUserCommand implements Command<DeleteUserCommandPayload> {
  public type: string = DELETE_USER_COMMAND_TYPE;

  constructor(public payload: DeleteUserCommandPayload) {}
}
```

#### Business Logic Commands
```typescript
// activate-user.command.ts
export const ACTIVATE_USER_COMMAND_TYPE = "users/ACTIVATE_USER";

export interface ActivateUserCommandPayload {
  id: string;
  activatedBy: string;
  activationReason?: string;
}

export class ActivateUserCommand implements Command<ActivateUserCommandPayload> {
  public type: string = ACTIVATE_USER_COMMAND_TYPE;

  constructor(public payload: ActivateUserCommandPayload) {}
}
```

#### Complex Business Commands
```typescript
// process-order.command.ts
export const PROCESS_ORDER_COMMAND_TYPE = "orders/PROCESS_ORDER";

export interface ProcessOrderCommandPayload {
  orderId: string;
  items: OrderItem[];
  shippingAddress: Address;
  paymentMethod: PaymentMethod;
  couponCode?: string;
  specialInstructions?: string;
}

export interface OrderItem {
  productId: string;
  quantity: number;
  price: number;
  customization?: ProductCustomization;
}

export class ProcessOrderCommand implements Command<ProcessOrderCommandPayload> {
  public type: string = PROCESS_ORDER_COMMAND_TYPE;

  constructor(public payload: ProcessOrderCommandPayload) {}
}
```

## Query Structure

### Basic Query Pattern
Queries represent requests for data retrieval:

```typescript
import { Query } from "@tshio/query-bus";

export const USERS_QUERY_TYPE = "users/USERS";

export interface UsersQueryPayload {
  page?: number;
  limit?: number;
  sort?: Record<string, 'ASC' | 'DESC'>;
  filter?: UserFilters;
  search?: string;
}

export class UsersQuery implements Query<UsersQueryPayload> {
  public type: string = USERS_QUERY_TYPE;

  constructor(public payload: UsersQueryPayload) {}
}
```

### Query Result Classes
Define structured result classes for complex queries:

```typescript
export class UsersQueryResult {
  constructor(
    public readonly data: PaginationResult<UserEntity>
  ) {}
}

export class GetUserQueryResult {
  constructor(
    public readonly user: UserEntity,
    public readonly permissions: UserPermissions
  ) {}
}
```

### Query Payload Patterns

#### List Queries with Pagination
```typescript
// users.query.ts
import { PaginationParamsDto } from "../../../shared/pagination-utils/pagination-utils";

export const USERS_QUERY_TYPE = "users/USERS";

export interface UsersQueryPayload extends PaginationParamsDto {
  search?: string;
  filter?: {
    status?: UserStatus[];
    role?: UserRole[];
    createdAfter?: Date;
    createdBefore?: Date;
  };
  sort?: {
    firstName?: 'ASC' | 'DESC';
    lastName?: 'ASC' | 'DESC';
    createdAt?: 'ASC' | 'DESC';
    email?: 'ASC' | 'DESC';
  };
}

export class UsersQuery implements Query<UsersQueryPayload> {
  public type: string = USERS_QUERY_TYPE;

  constructor(public payload: UsersQueryPayload) {}
}

export class UsersQueryResult {
  constructor(
    public readonly data: PaginationResult<UserEntity>
  ) {}
}
```

#### Single Item Queries
```typescript
// get-user.query.ts
export const GET_USER_QUERY_TYPE = "users/GET_USER";

export interface GetUserQueryPayload {
  id: string;
  includePermissions?: boolean;
  includeProfile?: boolean;
  includeOrders?: boolean;
}

export class GetUserQuery implements Query<GetUserQueryPayload> {
  public type: string = GET_USER_QUERY_TYPE;

  constructor(public payload: GetUserQueryPayload) {}
}

export class GetUserQueryResult {
  constructor(
    public readonly user: UserEntity,
    public readonly permissions?: UserPermissions
  ) {}
}
```

#### Complex Search Queries
```typescript
// search-products.query.ts
export const SEARCH_PRODUCTS_QUERY_TYPE = "products/SEARCH_PRODUCTS";

export interface SearchProductsQueryPayload {
  query: string;
  category?: string[];
  priceRange?: {
    min: number;
    max: number;
  };
  inStock?: boolean;
  brand?: string[];
  location?: {
    latitude: number;
    longitude: number;
    radius: number;
  };
  page?: number;
  limit?: number;
}

export class SearchProductsQuery implements Query<SearchProductsQueryPayload> {
  public type: string = SEARCH_PRODUCTS_QUERY_TYPE;

  constructor(public payload: SearchProductsQueryPayload) {}
}
```

## Best Practices

### Command Guidelines
- **Immutable**: Never modify command payload after creation
- **Intention revealing**: Command names should describe the business intention
- **Single responsibility**: One command should handle one business operation

### Query Guidelines
- **Specific**: Design queries for specific use cases rather than generic data access
- **Cacheable**: Structure queries to enable effective caching
- **Pagination**: Always include pagination for list queries
- **Filtering**: Provide flexible filtering options

### Naming Conventions
- **Commands**: Use imperative verbs (CreateUser, UpdateOrder, CancelPayment)
- **Queries**: Use descriptive nouns (Users, GetUserDetails, SearchProducts)
- **Types**: Use namespace/action pattern (users/CREATE_USER, orders/SEARCH)

### Data Transfer
- **Type safety**: Use TypeScript interfaces for all payloads
- **Serializable**: Ensure all payload data is JSON serializable
- **No business logic**: Keep commands/queries as pure data containers and leave logic to handlers
- **Documentation**: Document complex payload structures with examples

This structure ensures clean separation between HTTP concerns (actions), business logic (handlers), and data transfer (commands/queries) while maintaining type safety and clear data flow throughout the application.