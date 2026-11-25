---
name: context-engine-api
description: Autonomously update the persistent memory via the Context Engine backend. Use this skill whenever you learn something important about the user, their preferences, the architecture of a codebase, or a hard-won lesson, and you want to ensure it is permanently stored in memory.json for future AI sessions.
---

# Context Engine API Skill

Communicate with the running Context Engine instance to persist contextual data.

## API Endpoints
- `POST http://127.0.0.1:3847/api/memory`
- `GET http://127.0.0.1:3847/api/memory`

---

## Action: Save a Memory

To save a memory, you must first read the current memory array, append to it, and then POST it back.
Use this exact PowerShell script. Replace `YOUR_NEW_FACT_HERE` with a concise, factual string.

```powershell
$newFact = "YOUR_NEW_FACT_HERE"

try {
    # 1. Fetch current memory
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:3847/api/memory" -Method Get
    $memoryData = $response
    
    # 2. Append new fact
    $memoryData.entries += @{
        id = [guid]::NewGuid().ToString()
        text = $newFact
        ts = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ssZ")
    }
    
    # 3. Post updated memory back
    $jsonPayload = $memoryData | ConvertTo-Json -Depth 5
    Invoke-RestMethod -Uri "http://127.0.0.1:3847/api/memory" -Method Post -Body $jsonPayload -ContentType "application/json"
    
    Write-Output "[OK] Successfully committed memory: $newFact"
} catch {
    Write-Output "[FAIL] Failed to update memory. Is Context Engine running on port 3847?"
    Write-Output $_.Exception.Message
}
```

## When to use this:
- You fix a major bug and want to document the architectural quirk so future sessions don't repeat the mistake.
- You learn a new user preference.
- DO NOT save temporary/ephemeral task states (e.g., "I finished step 2 of the refactoring"). Only save persistent, globally relevant facts.
