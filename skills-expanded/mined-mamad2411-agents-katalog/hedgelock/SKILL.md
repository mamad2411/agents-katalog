# Cursor Rules for HedgeLock

## Project Context
HedgeLock is an event-driven trading risk management system using Python FastAPI microservices with Apache Kafka.

## Mandatory Rules
1. Files must not exceed 500 lines (refactor if >600 lines)
2. Use type hints for all Python functions
3. Follow async/await patterns for I/O operations
4. Test Kafka integration before implementing business logic
5. Include trace_id in all logging statements

## Commit Format
`type(sprint-id): description`
- feat(HL-07-1): new feature
- fix(HL-07-2): bug fix
- test(HL-07-3): test addition

## Before Committing
```bash
make test      # Must pass
make lint      # Must pass
make test-cov  # Must be >60%
```

## Project Structure
```
src/hedgelock/
├── collector/     # Bybit data ingestion
├── risk_engine/   # LTV calculation
├── hedger/        # Hedge order generation
├── treasury/      # P&L tracking (TODO)
└── trade_executor/# Order execution (TODO)
```

## Key Commands
- `make compose-up` - Start all services
- `make logs-{service}` - View service logs
- `make kafka-topics` - List Kafka topics

## Current TODOs
1. Implement Trade Executor service
2. Add API authentication
3. Setup Prometheus monitoring
4. Implement Treasury module