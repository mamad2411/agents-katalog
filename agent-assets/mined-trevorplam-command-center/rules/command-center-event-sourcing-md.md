---
description: Run Event Sourcing and CQRS Implementation Standards Check
globs:
  [
    '**/eventsourcing/**/*.ts',
    '**/cqrs/**/*.ts',
    '**/event-store/**/*.ts',
    '**/projections/**/*.ts',
  ]
---

# Architecture: Event Sourcing & CQRS Implementation Standards

<audit_rules>

- You MUST implement proper event sourcing with immutable event logs for all state changes.
- You MUST ensure all events contain complete data needed for state reconstruction.
- You MUST implement proper event versioning and schema evolution strategies.
- You MUST configure proper event storage with append-only semantics and durability guarantees.
- You MUST implement proper snapshot strategies for performance optimization.
- You MUST ensure proper event replay and time-travel capabilities.
- You MUST implement proper event serialization and deserialization with backward compatibility.
- You MUST configure proper event metadata and correlation tracking.
- You MUST implement proper event deletion and GDPR compliance for sensitive data.
- You MUST ensure proper event consistency and ordering guarantees.
  </audit_rules>

<example_good>

```typescript
// Event Sourcing Implementation

export class EventSourcingAggregate {
  constructor(
    private eventStore: EventStore,
    private snapshotStore: SnapshotStore,
    private eventBus: EventBus
  ) {}

  protected id: string
  protected version: number = 0
  protected uncommittedEvents: DomainEvent[] = []
  protected loadedVersion: number = 0

  async load(aggregateId: string): Promise<void> {
    this.id = aggregateId

    // Try to load from snapshot first
    const snapshot = await this.snapshotStore.getLatestSnapshot(aggregateId)

    if (snapshot) {
      this.version = snapshot.version
      this.loadedVersion = snapshot.version
      this.applySnapshot(snapshot)

      // Load events after snapshot
      const events = await this.eventStore.getEvents(aggregateId, snapshot.version + 1)
      events.forEach((event) => this.applyEvent(event))
    } else {
      // Load all events from beginning
      const events = await this.eventStore.getEvents(aggregateId)
      events.forEach((event) => this.applyEvent(event))
    }
  }

  protected async apply(event: DomainEvent): Promise<void> {
    // Apply event to aggregate state
    this.when(event)

    // Add to uncommitted events
    this.uncommittedEvents.push(event)

    // Update version
    this.version++
  }

  protected when(event: DomainEvent): void {
    // Implement event-specific state changes
    switch (event.type) {
      case 'UserCreated':
        this.whenUserCreated(event as UserCreatedEvent)
        break
      case 'UserUpdated':
        this.whenUserUpdated(event as UserUpdatedEvent)
        break
      case 'UserDeleted':
        this.whenUserDeleted(event as UserDeletedEvent)
        break
      default:
        throw new Error(`Unknown event type: ${event.type}`)
    }
  }

  async save(): Promise<void> {
    if (this.uncommittedEvents.length === 0) {
      return
    }

    // Validate events
    await this.validateEvents(this.uncommittedEvents)

    // Save events to event store
    await this.eventStore.saveEvents(this.id, this.uncommittedEvents, this.loadedVersion)

    // Publish events to event bus
    for (const event of this.uncommittedEvents) {
      await this.eventBus.publish(event)
    }

    // Create snapshot if needed
    if (this.shouldCreateSnapshot()) {
      await this.createSnapshot()
    }

    // Clear uncommitted events
    this.uncommittedEvents = []
    this.loadedVersion = this.version
  }

  private async validateEvents(events: DomainEvent[]): Promise<void> {
    for (const event of events) {
      // Validate event structure
      if (!event.id || !event.type || !event.timestamp) {
        throw new Error(`Invalid event structure: ${JSON.stringify(event)}`)
      }

      // Validate event data
      await this.validateEventData(event)

      // Check for business rule violations
      await this.validateBusinessRules(event)
    }
  }

  private shouldCreateSnapshot(): boolean {
    // Create snapshot every 100 events or if complex aggregate
    return this.version % 100 === 0 || this.uncommittedEvents.length > 50
  }

  private async createSnapshot(): Promise<void> {
    const snapshot: Snapshot = {
      aggregateId: this.id,
      aggregateType: this.constructor.name,
      version: this.version,
      data: this.getSnapshotData(),
      timestamp: Date.now(),
    }

    await this.snapshotStore.saveSnapshot(snapshot)
  }

  protected abstract getSnapshotData(): any
  protected abstract applySnapshot(snapshot: Snapshot): void
  protected abstract validateEventData(event: DomainEvent): Promise<void>
  protected abstract validateBusinessRules(event: DomainEvent): Promise<void>
}

// User Aggregate Implementation
export class UserAggregate extends EventSourcingAggregate {
  private email: string
  private name: string
  private status: UserStatus
  private createdAt: Date
  private updatedAt: Date

  static async create(
    userData: CreateUserCommand,
    eventStore: EventStore,
    snapshotStore: SnapshotStore
  ): Promise<UserAggregate> {
    const user = new UserAggregate(eventStore, snapshotStore)
    user.id = generateId()

    const event: UserCreatedEvent = {
      id: generateEventId(),
      aggregateId: user.id,
      aggregateType: 'User',
      type: 'UserCreated',
      data: {
        email: userData.email,
        name: userData.name,
        status: 'active',
      },
      metadata: {
        userId: userData.requestedBy,
        correlationId: userData.correlationId,
        causationId: userData.causationId,
      },
      timestamp: Date.now(),
      version: 1,
    }

    await user.apply(event)
    await user.save()

    return user
  }

  async updateName(newName: string, metadata: EventMetadata): Promise<void> {
    if (this.status !== 'active') {
      throw new Error('Cannot update name of inactive user')
    }

    if (newName === this.name) {
      return // No change needed
    }

    const event: UserUpdatedEvent = {
      id: generateEventId(),
      aggregateId: this.id,
      aggregateType: 'User',
      type: 'UserUpdated',
      data: {
        name: newName,
        previousName: this.name,
      },
      metadata,
      timestamp: Date.now(),
      version: this.version + 1,
    }

    await this.apply(event)
  }

  async delete(metadata: EventMetadata): Promise<void> {
    if (this.status === 'deleted') {
      throw new Error('User already deleted')
    }

    const event: UserDeletedEvent = {
      id: generateEventId(),
      aggregateId: this.id,
      aggregateType: 'User',
      type: 'UserDeleted',
      data: {
        deletedAt: Date.now(),
        reason: metadata.reason || 'User requested deletion',
      },
      metadata,
      timestamp: Date.now(),
      version: this.version + 1,
    }

    await this.apply(event)
  }

  protected whenUserCreated(event: UserCreatedEvent): void {
    this.email = event.data.email
    this.name = event.data.name
    this.status = event.data.status
    this.createdAt = new Date(event.timestamp)
    this.updatedAt = new Date(event.timestamp)
  }

  protected whenUserUpdated(event: UserUpdatedEvent): void {
    this.name = event.data.name
    this.updatedAt = new Date(event.timestamp)
  }

  protected whenUserDeleted(event: UserDeletedEvent): void {
    this.status = 'deleted'
    this.updatedAt = new Date(event.timestamp)
  }

  protected getSnapshotData(): any {
    return {
      email: this.email,
      name: this.name,
      status: this.status,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
    }
  }

  protected applySnapshot(snapshot: Snapshot): void {
    const data = snapshot.data
    this.email = data.email
    this.name = data.name
    this.status = data.status
    this.createdAt = new Date(data.createdAt)
    this.updatedAt = new Date(data.updatedAt)
  }

  protected async validateEventData(event: DomainEvent): Promise<void> {
    switch (event.type) {
      case 'UserCreated':
        await this.validateUserCreatedEvent(event as UserCreatedEvent)
        break
      case 'UserUpdated':
        await this.validateUserUpdatedEvent(event as UserUpdatedEvent)
        break
      case 'UserDeleted':
        await this.validateUserDeletedEvent(event as UserDeletedEvent)
        break
    }
  }

  private async validateUserCreatedEvent(event: UserCreatedEvent): Promise<void> {
    const data = event.data

    if (!data.email || !isValidEmail(data.email)) {
      throw new Error('Invalid email address')
    }

    if (!data.name || data.name.trim().length === 0) {
      throw new Error('Name cannot be empty')
    }

    if (data.name.length > 100) {
      throw new Error('Name too long')
    }

    // Check for duplicate email
    const existingUser = await this.checkDuplicateEmail(data.email)
    if (existingUser) {
      throw new Error('Email already exists')
    }
  }

  private async validateUserUpdatedEvent(event: UserUpdatedEvent): Promise<void> {
    const data = event.data

    if (!data.name || data.name.trim().length === 0) {
      throw new Error('Name cannot be empty')
    }

    if (data.name.length > 100) {
      throw new Error('Name too long')
    }
  }

  protected async validateBusinessRules(event: DomainEvent): Promise<void> {
    // Additional business rule validations
    if (event.type === 'UserCreated') {
      // Check if user creation is allowed
      const isAllowed = await this.isUserCreationAllowed()
      if (!isAllowed) {
        throw new Error('User creation not allowed at this time')
      }
    }
  }

  private async checkDuplicateEmail(email: string): Promise<boolean> {
    // Implement duplicate email check
    return false // Placeholder
  }

  private async isUserCreationAllowed(): Promise<boolean> {
    // Implement business rule for user creation
    return true // Placeholder
  }

  // Getters for read model
  getEmail(): string {
    return this.email
  }
  getName(): string {
    return this.name
  }
  getStatus(): UserStatus {
    return this.status
  }
  getCreatedAt(): Date {
    return this.createdAt
  }
  getUpdatedAt(): Date {
    return this.updatedAt
  }
}

// Event Store Implementation
export class EventStore {
  constructor(
    private database: Database,
    private serializer: EventSerializer
  ) {}

  async saveEvents(
    aggregateId: string,
    events: DomainEvent[],
    expectedVersion: number
  ): Promise<void> {
    const transaction = await this.database.beginTransaction()

    try {
      let currentVersion = expectedVersion

      for (const event of events) {
        // Serialize event
        const serializedEvent = await this.serializer.serialize(event)

        // Save event
        await this.database.query(
          `
          INSERT INTO events (id, aggregate_id, aggregate_type, type, data, metadata, timestamp, version)
          VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        `,
          [
            event.id,
            aggregateId,
            event.aggregateType,
            event.type,
            serializedEvent.data,
            serializedEvent.metadata,
            new Date(event.timestamp),
            ++currentVersion,
          ]
        )

        event.version = currentVersion
      }

      await transaction.commit()
    } catch (error) {
      await transaction.rollback()
      throw error
    }
  }

  async getEvents(aggregateId: string, fromVersion?: number): Promise<DomainEvent[]> {
    const query = fromVersion
      ? `
        SELECT * FROM events 
        WHERE aggregate_id = $1 AND version >= $2 
        ORDER BY version ASC
      `
      : `
        SELECT * FROM events 
        WHERE aggregate_id = $1 
        ORDER BY version ASC
      `

    const params = fromVersion ? [aggregateId, fromVersion] : [aggregateId]
    const rows = await this.database.query(query, params)

    const events = []
    for (const row of rows) {
      const event = await this.serializer.deserialize({
        id: row.id,
        aggregateId: row.aggregate_id,
        aggregateType: row.aggregate_type,
        type: row.type,
        data: row.data,
        metadata: row.metadata,
        timestamp: row.timestamp.getTime(),
        version: row.version,
      })

      events.push(event)
    }

    return events
  }

  async getEventsByType(eventType: string, fromTimestamp?: number): Promise<DomainEvent[]> {
    const query = fromTimestamp
      ? `
        SELECT * FROM events 
        WHERE type = $1 AND timestamp >= $2 
        ORDER BY timestamp ASC
      `
      : `
        SELECT * FROM events 
        WHERE type = $1 
        ORDER BY timestamp ASC
      `

    const params = fromTimestamp ? [eventType, new Date(fromTimestamp)] : [eventType]
    const rows = await this.database.query(query, params)

    const events = []
    for (const row of rows) {
      const event = await this.serializer.deserialize({
        id: row.id,
        aggregateId: row.aggregate_id,
        aggregateType: row.aggregate_type,
        type: row.type,
        data: row.data,
        metadata: row.metadata,
        timestamp: row.timestamp.getTime(),
        version: row.version,
      })

      events.push(event)
    }

    return events
  }

  async deleteEvents(aggregateId: string, reason: string, deletedBy: string): Promise<void> {
    // GDPR compliance - soft delete with audit trail
    await this.database.query(
      `
      UPDATE events 
      SET deleted_at = NOW(), deletion_reason = $1, deleted_by = $2
      WHERE aggregate_id = $3
    `,
      [reason, deletedBy, aggregateId]
    )
  }
}

// Event Serializer
export class EventSerializer {
  private eventVersions = new Map<string, number>()

  async serialize(event: DomainEvent): Promise<SerializedEvent> {
    const eventVersion = this.eventVersions.get(event.type) || 1

    return {
      data: JSON.stringify(event.data),
      metadata: JSON.stringify(event.metadata),
      version: eventVersion,
    }
  }

  async deserialize(eventData: any): Promise<DomainEvent> {
    const data = JSON.parse(eventData.data)
    const metadata = JSON.parse(eventData.metadata)

    // Handle version migration
    const migratedData = await this.migrateEventData(eventData.type, data, eventData.version || 1)

    return {
      id: eventData.id,
      aggregateId: eventData.aggregateId,
      aggregateType: eventData.aggregateType,
      type: eventData.type,
      data: migratedData,
      metadata,
      timestamp: eventData.timestamp,
      version: eventData.version,
    }
  }

  private async migrateEventData(eventType: string, data: any, version: number): Promise<any> {
    // Implement event version migration logic
    switch (eventType) {
      case 'UserCreated':
        return this.migrateUserCreatedEvent(data, version)
      default:
        return data
    }
  }

  private migrateUserCreatedEvent(data: any, version: number): any {
    if (version === 1) {
      // Migrate from version 1 to 2
      return {
        ...data,
        status: data.status || 'active', // Add default status
      }
    }
    return data
  }
}

// Projection Manager
export class ProjectionManager {
  constructor(
    private eventStore: EventStore,
    private projections: Map<string, Projection>
  ) {}

  async rebuildProjection(projectionName: string): Promise<void> {
    const projection = this.projections.get(projectionName)
    if (!projection) {
      throw new Error(`Projection not found: ${projectionName}`)
    }

    // Clear existing projection data
    await projection.clear()

    // Get all relevant events
    const eventTypes = projection.getEventTypes()
    const allEvents = []

    for (const eventType of eventTypes) {
      const events = await this.eventStore.getEventsByType(eventType)
      allEvents.push(...events)
    }

    // Sort events by timestamp
    allEvents.sort((a, b) => a.timestamp - b.timestamp)

    // Apply events to projection
    for (const event of allEvents) {
      await projection.handleEvent(event)
    }

    // Finalize projection
    await projection.finalize()
  }

  async updateProjection(projectionName: string, event: DomainEvent): Promise<void> {
    const projection = this.projections.get(projectionName)
    if (!projection) {
      return
    }

    if (projection.getEventTypes().includes(event.type)) {
      await projection.handleEvent(event)
    }
  }
}

// User Read Model Projection
export class UserReadModelProjection implements Projection {
  constructor(private database: Database) {}

  getEventTypes(): string[] {
    return ['UserCreated', 'UserUpdated', 'UserDeleted']
  }

  async handleEvent(event: DomainEvent): Promise<void> {
    switch (event.type) {
      case 'UserCreated':
        await this.handleUserCreated(event as UserCreatedEvent)
        break
      case 'UserUpdated':
        await this.handleUserUpdated(event as UserUpdatedEvent)
        break
      case 'UserDeleted':
        await this.handleUserDeleted(event as UserDeletedEvent)
        break
    }
  }

  private async handleUserCreated(event: UserCreatedEvent): Promise<void> {
    await this.database.query(
      `
      INSERT INTO user_read_model (id, email, name, status, created_at, updated_at)
      VALUES ($1, $2, $3, $4, $5, $6)
    `,
      [
        event.aggregateId,
        event.data.email,
        event.data.name,
        event.data.status,
        new Date(event.timestamp),
        new Date(event.timestamp),
      ]
    )
  }

  private async handleUserUpdated(event: UserUpdatedEvent): Promise<void> {
    await this.database.query(
      `
      UPDATE user_read_model 
      SET name = $1, updated_at = $2 
      WHERE id = $3
    `,
      [event.data.name, new Date(event.timestamp), event.aggregateId]
    )
  }

  private async handleUserDeleted(event: UserDeletedEvent): Promise<void> {
    await this.database.query(
      `
      UPDATE user_read_model 
      SET status = 'deleted', updated_at = $1 
      WHERE id = $2
    `,
      [new Date(event.timestamp), event.aggregateId]
    )
  }

  async clear(): Promise<void> {
    await this.database.query('DELETE FROM user_read_model')
  }

  async finalize(): Promise<void> {
    await this.database.query('ANALYZE user_read_model')
  }
}
```

</example_good>

<example_bad>

```typescript
// BAD: No event sourcing implementation
export class BasicUser {
  // BAD: Direct database mutations
  async updateUser(userId: string, data: any) {
    // BAD: No event log
    // BAD: No audit trail
    // BAD: No versioning
    await db.user.update({ where: { id: userId }, data })
  }

  // BAD: No event sourcing
  // BAD: No snapshots
  // BAD: No event replay
  // BAD: No CQRS separation
}
```

</example_bad>
