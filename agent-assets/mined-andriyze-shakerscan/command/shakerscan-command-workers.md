# Worker Management

View and scale scanner workers.

**Usage**: `/workers [count]`

## Instructions

Call the API with `shakerscan api METHOD PATH [JSON]` (it knows the instance address and credential; `SHAKERSCAN_API_BASE` overrides the address). On a remote VPS, set it
to the API URL printed by `./scanner.sh status`.

1. Check if scanner is running:
   ```bash
   shakerscan api GET /health
   ```

2. If no count argument provided, show current worker status:
   ```bash
   # Get worker count via API
   shakerscan api GET /workers

   # Get queue stats
   shakerscan api GET /queue/stats
   ```

3. Report current status:
   ```
   Workers: X running
   Queue: Y pending, Z running
   ```

4. If count argument provided (e.g., `/workers 5`):
   - Parse the number from $ARGUMENTS
   - Validate it's between 1-20
   - Scale workers:
     ```bash
     shakerscan api POST /workers '{"count": N}'
     ```
   - If API scaling fails, suggest CLI:
     ```
     ./scanner.sh scale N
     ```

5. After scaling, verify new count:
   ```bash
   shakerscan api GET /workers
   ```

6. Report result:
   ```
   Scaled to N workers
   - Running: X
   - Pending jobs: Y
   ```
