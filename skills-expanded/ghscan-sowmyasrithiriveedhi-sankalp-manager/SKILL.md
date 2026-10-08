# Rental Skill

Purpose:
Handle construction material rental workflows.

Responsibilities:
- Validate stock availability
- Allocate rentals
- Reduce available stock
- Prevent over-allocation
- Process return workflows
- Calculate rental amount

Rules:
- Do not allow rentals exceeding available stock
- Automatically update stock after rental
- Mark returned rentals properly
- Calculate rent using:
  Quantity × Price Per Day × Number of Days

Workflow:
1. Receive rental request
2. Validate stock
3. Create rental entry
4. Update inventory
5. Generate rental summary