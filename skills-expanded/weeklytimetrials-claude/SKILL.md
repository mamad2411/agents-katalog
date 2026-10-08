# Mario Kart World Time Trial Bot - Development Documentation

## Overview

This Discord bot manages weekly time trial challenges for Mario Kart World tracks. It was built using pure Python with raw SQL queries (PostgreSQL) for hands-on database learning and production-ready Discord bot development.

## Architecture Decisions

### Why Raw SQL Instead of ORM?

The original plan considered SQLAlchemy, but we chose raw SQL for several key reasons:

1. **Learning SQL for Job Requirements**: The developer needed hands-on SQL experience for a new job role requiring "proficiency with SQL"
2. **Direct Database Skills**: Raw SQL provides direct experience with queries, joins, indexing, and performance optimization
3. **Production Readiness**: Understanding SQL execution and query optimization is crucial for production systems
4. **Transparency**: No hidden query generation or ORM abstractions to debug

### Database Design Philosophy

- **Normalized Schema**: Proper foreign key relationships between trials and times
- **Performance Indexes**: Strategic indexing for common query patterns (leaderboards, user lookups)
- **Data Integrity**: CHECK constraints and proper data types
- **Audit Trail**: Created/updated timestamps for all records

### Time Handling Strategy

- **Storage**: Times stored as milliseconds (INTEGER) for precise comparison
- **Format**: User input/display in MM:SS.mmm format (e.g., "2:23.640")
- **Range**: 0:00.000 to 9:59.999 (realistic Mario Kart times)
- **Validation**: Comprehensive regex validation with clear error messages

### User Name Resolution

Instead of storing usernames in the database (which become stale), we:
- Store only Discord user IDs (permanent)
- Resolve display names dynamically using Discord API
- Handle edge cases (user left server, API errors)
- Cache results during leaderboard generation for performance

## SQL Learning Outcomes

This project provided hands-on experience with:

### DDL (Data Definition Language)
- CREATE TABLE with proper constraints
- ALTER TABLE for schema modifications
- DROP TABLE for cleanup
- INDEX creation for performance

### DML (Data Manipulation Language)
- Complex SELECT queries with joins
- INSERT with RETURNING clause
- UPDATE with conditional logic
- DELETE with CASCADE effects

### Advanced SQL Features
- ROW_NUMBER() for rankings
- CASE statements for medal calculations
- Subqueries for complex filtering
- UPSERT with ON CONFLICT
- Transaction management
- Date/time functions

### Performance Optimization
- Strategic indexing for common queries
- Composite indexes for multi-column searches
- Query execution planning
- Connection pooling

## Discord Bot Implementation

### Command Architecture

Used inheritance-based design with BaseCommand class providing:
- Common error handling
- Database connection management
- Input validation
- Response formatting
- Logging integration

### Challenge Categories System

The bot supports two types of time trials:
- **Shrooms**: Items/mushrooms are allowed during the trial
- **Shroomless**: No items/mushrooms allowed (pure racing skill)

**Key Implementation Details:**
- Category stored as VARCHAR(20) with CHECK constraint in `weekly_trials` table
- Each track can have one active trial per category (shrooms AND shroomless simultaneously)
- Unique constraint: `unique_active_trial_per_guild_track_category` ensures no duplicate active trials
- Users must specify category when creating challenges with `/set-challenge`
- Category can be updated after creation using `/update-category` command
- Leaderboards are separate for each category

### Live Leaderboard System

The bot automatically creates and updates leaderboard messages in Discord:
- **Automatic Creation**: When a challenge is created, a live leaderboard message is posted
- **Auto-Updates**: Leaderboard updates when users submit times (no need to run `/leaderboard` repeatedly)
- **Message Tracking**: Message ID and channel ID stored in `weekly_trials` table
  - `leaderboard_message_id`: Discord message ID of the live leaderboard
  - `leaderboard_channel_id`: Discord channel ID where leaderboard is posted
- **Smart Updates**: If message is deleted, bot creates a new one and updates the stored ID
- **Final Results**: When trial ends, leaderboard is updated to show final status

**How It Works:**
1. Admin creates challenge with `/set-challenge`
2. Bot posts initial leaderboard embed in designated channel
3. Bot stores message ID and channel ID in database
4. When users submit times, bot edits the existing message with updated rankings
5. If category is changed with `/update-category`, leaderboard is updated to reflect new category
6. When trial ends, leaderboard shows final results

### Autocomplete Strategy

Each command requiring track selection implements smart autocomplete:
- `/weeklytimesave`: Shows tracks with active trials (includes category, e.g., "Rainbow Road (Shrooms)")
- `/leaderboard`: Shows tracks with any trials, including category (historical data)
- `/remove-time`: Shows only tracks where user has submissions
- `/set-challenge`: Prioritizes tracks without active trials
- `/end-challenge`: Uses trial numbers (not track names)
- `/update-category`: Uses trial numbers (not track names)

### Error Handling Hierarchy

1. **Validation Errors**: User input problems (friendly messages)
2. **Command Errors**: Business logic failures (clear explanations)
3. **Database Errors**: Technical issues (generic user message, detailed logging)
4. **Unexpected Errors**: Catch-all with logging for debugging

## Database Schema Deep Dive

### weekly_trials Table

```sql
CREATE TABLE weekly_trials (
    id SERIAL PRIMARY KEY,
    trial_number INTEGER NOT NULL,           -- For "Weekly Time Trial #N"
    track_name VARCHAR(100) NOT NULL,        -- Mario Kart World track
    category VARCHAR(20) DEFAULT 'shrooms' NOT NULL,  -- 'shrooms' or 'shroomless'
    gold_time_ms INTEGER,                    -- Goal times in milliseconds (optional)
    silver_time_ms INTEGER,
    bronze_time_ms INTEGER,
    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_date TIMESTAMP,                      -- NULL = active forever
    status VARCHAR(20) DEFAULT 'active',     -- 'active', 'expired', 'ended'
    guild_id BIGINT NOT NULL,                -- Discord server ID
    leaderboard_channel_id BIGINT,           -- Channel where live leaderboard is posted
    leaderboard_message_id BIGINT,           -- Message ID of live leaderboard
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_category CHECK (category IN ('shrooms', 'shroomless'))
);

-- Unique constraint: only one active trial per track per category per guild
CREATE UNIQUE INDEX unique_active_trial_per_guild_track_category
ON weekly_trials(guild_id, track_name, category) WHERE status = 'active';
```

**Key Design Decisions:**
- `trial_number` for human-readable naming instead of using database ID
- `category` column with CHECK constraint enforces valid values ('shrooms' or 'shroomless')
- `status` enum for trial lifecycle management
- `end_date` nullable to support permanent trials if needed
- `leaderboard_message_id` and `leaderboard_channel_id` track live leaderboard messages for auto-updates
- Unique constraint allows one active trial per track per category (can have both shrooms and shroomless active simultaneously)
- Medal times are now optional (can be NULL for challenges without medal requirements)

### player_times Table

```sql
CREATE TABLE player_times (
    id SERIAL PRIMARY KEY,
    trial_id INTEGER NOT NULL REFERENCES weekly_trials(id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL,                 -- Discord user ID (permanent)
    time_ms INTEGER NOT NULL,                -- Time in milliseconds
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(trial_id, user_id)               -- One time per user per trial
);
```

**Key Design Decisions:**
- Foreign key with CASCADE DELETE for data integrity
- UNIQUE constraint prevents duplicate submissions
- No username storage (resolved dynamically)
- Millisecond precision for accurate time comparison

### Performance Indexes

```sql
-- Leaderboard queries (most frequent)
CREATE INDEX idx_player_times_trial_time ON player_times(trial_id, time_ms);

-- User-specific queries
CREATE INDEX idx_player_times_user_id ON player_times(user_id);

-- Active trial lookups
CREATE INDEX idx_weekly_trials_status_guild ON weekly_trials(status, guild_id);

-- Composite index for admin queries
CREATE INDEX idx_weekly_trials_guild_status_track ON weekly_trials(guild_id, status, track_name);
```

## Deployment Strategy

### Railway Configuration

Chose Railway for deployment because:
- Built-in PostgreSQL provisioning
- Git-based automatic deployments
- Environment variable management
- Persistent storage for database
- Simple scaling options

### Environment Variables

```bash
BOT_TOKEN=your_discord_bot_token
DATABASE_URL=postgresql://user:pass@host:port/dbname
DEBUG=false
```

### Health Monitoring

- Automatic trial expiration via background tasks
- Database connection health checks
- Graceful shutdown handling
- Comprehensive logging for debugging

## Bot Commands Reference

### User Commands - Weekly Time Trials

**`/weeklytimesave`**
- Submit your time for an active weekly trial
- Parameters: `track` (with category), `time` (MM:SS.mmm format)
- Only accepts improvements (faster times than your current best)
- Real-time medal calculation
- Automatically updates live leaderboard

**`/leaderboard`**
- View leaderboard for any trial (active or historical)
- Parameters: `track` (with category)
- Shows rankings, times, and medals for all participants

**`/active`**
- View all currently active time trials
- No parameters
- Shows trial numbers, track names, categories, and expiration times

**`/remove-time`**
- Remove your submitted time from a trial
- Parameters: `track` (with category)
- Can only remove your own times

### User Commands - 1v1 Duels

**`/create-duel`**
- Challenge another user to a 1v1 time trial duel
- Parameters: `opponent`, `track`, `category`, `duration_days`

**`/accept-duel`**
- Accept a pending duel challenge
- Parameters: `duel_id`

**`/decline-duel`**
- Decline a pending duel challenge
- Parameters: `duel_id`

**`/dueltimesave`**
- Submit your time for an active duel
- Parameters: `duel_id`, `time`

**`/duel-results`**
- View results of a completed duel
- Parameters: `duel_id`

**`/cancel-duel`**
- Cancel a duel you created (before opponent accepts)
- Parameters: `duel_id`

**`/end-duel`**
- Manually end an active duel
- Parameters: `duel_id`

### Admin Commands

**`/set-challenge`**
- Create a new weekly time trial challenge
- Parameters: `track`, `duration_days`, `category` (shrooms/shroomless), optional medal times
- Creates live leaderboard message automatically
- Only one active trial per track per category allowed

**`/end-challenge`**
- Manually end an active trial before expiration
- Parameters: `trial_number`
- Updates live leaderboard to show final results
- Trial becomes read-only

**`/update-category`** ⭐ NEW
- Change the category (shrooms/shroomless) of an existing trial
- Parameters: `trial_number`, `category`
- Automatically updates the live leaderboard with new category
- Prevents conflicts (can't change to a category that already has an active trial for that track)
- All existing times remain intact

**`/set-medal-times`**
- Update or add medal times to an existing trial
- Parameters: `trial_number`, `gold_time`, `silver_time`, `bronze_time`
- Updates live leaderboard with new medal thresholds

**`/remove-medal-times`**
- Remove medal requirements from a trial
- Parameters: `trial_number`

**`/set-leaderboard-channel`**
- Set default channel for live leaderboard messages
- Parameters: `channel`
- All future trials will post leaderboards in this channel

## Time Trial Business Logic

### Trial Lifecycle

1. **Creation**: Admin creates trial with `/set-challenge`
   - Validates track doesn't already have active trial for chosen category
   - Sets category (shrooms or shroomless)
   - Sets optional medal times and duration
   - Creates live leaderboard message in designated channel

2. **Active Phase**: Users submit times with `/weeklytimesave`
   - Only accepts improvements (faster times)
   - Real-time medal calculation
   - Prevents duplicate submissions
   - Live leaderboard auto-updates after each submission

3. **Management**: Admins can update trial settings
   - `/update-category`: Change between shrooms/shroomless
   - `/set-medal-times`: Update or add medal thresholds
   - `/remove-medal-times`: Remove medal requirements
   - Live leaderboard updates automatically after changes

4. **Expiration**: Automatic or manual ending
   - Background task marks expired trials
   - Manual ending via `/end-challenge`
   - Trials become read-only
   - Live leaderboard shows final results

5. **Cleanup**: Automated removal after grace period
   - 3-day grace period for viewing results
   - Automatic deletion to prevent database bloat

### Medal System

Medal thresholds are set per trial:
- 🥇 Gold: time_ms ≤ gold_time_ms
- 🥈 Silver: time_ms ≤ silver_time_ms
- 🥉 Bronze: time_ms ≤ bronze_time_ms

Calculated dynamically in SQL queries for real-time accuracy.

## Development Patterns

### DRY Principles

- BaseCommand class eliminates code duplication
- Shared utilities for common operations
- Consistent error handling across all commands
- Reusable database query patterns

### Type Safety

- Comprehensive type hints throughout codebase
- Input validation with clear error messages
- Database schema constraints prevent invalid data
- Discord.py typing for interaction handling

### Logging Strategy

- Structured logging with different levels
- Command execution tracking
- Database operation monitoring
- Error reporting with stack traces
- Production-ready log formatting

## Testing Considerations

### Manual Testing Checklist

1. **Command Validation**
   - All slash commands register properly
   - Autocomplete works for each parameter
   - Error messages are user-friendly

2. **Database Operations**
   - Trial creation with various parameters
   - Time submissions (new, improvements, duplicates)
   - Leaderboard generation with multiple users
   - Trial expiration and cleanup

3. **Edge Cases**
   - Invalid time formats
   - Non-existent tracks
   - Users leaving server (name resolution)
   - Database connection failures

4. **Performance**
   - Large leaderboards (100+ participants)
   - Concurrent command execution
   - Background task execution

### Production Monitoring

- Railway deployment health
- Database connection pooling effectiveness
- Command execution time tracking
- Error rate monitoring

## Future Enhancements

### Potential Features

1. **Advanced Statistics**
   - Personal best tracking across all trials
   - Average improvement over time
   - Guild-wide statistics

2. **Competition Features**
   - Seasonal championships
   - Team-based challenges
   - Cross-server leaderboards

3. **Integration Options**
   - Web dashboard for viewing results
   - API endpoints for external tools
   - Export functionality for data analysis

### Performance Optimizations

1. **Database**
   - Materialized views for complex queries
   - Partitioning for historical data
   - Read replicas for scaling

2. **Application**
   - Redis caching for leaderboards
   - Background queue for heavy operations
   - Connection pooling tuning

## Lessons Learned

### SQL Mastery

- Raw SQL provided deep understanding of query optimization
- Index design is crucial for performance at scale
- Transaction management prevents data inconsistencies
- Proper constraints catch bugs early

### Discord Bot Development

- Slash commands provide better UX than prefix commands
- Autocomplete significantly improves usability
- Error handling must be comprehensive and user-friendly
- Background tasks need careful lifecycle management

### Production Deployment

- Environment configuration is critical
- Logging is essential for debugging production issues
- Graceful shutdown prevents data corruption
- Health checks enable automatic recovery

This project successfully combines SQL learning with production Discord bot development, providing practical experience with both database management and real-time application development.