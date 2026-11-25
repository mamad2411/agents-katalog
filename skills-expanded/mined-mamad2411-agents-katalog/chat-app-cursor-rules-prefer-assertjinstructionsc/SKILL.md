---
description: "Prefer AssertJ assertions over JUnit Assertions in Java tests."
globs: "**/*Test.java"
alwaysApply: false
---

# Prefer AssertJ Over JUnit Assertions

Prefer AssertJ for **all** assertion logic (`assertThat`, `assertThatThrownBy`, etc.) over JUnit `Assertions.*` (`assertEquals`, `assertTrue`, `assertNull`, `assertThrows`, …).

```java
// BAD
Assertions.assertEquals("Backend Team", response.getName());
Assertions.assertTrue(response.getUnreadCount() == 0);
ForbiddenException ex = Assertions.assertThrows(ForbiddenException.class, () -> service.doThing());
Assertions.assertEquals("message", ex.getMessage());

// GOOD
assertThat(response.getName()).isEqualTo("Backend Team");
assertThat(response.getUnreadCount()).isZero();
assertThatThrownBy(() -> service.doThing())
        .isInstanceOf(ForbiddenException.class)
        .hasMessage("message");
```

Keep using JUnit for the test runner (`@Test`, `@ExtendWith`, lifecycle annotations).
