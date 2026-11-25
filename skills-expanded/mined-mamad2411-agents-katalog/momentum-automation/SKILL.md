---
name: momentum-automation
description: Use this skill to control the Momentum laboratory automation system for high-throughput experiments. This includes scheduling protocols and monitoring instrument status.
---

# Momentum Automation

## Overview
This skill interfaces with the Thermo Scientific Momentum scheduling software for automating laboratory workflows.

## Capabilities
- **Schedule Momentum Protocol**: Submit and run protocols.
- **Monitor Momentum Status**: Check the status of instruments and running jobs.

## Usage
- "Schedule the 'PCR_Setup' protocol to run at 2 PM."
- "What is the status of the Echo liquid handler?"

## Example: Scheduling
```python
# Pseudo-code for scheduling
def schedule_protocol(protocol_name, start_time):
    # Connect to Momentum API
    # Submit job
    return job_id
```
