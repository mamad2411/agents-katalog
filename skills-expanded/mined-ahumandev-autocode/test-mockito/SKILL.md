---
name: test-mockito
description: Use this skill when writing or fixing unit tests that use Mockito for mocking in Java.
---

# Mockito Testing Skill

Mockito is the standard Java mocking framework, used alongside JUnit 5 to isolate the unit under test by replacing dependencies with controlled test doubles.

## Detection

Mockito is in use when:
- `pom.xml` includes `mockito-core` or `mockito-junit-jupiter`
- `build.gradle` includes `testImplementation 'org.mockito:mockito-core'`
- Test files import from `org.mockito.*`

## Setup with JUnit 5

Use `@ExtendWith(MockitoExtension.class)` to automatically initialize mocks and verify interactions after each test:

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

  @Mock
  private PaymentGateway paymentGateway;

  @Mock
  private InventoryRepository inventoryRepository;

  @InjectMocks
  private OrderService orderService;  // Mockito injects the mocks above

  @Test
  void processOrder_shouldChargePayment_whenItemsAreInStock() {
    // Arrange
    when(inventoryRepository.isInStock("ITEM-1")).thenReturn(true);
    when(paymentGateway.charge(100.0)).thenReturn(new PaymentResult(true));

    // Build
    boolean result = orderService.processOrder("ITEM-1", 100.0);

    // Assert
    assertTrue(result);
    verify(paymentGateway).charge(100.0);
  }
}
```

## Annotations

| Annotation | Purpose |
|---|---|
| `@Mock` | Creates a mock of the type |
| `@InjectMocks` | Creates instance and injects `@Mock` fields |
| `@Spy` | Wraps a real object, allows partial mocking |
| `@Captor` | Captures argument passed to a mock |
| `@ExtendWith(MockitoExtension.class)` | Enables annotation-based mock init |

## Stubbing (when/thenReturn)

```java
// Return a value
when(mock.method()).thenReturn("value")

// Return different values on consecutive calls
when(mock.method())
  .thenReturn("first")
  .thenReturn("second")
  .thenReturn("third")

// Throw an exception
when(mock.method()).thenThrow(new RuntimeException("error"))

// Return void method throwing
doThrow(new RuntimeException()).when(mock).voidMethod()

// Execute custom logic
when(mock.method(any())).thenAnswer(invocation -> {
  String arg = invocation.getArgument(0);
  return arg.toUpperCase();
})
```

## Argument Matchers

```java
when(mock.method(any()))                     // any non-null object
when(mock.method(anyString()))               // any String
when(mock.method(anyInt()))                  // any int
when(mock.method(eq("exact")))               // exact value
when(mock.method(isNull()))                  // null
when(mock.method(argThat(s -> s.length() > 3)))  // custom predicate

// IMPORTANT: if using matchers, ALL arguments must use matchers
when(mock.method(eq("key"), anyInt()))       // correct
when(mock.method("key", anyInt()))           // WRONG — mix not allowed
```

## Verification

```java
// Verify called once
verify(mock).method("arg")

// Verify exact number of calls
verify(mock, times(3)).method()

// Verify never called
verify(mock, never()).method()

// Verify at least / at most
verify(mock, atLeast(1)).method()
verify(mock, atMost(2)).method()
```

Only use: `verifyNoMoreInteractions(mock)` and `verifyNoInteractions(mock)` if you know that more interactions would have severe effects on system

## Argument Captors

```java
@Captor
private ArgumentCaptor<String> captor;

@Test
void shouldPassCorrectArgumentToService() {
  orderService.submit("order-1");

  verify(emailService).sendConfirmation(captor.capture());
  assertEquals("order-1", captor.getValue());
}
```

## Spy (Partial Mock)

Use `@Spy` or `spy()` when you want a real object but need to stub specific methods:

```java
@Spy
private List<String> spyList = new ArrayList<>();

@Test
void shouldUseRealImplementationExceptStubbedMethod() {
  doReturn(42).when(spyList).size();  // stub one method

  spyList.add("hello");              // real add
  assertEquals(42, spyList.size())   // stubbed size
  assertEquals("hello", spyList.get(0))  // real get
}
```

## Void Methods

```java
// Do nothing (default for void mocks, but explicit)
doNothing().when(mock).voidMethod()

// Throw from void method
doThrow(new RuntimeException()).when(mock).voidMethod()

// Execute custom logic for void method
doAnswer(invocation -> {
  System.out.println("called");
  return null;
}).when(mock).voidMethod()
```

## Static Methods (Mockito 3.4+)

```java
try (MockedStatic<Utilities> mocked = mockStatic(Utilities.class)) {
  mocked.when(Utilities::generateId).thenReturn("test-id");
  assertEquals("test-id", Utilities.generateId());
}
```

## pom.xml Dependency

```xml
<dependency>
  <groupId>org.mockito</groupId>
  <artifactId>mockito-junit-jupiter</artifactId>
  <version>5.5.0</version>
  <scope>test</scope>
</dependency>
```

`mockito-junit-jupiter` includes `mockito-core` — no need to add both.

## Common Pitfalls

- **Don't stub what you don't verify** — unnecessary stubbing causes `UnnecessaryStubbingException` with `MockitoExtension`
- **Argument matcher mixing** — if one argument uses a matcher (`any()`), ALL arguments must use matchers
- **`@InjectMocks` limitations** — constructor injection is preferred; if the class has no single matching constructor, injection may silently fail
- **Verify after build** — `verify()` calls go AFTER the method call being tested, not before
- **Don't mock value objects** — mock services, repositories, gateways; use real instances for simple data objects
- **`spy` on final classes** — not supported by default; enable with Mockito extensions or use a wrapper
