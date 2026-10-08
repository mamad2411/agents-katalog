---
description: 
globs: 
alwaysApply: true
---
# State Table Management in This Go Application

This document outlines the event-driven architecture used for managing "state tables" within this Go application. State tables are SQL tables (e.g., `users_v1`, `applications_v1`) that store persistent data. Their schema is defined and their contents are updated in response to specific events processed by dedicated handler functions.

## 1. Overview

The system employs an event-sourcing-inspired pattern where changes to application state are driven by events. Key components include:

*   **Events**: Go structs representing significant occurrences or actions within the system (e.g., a user being added, an application being registered). They typically embed `events.GenericEvent`.
*   **State Handlers**: Functions (e.g., `state.UserStateHandler`, `state.ApplicationStateHandler`) responsible for processing these events and updating the corresponding state tables in the database. Each handler manages a specific domain or set of tables.
*   **Event Mapper**: A function (e.g., `state.MapUserEventType`) responsible for deserializing generic event messages (often from JSON) into specific, typed Go event structs.
*   **Database Core (`database` package)**: Manages event persistence, transaction handling, and dispatching events to registered state handlers.

## 2. Defining State Tables & Their Initialization

State tables are standard SQL tables. Their schema definition and initialization are managed by their respective state handler functions.

*   **Responsibility**: Each state handler is associated with a logical group of tables or a domain. For instance, `ObjectStateHandler` is responsible for tables related to objects, such as `objects_v1`.
*   **Initialization Event (`events.DBInitEvent`)**: This special event is dispatched by the `database` core during system startup or when the database schema needs to be initialized/verified.
*   **Handler Logic for `DBInitEvent`**:
    *   When a state handler receives an `*events.DBInitEvent`, it executes SQL Data Definition Language (DDL) statements, typically `CREATE TABLE IF NOT EXISTS ...`. This ensures the necessary tables for its domain exist.
    *   Example from `users/state/db-objects.go`'s `ObjectStateHandler`:
        ```go
        case *events.DBInitEvent:
            // Create objects table
            _, err := tx.Exec(`
                CREATE TABLE IF NOT EXISTS objects_v1 (
                    id TEXT PRIMARY KEY,
                    display_name TEXT NOT NULL,
                )`)
            if err != nil {
                return false, fmt.Errorf("failed to create objects table: %w", err)
            }
            fmt.Println("Object tables initialized.")
            return true, nil
        ```
*   **Idempotency**: The use of `IF NOT EXISTS` in DDL statements makes the initialization process idempotent, meaning it can be run multiple times without causing errors or unintended side effects.

## 3. Defining Events

Events are Go structs that carry data about a specific occurrence.

*   **`events.GenericEvent`**: This struct is typically embedded in specific event types. It provides common fields like `Id` (usually system-generated) and `Type` (a string uniquely identifying the event, e.g., `"application:CREATE_OBJECT"`).
*   **Specific Event Structs**:
    *   Define fields for the data payload specific to that event.
    *   Use `json:"..."` struct tags for serialization from/to JSON if events are transmitted or stored in JSON format.
    *   Example: `users/state/db-objects.go` defines `CreateObjectEvent`:
        ```go
        type CreateObjectEvent struct {
            events.GenericEvent
            ObjectID    string `json:"id"`
            DisplayName string `json:"display_name"`
        }
        ```
*   **Event Type Naming Convention**: The `Type` string often follows a `application:ACTION` pattern (e.g., `notes:ADD_NOTE`). This helps in routing and understanding the event's purpose.

## 4. State Handler Logic

State handlers are functions that contain the business logic for reacting to events and modifying the state tables.

*   **Signature**: Typically `func(tx *sqlx.Tx, event events.Event) (bool, error)`
    *   `tx *sqlx.Tx`: An active `sqlx` database transaction. All database operations within a handler for a single event are performed within this transaction, ensuring atomicity.
    *   `event events.Event`: The specific, typed event instance (e.g., `*CreateObjectEvent`) to be processed.
    *   Return Values:
        *   `bool`: Indicates if the event was relevant to and handled by this specific handler (`true`) or not (`false`).
        *   `error`: Any error that occurred during processing.
*   **Event Processing**:
    *   A `switch evt := event.(type)` statement is used to differentiate between various event types the handler is concerned with.
    *   Based on the event type and its payload, the handler executes SQL Data Manipulation Language (DML) statements (e.g., `INSERT`, `UPDATE`, `DELETE`) against its managed state tables.
    *   Example from `ObjectStateHandler` handling `*CreateObjectEvent`:
        ```go
        case *CreateObjectEvent:
            fmt.Printf("Adding object: %s (ID: %s)\n", evt.DisplayName, evt.ObjectID)
            _, err := tx.Exec(`INSERT INTO objects_v1 (id, display_name) VALUES ($1, $2)`,
                evt.ObjectID, evt.DisplayName)
            // ... error handling ...
            return true, nil
        ```
*   **Error Handling**: Robust error handling is crucial. If an error occurs, it should be returned to the caller (the `database` core) so the transaction can be rolled back.
*   **Irrelevant Events**: If an event type is not relevant to a particular handler, the handler should return `false, nil` to indicate it did not process the event, allowing other potential handlers to process it.

## 5. Event Mapping

Events might originate from external sources as generic messages (e.g., JSON payloads from an API or a message queue). An event mapper translates these into concrete, typed Go event structs that state handlers can work with.

*   **Mapper Function** (e.g., `state.MapUserEventType` in `users/state/mapper.go`):
    *   Signature Example: `func(rawMessage *json.RawMessage, generic *events.GenericEvent) (events.Event, error)`
    *   It takes the raw event data (e.g., `*json.RawMessage`) and an `*events.GenericEvent` (which would have been unmarshaled first to determine its `Type`).
*   **Logic**:
    *   It uses a `switch` statement on `generic.GetType()`.
    *   For each recognized event type string, it unmarshals the `rawMessage` into the corresponding specific Go event struct (e.g., `ObjectCreatedEvent`).
    *   It copies the common fields from the input `generic` event to the specific event's embedded `GenericEvent`.
    *   It returns the fully populated, specific typed event.
    *   Example for `application:CREATE_OBJECT` (as added to `MapUserEventType`):
        ```go
        case "application:CREATE_OBJECT":
            var specificEvent CreateObjectEvent
            if err := json.Unmarshal(*rawMessage, &specificEvent); err != nil {
                return nil, fmt.Errorf("failed to unmarshal CreateObjectEvent: %w", err)
            }
            specificEvent.GenericEvent = *generic // Copy generic fields
            return &specificEvent, nil
        ```
*   **Handling Unknown/Non-Domain Events**: If an event type is not recognized or not relevant to the domain of the mapper, it might return the original `generic` event (allowing other mappers or handlers to process it) or an error, depending on system design.

## 6. Registration and Initialization (in `users/cmd/serve/main.go`)

For the system to function, state handlers and the event mapper must be registered with the central `database` component.

*   **State Handler Map**:
    *   A map (e.g., `handlers` in `main()`) associates string keys with their respective state handler functions. The keys (e.g., `"application_v1"`) act as identifiers for the table managed by the handler.
        ```go
        handlers := map[string]database.EventUpdateHandler{
            "application_v1":  state.ApplicationStateHandler, // Registered here
        }
        ```
    *   This map is passed to `database.Connect()`. The `database` package likely uses these keys to route events or manage schema versions associated with each handler.
*   **Event Mapper Initialization**:
    *   The event mapper function is provided to the database system, for example, via `db.InitHandlers(state.MapUserEventType)`. This tells the event processing pipeline how to convert raw event messages into typed Go structs.
*   **API Endpoint Initialization**:
    *   Helper functions (e.g., `state.InitApplicationHandlers(db)`) are called in `main()` to set up any HTTP API endpoints related to the data managed by these state tables (e.g., `/api/listobjects`).

This event-driven architecture provides a decoupled and organized way to manage database schema evolution and state modifications, enhancing modularity and making changes traceable through events.
