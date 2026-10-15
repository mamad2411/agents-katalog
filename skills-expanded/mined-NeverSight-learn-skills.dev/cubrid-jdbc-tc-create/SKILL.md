---
name: cubrid-jdbc-tc-create
description: "Create, draft, or scaffold a new CUBRID JDBC testcase as a standard JUnit 4 class — for a CBRD bug fix (default) or a JDBC spec/feature. Use whenever someone says \"jdbc tc 만들어줘\", \"jdbc tc 초안 작성해줘\", \"jdbc 테스트케이스 작성\", \"create jdbc test\", \"draft jdbc testcase\", or \"create jdbc tc for CBRD-XXXXX\", even without the word \"testcase\". They usually give a CBRD number, the behavior to test, and sometimes a target category. NOT for: running/reviewing existing JDBC tests (use cubrid-jdbc-tc-verify), or shell/SQL/CCI/HA testcases (use the matching cubrid-*-tc-* skill)."
---

# JDBC Testcase Creator (CTP)

Generate a CUBRID JDBC testcase as a **standard JUnit 4 class** that drops into the real `test_jdbc` tree and runs unchanged under CTP's `JdbcLocalTest` runner and Ant `batchtest`. Two patterns; pick by intent.

## Scope

**Produces:** one JUnit 4 `Test*.java` class with `@Before`/`@Test`/`@After` methods, the correct package + on-disk directory, and `test1()/test2()/…` methods.

**Does NOT produce:** `jdbc.properties` / `cubrid.conf` / the CTP conf (CTP fills these at runtime), `build.xml` changes (Ant `batchtest` auto-discovers any `Test*` class), or non-JDBC tests.

## Before you start

- **Testcase repo.** Resolve its root without a hardcoded home path: use `$CUBRID_TESTCASES_PRIVATE` if set, else discover the `cubrid-testcases-private` checkout from the current dir (`git rev-parse --show-toplevel` or search upward), else ask the user. Call it `$TC` below. The JDBC develop tree lives at `$TC/interface/JDBC/test_jdbc`; sanity check: `ls $TC/interface/JDBC/test_jdbc/build.xml`. CTP itself is only needed to *run* (that's `cubrid-jdbc-tc-verify`).
- **JIRA context (optional).** If a `CBRD-XXXXX` is referenced, run `cubrid-jira search CBRD-XXXXX` first to ground the work (reuse if already fetched). If the CLI isn't installed, skip — but installing `cubrid-jira` improves accuracy.

## Directory convention

Pick the pattern by intent. Package declaration and on-disk directory **must match**; class name **must equal** the filename and **must start with `Test`** (Ant `batchtest` discovers `**/Test*.class`).

```
# Bug / regression (DEFAULT):
#   src/cubrid/jdbc/driver/TestCBRD<num>.java        pkg cubrid.jdbc.driver
#   multiple tests for one issue:  TestCBRD<num>_1, TestCBRD<num>_2
# Spec / feature (when explicitly a JDBC spec test):
#   src/com/cubrid/jdbc/test/spec/<category>/Test<Feature>.java   pkg com.cubrid.jdbc.test.spec.<category>
#   <category> ∈ connection | statement | resultset | metadata | transaction
```

## Lifecycle contract

Standard JUnit 4: `@Before` opens the connection, each `@Test` (`test1`, `test2`, …) does one scenario, `@After` cleans up and closes. Missing a step fails review.

**Driver pattern (default)** — independent class, `ConnectionProvider` + `SqlUtil`:
```java
package cubrid.jdbc.driver;

import java.sql.SQLException;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.Assert;
import cubrid.jdbc.ConnectionProvider;

public class TestCBRD12345 {
    CUBRIDConnection conn;                       // same package — no import needed

    @Before public void before() throws SQLException { conn = ConnectionProvider.getConnection(); }

    @Test public void test1() throws SQLException {
        SqlUtil.createTable(conn, "t1", "a int primary key");
        SqlUtil.insertRow(conn, "t1", new SqlUtil.Arg("a", java.sql.Types.INTEGER, "1"));
        Assert.assertEquals(1, SqlUtil.getCount(conn, "t1", null));
    }

    @Test(expected = SQLException.class)         // expected exceptions are an ANNOTATION, not try/catch
    public void test2() throws SQLException { conn.createStatement().execute("SELECT bad_syntax"); }

    @After public void after() throws SQLException { SqlUtil.dropTable(conn, "t1"); conn.close(); }
}
```

**Spec pattern (feature tests)** — `extends GeneralTestCase`; the base owns `@Before`/`@After` and gives you `conn()` + static helpers (`createTable`, `dropTable`, `queryAsList`, `getCount`, `executeSql`, `insertRow`):
```java
package com.cubrid.jdbc.test.spec.statement;
import org.junit.Test;
import org.junit.Assert;
import com.cubrid.jdbc.test.spec.GeneralTestCase;

public class TestFetchSize extends GeneralTestCase {
    @Test public void test1() throws Exception {
        createTable(conn(), "t1", "a int");
        Assert.assertEquals(0, getCount(conn(), "t1", null));
    }
}
```

### Why each part matters (not just ritual)

- **`ConnectionProvider` / `conn()`, never a literal URL** — CTP rewrites `jdbc.properties` with the live broker port at runtime; a hardcoded URL only passes on one machine.
- **`@Before`/`@After`, not per-method connect** — the base/`before()` opens one connection and `after()` always closes it even when a `@Test` throws, so no session leaks into the next test. (This is the house standard; the spec base enforces it.)
- **`@Test(expected = …)`** — the standard, self-documenting way to assert a throw. A `try { … } catch` that forgets to fail on the no-throw path silently passes.
- **Class name starts with `Test`** — Ant `batchtest` matches `Test*.class`; `JdbcLocalTest` additionally matches `@Test`/`test*` methods. Both must agree or the case never runs.

## Essential helpers (use these, not raw equivalents)

| Use | Instead of | Why |
|---|---|---|
| `ConnectionProvider.getConnection()` (driver) / `conn()` (spec) | `DriverManager.getConnection("jdbc:cubrid:...")` | env-portable; CTP fills the live port |
| `SqlUtil.*` (driver) / `GeneralTestCase` static helpers (spec) | hand-rolled `Statement` boilerplate | matches the corpus; less to get wrong |
| `@Test(expected = SQLException.class)` | `try { op; Assert.fail(); } catch (SQLException e) {}` | standard, no silent-pass hole |
| `@Ignore` + one-line reason | commenting out the method | JUnit reports it skipped, not dropped |

Asserts: `org.junit.Assert.assertEquals/assertTrue/assertFalse/assertNull/assertNotNull`.

## Writing rules (principles, not ritual)

- **Standard JUnit 4 shape** — `@Before`/`@After` lifecycle, numbered `test1()/test2()` methods returning `void`.
- **Connections via `ConnectionProvider`/`conn()`** — never a literal URL, host, or port.
- **Re-runnable** — `drop table if exists` (or `SqlUtil.dropTable`) before create; clean up in `@After`.
- **Expected exceptions** via `@Test(expected = …)`, not a catch block.
- **JDK 1.8 / JUnit 4.8.2 API only** — no JUnit 5 (`org.junit.jupiter`), no try-with-resources beyond 1.8.
- **`@Ignore` (with a reason)** for disabled tests; never comment out the body.
- **Class name starts with `Test`**, equals the filename; package equals the directory.

## House idioms (quick recipes)

- **PreparedStatement / batch:** `PreparedStatement ps = conn.prepareStatement("… ?")`; `ps.setInt(1, v)`; for batch `ps.addBatch()` in a loop then assert the `int[]` from `ps.executeBatch()`.
- **Expected error code:** combine `@Test(expected = SQLException.class)` with a body that triggers it; assert `e.getErrorCode()` inside only when the specific code matters.
- **Read values by column name** (`rs.getString("a")`) so a column-order change can't silently pass.
- **PowerMock/EasyMock** (driver unit tests): `@RunWith(PowerMockRunner.class)` + `@PrepareForTest` — only when mocking driver internals; jars are already in `lib/`.

## Verify before claiming done

Prove it compiles and runs — don't just eyeball it.

1. **Run it (ground truth):** hand off to `cubrid-jdbc-tc-verify` with a build to execute the class under CTP and read the OK/NOK.
2. **Compile fallback:** `cd $TC/interface/JDBC/test_jdbc && javac -cp "lib/*:$CUBRID/jdbc/cubrid_jdbc.jar" -d /tmp/jdbc_bin $(find src -name '*.java')` (or `ant compile`) to confirm it builds.

## Self-review checklist

- Package == on-disk directory? Class name == filename and starts with `Test`? Right tree (driver vs spec/<category>)?
- `@Before` opens via `ConnectionProvider`/base, `@After` closes? Methods named `test1`, `test2`, …?
- Expected exceptions via `@Test(expected = …)` (not try/catch)?
- Connection from `ConnectionProvider`/`conn()` — no literal URL/host/port?
- Re-runnable (`drop … if exists`), cleaned up in `@After`?
- JUnit 4.8.2 / JDK 1.8 API only? `@Ignore` (not a comment) on disabled tests?
- Compiles (`ant compile`/`javac`), and verified via `cubrid-jdbc-tc-verify` when a build is available?

## Examples & references

- `@examples/TestCBRD12345.java` — driver pattern (`ConnectionProvider`, `SqlUtil`, `@Test(expected=…)`).
- `@examples/TestFeatureSpec.java` — spec pattern (`extends GeneralTestCase`, `conn()`, static helpers).
- Real corpus: `$TC/interface/JDBC/test_jdbc/` — `build.xml` (discovery rules), `src/cubrid/jdbc/ConnectionProvider.java`, `src/cubrid/jdbc/SqlUtil.java`, `src/com/cubrid/jdbc/test/spec/GeneralTestCase.java`.
- Test guide: `jdbc_guide.md` — https://github.com/CUBRID/cubrid-testtools/blob/develop/doc/jdbc_guide.md (or `$CTP_HOME/../doc/jdbc_guide.md` if CTP is checked out locally).
