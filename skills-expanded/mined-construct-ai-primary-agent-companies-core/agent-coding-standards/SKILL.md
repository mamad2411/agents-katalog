---
memory_layer: durable_knowledge
para_section: pages/skills/agent-coding-standards
gigabrain_tags: coding-standards, agent-development, codebase-standards, development-practices
openstinger_context: coding-standards-practices, agent-development-standards
last_updated: 2026-03-30
related_docs:
  - docs_construct_ai/codebase/coding-standards/0000_AGENT_CODING_STANDARDS.md
  - docs_construct_ai/codebase/coding-standards/0000_AGENT_DEVELOPMENT_STANDARDS.md
  - docs_construct_ai/codebase/coding-standards/0000_CODE_STANDARDIZATION_MASTER_PLAN.md
related_skills:
  - writing-plans
  - test-driven-development
  - verification-before-completion
frequency_percent: 95.0
success_rate_percent: 92.0
---

# Agent Coding Standards Skill

## Overview

**Core principle:** Apply Construct AI coding standards systematically to ensure consistent, maintainable, and secure agent development.

**Reference:** This skill focuses on *how to apply* standards. For detailed standards documentation, see [Agent Coding Standards Reference](docs_construct_ai/codebase/coding-standards/0000_AGENT_CODING_STANDARDS.md).

## When to Use This Skill

**Trigger Conditions:**
- When developing or modifying AI agents for Construct AI
- Before implementing any agent functionality
- When reviewing agent code for standards compliance
- When setting up new agent development environments
- When integrating agents with existing Construct AI systems
- When debugging agent-related issues
- When deploying agents to production

**Mandatory Application:**
- Required for all agent development work
- Must be applied before any agent implementation
- Required for both new agents and agent modifications
- Must be verified before agent deployment

## Step-by-Step Procedure

### Step 1: Review Reference Standards
**Access the comprehensive coding standards documentation:**

```bash
# Open the primary reference document
open docs_construct_ai/codebase/coding-standards/0000_AGENT_CODING_STANDARDS.md
```

**Key Reference Sections:**
- Project Overview & Technical Stack
- JavaScript/Node.js Standards
- File Structure Requirements
- Import/Export Conventions
- Error Handling Patterns
- Database Standards
- API Design Guidelines
- Security Requirements
- Testing Standards
- Prompt Key Naming Conventions
- Governance Integration Requirements

### Step 2: Environment Standards Verification
**Verify development environment meets requirements:**

```javascript
// Environment validation checklist
const environmentChecklist = {
  nodeVersion: process.version >= '18.0.0',
  databaseConnection: await testSupabaseConnection(),
  authenticationConfigured: checkCustomAuthSetup(),
  requiredEnvVars: validateEnvironmentVariables([
    'SUPABASE_URL',
    'SUPABASE_ANON_KEY',
    'JWT_SECRET'
  ]),
  fileStructure: validateProjectStructure()
};

function validateEnvironmentVariables(requiredVars) {
  return requiredVars.every(varName => process.env[varName] !== undefined);
}

function validateProjectStructure() {
  const requiredDirs = ['server/', 'client/', 'docs/', 'server/sql/'];
  return requiredDirs.every(dir => fs.existsSync(path.join(process.cwd(), dir)));
}

// Execute validation
const results = await runEnvironmentValidation(environmentChecklist);
if (!results.allPassed) {
  console.error('Environment validation failed:', results.failures);
  // Fix environment issues before proceeding
}
```

### Step 3: Code Standards Application
**Apply coding standards systematically to new or modified code:**

```javascript
// Code standards application checklist
const codeStandardsChecklist = {
  namingConventions: validateNamingConventions(code),
  importExport: validateImportExportPatterns(code),
  errorHandling: validateErrorHandling(code),
  security: validateSecurityMeasures(code),
  testing: validateTestingCoverage(code),
  promptKeys: validatePromptKeyNaming(code),
  governance: validateGovernanceIntegration(code)
};

// Validation functions
function validateNamingConventions(code) {
  // Check camelCase for variables/functions
  // Check PascalCase for components/classes
  // Check snake_case for database columns
  // Return validation results
}

function validateImportExportPatterns(code) {
  // Check ES6 import/export usage
  // Check import grouping (stdlib, third-party, local)
  // Check relative path usage
  // Return validation results
}

// Apply standards to code
function applyCodingStandards(code) {
  const validation = runStandardsValidation(code);

  if (!validation.passed) {
    console.warn('Code standards violations found:');
    validation.issues.forEach(issue => {
      console.warn(`- ${issue.type}: ${issue.message} (line ${issue.line})`);
    });

    // Auto-fix where possible
    const fixedCode = autoFixStandardsViolations(code, validation.issues);
    return fixedCode;
  }

  return code;
}
```

### Step 4: Database Standards Implementation
**Ensure database interactions follow security and performance standards:**

```javascript
// Database standards application
class DatabaseStandardsEnforcer {
  constructor(dbClient) {
    this.db = dbClient;
    this.queryValidator = new QueryValidator();
  }

  async executeQuery(query, params) {
    // Validate query for security
    const validation = this.queryValidator.validate(query, params);

    if (!validation.safe) {
      throw new SecurityError(`Unsafe query detected: ${validation.issues.join(', ')}`);
    }

    // Execute with proper error handling
    try {
      const result = await this.db.query(query, params);
      this.logQueryExecution(query, params, result.rowCount);
      return result;
    } catch (error) {
      this.logQueryError(query, params, error);
      throw new DatabaseError('Query execution failed', error);
    }
  }

  // Transaction wrapper with standards
  async executeTransaction(operations) {
    const client = await this.db.getClient();

    try {
      await client.query('BEGIN');

      for (const operation of operations) {
        await this.executeQuery(operation.query, operation.params);
      }

      await client.query('COMMIT');
      this.logTransactionSuccess(operations.length);

    } catch (error) {
      await client.query('ROLLBACK');
      this.logTransactionFailure(error);
      throw error;
    } finally {
      client.release();
    }
  }
}

// Usage
const dbEnforcer = new DatabaseStandardsEnforcer(dbClient);
const result = await dbEnforcer.executeQuery(
  'SELECT * FROM agents WHERE id = $1 AND organization_id = $2',
  [agentId, orgId]
);
```

### Step 5: API Standards Implementation
**Apply RESTful API design patterns with proper error handling:**

```javascript
// API standards implementation
function createStandardsCompliantRouter(basePath) {
  const router = express.Router();

  // Apply standard middleware
  router.use(standardMiddleware.cors);
  router.use(standardMiddleware.requestLogging);
  router.use(standardMiddleware.rateLimiting);
  router.use(standardMiddleware.inputValidation);

  // Standard CRUD endpoints
  router.get(`${basePath}`, async (req, res) => {
    try {
      const result = await handleGetRequest(req.query);
      res.json(standardResponse.success(result));
    } catch (error) {
      res.status(getHttpStatus(error)).json(standardResponse.error(error));
    }
  });

  router.post(`${basePath}`, async (req, res) => {
    try {
      const result = await handlePostRequest(req.body);
      res.status(201).json(standardResponse.success(result, 'Created successfully'));
    } catch (error) {
      res.status(getHttpStatus(error)).json(standardResponse.error(error));
    }
  });

  // Add standard health check
  router.get('/health', (req, res) => {
    res.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      service: basePath.replace('/', ''),
      standards: 'compliant'
    });
  });

  return router;
}

// Standard response formatters
const standardResponse = {
  success: (data, message = null) => ({
    success: true,
    data,
    message,
    timestamp: new Date().toISOString()
  }),

  error: (error) => ({
    success: false,
    error: error.message,
    type: error.constructor.name,
    timestamp: new Date().toISOString()
  })
};
```

### Step 6: Security Standards Application
**Implement comprehensive security measures:**

```javascript
// Security standards enforcer
class SecurityStandardsEnforcer {
  constructor() {
    this.inputValidator = new InputValidator();
    this.authMiddleware = new AuthMiddleware();
    this.rateLimiter = new RateLimiter();
  }

  applySecurityMiddleware(app) {
    // Apply in correct order
    app.use(this.rateLimiter.middleware());
    app.use(this.authMiddleware.requireAuth());
    app.use(this.inputValidator.sanitizeMiddleware());
  }

  validateInput(data, schema) {
    return this.inputValidator.validate(data, schema);
  }

  generateSecureToken(payload) {
    return jwt.sign(payload, process.env.JWT_SECRET, {
      expiresIn: '24h',
      issuer: 'construct-ai'
    });
  }

  hashPassword(password) {
    return bcrypt.hash(password, 12);
  }

  verifyPassword(password, hash) {
    return bcrypt.compare(password, hash);
  }
}

// Usage in routes
const security = new SecurityStandardsEnforcer();

router.post('/agents', security.authMiddleware.requireAuth(), async (req, res) => {
  // Validate input
  const validation = security.validateInput(req.body, agentCreationSchema);
  if (!validation.valid) {
    return res.status(400).json(standardResponse.error(new ValidationError(validation.errors)));
  }

  // Hash sensitive data if needed
  if (req.body.password) {
    req.body.passwordHash = await security.hashPassword(req.body.password);
    delete req.body.password;
  }

  // Proceed with secure data
  const result = await createAgent(req.body);
  res.status(201).json(standardResponse.success(result));
});
```

### Step 7: Testing Standards Implementation
**Apply comprehensive testing standards:**

```javascript
// Testing standards implementation
class TestingStandardsEnforcer {
  constructor() {
    this.testRunner = new JestRunner();
    this.coverageReporter = new CoverageReporter();
    this.mockGenerator = new MockGenerator();
  }

  async runStandardsTests(testFiles) {
    // Setup test environment
    await this.setupTestEnvironment();

    // Run tests with coverage
    const results = await this.testRunner.run(testFiles, {
      coverage: true,
      coverageThreshold: {
        global: {
          branches: 80,
          functions: 80,
          lines: 80,
          statements: 80
        }
      }
    });

    // Validate results against standards
    const standardsValidation = this.validateTestStandards(results);

    if (!standardsValidation.passed) {
      console.error('Testing standards violations:');
      standardsValidation.issues.forEach(issue => console.error(`- ${issue}`));
    }

    return { results, standardsValidation };
  }

  validateTestStandards(results) {
    const issues = [];

    // Check coverage thresholds
    if (results.coverage.global.branches < 80) {
      issues.push(`Branch coverage too low: ${results.coverage.global.branches}% (required: 80%)`);
    }

    // Check test naming conventions
    results.testResults.forEach(testFile => {
      testFile.testResults.forEach(test => {
        if (!test.title.match(/should .+/)) {
          issues.push(`Test name should start with 'should': "${test.title}"`);
        }
      });
    });

    return {
      passed: issues.length === 0,
      issues
    };
  }
}

// Usage
const tester = new TestingStandardsEnforcer();
const testResults = await tester.runStandardsTests([
  'server/tests/unit/**/*.test.js',
  'server/tests/integration/**/*.test.js'
]);
```

### Step 8: Prompt Key Standards Validation
**Ensure prompt keys follow naming conventions:**

```javascript
// Prompt key standards validation
class PromptKeyStandardsValidator {
  constructor() {
    this.validator = new PromptKeyValidator();
    this.auditor = new PromptKeyAuditor();
  }

  async validateProjectPromptKeys(projectRoot) {
    // Find all prompt key usages
    const keyUsages = await this.findPromptKeyUsages(projectRoot);

    // Validate each key
    const validationResults = keyUsages.map(usage => ({
      file: usage.file,
      line: usage.line,
      key: usage.key,
      validation: this.validator.validate(usage.key)
    }));

    // Report violations
    const violations = validationResults.filter(r => !r.validation.isValid);
    if (violations.length > 0) {
      console.error('Prompt key violations found:');
      violations.forEach(v => {
        console.error(`${v.file}:${v.line} - ${v.key}: ${v.validation.error}`);
      });
    }

    return {
      total: keyUsages.length,
      valid: validationResults.filter(r => r.validation.isValid).length,
      violations: violations.length,
      results: validationResults
    };
  }

  async findPromptKeyUsages(projectRoot) {
    // Search for getPromptByKey calls
    const pattern = /getPromptByKey\(['"]([^'"]+)['"]\)/g;
    const usages = [];

    // Search in JavaScript/TypeScript files
    const files = await glob('**/*.{js,ts,jsx,tsx}', { cwd: projectRoot });

    for (const file of files) {
      const content = await fs.readFile(path.join(projectRoot, file), 'utf8');
      let match;
      let lineNum = 1;

      while ((match = pattern.exec(content)) !== null) {
        const beforeMatch = content.substring(0, match.index);
        lineNum = (beforeMatch.match(/\n/g) || []).length + 1;

        usages.push({
          file,
          line: lineNum,
          key: match[1]
        });
      }
    }

    return usages;
  }
}

// Usage
const promptValidator = new PromptKeyStandardsValidator();
const validation = await promptValidator.validateProjectPromptKeys('./');
console.log(`Prompt keys: ${validation.valid}/${validation.total} valid`);
```

### Step 9: Governance Standards Integration
**Apply governance compliance requirements:**

```javascript
// Governance standards integration
class GovernanceStandardsEnforcer {
  constructor() {
    this.jurisdiction = process.env.PRIMARY_JURISDICTION || 'FI';
    this.strictMode = process.env.GOVERNANCE_STRICT_MODE === 'true';
  }

  applyGovernanceDecorator(targetClass) {
    // Apply @with_governance decorator
    return with_governance({
      jurisdiction: this.jurisdiction,
      strict_mode: this.strictMode
    })(targetClass);
  }

  async validateGovernanceCompliance(agentCode) {
    const checklist = {
      hasGovernanceDecorator: this.checkGovernanceDecorator(agentCode),
      specifiesJurisdiction: this.checkJurisdictionDeclaration(agentCode),
      handlesBlockedResults: this.checkBlockedResultHandling(agentCode),
      implementsAuditLogging: this.checkAuditLogging(agentCode),
      validatesCompliance: this.checkComplianceValidation(agentCode)
    };

    const passed = Object.values(checklist).every(item => item === true);

    if (!passed) {
      const failures = Object.entries(checklist)
        .filter(([_, passed]) => !passed)
        .map(([check, _]) => check);

      throw new GovernanceError(`Governance compliance failed: ${failures.join(', ')}`);
    }

    return { passed: true, checklist };
  }

  checkGovernanceDecorator(code) {
    return code.includes('@with_governance') || code.includes('with_governance(');
  }

  checkJurisdictionDeclaration(code) {
    return code.includes(`jurisdiction: '${this.jurisdiction}'`) ||
           code.includes(`jurisdiction: "${this.jurisdiction}"`);
  }

  checkBlockedResultHandling(code) {
    return code.includes('governance_blocked') ||
           code.includes('blocked') && code.includes('governance');
  }

  checkAuditLogging(code) {
    return code.includes('logGovernanceEvent') ||
           code.includes('audit') && code.includes('governance');
  }

  checkComplianceValidation(code) {
    return code.includes('evaluateCompliance') ||
           code.includes('checkCompliance');
  }
}

// Usage
const governance = new GovernanceStandardsEnforcer();
const GovernedAgent = governance.applyGovernanceDecorator(MyAgent);

// Validate compliance
const compliance = await governance.validateGovernanceCompliance(agentSourceCode);
```

### Step 10: Standards Compliance Verification
**Run comprehensive compliance checks:**

```javascript
// Comprehensive standards verification
class StandardsComplianceVerifier {
  constructor() {
    this.checkers = {
      environment: new EnvironmentStandardsChecker(),
      code: new CodeStandardsChecker(),
      database: new DatabaseStandardsChecker(),
      api: new APIStandardsChecker(),
      security: new SecurityStandardsChecker(),
      testing: new TestingStandardsChecker(),
      promptKeys: new PromptKeyStandardsChecker(),
      governance: new GovernanceStandardsChecker()
    };
  }

  async runFullComplianceCheck(projectRoot) {
    console.log('🔍 Running comprehensive standards compliance check...');

    const results = {};
    let allPassed = true;

    for (const [standard, checker] of Object.entries(this.checkers)) {
      console.log(`Checking ${standard} standards...`);
      try {
        const result = await checker.check(projectRoot);
        results[standard] = result;

        if (!result.passed) {
          allPassed = false;
          console.error(`❌ ${standard}: ${result.issues.length} issues found`);
          result.issues.forEach(issue => console.error(`  - ${issue}`));
        } else {
          console.log(`✅ ${standard}: Passed`);
        }
      } catch (error) {
        allPassed = false;
        results[standard] = { passed: false, error: error.message };
        console.error(`❌ ${standard}: Check failed - ${error.message}`);
      }
    }

    // Generate compliance report
    const report = this.generateComplianceReport(results, allPassed);

    console.log('\n📊 Compliance Summary:');
    console.log(`Overall: ${allPassed ? '✅ PASSED' : '❌ FAILED'}`);
    console.log(`Passed: ${Object.values(results).filter(r => r.passed).length}/${Object.keys(results).length}`);

    return { allPassed, results, report };
  }

  generateComplianceReport(results, allPassed) {
    return {
      timestamp: new Date().toISOString(),
      overall: allPassed ? 'compliant' : 'non-compliant',
      standards: results,
      recommendations: this.generateRecommendations(results)
    };
  }

  generateRecommendations(results) {
    const recommendations = [];

    if (!results.environment?.passed) {
      recommendations.push('Fix environment setup issues before development');
    }

    if (!results.security?.passed) {
      recommendations.push('Address security vulnerabilities immediately');
    }

    if (!results.governance?.passed) {
      recommendations.push('Implement governance compliance requirements');
    }

    if (!results.testing?.passed) {
      recommendations.push('Improve test coverage and quality');
    }

    return recommendations;
  }
}

// Run compliance check
const verifier = new StandardsComplianceVerifier();
const compliance = await verifier.runFullComplianceCheck('./');
```

## Success Criteria

- [ ] Reference standards documentation reviewed
- [ ] Environment meets all requirements
- [ ] Code follows naming and structural standards
- [ ] Database interactions use secure patterns
- [ ] API endpoints follow RESTful design
- [ ] Security measures properly implemented
- [ ] Testing standards applied comprehensively
- [ ] Prompt keys validated for naming compliance
- [ ] Governance integration completed
- [ ] Full compliance verification passed

## Common Pitfalls

1. **Not Reviewing Reference Documentation** - Always check the comprehensive standards first
2. **Environment Setup Issues** - Verify environment before starting development
3. **Inconsistent Application** - Apply standards systematically across all code
4. **Missing Security Validation** - Security must be implemented at all levels
5. **Incomplete Testing** - Tests must cover all functionality and edge cases
6. **Invalid Prompt Keys** - Use validation tools to ensure proper naming
7. **Governance Non-Compliance** - Governance requirements are mandatory
8. **Skipping Compliance Checks** - Always run full verification before deployment

## Cross-References

### Primary Reference Documents
- **[Agent Coding Standards Reference](docs_construct_ai/codebase/coding-standards/0000_AGENT_CODING_STANDARDS.md)** - Complete standards documentation
- **[Agent Development Standards](docs_construct_ai/codebase/coding-standards/0000_AGENT_DEVELOPMENT_STANDARDS.md)** - Development workflow standards
- **[Code Standardization Master Plan](docs_construct_ai/codebase/coding-standards/0000_CODE_STANDARDIZATION_MASTER_PLAN.md)** - Overall standardization approach

### Related Skills
- `writing-plans` - Planning agent development
- `test-driven-development` - Testing approach for agents
- `verification-before-completion` - Quality assurance for agent development

### Related Agents
- `DevForge_AI_Team` - Agent development assistance
- `QualityForge_AI_Team` - Code quality verification
