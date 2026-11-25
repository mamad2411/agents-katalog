---
name: tools-unity-test-framework
description: Unity Test Framework patterns for EditMode and PlayMode tests including async testing, mocking, and test organization.
---

# Unity Test Framework

## Overview

Unity Test Framework provides NUnit-based testing for Unity with EditMode (fast, no runtime) and PlayMode (full Unity lifecycle) test support.

## When to Use

- Unit testing game logic
- Integration testing systems
- Testing MonoBehaviour lifecycle
- Automated regression testing
- CI/CD test gates

## Test Assembly Setup

### Assembly Definition (EditMode)

```json
// Tests/Editor/MyGame.Tests.Editor.asmdef
{
    "name": "MyGame.Tests.Editor",
    "rootNamespace": "MyGame.Tests",
    "references": [
        "MyGame.Core",
        "MyGame.Gameplay",
        "VContainer",
        "UniTask"
    ],
    "includePlatforms": [
        "Editor"
    ],
    "excludePlatforms": [],
    "allowUnsafeCode": false,
    "overrideReferences": true,
    "precompiledReferences": [
        "nunit.framework.dll",
        "NSubstitute.dll"
    ],
    "autoReferenced": false,
    "defineConstraints": [
        "UNITY_INCLUDE_TESTS"
    ],
    "versionDefines": [],
    "noEngineReferences": false
}
```

### Assembly Definition (PlayMode)

```json
// Tests/Runtime/MyGame.Tests.Runtime.asmdef
{
    "name": "MyGame.Tests.Runtime",
    "references": [
        "MyGame.Core",
        "MyGame.Gameplay",
        "VContainer",
        "UniTask"
    ],
    "includePlatforms": [],
    "excludePlatforms": [],
    "overrideReferences": true,
    "precompiledReferences": [
        "nunit.framework.dll",
        "NSubstitute.dll"
    ],
    "defineConstraints": [
        "UNITY_INCLUDE_TESTS"
    ]
}
```

## EditMode Tests

### Basic Test Structure

```csharp
using NUnit.Framework;

namespace MyGame.Tests
{
    [TestFixture]
    public class DamageCalculatorTests
    {
        private DamageCalculator _calculator;
        
        [SetUp]
        public void SetUp()
        {
            _calculator = new DamageCalculator();
        }
        
        [TearDown]
        public void TearDown()
        {
            _calculator = null;
        }
        
        [Test]
        public void CalculateDamage_WithCrit_DoublesBaseDamage()
        {
            // Arrange
            var baseDamage = 100;
            var isCrit = true;
            
            // Act
            var result = _calculator.Calculate(baseDamage, isCrit);
            
            // Assert
            Assert.AreEqual(200, result);
        }
        
        [Test]
        public void CalculateDamage_NoCrit_ReturnsBaseDamage()
        {
            var result = _calculator.Calculate(100, false);
            Assert.AreEqual(100, result);
        }
    }
}
```

### Parameterized Tests

```csharp
[TestFixture]
public class AttributeTests
{
    [TestCase(100, 0.5f, 50)]
    [TestCase(100, 1.0f, 100)]
    [TestCase(100, 2.0f, 200)]
    [TestCase(0, 1.5f, 0)]
    public void ApplyMultiplier_ReturnsCorrectValue(float baseValue, float multiplier, float expected)
    {
        var result = AttributeCalculator.ApplyMultiplier(baseValue, multiplier);
        Assert.AreEqual(expected, result, 0.001f);
    }
    
    [TestCaseSource(nameof(DamageTestCases))]
    public void CalculateDamage_WithTestCases(int attack, int defense, int expected)
    {
        var result = DamageFormula.Calculate(attack, defense);
        Assert.AreEqual(expected, result);
    }
    
    private static IEnumerable<TestCaseData> DamageTestCases()
    {
        yield return new TestCaseData(100, 50, 75).SetName("Normal damage");
        yield return new TestCaseData(100, 100, 50).SetName("Equal stats");
        yield return new TestCaseData(50, 100, 25).SetName("High defense");
    }
}
```

### Testing with GameObjects

```csharp
[TestFixture]
public class HealthComponentTests
{
    private GameObject _testObject;
    private HealthComponent _health;
    
    [SetUp]
    public void SetUp()
    {
        _testObject = new GameObject("TestHealth");
        _health = _testObject.AddComponent<HealthComponent>();
        _health.Initialize(100);
    }
    
    [TearDown]
    public void TearDown()
    {
        Object.DestroyImmediate(_testObject);
    }
    
    [Test]
    public void TakeDamage_ReducesHealth()
    {
        _health.TakeDamage(30);
        Assert.AreEqual(70, _health.CurrentHealth);
    }
    
    [Test]
    public void TakeDamage_AtZero_TriggersDeath()
    {
        bool deathTriggered = false;
        _health.OnDeath += () => deathTriggered = true;
        
        _health.TakeDamage(100);
        
        Assert.IsTrue(deathTriggered);
        Assert.AreEqual(0, _health.CurrentHealth);
    }
}
```

## PlayMode Tests

### Basic PlayMode Test

```csharp
using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

[TestFixture]
public class PlayerMovementTests
{
    private GameObject _player;
    private PlayerMovement _movement;
    
    [UnitySetUp]
    public IEnumerator SetUp()
    {
        _player = new GameObject("Player");
        _movement = _player.AddComponent<PlayerMovement>();
        yield return null; // Wait one frame for Awake/Start
    }
    
    [UnityTearDown]
    public IEnumerator TearDown()
    {
        Object.Destroy(_player);
        yield return null;
    }
    
    [UnityTest]
    public IEnumerator Move_OverTime_ChangesPosition()
    {
        var startPos = _player.transform.position;
        
        _movement.Move(Vector3.forward);
        
        yield return new WaitForSeconds(0.5f);
        
        Assert.AreNotEqual(startPos, _player.transform.position);
    }
}
```

### Async Tests with UniTask

```csharp
using Cysharp.Threading.Tasks;

[TestFixture]
public class AsyncServiceTests
{
    [Test]
    public async Task LoadDataAsync_ReturnsValidData()
    {
        var service = new DataService();
        
        var result = await service.LoadDataAsync();
        
        Assert.IsNotNull(result);
        Assert.IsTrue(result.IsValid);
    }
    
    [UnityTest]
    public IEnumerator LoadDataAsync_WithUniTask_Works() => UniTask.ToCoroutine(async () =>
    {
        var service = new DataService();
        
        var result = await service.LoadDataAsync();
        
        Assert.IsNotNull(result);
    });
}
```

## Mocking with NSubstitute

### Basic Mocking

```csharp
using NSubstitute;

[TestFixture]
public class CombatSystemTests
{
    private ICombatSystem _combatSystem;
    private ITargetingService _mockTargeting;
    private IDamageCalculator _mockDamage;
    
    [SetUp]
    public void SetUp()
    {
        _mockTargeting = Substitute.For<ITargetingService>();
        _mockDamage = Substitute.For<IDamageCalculator>();
        
        _combatSystem = new CombatSystem(_mockTargeting, _mockDamage);
    }
    
    [Test]
    public void Attack_WithValidTarget_CalculatesDamage()
    {
        // Arrange
        var attacker = CreateTestCharacter();
        var target = CreateTestCharacter();
        
        _mockTargeting.GetTarget(attacker).Returns(target);
        _mockDamage.Calculate(Arg.Any<AttackData>()).Returns(50);
        
        // Act
        _combatSystem.Attack(attacker);
        
        // Assert
        _mockDamage.Received(1).Calculate(Arg.Any<AttackData>());
    }
    
    [Test]
    public void Attack_WithNoTarget_DoesNotCalculateDamage()
    {
        var attacker = CreateTestCharacter();
        _mockTargeting.GetTarget(attacker).Returns((Character)null);
        
        _combatSystem.Attack(attacker);
        
        _mockDamage.DidNotReceive().Calculate(Arg.Any<AttackData>());
    }
}
```

### Mocking Async Methods

```csharp
[Test]
public async Task SaveGame_CallsStorageService()
{
    var mockStorage = Substitute.For<IStorageService>();
    mockStorage.SaveAsync(Arg.Any<SaveData>()).Returns(UniTask.CompletedTask);
    
    var saveSystem = new SaveSystem(mockStorage);
    
    await saveSystem.SaveGameAsync();
    
    await mockStorage.Received(1).SaveAsync(Arg.Any<SaveData>());
}
```

### Argument Matchers

```csharp
[Test]
public void ApplyDamage_WithCorrectAmount()
{
    var mockHealth = Substitute.For<IHealthComponent>();
    var combat = new CombatHandler(mockHealth);
    
    combat.ApplyDamage(100);
    
    // Exact value
    mockHealth.Received().TakeDamage(100);
    
    // Any value
    mockHealth.Received().TakeDamage(Arg.Any<int>());
    
    // Value matching condition
    mockHealth.Received().TakeDamage(Arg.Is<int>(x => x > 0));
}
```

## Testing VContainer

### Testing with DI Container

```csharp
[TestFixture]
public class ServiceTests
{
    private LifetimeScope _testScope;
    
    [SetUp]
    public void SetUp()
    {
        _testScope = LifetimeScope.Create(builder =>
        {
            // Register mocks
            var mockRepo = Substitute.For<IPlayerRepository>();
            builder.RegisterInstance(mockRepo);
            
            // Register real service under test
            builder.Register<PlayerService>(Lifetime.Singleton);
        });
    }
    
    [TearDown]
    public void TearDown()
    {
        _testScope?.Dispose();
    }
    
    [Test]
    public void PlayerService_ResolvesCorrectly()
    {
        var service = _testScope.Container.Resolve<PlayerService>();
        Assert.IsNotNull(service);
    }
}
```

### Testing Installers

```csharp
[Test]
public void GameInstaller_RegistersAllDependencies()
{
    using var scope = LifetimeScope.Create(new GameInstaller());
    
    // Verify critical services resolve
    Assert.DoesNotThrow(() => scope.Container.Resolve<IPlayerService>());
    Assert.DoesNotThrow(() => scope.Container.Resolve<ICombatService>());
    Assert.DoesNotThrow(() => scope.Container.Resolve<IInventoryService>());
}
```

## Test Utilities

### Test Base Class

```csharp
public abstract class GameplayTestBase
{
    protected GameObject TestGameObject { get; private set; }
    
    [SetUp]
    public virtual void SetUp()
    {
        TestGameObject = new GameObject("Test");
    }
    
    [TearDown]
    public virtual void TearDown()
    {
        if (TestGameObject != null)
            Object.DestroyImmediate(TestGameObject);
    }
    
    protected T AddComponent<T>() where T : Component
    {
        return TestGameObject.AddComponent<T>();
    }
    
    protected GameObject CreateChild(string name = "Child")
    {
        var child = new GameObject(name);
        child.transform.SetParent(TestGameObject.transform);
        return child;
    }
}

// Usage
public class MyTests : GameplayTestBase
{
    [Test]
    public void Test()
    {
        var component = AddComponent<MyComponent>();
        // Test...
    }
}
```

### Async Test Helpers

```csharp
public static class AsyncTestHelpers
{
    public static IEnumerator WaitForCondition(
        Func<bool> condition,
        float timeout = 5f,
        string message = "Condition not met")
    {
        var startTime = Time.time;
        
        while (!condition())
        {
            if (Time.time - startTime > timeout)
            {
                Assert.Fail(message);
                yield break;
            }
            yield return null;
        }
    }
    
    public static IEnumerator WaitFrames(int frames)
    {
        for (int i = 0; i < frames; i++)
            yield return null;
    }
}
```

### ScriptableObject Test Helper

```csharp
public static class ScriptableObjectTestHelper
{
    public static T CreateInstance<T>() where T : ScriptableObject
    {
        return ScriptableObject.CreateInstance<T>();
    }
    
    public static T CreateInstance<T>(Action<T> configure) where T : ScriptableObject
    {
        var instance = ScriptableObject.CreateInstance<T>();
        configure(instance);
        return instance;
    }
}

// Usage
[Test]
public void AbilityConfig_HasCorrectDefaults()
{
    var ability = ScriptableObjectTestHelper.CreateInstance<AbilitySO>(a =>
    {
        a.Damage = 100;
        a.Cooldown = 5f;
    });
    
    Assert.AreEqual(100, ability.Damage);
}
```

## Test Categories and Filtering

### Categories

```csharp
[TestFixture]
[Category("Combat")]
public class CombatTests
{
    [Test]
    [Category("Critical")]
    public void CriticalCombatTest() { }
    
    [Test]
    [Category("Slow")]
    public void SlowCombatTest() { }
}

// Run specific category:
// Unity Test Runner > Category filter
// Or CLI: -testFilter "Category=Combat"
```

### Conditional Tests

```csharp
[Test]
[Platform(Include = "Editor")]
public void EditorOnlyTest() { }

[Test]
[UnityPlatform(RuntimePlatform.Android, RuntimePlatform.IPhonePlayer)]
public void MobileOnlyTest() { }

[Test]
[Ignore("Not implemented yet")]
public void FutureTest() { }
```

## Assertions

### Common Assertions

```csharp
// Equality
Assert.AreEqual(expected, actual);
Assert.AreNotEqual(unexpected, actual);

// Boolean
Assert.IsTrue(condition);
Assert.IsFalse(condition);

// Null
Assert.IsNull(obj);
Assert.IsNotNull(obj);

// Collections
Assert.Contains(item, collection);
Assert.IsEmpty(collection);
CollectionAssert.AreEqual(expected, actual);
CollectionAssert.AreEquivalent(expected, actual); // Order doesn't matter

// Exceptions
Assert.Throws<ArgumentException>(() => MethodThatThrows());
Assert.DoesNotThrow(() => SafeMethod());

// Floating point (with tolerance)
Assert.AreEqual(1.0f, actual, 0.001f);

// String
StringAssert.Contains("expected", actualString);
StringAssert.StartsWith("prefix", actualString);
```

### Custom Assertions

```csharp
public static class GameAssert
{
    public static void IsAlive(Character character)
    {
        Assert.IsTrue(character.IsAlive, $"Expected {character.Name} to be alive");
    }
    
    public static void HasTag(GameplayTagContainer container, string tag)
    {
        Assert.IsTrue(
            container.HasTag(GameplayTag.Get(tag)),
            $"Expected container to have tag '{tag}'"
        );
    }
}
```

## CI/CD Integration

### Command Line Execution

```bash
# Run EditMode tests
Unity -runTests -batchmode -projectPath /path/to/project \
  -testPlatform EditMode \
  -testResults results.xml \
  -logFile test.log

# Run specific category
Unity -runTests -batchmode -projectPath /path/to/project \
  -testPlatform EditMode \
  -testFilter "Category=Critical"

# Run PlayMode tests
Unity -runTests -batchmode -projectPath /path/to/project \
  -testPlatform PlayMode \
  -testResults results.xml
```

### GitHub Actions Example

```yaml
- name: Run Tests
  run: |
    Unity -runTests \
      -batchmode \
      -projectPath . \
      -testPlatform EditMode \
      -testResults TestResults.xml \
      -logFile TestLog.txt
      
- name: Upload Results
  uses: actions/upload-artifact@v3
  with:
    name: test-results
    path: TestResults.xml
```

## Best Practices

1. **Name tests clearly** - `Method_Scenario_ExpectedResult`
2. **One assertion per test** when possible
3. **Use SetUp/TearDown** for common initialization
4. **Mock external dependencies** - Don't test the framework
5. **Keep tests fast** - EditMode for logic, PlayMode only when needed
6. **Test edge cases** - Null, empty, boundary values
7. **Use categories** for filtering
8. **Run tests before commit** - Pre-commit hooks
9. **Maintain test independence** - No shared state
10. **Write tests for bugs** - Prevent regression
