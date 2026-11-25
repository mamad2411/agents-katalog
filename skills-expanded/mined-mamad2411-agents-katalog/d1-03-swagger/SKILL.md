---
name: d1-03-swagger
description: "Adds Swagger/OpenAPI UI to the up-api .NET project and redeploys it. Use when the user asks for Day 1 step 4 of the CRUD drill, or asks to add API docs / Swagger to up-api."
compatibility: "Requires the .NET 10 SDK, and an existing up-api project (from earlier drill steps)."
---

# Day 1 · Step 3 — Swagger

Check `up-api/Program.cs` first — recent `dotnet new webapi` templates already scaffold OpenAPI
(`AddOpenApi()` / `MapOpenApi()`). If Swagger UI specifically is wanted (not just the raw OpenAPI JSON),
add Swashbuckle:

```Run bash
cd up-api
dotnet add package Swashbuckle.AspNetCore
```

In `Program.cs`:
```csharp
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
// ...
app.UseSwagger();
app.UseSwaggerUI();
```