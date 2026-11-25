---
name: hashhttpseffectwebsitedocstraithash
description: [Hash](https://effect.website/docs/trait/hash/) documentation and resources. Use this skill when working with [Hash](https://effect.website/docs/trait/hash/) or when the user mentions [hash](https://effect.website/docs/trait/hash/).
metadata:
  source: llms.txt
  source_url: https://effect.website/llms-full.txt
  generated: 2026-02-21T11:28:01.754Z
---

# [Hash](https://effect.website/docs/trait/hash/)

## Available Resources

### Overview

### Batching

### Caching

### Final Program

### Customizing Request Caching

### Overview

- **HostPort**
  - URL: #custom-configuration-types

### Basic Configuration Types

### Using Config with Schema

### Providing Default Values

### Handling Sensitive Values

### Combining Configurations

### Operators

### Custom Configuration Types

### Nested Configurations

### Mocking Configurations in Tests

### ConfigProvider

### Deprecations

### Overview

### What is a Runtime System?

- **context**
  - URL: /docs/requirements-management/services/#how-it-works

### The Default Runtime

- **context**
  - URL: /docs/requirements-management/services/#how-it-works

- **default services**
  - URL: /docs/requirements-management/default-services/

### Locally Scoped Runtime Configuration

### ManagedRuntime

### Overview

- **`effect`**
  - URL: https://effect-ts.github.io/effect/docs/effect

- **`@effect/cli`**
  - URL: https://effect-ts.github.io/effect/docs/cli

- **`@effect/opentelemetry`**
  - URL: https://effect-ts.github.io/effect/docs/opentelemetry

- **`@effect/platform`**
  - URL: https://effect-ts.github.io/effect/docs/platform

- **`@effect/printer`**
  - URL: https://effect-ts.github.io/effect/docs/printer

- **`@effect/rpc`**
  - URL: https://effect-ts.github.io/effect/docs/rpc

- **`@effect/typeclass`**
  - URL: https://effect-ts.github.io/effect/docs/typeclass

### Overview

### Environment

### Rationale

### Type Aliases

### Overview

### Key Developments

- **announcement here**
  - URL: https://dev.to/effect/a-bright-future-for-effect-455m

### FAQ

### Comparison Table

### Overview

### Synchronous API

### Asynchronous API

### Utilities

### Overview

### Comparing Effects and Promises: Key Distinctions

### Type safety

- **Expected Errors**
  - URL: /docs/error-management/expected-errors/

- **Managing Services**
  - URL: /docs/requirements-management/services/

### Creating

### Thenable

### Comparing Effect.gen with async/await

### Concurrency

### FAQ

### Overview

### Effect heavily relies on generators and generators are slow!

### Effect will make your code 500x slower!

### Effect has a huge performance overhead!

### The bundle size is HUGE!

### Effect is impossible to learn, there are so many functions and modules!

- **Effect.succeed**
  - URL: /docs/getting-started/creating-effects/#succeed

- **Effect.fail**
  - URL: /docs/getting-started/creating-effects/#fail

- **Effect.sync**
  - URL: /docs/getting-started/creating-effects/#sync

- **Effect.tryPromise**
  - URL: /docs/getting-started/creating-effects/#trypromise

- **Effect.gen**
  - URL: /docs/getting-started/using-generators/

- **Effect.runPromise**
  - URL: /docs/getting-started/running-effects/#runpromise

- **Effect.catchTag**
  - URL: /docs/error-management/expected-errors/#catchtag

- **Effect.catchAll**
  - URL: /docs/error-management/expected-errors/#catchall

- **Effect.acquireRelease**
  - URL: /docs/resource-management/scope/#acquirerelease

- **Effect.acquireUseRelease**
  - URL: /docs/resource-management/introduction/#acquireuserelease

- **Effect.provide**
  - URL: /docs/requirements-management/layers/#providing-a-layer-to-an-effect

- **Effect.provideService**
  - URL: /docs/requirements-management/services/#providing-a-service-implementation

- **Effect.andThen**
  - URL: /docs/getting-started/building-pipelines/#andthen

- **Effect.map**
  - URL: /docs/getting-started/building-pipelines/#map

- **Effect.tap**
  - URL: /docs/getting-started/building-pipelines/#tap

- **Effect**
  - URL: https://effect-ts.github.io/effect/effect/Effect.ts.html

- **Context**
  - URL: /docs/requirements-management/services/#creating-a-service

- **Layer**
  - URL: /docs/requirements-management/layers/

- **Option**
  - URL: /docs/data-types/option/

- **Either**
  - URL: /docs/data-types/either/

- **Array**
  - URL: https://effect-ts.github.io/effect/effect/Array.ts.html

- **Match**
  - URL: /docs/code-style/pattern-matching/

### Effect is the same as RxJS and shares its problems

### Effect should be a language or Use a different language

### Overview

### Installation

### Define an Interaction with a Language Model

### Select a Provider

### Understanding `Model`

### Create a Provider Client

### Running the Program

### Overview

### Why Effect for AI?

### Core Concepts

### Packages

- **Chat Completions API**
  - URL: https://platform.openai.com/docs/api-reference/chat

- **Embeddings API**
  - URL: https://platform.openai.com/docs/api-reference/embeddings

- **Messages API**
  - URL: https://docs.anthropic.com/en/api/messages

- **Converse API**
  - URL: https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html

- **Gemini API**
  - URL: https://ai.google.dev/api

### Overview

### Planning LLM Interactions

### Creating Execution Plans

### Adding Fallback Models

### End-to-End Usage

### Overview

### Defining a Tool

### Benefits

### Overview

### What is Equivalence?

### Using Built-in Equivalences

### Deriving Equivalences

### Overview

### Using the Built-in Orders

### Sorting Arrays

### Deriving Orders

### Combining Orders

### Additional Useful Functions

### Overview

### Creating a Cache

### Concurrent Access

### Capacity

### Time To Live (TTL)

### Methods

### Overview

### cachedFunction

### once

### cached

### cachedWithTTL

### cachedInvalidateWithTTL

### Overview

### The Problem with TypeScript's Structural Typing

### How Branded Types Help

### Generalizing Branded Types

### Constructing Branded Types

### Combining Branded Types

### Overview

### Using plain pipe

### Using the "do simulation"

### Using Effect.gen

### Overview

### Effect.map as a dual API

### Overview

### Using runMain

### Avoid Tacit Usage

- **link to thread**
  - URL: https://twitter.com/MichaelArnaldi/status/1670715270845935616

### Overview

### How Pattern Matching Works

- **type**
  - URL: #matching-by-type

### Creating a matcher

### Defining patterns

### Completing the match

### Overview

### Concurrency Options

### Interruptions

### Racing

### Overview

### Creating a Deferred

### Awaiting

### Completing

### Checking Completion Status

### Common Use Cases

### Overview

### What Are Virtual Threads?

### How Fibers work

### The Fiber Data Type

### Forking Effects

### Joining Fibers

### Awaiting Fibers

### Interruption Model

### Composing Fibers

### Lifetime of Child Fibers

### When do Fibers run?

### Overview

### The Latch Interface

### Creating a Latch

### Latch vs Semaphore

### Overview

### Basic Operations

### Creating a PubSub

### Operators On PubSubs

### PubSub as an Enqueue

### Overview

### Basic Operations

### Creating a Queue

### Adding Items to a Queue

### Consuming Items from a Queue

### Shutting Down a Queue

### Offer-only / Take-only Queues

### Overview

### Creating a Semaphore

### withPermits

### Overview

### How BigDecimal Works

### Creating a BigDecimal

### Basic Arithmetic Operations

### Comparison Operations

### Normalization and Equality

### Overview

### Creating Causes

### Cause Variations

### Retrieving the Cause of an Effect

### Guards

### Pattern Matching

### Pretty Printing

### Retrieval of Failures and Defects

### Overview

### Why Use Chunk?

### Creating a Chunk

### Concatenating

### Dropping

### Comparing

### Converting

### Overview

### The DateTime Type

### The DateTime.Parts Type

### The DateTime.Input Type

- **parts**
  - URL: #the-datetimeparts-type

- **Date.parse**
  - URL: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/parse

### Utc Constructors

### Zoned Constructors

### Current Time

### Guards

### Time Zone Management

### Comparisons

### Conversions

### Parts

### Math

### Formatting

### Layers for Current Time Zone

### Overview

### Value Equality

### Constructors

### Union of Tagged Structs

### Errors

### Overview

### Creating Durations

### Getting the Duration Value

### Comparing Durations

### Performing Arithmetic Operations

### Conversions

### Overview

### Understanding Either and Exit

### Creating Eithers

### Guards

### Pattern Matching

### Mapping

### Interop with Effect

### Combining Two or More Eithers

### gen

### Overview

- **Cause**
  - URL: /docs/data-types/cause/

### Creating Exits

### Pattern Matching

### Exit vs Either

### Exit vs Effect

### Overview

- **HashSet**
  - URL: /docs/data-types/hash-set/#hashset

- **MutableHashSet**
  - URL: /docs/data-types/hash-set/#mutablehashset

### Performance characteristics

### Equality and uniqueness

### HashSet

### MutableHashSet

### Interoperability with JavaScript

### Overview

### Creating Options

### Guards

### Pattern Matching

### Working with Option

### Getting the Value from an Option

### Fallback

### Interop with Nullable Types

### Interop with Effect

### Combining Two or More Options

### gen

### Equivalence

### Sorting

### Overview

### make

### value

### unsafeWipe

### getEquivalence

### Overview

### validate

### validateAll

### validateFirst

### partition

### Overview

### Map Operations

### Filtering the Success Channel

### Inspecting Errors

### Exposing Errors in The Success Channel

### Exposing the Cause in The Success Channel

### Merging the Error Channel into the Success Channel

### Flipping Error and Success Channels

### Overview

### Error Tracking

### Short-Circuiting

### Catching All Errors

### Catching Some Errors

### Effect.fn

- **tracing**
  - URL: /docs/observability/tracing/

### Overview

### orElse

### orElseFail

### orElseSucceed

### firstSuccessOf

### Overview

### match

### ignore

### matchEffect

### matchCause

### matchCauseEffect

### Overview

### Parallel Errors

### Sequential Errors

### Overview

### retry

### retryOrElse

### Overview

### sandbox / unsandbox

### Overview

### Basic Usage

### Handling Timeouts

### Disconnection on Timeout

### Customizing Timeout Behavior

### Overview

### Expected Errors

### Unexpected Errors

### Overview

### Creating Unrecoverable Errors

### Converting Failures to Defects

### Catching All Defects

### Catching Some Defects

### Overview

### Data.Error

### Data.TaggedError

### Overview

### Why Pipelines are Good for Structuring Your Application

### Functions vs Methods

### pipe

### map

### as

### flatMap

### andThen

### tap

### all

### Build your first pipeline

### The pipe method

### Cheatsheet

### Overview

### if Expression

### Conditional Operators

### Zipping

### Looping

### Collecting

### Overview

### Why Not Throw Errors?

### Error Tracking

### Modeling Synchronous Effects

### Modeling Asynchronous Effects

### From a Callback

### Suspended Effects

### Cheatsheet

### Overview

### Effect LSP

### VS Code / Cursor Extension

### Overview

### Installing Effect

### Importing Modules and Functions

### Namespace imports

### Functions vs Methods

### Commonly Used Functions

### Overview

### Manual Installation

### Overview

### How to Use These Docs

- **/llms.txt**
  - URL: https://effect.website/llms.txt

- **/llms-full.txt**
  - URL: https://effect.website/llms-full.txt

- **/llms-small.txt**
  - URL: https://effect.website/llms-small.txt

### Join our Community

### Overview

### runSync

### runSyncExit

- **Cause**
  - URL: /docs/data-types/cause/

### runPromise

### runPromiseExit

- **Cause**
  - URL: /docs/data-types/cause/

### runFork

### Synchronous vs. Asynchronous Effects

### Cheatsheet

### Overview

### Type Parameters

### Extracting Inferred Types

### Overview

### Understanding Effect.gen

### Comparing Effect.gen with async/await

### Embracing Control Flow

### How to Raise Errors

### The Role of Short-Circuiting

### Passing `this`

### Adapter <Badge text="Deprecated" variant="caution" />

### Overview

### The Effect Pattern

### Don't Re-Invent the Wheel

### Solving Practical Problems

### Enjoy Building and Learning

### Overview

### Importing Micro

### Main Types

### How to Use This Guide

### Creating Effects

### Running Effects

### Building Pipelines

### Expected Errors

### Unexpected Errors

### Timing Out

### Requirements Management

### Scope

### Retrying

### Repetition

### Timing out

### Sandboxing

### Error Channel Operations

### Requirements Management

### Scoping, Resources and Finalization

### Concurrency

### Overview

### Importing Micro

### The Micro Type

### The MicroExit Type

### The MicroCause Type

### Wrapping a Promise-based API with Micro

### Expected Errors

### Unexpected Errors

### Fallback

### Matching

### Retrying

### Timing out

### Sandboxing

### Inspecting Errors

### Yieldable Errors

### Requirements Management

### Resource Management

### Scheduling

### Concurrency

### Interruptions

### Racing

### Overview

### Advantages Over Traditional Logging

- **custom logger**
  - URL: #custom-loggers

### log

### Log Levels

### Custom Annotations

### Log Spans

### Disabling Default Logging

### Loading the Log Level from Configuration

### Custom loggers

### Built-in Loggers

### Combine Loggers

### Overview

### Counter

### Gauge

### Histogram

### Summary

### Frequency

### Tagging Metrics

### Overview

### Overview

### Spans

### Traces

### Creating Spans

### Printing Spans

### Adding Annotations

### Logs as events

### Nesting Spans

### Tutorial: Visualizing Traces

- **https://www.docker.com/**
  - URL: https://www.docker.com/

- **Tempo TraceQL Interface**
  - URL: ../_assets/tempo-traceql-interface.png "The Grafana Tempo TraceQL interface without a TraceQL query specified"

### Integrations

### Overview

### Creating Commands

### Running Commands

### Custom Environment Variables

### Feeding Input to a Command

### Fetching Process Details

### Streaming stdout to process.stdout

### Overview

### Basic Usage

### Mocking the File System

### Overview

### Installation

### Getting Started with Cross-Platform Programming

### Overview

### Basic Usage

### Built-in Implementations

### Working with Non-String Values

### Overview

### Basic Usage

### Overview

### Overview

### Running Your Main Program with runMain

### Overview

### Basic Usage

### Writing to standard output

### Reading from standard input

### Example: Number guessing game

### Overview

### Overriding Default Services

### Overview

### Memoization When Providing Globally

### Acquiring a Fresh Version

### No Memoization When Providing Locally

### Manual Memoization

### Overview

### Designing the Dependency Graph

### Avoiding Requirement Leakage

### Creating Layers

### Combining Layers

### Providing a Layer to an Effect

### Converting a Layer to an Effect

### Tapping

### Error Handling

### Simplifying Service Definitions with Effect.Service

### Overview

### Managing Services with Effect

### How It Works

### Creating a Service

### Using the Service

### Providing a Service Implementation

### Extracting the Service Type

### Using Multiple Services

### Handling Services with Dependencies

### Overview

### Finalization

### acquireUseRelease

### Overview

### addFinalizer

### Manually Create and Close Scopes

### Defining Resources

### Overview

### Infinite and Fixed Repeats

### Recurring at specific intervals

### Increasing Delays Between Executions

### Overview

### Creating a Cron

### Parsing Cron Expressions

### Checking Dates with match

### Finding the Next Run

### Iterating Over Future Dates

### Converting to Schedule

### Overview

### Handling Timeouts and Retries for API Calls

### Retrying API Calls Based on Specific Errors

### Retrying with Dynamic Delays Based on Error Information

### Running Periodic Tasks Until Another Task Completes

### Overview

### Retrying and Repetition

### Composability of Schedules

### Overview

### repeat

### repeatN

### repeatOrElse

### Repeating Based on a Condition

### Overview

### Composition

### Adding Randomness to Retry Delays

### Controlling Repetitions with Filters

### Adjusting Delays Based on Output

### Tapping

### Overview

### Declaring New Data Types

### Branded types

- **`effect/Brand`**
  - URL: /docs/code-style/branded-types/

### Property Signatures

### Extending Schemas

### Renaming Properties

### Recursive Schemas

### Overview

### Built-in Annotations

### Concurrency Annotation

### Handling Decoding Errors with Fallbacks

### Custom Annotations

### Overview

### Filters

### Transformations and Arbitrary Generation

### Customizing Arbitrary Data Generation

### Overview

### Primitives

### asSchema

### Unique Symbols

### Literals

### Template literals

### Native enums

### Unions

### Tuples

### Arrays

### Non Empty Arrays

### Records

### Structs

### Tagged Structs

### instanceOf

### Picking

### Omitting

### partial

### required

### keyof

### Overview

- **Data.Class**
  - URL: /docs/data-types/data/#class

### Definition

### Validating Properties via Class Constructors

### Automatic Hashing and Equality in Classes

### Extending Classes with Custom Logic

### Leveraging Classes as Schema Definitions

### Adding Annotations

### Recursive Schemas

### Tagged Class variants

### Extending existing Classes

### Transformations

### Overview

### Structs

### Records

### Filters

### Branded Types

### Error Handling in Constructors

### Setting Default Values

### Overview

### Interop With Data

### Config

- **TreeFormatter.formatErrorSync**
  - URL: /docs/schema/error-formatters/#treeformatter-default

### Option

### Either

### Exit

### ReadonlySet

### ReadonlyMap

### HashSet

### HashMap

### SortedSet

### Duration

### Redacted

### Overview

### Equivalence for Any, Unknown, and Object

### Customizing Equivalence Generation

### Overview

### TreeFormatter (default)

### ArrayFormatter

### React Hook Form

### Overview

### Default Error Messages

### Custom Error Messages

### Overview

### Declaring Filters

### The Predicate Function

### Adding Annotations

### Specifying Error Paths

### Multiple Error Reporting

### Exposed Values

### Built-in Filters

### Overview

### Defining a schema

### Extracting Inferred Types

### Readonly Types by Default

### Decoding

### Encoding

- **Either**
  - URL: /docs/data-types/either/

### ParseError

### Parse Options

### Type Guards

### Assertions

### Managing Missing Properties

### Naming Conventions

### Overview

### Requirements

### The Schema Type

### Understanding Schema Values

### Understanding Decoding and Encoding

### The Rule of Schemas

### Overview

### Targeting a Specific JSON Schema Version

### Specific Outputs for Schema Types

### Identifier Annotations

### Standard JSON Schema Annotations

### Recursive and Mutually Recursive Schemas

### Customizing JSON Schema Generation

### Specialized JSON Schema Generation with Schema.parseJson

### Overview

### Customizing Pretty Printer Generation

### Overview

### typeSchema

### encodedSchema

### encodedBoundSchema

### Overview

### Sync vs Async Validation

### Defects

### Overview

### transform

### transformOrFail

### One-Way Transformations with Forbidden Encoding

### Composition

### Effectful Filters

### String Transformations

### Number Transformations

### Boolean Transformations

### Symbol transformations

### BigInt transformations

### Date transformations

### BigDecimal Transformations

### Overview

### Combining Results with Concurrent Zipping

### Racing Sinks: First Completion Wins

### Overview

### Common Constructors

### Creating Sinks from Success and Failure

### Collecting

### Folding

### Overview

- **Chunk**
  - URL: /docs/data-types/chunk/

### Overview

### Collecting Leftovers

### Ignoring Leftovers

### Overview

### Adapting Sink Input

### Transforming Both Input and Output

### Filtering Input

### Overview

### Using Ref

### Using Ref in a Concurrent Environment

### Using Ref as a Service

### Sharing State Between Fibers

### Overview

### Overview

### Overview

### Using runCollect

### Using runForEach

### Using a Fold Operation

### Using a Sink

### Overview

### Common Constructors

### From Success and Failure

### From Chunks

### From Effect

### From Asynchronous Callback

### From Iterables

### From Repetition

### From Unfolding/Pagination

### From Queue and PubSub

### From Schedule

### Overview

### Recovering from Failure

### Recovering from Defects

### Recovery from Some Errors

### Recovering to Effect

### Retry a Failing Stream

### Refining Errors

### Timing Out

### Overview

### Use Cases

### What is a Stream?

### Understanding Streams

### Overview

### Acquire Release

### Finalization

### Ensuring

### Overview

### Tapping

### Taking Elements

### Streams as an Alternative to Async Iterables

### Mapping

### Filtering

### Scanning

### Draining

### Detecting Changes in a Stream

### Zipping

### Cartesian Product of Streams

### Partitioning

### Grouping

### Concatenation

### Merging

### Interleaving

### Interspersing

### Broadcasting

### Buffering

### Debouncing

### Throttling

### Scheduling

### Overview

### How TestClock Works

### Testing Recurring Effects

### Testing Clock

### Testing Deferred

### Overview

### How to Perform Equality Checking in Effect

- **Data**
  - URL: /docs/data-types/data/

### Working with Collections

### Overview

### Role of Hash in Equality Checking

- **Equal**
  - URL: /docs/trait/equal/

### Implementing the Hash Interface

## Additional Resources (Optional)

### Modeling Optional Properties

### Optional Services

### Optional Fields Primitives

## How to Use This Skill

Reference these resources when working with [Hash](https://effect.website/docs/trait/hash/).