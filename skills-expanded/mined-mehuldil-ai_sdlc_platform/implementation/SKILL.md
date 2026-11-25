# /project:implementation

**Interactive Development Guidance & Progress Tracking**

Works in: Cursor IDE chat + Claude Code + CLI

## Usage

```
/project:implementation AB#123
/project:implementation AB#123 --task=BKD-01
/project:implementation AB#123 --status=update
```

## What This Does

1. **Loads task** details and acceptance criteria
2. **Provides implementation guidance** (architecture, code patterns, examples)
3. **Generates code templates** (boilerplate, stubs)
4. **Tracks progress** during development (checkpoints)
5. **Validates completion** against AC
6. **Updates ADO task** status and progress

## Interactive Flow

```
User: /project:implementation AB#123 --task=BKD-01

Claude: 💻 Development Guidance & Progress

✅ TASK LOADED:
  Task: BKD-01 — Setup signup service (auth + phone validation)
  Story: Multi-language signup (AB#123)
  Estimate: 4 hours
  AC: 4 items (service setup, phone validation, error handling, logging)

📋 IMPLEMENTATION GUIDE:

1. SERVICE SETUP:
   • Create SignupService interface
   • Wire dependency injection (Spring Boot)
   • Configure Twilio client
   
   Code template:
   ```java
   @Service
   public class SignupService implements ISignupService {
       @Autowired private TwilioClient twilioClient;
       @Autowired private UserRepository userRepo;
       
       public SignupSession initiate(String phoneNumber, String language) {
           // TODO: Validate phone format
           // TODO: Create session record
           // TODO: Return session ID
       }
   }
   ```

2. PHONE VALIDATION:
   • Use libphonenumber library for international formats
   • Validate against country code
   • Check for existing user with phone
   
   Code template:
   ```java
   private void validatePhone(String phoneNumber) throws ValidationException {
       PhoneNumberUtil util = PhoneNumberUtil.getInstance();
       try {
           PhoneNumber number = util.parse(phoneNumber, "US");
           if (!util.isValidNumber(number)) {
               throw new ValidationException("Invalid phone format");
           }
       } catch (Exception e) {
           throw new ValidationException("Phone validation failed: " + e.getMessage());
       }
   }
   ```

3. ERROR HANDLING:
   • Define custom exceptions (PhoneValidationException, etc.)
   • Return meaningful error responses
   • Log errors for monitoring
   
   Code template:
   ```java
   @ExceptionHandler(PhoneValidationException.class)
   public ResponseEntity<ErrorResponse> handlePhoneError(
       PhoneValidationException ex, HttpServletRequest req) {
       ErrorResponse error = new ErrorResponse(
           "INVALID_PHONE", ex.getMessage(), req.getRequestURI());
       return ResponseEntity.badRequest().body(error);
   }
   ```

4. LOGGING:
   • Use SLF4J + Logback
   • Log important checkpoints (phone validation, session creation)
   • Avoid logging sensitive data (PII)
   
   Code template:
   ```java
   logger.info("Phone validation initiated for phone: REDACTED");
   logger.debug("Phone validation passed, creating session");
   logger.error("Phone validation failed: {}", ex.getMessage());
   ```

📊 PROGRESS TRACKING:

Checkpoint 1: Service setup + dependency injection
  [1] Done, proceed to checkpoint 2
  [2] Need help, show more detail
  [3] Skip checkpoint, move to next

User: [1]

✓ Checkpoint 1 complete.

Checkpoint 2: Phone validation logic + tests
  [1] Done, proceed to checkpoint 3
  [2] Need help
  [3] Skip

User: [1]

✓ Checkpoint 2 complete.

[Continue through all checkpoints...]

✅ TASK COMPLETION VALIDATION:

AC-01: Service interface created ✓
AC-02: Phone validation (international) ✓
AC-03: Error handling + custom exceptions ✓
AC-04: Logging (no PII) ✓

All AC met?
  [1] Yes, mark task complete
  [2] Review AC details
  [3] Some AC not complete yet

User: [1]

UPDATE ADO TASK?
  [1] Mark as Complete, move to In Review
  [2] Update progress (90%), leave In Progress
  [3] Save locally, don't update ADO
  [4] Cancel

User: [1]

✓ Task marked Complete in ADO
✓ Task moved to In Review
✓ Progress logged to .sdlc/memory/implementation-AB#123.md

NEXT STEP?
  [1] Start next task (BKD-02)
  [2] Create pull request for this task
  [3] Run unit tests
  [4] View overall sprint progress

User: [2]

✓ Ready to create PR? See `/project:code-review` next.
```

## CLI Mode

```bash
$ sdlc skill implementation AB#123 --task=BKD-01
$ sdlc skill implementation AB#123 --checkpoint=2
$ sdlc skill implementation AB#123 --status=update --progress=90%
```

## Outputs Generated

- **Code Templates**: Boilerplate with TODO markers
- **Implementation Guide**: Step-by-step instructions per AC
- **Progress Log**: Checkpoint tracking in .sdlc/memory/
- **ADO Update**: Task status + progress

## G6 Gate Clear Conditions

Gate G6 is CLEAR when:
- All AC implemented and tested
- Code merged to feature branch (all checks passing)
- Coverage >80% on modified files
- Code review comments addressed
- Task marked Complete in ADO

## Next Commands

- `/project:code-review AB#123` - Code review + PR handling
- `/project:test-design AB#123` - QA test design
- `/project:performance-testing AB#123` - Performance validation

---

## Model & Token Budget
- **Model Tier:** Sonnet (code generation + guidance)
- Input: ~1.5K tokens (task + AC)
- Output: ~2K tokens (templates + guide + progress)

