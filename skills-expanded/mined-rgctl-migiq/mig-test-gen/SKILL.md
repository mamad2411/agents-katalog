---
name: mig-test-gen
description: Generate prioritized test suites based on rgctl knowledge graph analysis. Use when the user needs to add tests to an existing codebase, especially during migrations or when improving test coverage. Triggers on phrases like "generate tests", "add test coverage", "need tests for migration", "create unit tests", or when preparing a codebase for refactoring/migration. Requires the codebase to be indexed with rgctl first.
---

# Graph-Driven Test Generation

This skill generates comprehensive test suites using rgctl's knowledge graph to intelligently prioritize which code needs the most testing. By analyzing PageRank, blast-radius, and call-graph connectivity, it focuses testing effort where it matters most: architectural hotspots, public APIs, and critical integration points.

## Prerequisites

**Prerequisite:** Codebase indexed via **mig-rgctl** ([workflow](../mig-rgctl/references/workflow.md#mig-test-gen--mig-deploy)).

## When to Use This Skill

Use this skill when you need to:
- Generate tests for an existing codebase (especially legacy code)
- Add test coverage before a migration or major refactoring
- Create characterization tests to lock down current behavior
- Fill test coverage gaps identified during code review
- Ensure critical code paths are well-tested

The graph-driven approach ensures you test what matters, not just hit arbitrary coverage percentages.

## Workflow

### Step 1: Ensure rgctl Index and Communities Exist

```bash
rgctl -f json metrics --pagerank
rgctl -f json communities list
```

If either fails, invoke **mig-rgctl**, run discover per [workflow](../mig-rgctl/references/workflow.md), then STOP. After generating tests into the app tree, run `rgctl update` before further graph queries or the next migration phase.

### Step 2: Analyze Graph to Identify Critical Code

Query the graph to understand what needs testing:

```bash
# Architectural hotspots (Priority 1 test targets)
rgctl -f json metrics --pagerank --communities

# Community boundaries for integration tests
rgctl -f json communities list
```

Look for:
- **PageRank top symbols** — These are your Priority 1 test targets (high connectivity)
- **Communities** — Helps identify integration test boundaries
- **High blast-radius symbols** — Edge cases and ripple-effect paths that need coverage

Extract callers/callees for a symbol:
```bash
rgctl -f json gql "MATCH (a:Function)-[:CALLS]->(b:Function) WHERE b.name = 'ClassName' RETURN a,b LIMIT 20"
```

### Step 3: Categorize Code by Test Priority

Based on graph analysis, categorize all classes/modules into priority tiers:

**Priority 1 - God Nodes (degree ≥ 10):**
- These are the most-connected classes that many others depend on
- Changes here ripple through the entire codebase
- **Coverage requirement:** 90%+
- **Test type:** Comprehensive characterization tests
- **Test weight:** 3× (generate 3× more tests than normal)

**Priority 2 - Public APIs (Controllers, Services, REST endpoints):**
- External-facing code that other systems depend on
- Breaking changes here affect users/clients
- **Coverage requirement:** 95%+
- **Test type:** Functional tests + contract tests
- **Test weight:** 2.5×

**Priority 3 - Hubs (degree 5-9):**
- Important integration points with moderate connectivity
- **Coverage requirement:** 85%+
- **Test type:** Standard unit + integration tests
- **Test weight:** 2×

**Priority 4 - Normal nodes (degree 2-4):**
- Regular classes with standard dependencies
- **Coverage requirement:** 75%+
- **Test type:** Basic unit tests
- **Test weight:** 1×

**Priority 5 - Leaf nodes (degree 0-1):**
- Isolated utilities or data classes with minimal dependencies
- **Coverage requirement:** 70%+
- **Test type:** Minimal unit tests
- **Test weight:** 0.5×

### Step 4: Generate Tests by Priority

Work through the priority tiers from highest to lowest.

**For each class to test:**

1. **Determine dependencies from graph:**
   ```bash
   rgctl -f json gql "MATCH (a:Function)-[:CALLS]->(b:Function) WHERE a.name = 'ClassName' RETURN a,b LIMIT 20"
   # Know what to mock
   ```

2. **Read the actual class implementation:**
   ```bash
   # Only NOW read the source file
   # Use Read tool to get method signatures and behavior
   ```

3. **Check for existing tests:**
   ```bash
   find . -name "*Test.java" -o -name "*Test.py" -o -name "*.test.js" | xargs grep -l "ClassName"
   # Avoid duplicating existing tests
   ```

4. **Generate tests based on priority tier:**

   **For God Nodes (Priority 1):**
   - Test every public method
   - Test edge cases and error handling
   - Test integration with top 3 dependencies
   - Add parametrized tests for data-driven scenarios
   - Include performance tests if relevant

   **For Public APIs (Priority 2):**
   - Test all API endpoints/public methods
   - Test request/response contracts
   - Test error responses (400, 401, 404, 500)
   - Test authentication/authorization
   - Add integration tests for full request flows

   **For Hubs (Priority 3):**
   - Test main public methods
   - Test integration with key dependencies
   - Basic error handling

   **For Normal/Leaf (Priority 4-5):**
   - Test primary use cases
   - Basic happy path coverage

### Step 5: Use Graph Paths for Integration Tests

For integration tests, use the graph to understand end-to-end flows:

```bash
rgctl -f json gql "MATCH (n:Function) WHERE n.name LIKE '*Controller' RETURN n LIMIT 50"
# Find all controllers (entry points)
```

For each controller, trace the dependency path:
```bash
rgctl -f json gql "MATCH (a:Function)-[:CALLS*1..3]->(b:Function) WHERE a.name = 'UserController' RETURN a,b LIMIT 50"
# Example: UserController → UserService → UserRepository
```

Generate integration tests that follow these paths:
- Test the full request → controller → service → repository → DB flow
- Mock only external dependencies (database, external APIs)
- Keep internal dependencies real to test actual integration

### Step 6: Calculate and Report Test Coverage

After generating tests, calculate weighted coverage:

```bash
# Run test coverage tool (language-specific)
# Java: mvn test jacoco:report
# Python: pytest --cov
# JavaScript: npm test -- --coverage
```

For each priority tier, check if coverage meets requirements:
- God nodes: 90%+ ✓/✗
- Public APIs: 95%+ ✓/✗
- Hubs: 85%+ ✓/✗
- Normal: 75%+ ✓/✗
- Leaves: 70%+ ✓/✗

**Weighted coverage score:**
```
Total Coverage = (
  (God_Node_Coverage × 3) +
  (Public_API_Coverage × 2.5) +
  (Hub_Coverage × 2) +
  (Normal_Coverage × 1) +
  (Leaf_Coverage × 0.5)
) / Total_Weight
```

This ensures critical code is weighted appropriately.

## Test Generation Patterns

### Pattern 1: Characterization Tests (God Nodes)

**Goal:** Lock down existing behavior before refactoring

```java
// Example for a god node class
@Test
public void testUserService_existingBehavior() {
    // Arrange: Set up exact current state
    UserService service = new UserService();
    
    // Act: Call method with known inputs
    User result = service.getUser(123L);
    
    // Assert: Verify current behavior (even if wrong)
    assertEquals("currentBehavior", result.getStatus());
    // Document: Add comment if behavior seems wrong
    // TODO: This returns "currentBehavior" but should probably return "active"
}
```

**Why:** For legacy code migrations, you need to preserve existing behavior (bugs and all) until you understand what's intentional.

### Pattern 2: Contract Tests (Public APIs)

**Goal:** Ensure API contracts don't break

```java
@Test
public void testGetUser_returnsCorrectSchema() {
    Response response = api.getUser(123L);
    
    assertEquals(200, response.getStatus());
    assertTrue(response.hasField("id"));
    assertTrue(response.hasField("username"));
    assertTrue(response.hasField("email"));
    // Validate exact schema
}
```

**Why:** During migration, you're likely changing implementation but need to maintain API compatibility.

### Pattern 3: Dependency Integration Tests (Hubs)

**Goal:** Test real integration between components

```java
@Test
public void testUserService_integratesWithRepository() {
    // Use REAL repository, mock only DB
    UserRepository repo = new UserRepository(mockDatabase);
    UserService service = new UserService(repo);
    
    service.createUser(newUser);
    
    verify(mockDatabase).insert(any());
    // Tests real service → repository integration
}
```

**Why:** The graph shows these classes work together - test the actual integration, not just mocked interactions.

## Language-Specific Patterns

### Java (Spring Boot)

**Unit Test Pattern:**
```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    @Mock private UserRepository repository;
    @InjectMocks private UserService service;
    
    @Test
    void testGetUser_whenExists_returnsUser() {
        when(repository.findById(1L)).thenReturn(Optional.of(testUser));
        User result = service.getUser(1L);
        assertNotNull(result);
    }
}
```

**Integration Test Pattern:**
```java
@SpringBootTest
@AutoConfigureMockMvc
class UserControllerIntegrationTest {
    @Autowired private MockMvc mvc;
    
    @Test
    void testGetUser_endToEnd() throws Exception {
        mvc.perform(get("/api/users/1"))
           .andExpect(status().isOk())
           .andExpect(jsonPath("$.username").exists());
    }
}
```

### Python (Django/pytest)

**Unit Test Pattern:**
```python
from unittest.mock import Mock
import pytest

class TestUserService:
    def test_get_user_when_exists_returns_user(self):
        mock_repo = Mock()
        mock_repo.find_by_id.return_value = test_user
        
        service = UserService(mock_repo)
        result = service.get_user(1)
        
        assert result is not None
```

**Integration Test Pattern:**
```python
@pytest.mark.django_db
class TestUserAPI:
    def test_get_user_endpoint(self, client):
        user = User.objects.create(username="test")
        
        response = client.get(f'/api/users/{user.id}/')
        
        assert response.status_code == 200
        assert response.json()['username'] == 'test'
```

### JavaScript (Node.js/Jest)

**Unit Test Pattern:**
```javascript
describe('UserService', () => {
  it('should get user when exists', async () => {
    const mockRepo = { findById: jest.fn().resolves(testUser) };
    const service = new UserService(mockRepo);
    
    const result = await service.getUser(1);
    
    expect(result).toBeDefined();
  });
});
```

**Integration Test Pattern:**
```javascript
describe('User API', () => {
  it('GET /api/users/:id returns user', async () => {
    const user = await User.create({ username: 'test' });
    
    const response = await request(app).get(`/api/users/${user.id}`);
    
    expect(response.status).toBe(200);
    expect(response.body.username).toBe('test');
  });
});
```

## Output Format

Generate a test suite report showing:

```markdown
# Test Suite Generation Report

## Summary
- **Total classes analyzed:** [count from graph]
- **Tests generated:** [count]
- **Estimated coverage:** [percentage]
- **Priority breakdown:**
  - God nodes: [count] classes → [count] tests
  - Public APIs: [count] classes → [count] tests
  - Hubs: [count] classes → [count] tests
  - Normal/Leaf: [count] classes → [count] tests

## Priority 1: God Nodes
### [ClassName] (degree: [N])
- **Location:** [file path]
- **Tests generated:** [count]
- **Coverage target:** 90%+
- **Test files created:**
  - `[TestFileName]` - [brief description]

## Priority 2: Public APIs
[Same structure]

## Priority 3: Hubs
[Same structure]

## Priority 4: Normal/Leaf
[Summary only - don't list every class]

## Coverage Report
| Priority | Classes | Tests | Target | Actual | Status |
|----------|---------|-------|--------|--------|--------|
| God Nodes | [N] | [N] | 90%+ | [%] | ✓/✗ |
| Public APIs | [N] | [N] | 95%+ | [%] | ✓/✗ |
| Hubs | [N] | [N] | 85%+ | [%] | ✓/✗ |
| Normal/Leaf | [N] | [N] | 70-75%+ | [%] | ✓/✗ |

**Weighted Coverage Score:** [percentage]

## Next Steps
1. Review generated tests for [ClassName] (highest priority god node)
2. Run test suite to verify all tests pass
3. Adjust coverage for any failing priority tier
4. Consider additional integration tests for [specific paths]
```

## Key Principles

**Graph-First, Not Coverage-First:**
Don't chase arbitrary coverage percentages. Use the graph to identify what's critical, then test that thoroughly. 70% coverage on god nodes is better than 95% coverage on leaf nodes.

**Minimize File Reads:**
The graph tells you what to test and what it depends on. Only read source files to understand method signatures and implementation details. Target: <5 file reads per class tested.

**Prioritize Ruthlessly:**
If you only have time for 20 tests, generate all 20 for god nodes. Don't spread them evenly across the codebase.

**Test Actual Integration:**
When the graph shows ClassA → ClassB, test that real integration, not just mocked calls. The graph reveals actual dependencies.

**Explain Coverage Gaps:**
If a god node only hits 70% coverage (below 90% target), explain why in the report. Maybe certain methods are deprecated or impossible to test. Don't force it.

**Use Graph Paths for Integration Tests:**
```
Controller → Service → Repository → Database
```
This path (from the graph) becomes one integration test. Test the whole flow.

---

Remember: The knowledge graph is your test strategy. High-degree nodes = high test priority. Low-degree nodes = minimal tests. Simple as that.
