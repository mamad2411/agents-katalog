---
name: revit-test
description: "Unit/integration test cho Revit Add-In. Decision tree giữa TUnit (Nice3point revit-test template, in-process), xUnitRevit/RevitTest (ricaun-io, VS Adapter), và xUnit thường (pure logic). Setup test runner trong Rider + Visual Studio. TRIGGER when: task chứa 'unit test', 'integration test', 'test revit', 'tunit', 'xunit', 'revit test framework', hoặc cần viết/fix test cho add-in. Khi setup test project, viết test cho code chạm Revit API, hoặc chọn framework test. Keywords: test, unit-test, tunit, xunit, ricaun, dynamods, revittest, integration, in-process."
user-invocable: true
when_to_use: "Khi setup test project, viết test cho code chạm Revit API, hoặc chọn framework test."
category: revit
keywords: [test, unit-test, tunit, xunit, ricaun, dynamods, revittest, integration, in-process]
metadata:
  author: hoang
  version: "1.0.0"
references:
  - https://chuongmep.com/posts/2024-06-01-run-revit-unit-test.html
  - https://github.com/ricaun-io/RevitTest
  - https://github.com/Nice3point/RevitTemplates
---

<!-- portable-host-contract:start -->
## Portable host contract

This skill is shared by Codex and Google Antigravity.

- Use the host's native task tracker. In Codex, use `update_plan`; in Antigravity, maintain the task-list artifact.
- Use native collaboration and user-input tools exposed by the host. Treat legacy tool names as capability descriptions, never literal calls.
- Resolve bundled resources from the project-local `.agents/skills/` tree. Do not create or write a user-global skill directory.
<!-- portable-host-contract:end -->

# Revit Testing — Framework Decision + Setup

## Decision Tree

```
Test này cần truy cập Revit API (Document, Element, Transaction)?
├── KHÔNG (pure logic — math, parser, geometry calc, DTO mapping)
│   → xUnit thường (test runner ngoài Revit)
│   → Fast feedback, chạy CI/CD dễ
│
└── CÓ (cần Revit context)
    ├── Project Nice3point sẵn template revit-test?
    │   → TUnit (mặc định, in-process)
    │
    └── Team quen xUnit + muốn VS Test Adapter UI?
        → xUnitRevit / ricaun-io RevitTest
```

## Framework Matrix

| Framework | Runner | Truy cập Revit API | VS Adapter | Khi nào dùng |
|---|---|---|---|---|
| **xUnit thường** | dotnet test (out-of-process) | ❌ | ✅ | Test pure logic, không cần Revit |
| **TUnit (Nice3point)** | Trong Revit process | ✅ | Yêu cầu cài "VS Code Adapter" trong Rider | In-process, modern, default cho Nice3point |
| **xUnitRevit (Speckle)** | Trong Revit process | ✅ | ✅ (VS Test Adapter) | Đã quen xUnit syntax |
| **RevitTest (ricaun-io)** | Trong Revit process | ✅ | ✅ (NUnit adapter) | Mature, có release pipeline |
| **DynamoDS RevitTestFramework** | Trong Revit process | ✅ | NUnit GUI | Legacy projects, Dynamo ecosystem |
| **NeVeSpl RevitTestLibrary** | Trong Revit process | ✅ | Manual | Specialized scenarios |

## Setup 1: TUnit (Nice3point default)

```bash
# Trong solution folder
mkdir MyAddIn.Tests && cd MyAddIn.Tests
dotnet new revit-test --name MyAddIn.Tests
```

Sample test:

```csharp
using TUnit.Core;
using Autodesk.Revit.DB;

namespace MyAddIn.Tests;

public class WallServiceTests
{
    protected override string FileName => @"<host-path>";

    [Test]
    public async Task GetAllWalls_ReturnsAllWallsInDocument()
    {
        // Arrange — Document được TUnit inject sẵn (Revit context)
        var doc = Context.Document;
        var service = new WallService();

        // Act
        var walls = service.GetAll(doc);

        // Assert
        await Assert.That(walls).IsNotEmpty();
        await Assert.That(walls.Count).IsGreaterThan(0);
    }
}
```

Build + run trong Revit process (Nice3point SDK tự handle).

## Setup 2: Rider config (theo blog chuongmep.com)

Khi dùng Rider và gặp tests không discover:

1. **Settings → Build, Execution, Deployment → Unit Testing**:
   - Enable "VS Code Adapter Support"
2. **Settings → Build → MSBuild project build**:
   - Switch build engine sang "Visual Studio" nếu .NET SDK gặp issue
3. **Tab NUnit (nếu dùng RevitTest/xUnitRevit)**:
   - Đổi setting "Metadata" → "TestRunner"
4. Refresh Unit Test Tree (Ctrl+Shift+F10).

## Setup 3: Visual Studio + ricaun-io RevitTest

```bash
# Cài NUnit Test Adapter extension trong VS
# Reference NuGet
dotnet add package Nice3point.Revit.Api.RevitAPI
dotnet add package ricaun.RevitTest.TestAdapter
dotnet add package NUnit
```

Sample test:

```csharp
using NUnit.Framework;
using Autodesk.Revit.DB;
using ricaun.RevitTest.TestAdapter;

[TestFixture]
public class WallReportTests : RevitTestFixture
{
    protected override string FileName => @"<host-path>";

    [Test]
    public void Document_HasAtLeastOneWall()
    {
        var walls = new FilteredElementCollector(Document)
            .OfClass(typeof(Wall))
            .ToElements();

        Assert.That(walls.Count, Is.GreaterThan(0));
    }
}
```

Run trong VS Test Explorer — RevitTest runner sẽ tự launch Revit headless.

## Setup 4: xUnit thường (pure logic)

```bash
dotnet new xunit -n MyAddIn.Logic.Tests
cd MyAddIn.Logic.Tests
dotnet add reference ../MyAddIn.Logic/MyAddIn.Logic.csproj
```

Sample:

```csharp
using Xunit;
using MyAddIn.Logic;

public class GeometryCalculatorTests
{
    [Theory]
    [InlineData(10, 5, 50)]
    [InlineData(0, 5, 0)]
    public void CalculateArea_ReturnsLengthTimesWidth(double l, double w, double expected)
    {
        var calc = new GeometryCalculator();
        Assert.Equal(expected, calc.CalculateArea(l, w));
    }
}
```

Run:
```bash
dotnet test
```

## Quy tắc tách logic ra khỏi Revit API

Để test được nhiều với xUnit thường → **tách layer**:

```
Models/                      ← POCO, no Revit dep → test xUnit
Services/
├── IWallService.cs          ← interface
├── WallService.cs           ← gọi Revit API → test TUnit/xUnitRevit
└── WallCalculator.cs        ← pure math, lấy Wall info đã extract → test xUnit
```

Pattern:

```csharp
// Service chạm Revit API (test in-process)
public class WallService : IWallService
{
    public IReadOnlyList<WallInfo> GetAll(Document doc)
    {
        return new FilteredElementCollector(doc)
            .OfClass(typeof(Wall))
            .Cast<Wall>()
            .Select(w => new WallInfo(w.Id.Value, w.Width, w.WallType.Name))  // Extract POCO
            .ToList();
    }
}

// Calculator pure logic (test xUnit out-of-process)
public class WallCalculator
{
    public double TotalArea(IEnumerable<WallInfo> walls) =>
        walls.Sum(w => w.Length * w.Height);
}
```

→ 70% logic test xUnit (fast, CI/CD), 30% Revit-dependent test in-process.

## References

- `references/test-setup-rider.md` — Chi tiết setup Rider (blog chuongmep.com)
- `references/test-setup-rider.md` — VS + RevitTest detail
- `references/projects-to-track.md` — Danh sách project tham khảo

## Quy tắc

| ✅ DO | ❌ DON'T |
|---|---|
| Tách pure logic ra khỏi Revit API → test xUnit | Test ViewModel/Service đan xen Revit API trong cùng class |
| In-process test có `FileName` trỏ tới `.rvt` test fixture | Test phụ thuộc project Revit production của user |
| CI/CD chỉ chạy xUnit (in-process cần Revit installed) | Bắt CI build Revit licensed (đắt + phức tạp) |
| Test data builder pattern cho `WallInfo`, `ElementId` mock | Mock `Document` (impossible, sealed) |
| 1 test = 1 assertion concept | Multiple unrelated asserts trong 1 test |
| Test naming: `MethodName_Scenario_ExpectedResult` | `Test1`, `WallTest` |
