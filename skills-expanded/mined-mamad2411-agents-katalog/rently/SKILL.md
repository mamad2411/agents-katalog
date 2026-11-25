---
name: rently
description: "Rently CLI — manage car rental bookings, customers, fleet, operations, and more via the rently command-line tool. Use when the user asks about bookings, customers, cars, deliveries, returns, payments, or any Rently car rental operations."
allowed-tools: Bash(rently *)
argument-hint: "[what you want to do]"
---

You have access to the `rently` CLI tool for managing a car rental SaaS platform.

Always start by running `rently auth status` to verify authentication before executing commands.

## Key Concepts
- **Booking statuses:** Reserved -> Confirmed -> Delivered -> Closed | Canceled | Quoted
- **Places:** pickup/dropoff locations (use `rently info places` to get IDs)
- **Branch offices:** physical offices managing fleet and operations
- **Categories:** vehicle groupings (economy, SUV, etc.) containing models
- **Additionals:** extra services (GPS, child seat, insurance, etc.)
- **Operations:** delivery = handing car to customer; return = customer returns car

## Two Ways to Pass Data

Commands that write data accept **both** individual options and `--json-body`:

```bash
# Option 1: Individual parameters (simpler for flat data)
rently bookings cancel --booking-id 2300 --lastname Doe

# Option 2: Raw JSON (required for nested objects like Customer, arrays, etc.)
rently bookings cancel --json-body '{"BookingId":2300,"Lastname":"Doe"}'
```

## Output Format
- Default: compact JSON
- `--pretty`: indented JSON
- `--table`: ASCII table output — **use this when listing results so the user can read them**
- `--columns "Col1,Col2,Nested.Field"`: choose which columns in table mode

## Common Workflows

### Search and book a car
```bash
rently info places
rently search availability --from "2026-04-01T10:00:00" --to "2026-04-05T10:00:00" --from-place 1
rently search price --from "2026-04-01T10:00:00" --to "2026-04-05T10:00:00" --from-place 1 --model-id 5
rently bookings create --json-body '{"Customer":{"Id":123},"Category":{"Id":1},"FromDate":"2026-04-01T10:00:00","ToDate":"2026-04-05T10:00:00","DeliveryPlace":{"Id":9},"ReturnPlace":{"Id":9},"Currency":"USD","IlimitedKm":true}'
rently bookings reserve --booking-id 456 --lastname Doe
```

### Process delivery / return
```bash
rently operations deliver --booking-id 2300 --kilometers 15000 --gasoline 8 --make-delivery --run-validations
rently operations return --booking-id 2300 --kilometers 15500 --gasoline 6 --make-return --run-validations --date "2026-04-05T10:00:00"
```

### Check today's operations
```bash
rently operations list-deliveries --branch-office-id 1
rently operations list-returns --branch-office-id 1
```

## Tips
- Use `--table` when the user asks to see or list results, with `--columns` to keep it readable
- Use JSON output (default) when you need to process data programmatically
- Use `--json-body` for nested objects or arrays
- Date format: ISO 8601 `"2026-04-01T10:00:00"`
- Use `rently info places` and `rently info categories` to discover valid IDs before creating bookings
- Pagination: most list commands support `--offset` and `--limit`
- Run `rently <command> <subcommand> --help` to see all options for any command

The user's request: $ARGUMENTS
