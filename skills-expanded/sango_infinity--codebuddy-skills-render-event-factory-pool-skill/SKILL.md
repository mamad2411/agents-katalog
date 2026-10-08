---
name: "render-event-factory-pool"
description: "Implements factory and pool for RenderEventBase classes. Invoke when creating or managing render events that need object pooling for memory optimization."
---

# Render Event Factory and Pool

## Overview

This skill provides a comprehensive implementation of a factory and pool system for `RenderEventBase` classes, enabling efficient object reuse and memory optimization in game rendering systems.

## Key Features

1. **Factory Pattern**: Creates instances of `RenderEventBase` subclasses through a centralized factory method
2. **Object Pooling**: Reuses event instances instead of creating new ones, reducing memory allocation and garbage collection
3. **Automatic Registration**: Automatically registers all `RenderEventBase` subclasses
4. **Lifecycle Management**: Handles event creation, initialization, and recycling

## Implementation Steps

### 1. Modify RenderEvent Class

Add the following components to the `RenderEvent` class:

- **Event Pool**: A dictionary of stacks to store reusable event instances
- **Event Types Registry**: A dictionary to store event type information
- **Factory Method**: `Create<T>()` to create or retrieve events from the pool
- **Registration Methods**: `RegisterEvent<T>()` and `RegisterAllEvents()` to register event types
- **Init Method**: To initialize the factory and register all event types
- **Return to Pool**: `ReturnToPool()` to recycle event instances

### 2. Add Init Methods to Event Classes

For each `RenderEventBase` subclass, add an `Init` method that:

- Takes all public member variables as parameters
- Initializes the event's state
- Resets the `IsDone` flag to `false`

### 3. Replace Direct Instantiation

Replace all instances of `new RenderEventBaseSubclass()` with `RenderEvent.Instance.Create<RenderEventBaseSubclass>()` followed by a call to the `Init` method.

## Usage Example

```csharp
// Before
CameraMoveEvent cameraMoveEvent = new CameraMoveEvent()
{
    targetPosition = position,
    dialogStyle = UIDialog.DialogStyle.ClickPersonSay,
    content = "Hello World",
    person = somePerson
};
RenderEvent.Instance.Add(cameraMoveEvent);

// After
CameraMoveEvent cameraMoveEvent = RenderEvent.Instance.Create<CameraMoveEvent>();
cameraMoveEvent.Init(position, 0.5f, UIDialog.DialogStyle.ClickPersonSay, "Hello World", somePerson, null, null);
RenderEvent.Instance.Add(cameraMoveEvent);
```

## Benefits

- **Memory Optimization**: Reduces memory allocation and garbage collection
- **Performance Improvement**: Faster event creation through object reuse
- **Centralized Management**: All event creation goes through a single factory
- **Consistent Initialization**: All events are initialized through standardized `Init` methods
- **Scalability**: Easy to add new event types without modifying the factory

## When to Use

Invoke this skill when:
- You need to optimize memory usage in your game's rendering system
- You're creating multiple instances of render events
- You want to standardize event creation and initialization
- You're working with a system that generates many short-lived events

## Best Practices

- Always use `RenderEvent.Instance.Create<T>()` instead of direct instantiation
- Always call `Init()` after creating an event instance
- Ensure all `RenderEventBase` subclasses have a properly implemented `Init` method
- Call `RenderEvent.Instance.Init()` during game initialization to register all event types
