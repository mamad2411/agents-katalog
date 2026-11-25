---
name: d1-06-crud-endpoints
description: "Adds the five CRUD REST endpoints (all, detail/{id}, save, update, delete) for an entity to up-api and redeploys. Use when the user asks for Day 1 step 7 of the CRUD drill, or asks to add CRUD API endpoints to up-api. Needs the same entity that was used in the entity-migration step."
compatibility: "Requires the .NET 10 SDK, and up-api with the target entity + DbContext already set up (from the entity-migration step)."
---

# Day 1 · Step 6 — CRUD endpoints, then redeploy

**Before starting:** Ask which entity to create endpoints for (must match one already migrated in D1_05).
Do not assume or proceed without confirmation.

`up-api/Controllers/<Entity>sController.cs`:
```csharp
[ApiController]
[Route("api/[controller]")]
public class <Entity>sController : ControllerBase
{
    private readonly AppDbContext _db;
    public <Entity>sController(AppDbContext db) => _db = db;

    [HttpGet]
    public async Task<IActionResult> All() => Ok(await _db.<Entity>s.ToListAsync());

    [HttpGet("detail/{id}")]
    public async Task<IActionResult> Detail(int id)
    {
        var item = await _db.<Entity>s.FindAsync(id);
        return item is null ? NotFound() : Ok(item);
    }

    [HttpPost("save")]
    public async Task<IActionResult> Save(<Entity> input)
    {
        _db.<Entity>s.Add(input);
        await _db.SaveChangesAsync();
        return Ok(input);
    }

    [HttpPut("update/{id}")]
    public async Task<IActionResult> Update(int id, <Entity> input)
    {
        var item = await _db.<Entity>s.FindAsync(id);
        if (item is null) return NotFound();
        // copy updated fields from input onto item
        await _db.SaveChangesAsync();
        return Ok(item);
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        var item = await _db.<Entity>s.FindAsync(id);
        if (item is null) return NotFound();
        _db.<Entity>s.Remove(item);
        await _db.SaveChangesAsync();
        return NoContent();
    }
}
```