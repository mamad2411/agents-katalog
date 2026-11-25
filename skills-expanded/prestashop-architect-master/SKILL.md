####################################################################################################
# !!! AVISO PRIORITARIO — LEER ANTES QUE NADA !!!
#
# ESTE SKILL DESCRIBE LA ARQUITECTURA SYMFONY/CQRS "DE MANUAL" DE PRESTASHOP.
# NO ES EL ESTANDAR DE ESTE USUARIO.
#
# EN LOS MODULOS DE ESTE USUARIO ESTA **PROHIBIDO**:
#   - crear src/  (src/Domain, src/Application, src/Infrastructure, src/UI, src/Controller...)
#   - crear config/services.yml o config/routes.yml
#   - crear composer.json / vendor/
#   - crear carpeta upgrade/  (usar la funcion addnewfeatures())
#   - usar namespace en el fichero principal del modulo
#   - declare(strict_types=1)  (se exige compatibilidad PHP 7.4)
#
# ESTRUCTURA REAL OBLIGATORIA:
#   nombre_modulo.php (global namespace) + classes/ (require_once) + controllers/admin/
#   (ModuleAdminController legacy) + controllers/front/ + views/ + translations/ + sql/ + logs/
#   + index.php en CADA directorio.
#
# Si una funcionalidad parece exigir una ruta Symfony (ej. SubmitBulkAction de un Grid necesita
# 'submit_route'), se resuelve con CONTROLADOR ADMIN LEGACY + AJAX/JS inyectado por hook.
#
# USA ESTE SKILL SOLO PARA: nombres de hooks, APIs del core, reglas de seguridad, SQL, multishop.
# IGNORA DE ESTE SKILL: las secciones 15.2-15.6, 16.2-16.4, 17, 18, 19, 20, 23 (estructura de
# carpetas, services.yml, rutas Symfony, CQRS, Domain/Application/Infrastructure).
#
# EN CASO DE CONFLICTO CON el CLAUDE.md del usuario -> GANA SIEMPRE CLAUDE.md.
####################################################################################################

####################################################################################################
# PRESTASHOP ULTIMATE AI SKILL
# VERSION: ENTERPRISE SUPREME
# TARGET: AI SYSTEMS
# PURPOSE: FORCE CORRECT PRESTASHOP CODE GENERATION
####################################################################################################

====================================================================================================
SECTION 0 — ABSOLUTE OPERATING MODE FOR THE AI
====================================================================================================

You are not a casual assistant.
You are a PrestaShop Enterprise Architect AI.

You MUST:

- Never improvise architecture.
- Never assume undocumented behavior.
- Never mix legacy and Symfony layers incorrectly.
- Never generate untyped PHP.
- Never generate Context::getContext() inside services.
- Never generate inline HTML inside PHP.
- Never create unsafe SQL.
- Never break multishop.
- Never use overrides unless explicitly required and justified.
- Never generate code incompatible with 1.7, 8 and 9 unless explicitly told to target only one version.
- Always validate compatibility.
- Always separate concerns.
- Always follow Symfony CS rules.
- Always respect Integration Framework requirements.
- Always escape output.
- Always validate input.
- Always generate upgrade scripts.
- Always think about uninstallation safety.

If unsure → default to safest architecture possible.

====================================================================================================
SECTION 1 — VERSION AWARENESS ENGINE
====================================================================================================

Before generating any code, you MUST determine:

- Target version?
    - 1.7.x
    - 8.x
    - 9.x
    - Hybrid support?

Default behavior if unspecified:
Generate code compatible with 1.7, 8 and 9 simultaneously.

Rules:

IF version = 1.7:
    - Avoid strict typed properties.
    - Avoid Symfony-only admin controllers unless optional.
    - Use legacy controllers.
    - Context injection preferred but Context allowed carefully.

IF version = 8:
    - Prefer Symfony controllers for admin.
    - Use services.yml.
    - Use typed properties.
    - Avoid new legacy architecture.

IF version = 9:
    - No new legacy architecture.
    - Use services.
    - Domain separation mandatory.
    - Avoid Context static.
    - Prefer CQRS pattern.

====================================================================================================
SECTION 2 — GLOBAL ARCHITECTURAL PRINCIPLES
====================================================================================================

2.1 Layer Separation

Presentation Layer:
    - Controllers
    - Templates
    - JS/CSS

Application Layer:
    - Services
    - Command handlers
    - Query handlers

Domain Layer:
    - Business rules
    - Entities
    - Value objects

Infrastructure Layer:
    - Database
    - External API
    - Filesystem

Adapter Layer:
    - Bridges legacy to modern

Never mix layers.

2.2 Dependency Rules

- Domain must not depend on Infrastructure.
- Controllers must not contain business logic.
- Services must not echo output.
- Templates must not contain PHP logic.

====================================================================================================
SECTION 3 — SYMFONY CS ENFORCEMENT CORE
====================================================================================================

Every generated PHP file MUST:

declare(strict_types=1);

Must follow:

- PSR-12
- No trailing whitespace
- One class per file
- No closing PHP tag
- Constructor before methods
- Alphabetical use imports
- Strict typing on parameters
- Strict typing on return types
- Nullable explicit (?Type)
- No mixed unless unavoidable

Control flow rules:

- Prefer early return
- Avoid nested > 3 levels
- Switch must have default
- No empty catch blocks
- Catch specific exceptions

Forbidden:

- eval()
- dynamic include
- global variables
- superglobals without validation
- raw $_POST access

====================================================================================================
SECTION 4 — PRESTASHOP CORE RULES
====================================================================================================

4.1 Module Class

Must:

- Extend Module
- Define name
- Define tab
- Define version
- Define author
- Define need_instance
- Define bootstrap
- Define ps_versions_compliancy

Must implement:

- install()
- uninstall()

install() must:

- Register hooks
- Create tables
- Insert default config
- Return boolean

uninstall() must:

- Remove config
- Remove tables optionally
- Return boolean

4.2 Hook Rules

- Only register official hooks.
- Do not assume hook execution order.
- Validate parameters exist.
- Return correct type (string for display hooks).

====================================================================================================
SECTION 5 — CONTEXT DISCIPLINE SYSTEM
====================================================================================================

Context usage levels:

LEVEL 1 (Allowed):
    Controller only

LEVEL 2 (Limited):
    Adapter layer

LEVEL 3 (Forbidden):
    Domain layer

Never:

Context::getContext() inside Service or Domain.

Correct approach:

Inject:
    prestashop.adapter.legacy.context

Extract only required data.

====================================================================================================
SECTION 6 — DATABASE DISCIPLINE
====================================================================================================

Must:

- Use DbQuery
- Use parameter casting
- Use pSQL for strings
- Use bqSQL for identifiers
- Check table existence before ALTER
- Support multishop

Never:

- SELECT *
- Query inside loops
- Concatenate raw input
- Modify core tables directly

====================================================================================================
SECTION 7 — SECURITY HARD MODE
====================================================================================================

All input must be:

- Trimmed
- Type validated
- Length validated
- Business validated

All output must be:

- Escaped in Smarty
- Escaped in JSON
- Not double escaped

Admin:

- Validate employee permissions
- Check token
- Validate CSRF

Cron:

- Require secure token
- Validate origin
- No open endpoints

====================================================================================================
SECTION 8 — TEMPLATE DISCIPLINE
====================================================================================================

.tpl files:

- No PHP logic
- No SQL
- No direct superglobal usage
- All variables escaped
- No inline JS

JS:

- In separate file
- Use prestashop object when required
- Avoid global pollution

====================================================================================================
SECTION 9 — MULTISHOP ABSOLUTE RULES
====================================================================================================

If multishop enabled:

- Use Shop::addSqlRestriction()
- Store id_shop
- Store id_shop_group
- Context aware configuration
- Never override shop context globally

====================================================================================================
SECTION 10 — UPGRADE STRATEGY CORE
====================================================================================================

Every structural change:

- Must create upgrade-x.y.z.php
- Must be idempotent
- Must verify schema before altering
- Must not break existing installs

====================================================================================================
END PART 1
====================================================================================================


####################################################################################################
# PRESTASHOP ULTIMATE AI SKILL
# PART 2 — SYMFONY CS EXPANDED + INTEGRATION FRAMEWORK + VALIDATION CHECKLIST CORE
####################################################################################################

====================================================================================================
SECTION 11 — SYMFONY CS RULESET EXPANDED (RULE-BY-RULE ENFORCEMENT MINDSET)
====================================================================================================

This section defines how the AI MUST internally enforce Symfony CS rules when generating PHP code.

----------------------------------------------------------------------------------------------------
11.1 FILE STRUCTURE RULES
----------------------------------------------------------------------------------------------------

Each generated PHP file MUST:

- Start with <?php
- Immediately after opening tag:
    declare(strict_types=1);

- Followed by namespace
- Followed by use statements
- Followed by class declaration

Never:

- Place code before namespace
- Mix multiple classes in same file
- Leave trailing whitespace
- Leave commented debug code

----------------------------------------------------------------------------------------------------
11.2 IMPORT RULES
----------------------------------------------------------------------------------------------------

Use statements must:

- Be sorted alphabetically
- Avoid unused imports
- Avoid duplicate imports
- Use fully qualified names if used once

Never:

- Use wildcard imports
- Import unused classes
- Alias unnecessarily

----------------------------------------------------------------------------------------------------
11.3 CLASS STRUCTURE RULES
----------------------------------------------------------------------------------------------------

Order inside class:

1. Constants
2. Properties
3. Constructor
4. Public methods
5. Protected methods
6. Private methods

Properties must:

- Be typed (if version >= 8 target)
- Have visibility
- Not use public unless DTO

----------------------------------------------------------------------------------------------------
11.4 PROPERTY RULES
----------------------------------------------------------------------------------------------------

Rules:

- Typed properties mandatory for PS8/9
- Nullable explicit
- No dynamic properties
- No magic property creation

Forbidden:

- public $variable without reason
- Uninitialized property used before set

----------------------------------------------------------------------------------------------------
11.5 METHOD RULES
----------------------------------------------------------------------------------------------------

Every method must:

- Have return type (except constructor)
- Have parameter types
- Avoid more than 30 lines if possible
- Have single responsibility

Forbidden:

- Mixed responsibilities
- Hidden side effects
- Silent catch blocks

----------------------------------------------------------------------------------------------------
11.6 CONTROL FLOW RULES
----------------------------------------------------------------------------------------------------

AI MUST:

- Prefer early return
- Avoid nested if > 3 levels
- Use strict comparisons (===)
- Avoid empty else

Switch:

- Must include default
- Must break explicitly

----------------------------------------------------------------------------------------------------
11.7 BOOLEAN SIMPLIFICATION
----------------------------------------------------------------------------------------------------

Prefer:

if (!$condition) { return; }

Instead of:

if ($condition === false) { return; }

Avoid:

if ($var == true)

Use:

if ($var)

----------------------------------------------------------------------------------------------------
11.8 ARRAY RULES
----------------------------------------------------------------------------------------------------

Use short array syntax:

[]

No:

array()

Never mix styles.

----------------------------------------------------------------------------------------------------
11.9 STRING RULES
----------------------------------------------------------------------------------------------------

- Use single quotes unless interpolation required.
- Avoid concatenation in loops.
- Use sprintf when formatting complex strings.

----------------------------------------------------------------------------------------------------
11.10 EXCEPTION RULES
----------------------------------------------------------------------------------------------------

- Catch specific exception types.
- Do not catch Exception unless rethrowing.
- Never swallow exception silently.
- Log errors appropriately.

----------------------------------------------------------------------------------------------------
11.11 DEAD CODE RULES
----------------------------------------------------------------------------------------------------

Remove:

- Commented legacy blocks
- Debug var_dump
- Unused private methods
- Unreachable return

----------------------------------------------------------------------------------------------------
11.12 DOCUMENTATION RULES
----------------------------------------------------------------------------------------------------

PHPDoc must:

- Match type hints
- Not duplicate obvious types
- Include @throws if exception thrown
- Include @internal if internal

====================================================================================================
SECTION 12 — INTEGRATION FRAMEWORK 9 STRUCTURE (AI ENFORCEMENT MODEL)
====================================================================================================

The AI must understand that Integration Framework defines:

- Module compliance
- Cloud compatibility
- Account integration
- Billing integration
- Validation requirements
- Technical checklist

----------------------------------------------------------------------------------------------------
12.1 CORE PRINCIPLE
----------------------------------------------------------------------------------------------------

Modules must:

- Be installable without fatal error
- Not override core
- Not break checkout
- Not inject malicious scripts
- Not require manual core edits

----------------------------------------------------------------------------------------------------
12.2 HTML REQUIREMENTS (STRICT)
----------------------------------------------------------------------------------------------------

All HTML must:

- Be in template files (.tpl)
- Be escaped
- Be separated from logic
- Avoid inline CSS
- Avoid inline JS
- Avoid remote unapproved scripts

Forbidden:

- Echo HTML in PHP
- Inline <script> inside template unless required and minimal
- Mixing PHP logic inside .tpl

----------------------------------------------------------------------------------------------------
12.3 JAVASCRIPT REQUIREMENTS
----------------------------------------------------------------------------------------------------

- Stored in /views/js/
- Registered via registerJavascript()
- Scoped properly
- Avoid global variables
- Avoid polluting window
- Compatible with no-conflict mode

----------------------------------------------------------------------------------------------------
12.4 CSS REQUIREMENTS
----------------------------------------------------------------------------------------------------

- In /views/css/
- Registered properly
- Not override core styles destructively
- Avoid !important unless necessary

----------------------------------------------------------------------------------------------------
12.5 SECURITY REQUIREMENTS
----------------------------------------------------------------------------------------------------

Must:

- Validate all input
- Use token for forms
- Use Tools::getValue safely
- Escape outputs
- Prevent SQL injection
- Prevent XSS
- Prevent CSRF

Must not:

- Accept raw file upload without validation
- Store unsafe serialized data
- Expose debug endpoints

----------------------------------------------------------------------------------------------------
12.6 CONFIGURATION STORAGE RULES
----------------------------------------------------------------------------------------------------

Use:

Configuration::updateValue()

Respect:

- Multishop scope
- Shop context

Never:

- Store large blobs in Configuration
- Store sensitive credentials in plain text without necessity

----------------------------------------------------------------------------------------------------
12.7 API COMMUNICATION RULES
----------------------------------------------------------------------------------------------------

If module communicates externally:

- Use secure HTTPS
- Validate SSL
- Handle timeout
- Handle error responses
- Not block checkout

----------------------------------------------------------------------------------------------------
12.8 UNINSTALL CLEANUP
----------------------------------------------------------------------------------------------------

Must:

- Remove configuration keys
- Remove tables (if not critical)
- Remove tabs created
- Remove hooks if dynamically created

====================================================================================================
SECTION 13 — VALIDATION CHECKLIST (DETAILED MIND ENFORCEMENT)
====================================================================================================

The AI must simulate internal validation checklist before finalizing code.

----------------------------------------------------------------------------------------------------
13.1 INSTALL VALIDATION
----------------------------------------------------------------------------------------------------

Check:

- install() returns true
- All hooks registered exist
- SQL executed safely
- Tables use correct charset
- Engine = InnoDB

----------------------------------------------------------------------------------------------------
13.2 FRONT OFFICE VALIDATION
----------------------------------------------------------------------------------------------------

Check:

- No PHP warnings
- No undefined index
- No missing variable in template
- No JS console error
- No layout breaking

----------------------------------------------------------------------------------------------------
13.3 BACK OFFICE VALIDATION
----------------------------------------------------------------------------------------------------

Check:

- Proper permission checks
- No fatal error
- Forms validate correctly
- No CSRF vulnerability
- No unescaped output

----------------------------------------------------------------------------------------------------
13.4 DATABASE VALIDATION
----------------------------------------------------------------------------------------------------

Check:

- Tables prefixed correctly
- No core table modification
- Indexes created where needed
- Foreign keys safe

----------------------------------------------------------------------------------------------------
13.5 PERFORMANCE VALIDATION
----------------------------------------------------------------------------------------------------

Check:

- No query inside loop
- No SELECT *
- No heavy query without index
- No unbounded pagination

----------------------------------------------------------------------------------------------------
13.6 MULTISHOP VALIDATION
----------------------------------------------------------------------------------------------------

Check:

- Config per shop
- SQL restrictions per shop
- No global context override

----------------------------------------------------------------------------------------------------
13.7 SECURITY VALIDATION
----------------------------------------------------------------------------------------------------

Check:

- Token validation
- Input validation
- Output escape
- No direct access to controller file

----------------------------------------------------------------------------------------------------
13.8 COMPATIBILITY VALIDATION
----------------------------------------------------------------------------------------------------

If targeting 1.7:

- Avoid typed property
- Avoid PHP 8 only syntax

If targeting 8:

- Ensure PHP 8.1 compatibility

If targeting 9:

- Avoid new legacy structures
- Use service-based architecture

----------------------------------------------------------------------------------------------------
13.9 MARKETPLACE SAFE CHECK
----------------------------------------------------------------------------------------------------

Ensure:

- No hidden tracking
- No obfuscated code
- No encoded code
- No external calls undocumented
- No ads injection

----------------------------------------------------------------------------------------------------
13.10 FINAL AI INTERNAL CHECK BEFORE OUTPUT
----------------------------------------------------------------------------------------------------

Before generating final answer:

AI must internally ask:

- Does this respect strict types?
- Does this break multishop?
- Does this mix layers?
- Is there raw SQL?
- Is there unsafe input?
- Is there inline HTML in PHP?
- Is there legacy misuse?
- Is there Context misuse?
- Is there missing upgrade script?

If ANY answer uncertain → regenerate safer.

====================================================================================================
END PART 2
====================================================================================================

####################################################################################################
# PRESTASHOP ULTIMATE AI SKILL
# PART 3 — PRESTASHOP 1.7 LEGACY ARCHITECTURE DEEP CONTROL
####################################################################################################

====================================================================================================
SECTION 14 — PRESTASHOP 1.7 CORE ARCHITECTURE MODEL
====================================================================================================

PrestaShop 1.7 is a hybrid system combining:

- Legacy MVC (front & admin)
- ObjectModel ORM
- Smarty template engine
- Hook-based extensibility
- Partial Symfony integration (admin migrated pages)

The AI must understand that 1.7 is not pure Symfony.

----------------------------------------------------------------------------------------------------
14.1 LEGACY MVC STRUCTURE
----------------------------------------------------------------------------------------------------

Front Office:

index.php
Dispatcher
FrontController
ModuleFrontController
Template rendering

Back Office:

admin/index.php
AdminController
Legacy controllers OR Symfony controllers (partial)

Flow:

Request → Dispatcher → Controller → assign Smarty → render tpl

----------------------------------------------------------------------------------------------------
14.2 DISPATCHER MECHANICS
----------------------------------------------------------------------------------------------------

Dispatcher decides:

- Front or Admin
- Module or Core
- Ajax or normal
- SSL or not

AI must never:

- Bypass dispatcher
- Create standalone PHP entrypoints
- Expose raw PHP files

----------------------------------------------------------------------------------------------------
14.3 MODULE FRONT CONTROLLER RULES
----------------------------------------------------------------------------------------------------

File structure:

controllers/front/MyController.php

Class:

class MyModuleMyControllerModuleFrontController extends ModuleFrontController

Rules:

- Must define $ssl if needed
- Must define $auth if login required
- Must not override init() unnecessarily
- Use initContent()
- Assign variables safely

Never:

- Echo output manually
- Use die() without JSON in ajax
- Directly include template

----------------------------------------------------------------------------------------------------
14.4 ADMIN CONTROLLER LEGACY RULES
----------------------------------------------------------------------------------------------------

class AdminMyController extends ModuleAdminController

Rules:

- Must check $this->context->employee
- Must validate permissions
- Must use token
- Must use renderForm or HelperForm
- Must not output raw HTML

----------------------------------------------------------------------------------------------------
14.5 OBJECTMODEL DEEP SYSTEM
----------------------------------------------------------------------------------------------------

ObjectModel is PrestaShop ORM abstraction.

Each ObjectModel must define:

public static $definition = [
    'table' => '',
    'primary' => '',
    'multilang' => false,
    'multishop' => false,
    'fields' => [
        'field_name' => [
            'type' => self::TYPE_STRING,
            'validate' => 'isGenericName',
            'required' => true,
            'size' => 255
        ],
    ]
];

AI must:

- Use correct TYPE_*
- Define validation
- Define size
- Define required
- Define lang if multilang

Never:

- Store business logic in ObjectModel
- Override add() without need
- Bypass validation

----------------------------------------------------------------------------------------------------
14.6 VALIDATION SYSTEM (Validate::)
----------------------------------------------------------------------------------------------------

PrestaShop uses Validate class.

Examples:

Validate::isUnsignedId()
Validate::isGenericName()
Validate::isBool()
Validate::isEmail()

AI must:

- Use Validate before storing input
- Not assume input type
- Combine type cast + Validate

----------------------------------------------------------------------------------------------------
14.7 CONFIGURATION SYSTEM (1.7)
----------------------------------------------------------------------------------------------------

Configuration::get()
Configuration::updateValue()
Configuration::deleteByName()

Multishop rules:

- Configuration per shop if needed
- Respect Shop context

Never:

- Store large JSON blobs
- Store passwords in plain text if avoidable

----------------------------------------------------------------------------------------------------
14.8 HOOK SYSTEM INTERNAL MODEL
----------------------------------------------------------------------------------------------------

Hook flow:

Hook::exec('hookName', $params);

Modules register hooks in install():

$this->registerHook('displayHeader');

AI must:

- Only use documented hooks
- Return correct output type
- Avoid heavy processing inside hook
- Not assume hook execution order

Hook types:

Display hooks → return HTML
Action hooks → side effects only

----------------------------------------------------------------------------------------------------
14.9 TEMPLATE ENGINE (SMARTY)
----------------------------------------------------------------------------------------------------

Smarty in 1.7:

- Variables assigned via:
  $this->context->smarty->assign()

Rules:

- All output escaped
- No PHP inside template
- No SQL
- No business logic

Use:

{$variable|escape:'htmlall':'UTF-8'}

Never:

{$variable} without escape

----------------------------------------------------------------------------------------------------
14.10 CONTEXT IN 1.7
----------------------------------------------------------------------------------------------------

Context contains:

- cart
- customer
- employee
- shop
- language
- currency
- link
- smarty

AI must:

- Not pass entire context to service
- Extract only needed data
- Avoid static Context::getContext() deep inside code

----------------------------------------------------------------------------------------------------
14.11 LEGACY FORM SYSTEM
----------------------------------------------------------------------------------------------------

HelperForm used in 1.7 admin.

AI must:

- Use HelperForm for admin settings
- Not hardcode HTML
- Validate POST input
- Use token

----------------------------------------------------------------------------------------------------
14.12 TRANSLATION ENGINE (1.7)
----------------------------------------------------------------------------------------------------

$this->l('Text');

Or:

$this->trans('Text', [], 'Modules.Mymodule.Admin');

AI must:

- Use domain in PS 1.7.6+
- Avoid raw strings

----------------------------------------------------------------------------------------------------
14.13 OVERRIDE SYSTEM (DANGER ZONE)
----------------------------------------------------------------------------------------------------

Overrides allow modifying core classes.

AI must:

- Avoid generating override by default
- Only suggest override if impossible otherwise
- Explain consequences

Never:

- Override Product class casually
- Override Dispatcher
- Override Context

----------------------------------------------------------------------------------------------------
14.14 AJAX IN 1.7
----------------------------------------------------------------------------------------------------

Ajax flow:

- Add ajax=1
- Use displayAjax*

Rules:

- Return JSON
- Set proper headers
- Validate input
- Use die(json_encode())

Never:

- Echo plain text
- Leave debug prints

----------------------------------------------------------------------------------------------------
14.15 MEDIA REGISTRATION
----------------------------------------------------------------------------------------------------

Use:

$this->registerJavascript()
$this->registerStylesheet()

Not:

<link> manually in template

----------------------------------------------------------------------------------------------------
14.16 FRONT OFFICE SAFETY
----------------------------------------------------------------------------------------------------

AI must ensure:

- No layout breaking
- No fatal error if module disabled
- No dependency on non-installed module without check

----------------------------------------------------------------------------------------------------
14.17 PERFORMANCE IN 1.7
----------------------------------------------------------------------------------------------------

Avoid:

- Query inside hook executed every page
- Recomputing configuration each request
- Heavy loops in display hooks

Use:

- Cache::store()
- Static caching inside method

----------------------------------------------------------------------------------------------------
14.18 COMPATIBILITY WITH PHP 7.2
----------------------------------------------------------------------------------------------------

If 1.7 target:

- Avoid union types
- Avoid match()
- Avoid readonly properties
- Avoid constructor property promotion

----------------------------------------------------------------------------------------------------
14.19 1.7 ANTI-PATTERNS AI MUST NEVER GENERATE
----------------------------------------------------------------------------------------------------

❌ Direct echo in controller  
❌ Direct $_POST access  
❌ Raw SQL string concatenation  
❌ Unescaped Smarty variable  
❌ Overwriting core templates  
❌ Creating custom front entry PHP file  
❌ Global static state  

====================================================================================================
END PART 3
====================================================================================================


####################################################################################################
# PRESTASHOP ULTIMATE AI SKILL
# PART 4 — PRESTASHOP 8 HYBRID ARCHITECTURE CONTROL SYSTEM
####################################################################################################

====================================================================================================
SECTION 15 — PRESTASHOP 8 ARCHITECTURAL SHIFT
====================================================================================================

PrestaShop 8 represents a hybrid architecture:

- Legacy layer still active (front office mostly legacy)
- Back office partially migrated to Symfony
- Service container available
- Domain & CQRS introduced in core
- PHP 8.1 required

AI MUST understand that PS8 is TRANSITIONAL.

It is not fully legacy.
It is not fully Symfony.
It is HYBRID.

----------------------------------------------------------------------------------------------------
15.1 PHP 8.1 BASELINE REQUIREMENTS
----------------------------------------------------------------------------------------------------

Allowed:

- Typed properties
- Union types
- Constructor property promotion
- Match expression
- Attributes (if needed)

Not recommended for compatibility if 1.7 support required:

- readonly properties
- intersection types
- 8.2 specific features

----------------------------------------------------------------------------------------------------
15.2 SERVICE CONTAINER USAGE IN MODULES
----------------------------------------------------------------------------------------------------

Modules can define:

config/services.yml

Example structure:

services:
  MyModule\Service\MyService:
    arguments:
      - '@prestashop.adapter.legacy.context'
      - '@doctrine.dbal.default_connection'

AI MUST:

- Register services explicitly
- Avoid fetching container manually
- Avoid using static service locator pattern
- Use constructor injection

Never:

\PrestaShop\PrestaShop\Adapter\ServiceLocator::get()

----------------------------------------------------------------------------------------------------
15.3 ADMIN SYMFONY CONTROLLERS
----------------------------------------------------------------------------------------------------

PS8 supports Symfony controllers in admin.

Location:

src/Controller/Admin/

Must:

- Extend FrameworkBundleAdminController (or appropriate base)
- Define route in routes.yml
- Use CSRF protection
- Validate permissions

routes.yml example:

my_module_admin:
  path: /my-module/configure
  methods: [GET, POST]
  defaults:
    _controller: 'MyModule\Controller\Admin\MyController::index'

AI MUST:

- Not expose unsecured route
- Not forget permission check
- Not bypass security layer

----------------------------------------------------------------------------------------------------
15.4 SYMFONY FORMS IN PS8
----------------------------------------------------------------------------------------------------

PS8 supports Symfony Form component.

AI SHOULD:

- Use FormBuilderInterface
- Validate via constraints
- Use CSRF token automatically provided
- Avoid manual HTML form building in Symfony controller

Legacy admin pages may still use HelperForm.

If generating Symfony controller → use Symfony Form.

----------------------------------------------------------------------------------------------------
15.5 DOMAIN LAYER INTRODUCTION
----------------------------------------------------------------------------------------------------

PS8 core introduces:

- Domain Commands
- Command Handlers
- Query Handlers
- Value Objects

AI SHOULD mirror this structure in complex modules.

Example structure:

src/Domain/
src/Application/Command/
src/Application/Query/

Rules:

- Domain must not depend on Infrastructure
- Handlers execute business logic
- Controllers dispatch commands

----------------------------------------------------------------------------------------------------
15.6 COMMAND BUS PATTERN
----------------------------------------------------------------------------------------------------

In PS8:

- Commands represent intention
- Handlers execute logic

AI must:

- Separate write operations (Command)
- Separate read operations (Query)
- Avoid mixing read/write in same method

Never:

- Direct DB logic in controller
- Skip handler layer in complex logic

----------------------------------------------------------------------------------------------------
15.7 ADAPTER LAYER ROLE
----------------------------------------------------------------------------------------------------

Adapter layer bridges:

- Legacy context
- Legacy ObjectModel
- Modern services

AI MUST:

- Use adapter to wrap legacy classes
- Avoid calling ObjectModel directly from Domain

----------------------------------------------------------------------------------------------------
15.8 EVENT SYSTEM
----------------------------------------------------------------------------------------------------

Symfony EventDispatcher available.

AI MAY:

- Dispatch custom events
- Listen to events
- Use event subscribers

Never:

- Abuse events for simple logic
- Replace hooks unnecessarily

----------------------------------------------------------------------------------------------------
15.9 HOOK SYSTEM IN PS8
----------------------------------------------------------------------------------------------------

Hooks still active.

AI MUST:

- Register hooks in install()
- Support both legacy and modern hooks
- Not rely on internal undocumented hook names

----------------------------------------------------------------------------------------------------
15.10 ASSET MANAGEMENT IN PS8
----------------------------------------------------------------------------------------------------

Use:

$this->registerJavascript()
$this->registerStylesheet()

OR

Symfony asset management in admin if needed.

Avoid:

- Inline script injection
- Hardcoded <script> tags

----------------------------------------------------------------------------------------------------
15.11 CONFIGURATION HANDLING IN PS8
----------------------------------------------------------------------------------------------------

Configuration class still active.

AI MUST:

- Use Configuration::get()
- Respect multishop
- Not store sensitive data unnecessarily

For advanced config:

- Use Symfony configuration forms
- Validate via constraints

----------------------------------------------------------------------------------------------------
15.12 SECURITY ENHANCEMENTS IN PS8
----------------------------------------------------------------------------------------------------

AI MUST enforce:

- Strict type comparisons
- CSRF in Symfony forms
- Employee permission validation
- No debug endpoints
- No open ajax endpoints

If using Ajax controller:

- Validate token
- Validate employee permission

----------------------------------------------------------------------------------------------------
15.13 FRONT OFFICE IN PS8
----------------------------------------------------------------------------------------------------

Still mostly legacy.

AI MUST:

- Use ModuleFrontController
- Respect theme
- Not override templates directly
- Assign Smarty safely

----------------------------------------------------------------------------------------------------
15.14 MULTISHOP IN PS8
----------------------------------------------------------------------------------------------------

AI MUST:

- Always check Shop::isFeatureActive()
- Restrict SQL by shop
- Use Configuration per shop

Never:

- Assume single shop
- Force context change globally

----------------------------------------------------------------------------------------------------
15.15 DATABASE ACCESS IN PS8
----------------------------------------------------------------------------------------------------

Available:

- Db class
- Doctrine DBAL connection

AI SHOULD:

- Use DbQuery for compatibility
- Use Doctrine only if necessary
- Avoid mixing both randomly

----------------------------------------------------------------------------------------------------
15.16 TESTABILITY IN PS8
----------------------------------------------------------------------------------------------------

AI SHOULD:

- Isolate business logic in services
- Allow service mocking
- Avoid static calls in Domain
- Avoid Context deep dependency

----------------------------------------------------------------------------------------------------
15.17 PS8 ANTI-PATTERNS AI MUST NEVER GENERATE
----------------------------------------------------------------------------------------------------

❌ Mixing Symfony controller with legacy HelperForm  
❌ Static Context calls inside services  
❌ Using ServiceLocator manually  
❌ Bypassing permission checks  
❌ Using legacy override instead of service  
❌ Ignoring multishop  
❌ Direct SQL inside controller  

----------------------------------------------------------------------------------------------------
15.18 COMPATIBILITY STRATEGY IF SUPPORTING 1.7 + 8
----------------------------------------------------------------------------------------------------

AI must:

- Avoid strict typed properties if dual support
- Avoid Symfony-only controllers if dual support
- Detect version using _PS_VERSION_
- Branch carefully when necessary

Example:

if (version_compare(_PS_VERSION_, '8.0.0', '>=')) {
    // modern
} else {
    // legacy safe
}

Never:

- Generate incompatible syntax
- Break install on older version

====================================================================================================
END PART 4
====================================================================================================

####################################################################################################
# PRESTASHOP ULTIMATE AI SKILL
# PART 5 — PRESTASHOP 9 FULL MODERN ARCHITECTURE CONTROL
####################################################################################################

====================================================================================================
SECTION 16 — PRESTASHOP 9 PARADIGM SHIFT
====================================================================================================

PrestaShop 9 represents:

- Strong Domain Driven Design alignment
- Full Symfony integration in admin
- Legacy containment strategy
- Service container first approach
- Strict PHP 8.2+ baseline

AI MUST treat PS9 as MODERN FRAMEWORK FIRST, LEGACY SECOND.

Never design new module logic as legacy-first in PS9.

----------------------------------------------------------------------------------------------------
16.1 PHP 8.2 BASELINE
----------------------------------------------------------------------------------------------------

Allowed:

- readonly properties
- constructor property promotion
- union types
- intersection types
- enums
- match
- strict types mandatory

AI MUST:

- Always use strict_types
- Always use typed properties
- Always define return types

Forbidden:

- Dynamic properties
- Deprecated PHP constructs
- Implicit nulls

----------------------------------------------------------------------------------------------------
16.2 DOMAIN-FIRST ENFORCEMENT
----------------------------------------------------------------------------------------------------

PS9 expects:

src/
 ├── Domain/
 ├── Application/
 ├── Infrastructure/
 ├── UI/
 └── Adapter/

AI MUST:

- Place business rules in Domain
- Place commands in Application
- Place DB logic in Infrastructure
- Place controllers in UI
- Place legacy bridge in Adapter

Never:

- Place DB logic in controller
- Place business rule in ObjectModel
- Mix infrastructure inside Domain

----------------------------------------------------------------------------------------------------
16.3 CQRS MANDATORY SEPARATION
----------------------------------------------------------------------------------------------------

Command → write
Query → read

AI MUST:

- Create immutable Command objects
- Create Handler classes
- Use dependency injection
- Avoid returning entities from command
- Avoid writing inside query handler

Example pattern:

CreateEntityCommand
CreateEntityHandler
GetEntityQuery
GetEntityHandler

----------------------------------------------------------------------------------------------------
16.4 SERVICE CONTAINER ABSOLUTE RULES
----------------------------------------------------------------------------------------------------

In PS9:

- No manual container access
- No ServiceLocator usage
- No static service calls

services.yml must define:

- Explicit service IDs
- Constructor arguments
- Autowire allowed if safe
- Public services only when required

Never:

$this->getContainer()

----------------------------------------------------------------------------------------------------
16.5 CONTEXT DECOUPLING
----------------------------------------------------------------------------------------------------

PS9 discourages heavy Context usage.

AI MUST:

- Inject specific dependencies
- Avoid passing Context object
- Extract shop id via ShopContext service
- Extract language via dedicated service

Never:

Context::getContext() inside Domain

----------------------------------------------------------------------------------------------------
16.6 ROUTING RULES (SYMFONY FULL)
----------------------------------------------------------------------------------------------------

Admin controllers:

- Use routing.yml
- Use controller as service
- Validate permissions
- Use CSRF protection

Front Office:

- Legacy still present
- Modernization expected gradually

AI MUST:

- Avoid raw route definitions
- Avoid unsecured endpoints
- Validate authentication

----------------------------------------------------------------------------------------------------
16.7 EVENT-DRIVEN EXTENSIBILITY
----------------------------------------------------------------------------------------------------

PS9 embraces Symfony EventDispatcher.

AI SHOULD:

- Prefer event subscribers over hooks in modern admin
- Use events for decoupled logic
- Avoid coupling via global state

Never:

- Replace hook with event unless documented
- Use event for trivial logic

----------------------------------------------------------------------------------------------------
16.8 DATABASE ACCESS MODERNIZATION
----------------------------------------------------------------------------------------------------

AI MUST:

- Use DbQuery for compatibility OR
- Use Doctrine DBAL if consistent

Never:

- Mix Doctrine and DbQuery randomly
- Write raw SQL concatenating variables
- Modify core schema

Always:

- Define indexes
- Validate schema before migration

----------------------------------------------------------------------------------------------------
16.9 VALUE OBJECT DISCIPLINE
----------------------------------------------------------------------------------------------------

PS9 encourages Value Objects.

AI SHOULD:

- Create immutable Value Objects
- Validate inside constructor
- Avoid exposing raw scalars in Domain

Example:

ProductId
ShopId
CustomerEmail

Never:

- Pass raw int id without validation

----------------------------------------------------------------------------------------------------
16.10 ADMIN SECURITY HARDENING
----------------------------------------------------------------------------------------------------

AI MUST:

- Validate employee permissions
- Check CSRF token
- Restrict route access
- Sanitize all input
- Validate file upload type and size

Never:

- Expose unsecured POST endpoint
- Allow mass assignment
- Trust request blindly

----------------------------------------------------------------------------------------------------
16.11 TEMPLATE LAYER IN PS9
----------------------------------------------------------------------------------------------------

Twig may coexist in migrated pages.

AI MUST:

- Escape all output
- Avoid inline JS
- Avoid business logic in template
- Not mix Smarty and Twig randomly

----------------------------------------------------------------------------------------------------
16.12 CONFIGURATION STRATEGY
----------------------------------------------------------------------------------------------------

Configuration remains but:

AI SHOULD:

- Encapsulate configuration in service
- Validate before saving
- Support multishop
- Avoid storing secrets unencrypted

----------------------------------------------------------------------------------------------------
16.13 MULTISHOP STRICT MODE
----------------------------------------------------------------------------------------------------

PS9 still supports multishop.

AI MUST:

- Respect shop context
- Scope configuration correctly
- Not force global context
- Restrict queries by shop

----------------------------------------------------------------------------------------------------
16.14 MIGRATION AWARENESS
----------------------------------------------------------------------------------------------------

If generating code compatible 8 and 9:

AI MUST:

- Avoid features only in 9 if 8 required
- Guard with version_compare
- Maintain backward compatibility layer

----------------------------------------------------------------------------------------------------
16.15 TESTABILITY ENFORCEMENT
----------------------------------------------------------------------------------------------------

PS9 encourages testable architecture.

AI SHOULD:

- Isolate Domain logic
- Allow unit tests without PrestaShop bootstrap
- Avoid static calls
- Avoid global state dependency

----------------------------------------------------------------------------------------------------
16.16 PERFORMANCE RULES IN PS9
----------------------------------------------------------------------------------------------------

AI MUST:

- Avoid N+1 queries
- Use caching layer
- Avoid expensive hooks
- Avoid blocking checkout

----------------------------------------------------------------------------------------------------
16.17 PS9 ANTI-PATTERNS AI MUST NEVER GENERATE
----------------------------------------------------------------------------------------------------

❌ New legacy controller for admin  
❌ Business logic inside ObjectModel  
❌ Static Context in service  
❌ Direct SQL in controller  
❌ No strict types  
❌ No return types  
❌ Mixing legacy and Symfony randomly  
❌ Ignoring service container  

----------------------------------------------------------------------------------------------------
16.18 FUTURE-PROOFING STRATEGY
----------------------------------------------------------------------------------------------------

AI must generate code that:

- Avoids deprecated methods
- Avoids undocumented APIs
- Avoids direct core file inclusion
- Avoids internal class usage not marked public API

====================================================================================================
END PART 5
====================================================================================================
 
 
####################################################################################################
# PRESTASHOP ULTIMATE AI SKILL
# PART 6 — CQRS + DOMAIN + SERVICE ARCHITECTURE SUPREME BLUEPRINT
####################################################################################################

====================================================================================================
SECTION 17 — ENTERPRISE MODULE STRUCTURE (PS8/PS9 READY)
====================================================================================================

AI MUST structure complex modules as:

mymodule/
 ├── mymodule.php
 ├── config/
 │   ├── services.yml
 │   ├── routes.yml
 │   └── packages/
 ├── src/
 │   ├── Domain/
 │   │   ├── Entity/
 │   │   ├── ValueObject/
 │   │   ├── Exception/
 │   │   └── Repository/
 │   ├── Application/
 │   │   ├── Command/
 │   │   ├── Query/
 │   │   ├── Handler/
 │   │   └── DTO/
 │   ├── Infrastructure/
 │   │   ├── Persistence/
 │   │   ├── External/
 │   │   └── Configuration/
 │   ├── Adapter/
 │   │   ├── Legacy/
 │   │   └── Context/
 │   ├── UI/
 │   │   ├── Controller/
 │   │   ├── Form/
 │   │   └── View/
 │   └── Service/
 ├── controllers/
 ├── views/
 ├── translations/
 ├── upgrade/
 └── tests/

Never collapse all logic into root file.

====================================================================================================
SECTION 18 — CQRS CORE ENFORCEMENT
====================================================================================================

----------------------------------------------------------------------------------------------------
18.1 COMMAND PRINCIPLES
----------------------------------------------------------------------------------------------------

Command:

- Represents intention
- Immutable
- Contains only data
- No logic
- No infrastructure

Example structure:

class CreateSomethingCommand
{
    private string $name;
    private int $shopId;

    public function __construct(string $name, int $shopId)
    {
        if ($name === '') {
            throw new InvalidArgumentException();
        }

        $this->name = $name;
        $this->shopId = $shopId;
    }

    public function getName(): string
    {
        return $this->name;
    }

    public function getShopId(): int
    {
        return $this->shopId;
    }
}

AI MUST:

- Validate in constructor
- Keep properties private
- No setter methods

----------------------------------------------------------------------------------------------------
18.2 COMMAND HANDLER PRINCIPLES
----------------------------------------------------------------------------------------------------

Handler:

- Receives command
- Injects repository/service
- Performs business logic
- Returns void or result ID

Example pattern:

class CreateSomethingHandler
{
    public function __construct(
        SomethingRepositoryInterface $repository
    ) {}

    public function handle(CreateSomethingCommand $command): int
    {
        // execute business logic
    }
}

Never:

- Inject Context here
- Access superglobals
- Echo output

----------------------------------------------------------------------------------------------------
18.3 QUERY PRINCIPLES
----------------------------------------------------------------------------------------------------

Query:

- Represents read request
- Immutable
- No logic

QueryHandler:

- Reads from repository
- Returns DTO
- No write

Never:

- Write in query handler
- Return raw DB array directly to controller

----------------------------------------------------------------------------------------------------
18.4 DTO RULES
----------------------------------------------------------------------------------------------------

DTO:

- Pure data container
- No business logic
- Typed properties
- Immutable if possible

Never:

- Pass ObjectModel directly to template
- Expose internal DB structure

====================================================================================================
SECTION 19 — DOMAIN LAYER DISCIPLINE
====================================================================================================

----------------------------------------------------------------------------------------------------
19.1 DOMAIN ENTITY RULES
----------------------------------------------------------------------------------------------------

Entity:

- Contains business rules
- No DB logic
- No framework dependency
- No Context

Example:

class Subscription
{
    private SubscriptionId $id;
    private CustomerId $customerId;
    private bool $active;

    public function deactivate(): void
    {
        if (!$this->active) {
            throw new DomainException();
        }

        $this->active = false;
    }
}

----------------------------------------------------------------------------------------------------
19.2 VALUE OBJECT RULES
----------------------------------------------------------------------------------------------------

ValueObject:

- Immutable
- Validated on creation
- No setter

Example:

class Email
{
    private string $value;

    public function __construct(string $value)
    {
        if (!filter_var($value, FILTER_VALIDATE_EMAIL)) {
            throw new InvalidArgumentException();
        }

        $this->value = $value;
    }
}

----------------------------------------------------------------------------------------------------
19.3 DOMAIN EXCEPTION RULES
----------------------------------------------------------------------------------------------------

- Custom exceptions extend DomainException
- Never use generic Exception
- Never swallow exception silently

====================================================================================================
SECTION 20 — INFRASTRUCTURE LAYER RULES
====================================================================================================

----------------------------------------------------------------------------------------------------
20.1 REPOSITORY INTERFACE
----------------------------------------------------------------------------------------------------

Domain:

interface SomethingRepositoryInterface
{
    public function save(Something $entity): void;
    public function findById(int $id): ?Something;
}

Infrastructure:

class DbSomethingRepository implements SomethingRepositoryInterface
{
    // actual DB logic
}

----------------------------------------------------------------------------------------------------
20.2 DB ACCESS RULES
----------------------------------------------------------------------------------------------------

- Use DbQuery
- Cast inputs
- Escape strings
- Map DB row to Entity

Never:

- Return DB row directly to controller
- Leak Infrastructure class outside Application layer

----------------------------------------------------------------------------------------------------
20.3 CONFIGURATION WRAPPER
----------------------------------------------------------------------------------------------------

Encapsulate Configuration calls:

class ConfigurationService
{
    public function getSomething(): string
    {
        return Configuration::get('MY_KEY');
    }
}

Never:

- Call Configuration directly from Domain

====================================================================================================
SECTION 21 — ADAPTER LAYER BRIDGE
====================================================================================================

Adapter bridges:

- Legacy ObjectModel
- Legacy Context
- Modern Domain

Example:

class LegacyCustomerAdapter
{
    public function getCustomerIdFromContext(Context $context): int
    {
        return (int) $context->customer->id;
    }
}

Never:

- Let Domain depend on Adapter

====================================================================================================
SECTION 22 — CONTROLLER ENFORCEMENT
====================================================================================================

Controller responsibilities:

- Validate request
- Dispatch command/query
- Handle response
- Assign view variables

Never:

- Contain business logic
- Perform DB query directly
- Access ObjectModel deeply

----------------------------------------------------------------------------------------------------
22.1 FRONT CONTROLLER FLOW
----------------------------------------------------------------------------------------------------

initContent():
    Validate input
    Create Command
    Dispatch Handler
    Assign DTO to Smarty

----------------------------------------------------------------------------------------------------
22.2 ADMIN SYMFONY CONTROLLER FLOW
----------------------------------------------------------------------------------------------------

index():
    Build Form
    Handle request
    Validate form
    Dispatch command
    Redirect safely

Never:

- Skip CSRF
- Trust request blindly

====================================================================================================
SECTION 23 — SERVICE INJECTION STRATEGY
====================================================================================================

services.yml:

services:
  MyModule\Application\Command\CreateSomethingHandler:
    arguments:
      - '@MyModule\Infrastructure\Persistence\DbSomethingRepository'

Rules:

- No public service unless necessary
- Autowire allowed cautiously
- Avoid circular dependency

Never:

- Access container manually

====================================================================================================
SECTION 24 — VERSION-AWARE ARCHITECTURE DECISION TREE
====================================================================================================

If simple module:

→ Legacy controller acceptable.

If complex module:

→ CQRS + Domain recommended.

If PS9 only:

→ Domain-first mandatory.

If 1.7 + 9 support:

→ Avoid typed property OR branch by version.

Never:

- Generate code incompatible without explicit instruction.

====================================================================================================
SECTION 25 — INTERNAL AI SAFETY DECISION LOOP
====================================================================================================

Before generating architecture, AI must ask internally:

- Is this business logic complex?
- Does it require CQRS?
- Is version modern?
- Is multishop involved?
- Does it need repository abstraction?
- Does it require adapter bridge?
- Does it need upgrade script?

If answer unclear → choose safest modern structure.

====================================================================================================
END PART 6
====================================================================================================

####################################################################################################
# PRESTASHOP ULTIMATE AI SKILL
# PART 7 — SECURITY ABSOLUTE ENFORCEMENT SYSTEM
####################################################################################################

====================================================================================================
SECTION 26 — SECURITY OPERATING MINDSET FOR THE AI
====================================================================================================

The AI MUST assume:

- Every input is malicious.
- Every external request can fail.
- Every file upload is dangerous.
- Every SQL parameter can be injected.
- Every admin endpoint can be targeted.
- Every cron endpoint can be abused.
- Every output can be XSS vector.

Security is not optional.
Security is not feature-based.
Security is mandatory baseline.

====================================================================================================
SECTION 27 — INPUT VALIDATION ABSOLUTE RULES
====================================================================================================

27.1 NEVER TRUST:

- $_POST
- $_GET
- $_REQUEST
- $_FILES
- JSON payload
- External API response
- Cookie values

27.2 VALIDATION PROCESS

For each input:

1. Trim
2. Cast type
3. Validate format
4. Validate business logic
5. Validate length
6. Sanitize if needed

Example enforcement pattern:

$value = Tools::getValue('id');
$id = (int) $value;

if (!Validate::isUnsignedId($id)) {
    throw new InvalidArgumentException();
}

Never:

- Use input without Validate
- Trust client-side validation
- Accept raw JSON without schema validation

====================================================================================================
SECTION 28 — SQL INJECTION PREVENTION DEEP MODE
====================================================================================================

28.1 ALWAYS:

- Cast integers
- Use pSQL() for strings
- Use bqSQL() for identifiers
- Use DbQuery builder
- Escape LIKE values

28.2 NEVER:

- Concatenate raw input into SQL
- Build WHERE clause dynamically without validation
- Trust ID from request

Unsafe:

"WHERE id = ".$_GET['id']

Safe:

$whereId = (int) Tools::getValue('id');
$query->where('id = '.$whereId);

28.3 DYNAMIC ORDER BY PROTECTION

If allowing sorting:

Whitelist allowed columns:

$allowed = ['name', 'date_add'];

if (!in_array($sort, $allowed, true)) {
    $sort = 'date_add';
}

====================================================================================================
SECTION 29 — XSS PREVENTION DEEP MODE
====================================================================================================

29.1 OUTPUT ESCAPING RULES

In Smarty:

{$variable|escape:'htmlall':'UTF-8'}

In Twig:

{{ variable|e }}

In JSON:

json_encode($data, JSON_THROW_ON_ERROR);

Never:

- Print raw user input
- Inject raw HTML unless sanitized
- Trust HTML editor content without purification

29.2 STORED XSS PROTECTION

If storing user content:

- Sanitize before save OR
- Sanitize before output

Prefer sanitizing before output.

29.3 JAVASCRIPT INJECTION PROTECTION

Never inject variable directly into JS:

<script>
var name = "{$name}";
</script>

Instead:

Assign JSON safely:

var data = {$data|json_encode nofilter};

====================================================================================================
SECTION 30 — CSRF PROTECTION
====================================================================================================

30.1 ADMIN FORMS

Must include token:

$this->context->link->getAdminLink()

Or Symfony CSRF token in PS8/9.

30.2 AJAX ENDPOINTS

Must validate:

- Employee permission
- Token
- Method (POST preferred)

Never:

- Accept state-changing GET request
- Expose unsecured POST endpoint

====================================================================================================
SECTION 31 — FILE UPLOAD HARDENING
====================================================================================================

31.1 ALWAYS VALIDATE:

- MIME type
- Extension
- File size
- File name
- Content

31.2 NEVER:

- Trust $_FILES['type']
- Allow .php upload
- Store file inside executable directory
- Use original filename blindly

Rename file:

$filename = uniqid().'.'.$extension;

Store outside public path if sensitive.

====================================================================================================
SECTION 32 — AUTHORIZATION & PERMISSIONS
====================================================================================================

32.1 BACK OFFICE

Check:

$this->context->employee->id

Validate permission:

$this->access('edit');

Never:

- Assume admin is authorized
- Skip permission check in controller

32.2 FRONT OFFICE

Check:

$this->context->customer->isLogged();

Never:

- Assume logged in if id present
- Allow modifying cart without validation

====================================================================================================
SECTION 33 — CRON SECURITY MODEL
====================================================================================================

Cron endpoint must:

- Require secret token
- Validate IP optionally
- Validate timestamp
- Not expose debug output

Example:

if (Tools::getValue('token') !== Configuration::get('MY_SECRET')) {
    die('Unauthorized');
}

Never:

- Public cron without authentication
- Print sensitive information

====================================================================================================
SECTION 34 — EXTERNAL API COMMUNICATION SECURITY
====================================================================================================

34.1 ALWAYS:

- Use HTTPS
- Validate SSL certificate
- Set timeout
- Catch exceptions
- Validate response schema

34.2 NEVER:

- Disable SSL verification
- Trust response blindly
- Store API key in plain code

Use configuration storage for API keys.

====================================================================================================
SECTION 35 — ENCRYPTION & SENSITIVE DATA
====================================================================================================

35.1 STORE SENSITIVE DATA

- Avoid plain text if possible
- Use PrestaShop encryption utilities if needed
- Limit access to configuration keys

35.2 NEVER:

- Hardcode API keys
- Log secret values
- Expose secrets in template

====================================================================================================
SECTION 36 — SESSION & COOKIE SECURITY
====================================================================================================

AI MUST:

- Avoid storing sensitive info in cookie
- Validate cookie before use
- Not trust cookie values

Never:

- Use cookie to store price
- Use cookie to store permission

====================================================================================================
SECTION 37 — RATE LIMIT & ABUSE PREVENTION
====================================================================================================

If endpoint sensitive:

- Implement basic throttling
- Log abuse attempts
- Avoid unlimited brute force

Example:

Limit login attempts
Limit token attempts

====================================================================================================
SECTION 38 — ERROR HANDLING SECURITY
====================================================================================================

38.1 PRODUCTION MODE

Never:

- Display stack trace
- Echo exception message to user

38.2 LOGGING

Use:

PrestaShopLogger::addLog()

Never:

- var_dump in production
- echo exception

====================================================================================================
SECTION 39 — MARKETPLACE SECURITY REQUIREMENTS
====================================================================================================

AI MUST ensure module:

- Contains no obfuscated code
- Contains no encoded PHP
- Contains no hidden tracking
- Contains no remote code execution
- Contains no eval
- Contains no base64_decode logic

====================================================================================================
SECTION 40 — CLOUD SAFE ENFORCEMENT
====================================================================================================

If Cloud-compatible:

- No blocking checkout
- No modifying payment flow dangerously
- No altering core tables
- No external script injection
- No iframe injection

====================================================================================================
SECTION 41 — ATTACK SURFACE MINIMIZATION
====================================================================================================

AI MUST:

- Avoid unnecessary endpoints
- Avoid open AJAX
- Avoid exposing internal IDs unnecessarily
- Avoid debug routes

====================================================================================================
SECTION 42 — FINAL SECURITY AI CHECK LOOP
====================================================================================================

Before generating final answer, AI must internally confirm:

- All inputs validated?
- All outputs escaped?
- All SQL safe?
- All endpoints secured?
- All tokens validated?
- All files validated?
- No secret exposed?
- No debug left?
- No override risk?

If ANY doubt → regenerate safer version.

====================================================================================================
END PART 7
====================================================================================================


####################################################################################################
# PRESTASHOP ULTIMATE AI SKILL
# PART 8 — MARKETPLACE + CLOUD + INTEGRATION FRAMEWORK SUPREME COMPLIANCE
####################################################################################################

====================================================================================================
SECTION 43 — MARKETPLACE OPERATING PRINCIPLES
====================================================================================================

The AI MUST assume that any module generated:

- May be submitted to PrestaShop Marketplace
- May be installed on PrestaShop Cloud
- May be audited manually
- May be scanned automatically
- Must pass Validation Checklist
- Must not contain suspicious patterns

Security, stability and neutrality are mandatory.

====================================================================================================
SECTION 44 — MARKETPLACE CODE COMPLIANCE RULES
====================================================================================================

44.1 NO OBFUSCATION

Forbidden:

- base64_decode
- eval
- gzinflate
- Encoded PHP blocks
- IonCube requirement

Code must be readable.

44.2 NO HIDDEN BEHAVIOR

Module must not:

- Inject hidden tracking
- Load external JS silently
- Send customer data externally without declaration
- Inject advertisement
- Modify checkout silently

44.3 NO CORE MODIFICATION

Forbidden:

- Editing core files
- Writing inside /classes
- Writing inside /controllers core
- Overriding core without reason

Overrides must be avoided.

====================================================================================================
SECTION 45 — PACKAGE STRUCTURE RULES
====================================================================================================

45.1 ZIP STRUCTURE

Root folder must:

- Contain module folder only
- No nested extra folder
- No node_modules
- No vendor development leftovers
- No test environment files

Remove:

- .git
- .env
- composer.lock if unnecessary
- phpunit files (if not needed)

45.2 FILE PERMISSIONS

Avoid:

- 777 permissions
- Executable permissions on non-script files

====================================================================================================
SECTION 46 — COMPOSER RULES
====================================================================================================

If using composer:

- Include composer.json
- Do not include dev dependencies
- Avoid heavy external frameworks
- Avoid conflicting dependencies

Never:

- Bundle entire Symfony framework
- Conflict with core libraries

====================================================================================================
SECTION 47 — INTEGRATION FRAMEWORK CORE REQUIREMENTS
====================================================================================================

The AI MUST ensure:

- Module installs without manual modification
- Module works without editing theme
- Module uses official hooks
- Module does not break checkout
- Module handles failure gracefully

----------------------------------------------------------------------------------------------------
47.1 INSTALLATION VALIDATION
----------------------------------------------------------------------------------------------------

Install must:

- Return true
- Register hooks safely
- Create tables with prefix
- Handle failure rollback if possible

----------------------------------------------------------------------------------------------------
47.2 UNINSTALLATION VALIDATION
----------------------------------------------------------------------------------------------------

Uninstall must:

- Remove configuration keys
- Remove tabs created
- Optionally remove tables
- Not leave orphan data without explanation

----------------------------------------------------------------------------------------------------
47.3 FRONT OFFICE STABILITY
----------------------------------------------------------------------------------------------------

Module must:

- Not break layout
- Not cause fatal errors
- Not depend on non-installed module blindly
- Fail gracefully if dependency missing

====================================================================================================
SECTION 48 — PRESTASHOP ACCOUNT INTEGRATION AWARENESS
====================================================================================================

If module interacts with:

- PrestaShop Account
- CloudSync
- Billing

AI MUST:

- Not duplicate authentication logic
- Not bypass official account flow
- Respect account module integration
- Use documented API only

Never:

- Modify account module
- Inject custom login flow

====================================================================================================
SECTION 49 — BILLING SAFETY MODEL
====================================================================================================

If module involves billing:

- Never block checkout on failure
- Fail gracefully
- Log errors
- Not modify payment core logic
- Respect subscription lifecycle

====================================================================================================
SECTION 50 — CLOUD COMPATIBILITY REQUIREMENTS
====================================================================================================

PrestaShop Cloud expects:

- No file system unsafe write
- No manual core modification
- No server-level assumption
- No shell execution
- No exec(), shell_exec()

AI MUST:

- Avoid server-specific assumptions
- Avoid using system commands
- Avoid writing outside module folder

====================================================================================================
SECTION 51 — PERFORMANCE MARKETPLACE RULES
====================================================================================================

Module must:

- Not add heavy queries to displayHeader
- Not run heavy code on every page
- Use caching where appropriate
- Avoid N+1 queries
- Avoid heavy loops

====================================================================================================
SECTION 52 — DATA PRIVACY & GDPR AWARENESS
====================================================================================================

If module stores personal data:

AI MUST:

- Declare data usage
- Provide data deletion mechanism
- Allow export if required
- Not transmit personal data externally without explicit purpose

Never:

- Store sensitive data without encryption
- Log personal data in debug

====================================================================================================
SECTION 53 — TRANSLATION & I18N COMPLIANCE
====================================================================================================

All strings must:

- Be translatable
- Use domain
- Not be hardcoded in template
- Respect language context

====================================================================================================
SECTION 54 — DEPENDENCY MANAGEMENT RULES
====================================================================================================

If module depends on another module:

AI MUST:

- Check if installed
- Fail gracefully
- Not cause fatal error

Example:

if (!Module::isInstalled('anothermodule')) {
    return;
}

====================================================================================================
SECTION 55 — VALIDATION CHECKLIST SIMULATION ENGINE
====================================================================================================

Before finalizing module generation, AI must internally simulate:

INSTALL TEST:
- Does install return true?
- Are hooks registered?
- Are tables valid?
- No SQL error?

UNINSTALL TEST:
- Does uninstall return true?
- Are config keys removed?

FRONT TEST:
- No PHP warnings?
- No undefined index?
- No console JS error?

BACK TEST:
- Permissions validated?
- Token validated?
- Form safe?

MULTISHOP TEST:
- Works with multiple shops?
- Config separated?

PERFORMANCE TEST:
- No heavy query in loop?
- No blocking logic?

SECURITY TEST:
- No XSS?
- No SQL injection?
- No CSRF?

====================================================================================================
SECTION 56 — MODULE SIGNATURE READINESS
====================================================================================================

AI MUST generate:

- Clean, readable code
- No malicious pattern
- No suspicious encoding
- No remote code loading
- No dynamic include of external URL

====================================================================================================
SECTION 57 — CLOUD & MARKETPLACE ANTI-PATTERNS AI MUST NEVER GENERATE
====================================================================================================

❌ Remote script injection  
❌ Hidden iframe injection  
❌ Background API call without declaration  
❌ Checkout flow modification  
❌ Payment override  
❌ Hidden tracking  
❌ Encoded payload  
❌ License enforcement via obfuscation  

====================================================================================================
SECTION 58 — FINAL MARKETPLACE AI CHECK LOOP
====================================================================================================

Before outputting module code, AI must internally verify:

- Is code readable?
- Is code compliant?
- Is code secure?
- Is code compatible?
- Is code stable?
- Is code multishop safe?
- Is code uninstall clean?
- Is code marketplace safe?
- Is code cloud safe?

If ANY doubt → regenerate safer version.

====================================================================================================
END PART 8
====================================================================================================

####################################################################################################
# PRESTASHOP ULTIMATE AI SKILL
# PART 9 — MULTISHOP + PERFORMANCE + SCALABILITY MASTER CONTROL
####################################################################################################

====================================================================================================
SECTION 59 — MULTISHOP CORE UNDERSTANDING
====================================================================================================

PrestaShop multishop allows:

- Multiple shops
- Multiple shop groups
- Shared or isolated catalog
- Shared or isolated configuration

AI MUST assume multishop may be enabled.

Never assume single shop unless explicitly stated.

====================================================================================================
SECTION 60 — SHOP CONTEXT DISCIPLINE
====================================================================================================

Shop context levels:

- CONTEXT_ALL
- CONTEXT_GROUP
- CONTEXT_SHOP

AI MUST:

- Never force context globally
- Use Shop::getContextShopID()
- Use Shop::getContext()

If storing configuration:

Configuration::updateValue('KEY', $value, false, null, $shopId);

Never:

Configuration::updateValue('KEY', $value) without scope awareness.

====================================================================================================
SECTION 61 — MULTISHOP DATABASE STRUCTURE
====================================================================================================

If data is shop-specific:

Table must include:

- id_shop
- Or linking table mytable_shop

Example linking pattern:

mytable
- id_mytable
- common fields

mytable_shop
- id_mytable
- id_shop

AI MUST:

- Restrict queries by shop
- Not mix data across shops

====================================================================================================
SECTION 62 — SQL SHOP RESTRICTION PATTERNS
====================================================================================================

Use:

Shop::addSqlRestriction()

Example:

$query->from('mytable', 'm');
$query->where('m.id_shop = '.(int)$shopId);

Never:

SELECT without shop restriction if data is shop dependent.

====================================================================================================
SECTION 63 — MULTISHOP CONFIGURATION STRATEGY
====================================================================================================

AI MUST determine:

Is config global?
Is config per shop?
Is config per group?

Never:

Store shop-dependent setting globally.

====================================================================================================
SECTION 64 — PERFORMANCE FUNDAMENTALS
====================================================================================================

64.1 NO N+1 QUERIES

Never:

foreach ($products as $product) {
    Db::getInstance()->getRow(...)
}

Instead:

Fetch all needed rows in one query.

----------------------------------------------------------------------------------------------------
64.2 NO SELECT *
----------------------------------------------------------------------------------------------------

Always:

Select only needed columns.

----------------------------------------------------------------------------------------------------
64.3 INDEX STRATEGY
----------------------------------------------------------------------------------------------------

If table large:

- Add index on foreign keys
- Add index on search columns
- Add composite index if needed

Never:

Create table without primary key
Create table without index for heavy queries

====================================================================================================
SECTION 65 — CACHING STRATEGY
====================================================================================================

65.1 STATIC CACHE

Use static variable inside method:

static $cache = [];

65.2 PRESTASHOP CACHE

Use:

Cache::store()
Cache::retrieve()

65.3 DO NOT CACHE:

- Customer-specific data globally
- Shop-specific data globally
- Sensitive data

----------------------------------------------------------------------------------------------------
65.4 CACHE INVALIDATION

AI MUST consider:

When updating data:
- Invalidate cache
- Avoid stale data

====================================================================================================
SECTION 66 — HOOK PERFORMANCE DISCIPLINE
====================================================================================================

Hooks like:

displayHeader
displayFooter
displayProductExtraContent

Executed frequently.

AI MUST:

- Avoid heavy queries
- Use caching
- Avoid loops inside loops
- Avoid loading entire ObjectModel

====================================================================================================
SECTION 67 — LARGE CATALOG SCALABILITY
====================================================================================================

If module interacts with products:

Assume:

- 100k+ products possible
- Large category trees
- Large order tables

AI MUST:

- Paginate queries
- Avoid loading all products
- Use LIMIT
- Avoid full table scans

====================================================================================================
SECTION 68 — MEMORY MANAGEMENT
====================================================================================================

Avoid:

- Loading entire dataset in memory
- Storing huge arrays
- JSON encoding massive dataset unnecessarily

If needed:

- Process in batches
- Use generator if applicable

====================================================================================================
SECTION 69 — ASYNCHRONOUS SAFETY
====================================================================================================

If module performs:

- API calls
- Heavy processing
- Recalculation

AI SHOULD:

- Avoid blocking checkout
- Offload heavy tasks to cron
- Queue processing

Never:

Perform long external API call in display hook.

====================================================================================================
SECTION 70 — FRONT PERFORMANCE OPTIMIZATION
====================================================================================================

AI MUST:

- Minimize JS footprint
- Avoid multiple JS files
- Avoid inline scripts
- Defer non-critical JS
- Not block rendering

====================================================================================================
SECTION 71 — BACK OFFICE PERFORMANCE
====================================================================================================

Admin grid queries:

- Must be paginated
- Must use filtering safely
- Must use indexed columns

Never:

Load all rows into memory for listing.

====================================================================================================
SECTION 72 — MULTISTORE EDGE CASES
====================================================================================================

Edge cases:

- Shop deleted
- Shop disabled
- Shop group changed

AI MUST:

- Validate shop existence
- Not crash if shop context invalid

====================================================================================================
SECTION 73 — FAIL-SAFE DESIGN
====================================================================================================

If module fails:

- Must not break front office
- Must not break checkout
- Must log error
- Must fail gracefully

Never:

Throw uncaught exception in hook.

====================================================================================================
SECTION 74 — HIGH TRAFFIC READINESS
====================================================================================================

If module used on high traffic store:

AI MUST:

- Avoid session lock long processing
- Avoid heavy logic in every request
- Use caching intelligently
- Avoid file writes per request

====================================================================================================
SECTION 75 — CONCURRENCY SAFETY
====================================================================================================

If updating data:

- Use transaction if needed
- Avoid race conditions
- Validate current state before update

Never:

Assume no concurrent update.

====================================================================================================
SECTION 76 — INDEX MIGRATION SAFETY
====================================================================================================

Upgrade script must:

- Check index existence before adding
- Avoid duplicate index error

====================================================================================================
SECTION 77 — PERFORMANCE ANTI-PATTERNS AI MUST NEVER GENERATE
====================================================================================================

❌ Query inside loop  
❌ SELECT * on big table  
❌ No index on foreign key  
❌ Heavy logic in displayHeader  
❌ Blocking API call in checkout  
❌ Loading entire product catalog  
❌ Global cache for shop-specific data  

====================================================================================================
SECTION 78 — FINAL PERFORMANCE AI CHECK LOOP
====================================================================================================

Before output:

- Any loop with DB inside?
- Any heavy hook logic?
- Any missing index?
- Any missing LIMIT?
- Any multishop leak?
- Any blocking external call?
- Any large memory allocation?
- Any missing pagination?

If ANY risk → optimize before returning code.

====================================================================================================
END PART 9
====================================================================================================


####################################################################################################
# PRESTASHOP ULTIMATE AI SKILL
# PART 10 — TESTING + UPGRADE + DEPLOYMENT + MIGRATION MASTER SYSTEM
####################################################################################################

====================================================================================================
SECTION 79 — MODULE LIFECYCLE UNDERSTANDING
====================================================================================================

A PrestaShop module has lifecycle phases:

1. Installation
2. Activation
3. Usage
4. Upgrade
5. Deactivation
6. Uninstallation
7. Reinstallation

AI MUST design module to survive ALL phases safely.

====================================================================================================
SECTION 80 — INSTALLATION HARDENING
====================================================================================================

install() must:

- Call parent::install()
- Register required hooks
- Create tables
- Insert default config
- Create admin tabs if needed
- Handle failure safely

Pattern:

public function install(): bool
{
    return parent::install()
        && $this->registerHook('displayHeader')
        && $this->installDatabase()
        && $this->installConfiguration();
}

Never:

- Return true without verifying SQL success
- Swallow SQL errors silently
- Assume table does not exist

====================================================================================================
SECTION 81 — DATABASE INSTALL SAFETY
====================================================================================================

AI MUST:

- Use _DB_PREFIX_
- Use ENGINE=InnoDB
- Use utf8mb4 charset
- Define primary key
- Define indexes

Example:

CREATE TABLE IF NOT EXISTS `PREFIX_mytable` (
  `id_mytable` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_shop` INT UNSIGNED NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id_mytable`),
  INDEX (`id_shop`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

Never:

- Omit primary key
- Use MyISAM
- Forget index on id_shop

====================================================================================================
SECTION 82 — UPGRADE SCRIPT ABSOLUTE RULES
====================================================================================================

Each version bump requiring DB or config change MUST create:

upgrade/upgrade-x.y.z.php

Structure:

function upgrade_module_1_1_0($module)
{
    // migration logic
    return true;
}

AI MUST:

- Check if column exists before ALTER
- Check if index exists
- Be idempotent
- Not drop table blindly
- Preserve data

----------------------------------------------------------------------------------------------------
82.1 COLUMN EXISTENCE CHECK
----------------------------------------------------------------------------------------------------

Use:

SHOW COLUMNS LIKE 'column_name'

Before:

ALTER TABLE ADD COLUMN

----------------------------------------------------------------------------------------------------
82.2 DATA MIGRATION SAFETY
----------------------------------------------------------------------------------------------------

If changing structure:

- Backup logic conceptually
- Convert data safely
- Avoid destructive operations

Never:

DROP TABLE without explicit user confirmation.

====================================================================================================
SECTION 83 — VERSION COMPATIBILITY STRATEGY
====================================================================================================

If supporting multiple versions:

AI MUST:

- Detect version with _PS_VERSION_
- Branch carefully
- Avoid syntax incompatible with lower version

Example:

if (version_compare(_PS_VERSION_, '8.0.0', '>=')) {
    // modern code
}

Never:

- Assume latest version always installed.

====================================================================================================
SECTION 84 — BACKWARD COMPATIBILITY STRATEGY
====================================================================================================

When refactoring:

- Keep old configuration keys
- Migrate old config to new structure
- Avoid breaking existing installations

If removing feature:

- Provide fallback
- Document change

====================================================================================================
SECTION 85 — DEACTIVATION SAFETY
====================================================================================================

On disable:

- Module should not break store
- Hooks removed
- No fatal errors in template
- No missing variable errors

Never:

- Leave template references active

====================================================================================================
SECTION 86 — UNINSTALL SAFETY
====================================================================================================

uninstall() must:

- Call parent::uninstall()
- Remove config keys
- Remove tabs
- Optionally remove tables
- Return boolean

AI MUST:

- Not leave orphan configuration
- Not break other modules

====================================================================================================
SECTION 87 — DATA PRESERVATION STRATEGY
====================================================================================================

If module stores business-critical data:

AI SHOULD:

- Ask before deleting data on uninstall
- Offer keep data option
- Avoid automatic destructive delete

====================================================================================================
SECTION 88 — TESTING STRATEGY FOR AI GENERATED CODE
====================================================================================================

AI SHOULD generate code that allows:

- Unit testing Domain logic
- Mocking repositories
- Testing command handlers independently
- Avoid requiring full PrestaShop bootstrap

----------------------------------------------------------------------------------------------------
88.1 UNIT TEST FRIENDLY DESIGN
----------------------------------------------------------------------------------------------------

- No static calls in Domain
- No global state
- No Context inside Domain
- Dependency injection used

----------------------------------------------------------------------------------------------------
88.2 INTEGRATION TEST FRIENDLY DESIGN
----------------------------------------------------------------------------------------------------

- DB logic isolated
- Repository mockable
- Configuration encapsulated

====================================================================================================
SECTION 89 — ERROR HANDLING STRATEGY
====================================================================================================

AI MUST:

- Catch expected exceptions
- Log error
- Return safe fallback
- Not expose sensitive error message

Example:

try {
    $handler->handle($command);
} catch (DomainException $e) {
    PrestaShopLogger::addLog($e->getMessage(), 3);
    $this->errors[] = $this->trans('Operation failed');
}

Never:

- Let exception bubble to front
- Print stack trace

====================================================================================================
SECTION 90 — DEPLOYMENT SAFETY
====================================================================================================

AI MUST ensure module:

- Does not require manual file edit
- Does not require core modification
- Does not require server-level config change
- Does not require special PHP extension unless declared

Never:

- Use exec()
- Use shell commands
- Assume Linux only

====================================================================================================
SECTION 91 — MIGRATION BETWEEN ARCHITECTURES
====================================================================================================

If module originally legacy and upgraded to modern:

AI MUST:

- Keep backward compatibility
- Introduce Adapter layer
- Avoid breaking public API
- Avoid removing hooks abruptly

====================================================================================================
SECTION 92 — DEPRECATION AWARENESS
====================================================================================================

AI MUST:

- Avoid deprecated PrestaShop methods
- Avoid deprecated PHP features
- Avoid undocumented internal APIs
- Not rely on internal class not marked public

====================================================================================================
SECTION 93 — ROLLBACK STRATEGY
====================================================================================================

If upgrade fails:

- Fail gracefully
- Not corrupt DB
- Not partially migrate schema without detection

====================================================================================================
SECTION 94 — PRODUCTION SAFETY CHECK
====================================================================================================

Before finalizing code:

AI MUST verify:

- No debug code
- No var_dump
- No die() outside Ajax JSON
- No hardcoded path
- No leftover TODO

====================================================================================================
SECTION 95 — LONG-TERM MAINTAINABILITY STRATEGY
====================================================================================================

AI SHOULD:

- Use clear naming
- Use consistent namespace
- Avoid magic numbers
- Avoid duplicated logic
- Centralize configuration access

====================================================================================================
SECTION 96 — MIGRATION ANTI-PATTERNS AI MUST NEVER GENERATE
====================================================================================================

❌ DROP TABLE without check  
❌ ALTER TABLE blindly  
❌ Overwriting config without migration  
❌ Breaking previous version data  
❌ Hardcoded version checks without fallback  
❌ Ignoring multishop in upgrade  

====================================================================================================
SECTION 97 — FINAL LIFECYCLE AI CHECK LOOP
====================================================================================================

Before returning module code, AI must internally verify:

INSTALL:
- Safe?
- SQL valid?
- Hooks exist?

UPGRADE:
- Idempotent?
- Data safe?
- Backward compatible?

UNINSTALL:
- Clean?
- No orphan config?
- No fatal error risk?

DEPLOYMENT:
- No server dependency?
- No core modification?
- No hidden risk?

If ANY uncertainty → redesign safer.

====================================================================================================
END PART 10
====================================================================================================

####################################################################################################
# PRESTASHOP ULTIMATE AI SKILL
# PART 11 — VERSION MATRIX + DIFFERENCE ENGINE + ARCHITECTURAL DECISION SYSTEM
####################################################################################################

====================================================================================================
SECTION 98 — GLOBAL VERSION AWARENESS CORE
====================================================================================================

PrestaShop evolution summary:

1.7 → Legacy dominant, partial Symfony
8.x → Hybrid transitional
9.x → Modern-first, Domain-driven

AI MUST:

- Detect version context
- Adjust syntax
- Adjust architecture
- Avoid deprecated APIs
- Avoid backward-breaking syntax

====================================================================================================
SECTION 99 — PHP COMPATIBILITY MATRIX
====================================================================================================

Feature                            1.7        8.x        9.x
-------------------------------------------------------------------------------
Minimum PHP                        7.2        8.1        8.2+
Strict types                       Optional   Recommended Mandatory
Typed properties                   Risky      Allowed     Mandatory
Constructor property promotion     No         Yes         Yes
Union types                        No         Yes         Yes
Readonly properties                No         Avoid       Yes
Enums                              No         Limited     Yes
Match expression                   No         Yes         Yes
Attributes                         No         Yes         Yes

AI DECISION RULE:

If supporting 1.7:
    Avoid typed properties
    Avoid union types
    Avoid match()
    Avoid readonly
    Avoid constructor property promotion

If supporting 8+:
    Use modern PHP
    Enforce typing

====================================================================================================
SECTION 100 — ARCHITECTURE DIFFERENCE MATRIX
====================================================================================================

Component                     1.7                 8.x                   9.x
-----------------------------------------------------------------------------------------
Admin Controllers            Legacy dominant      Hybrid                Symfony-first
Front Controllers            Legacy               Legacy                Legacy (migrating)
Service Container            Limited              Available             Core architecture
Domain Layer                 Not standard         Introduced            Core pattern
CQRS                         Not common           Partial               Encouraged/Expected
Context static usage         Common               Discouraged           Strongly discouraged
ObjectModel usage            Standard             Standard               Legacy containment
Twig                         No                   Partial               More present
Hook system                  Core mechanism       Core mechanism        Core + Events

AI RULE:

If PS9 target:
    Prefer Domain + Service container.
If PS8 target:
    Hybrid acceptable.
If PS1.7 target:
    Legacy acceptable but structured.

====================================================================================================
SECTION 101 — CONTEXT USAGE EVOLUTION
====================================================================================================

1.7:
    Context::getContext() common.

8.x:
    Context still available.
    Service injection preferred.

9.x:
    Context discouraged inside services.
    Use adapter or dedicated services.

AI MUST:

Never inject full Context into Domain.

====================================================================================================
SECTION 102 — HOOK SYSTEM EVOLUTION
====================================================================================================

Hooks remain across versions.

Differences:

1.7:
    Hook-only extension.

8:
    Hooks + Symfony controllers.

9:
    Hooks + EventDispatcher + Symfony services.

AI RULE:

Never invent hook names.
Never rely on undocumented hook behavior.
Always return correct type.

====================================================================================================
SECTION 103 — FORM SYSTEM EVOLUTION
====================================================================================================

1.7:
    HelperForm.

8:
    HelperForm + Symfony Forms.

9:
    Symfony Forms preferred.

AI DECISION:

If admin modern page:
    Use Symfony Form.

If legacy compatibility required:
    Use HelperForm.

Never mix both in same controller.

====================================================================================================
SECTION 104 — DATABASE ACCESS EVOLUTION
====================================================================================================

1.7:
    Db class + ObjectModel.

8:
    Db + Doctrine available.

9:
    Db + Doctrine, Domain repository pattern encouraged.

AI RULE:

For compatibility:
    Prefer DbQuery.

For modern architecture:
    Encapsulate DB in Repository.

====================================================================================================
SECTION 105 — CONFIGURATION HANDLING EVOLUTION
====================================================================================================

Configuration class remains.

But:

8/9:
    Encapsulation recommended.
    Service wrapper preferred.

AI MUST:

Avoid direct Configuration calls in Domain.

====================================================================================================
SECTION 106 — SECURITY EVOLUTION
====================================================================================================

1.7:
    CSRF manual in legacy forms.

8:
    Symfony CSRF available.

9:
    Symfony security stack stronger.

AI RULE:

Always include CSRF.
Always validate employee permission.
Always sanitize.

====================================================================================================
SECTION 107 — TEMPLATE ENGINE DIFFERENCE
====================================================================================================

1.7:
    Smarty only.

8:
    Smarty + Twig partial.

9:
    Smarty (FO) + Twig (BO modern pages).

AI RULE:

Never mix Smarty and Twig in same template.
Escape everything.

====================================================================================================
SECTION 108 — MULTISHOP DIFFERENCE
====================================================================================================

Multishop available across versions.

No major API difference.

AI RULE:

Always respect shop context.

====================================================================================================
SECTION 109 — UPGRADE SCRIPT DIFFERENCE
====================================================================================================

Mechanism same across versions.

AI RULE:

Always create upgrade-x.y.z.php
Never modify install() for upgrade logic.

====================================================================================================
SECTION 110 — DEPRECATED PATTERN MAPPING
====================================================================================================

Deprecated in modern context:

- Static Context usage deep
- Direct ObjectModel heavy logic
- Overrides as default extension
- Inline JS injection
- Manual service locator

AI MUST:

Replace deprecated patterns with:

- Dependency injection
- CQRS
- Domain separation
- Service container usage

====================================================================================================
SECTION 111 — VERSION DECISION TREE FOR AI
====================================================================================================

STEP 1: Identify version support.

STEP 2:

If only 9:
    Use modern architecture fully.
    Use typed properties.
    Use CQRS.
    Use service container.

If 8 + 9:
    Use modern architecture.
    Avoid 9-only PHP features.
    Guard with version_compare.

If 1.7 + 8 + 9:
    Avoid typed properties.
    Avoid union types.
    Avoid constructor promotion.
    Use hybrid design.
    Isolate modern features behind version condition.

STEP 3:
    Determine module complexity.

If simple display module:
    Legacy structure acceptable.

If business logic heavy:
    Use Domain + CQRS.

====================================================================================================
SECTION 112 — API STABILITY STRATEGY
====================================================================================================

AI MUST:

- Avoid internal core classes not marked public.
- Avoid accessing protected properties.
- Avoid reflection hacks.
- Avoid modifying core container.

====================================================================================================
SECTION 113 — EXTENSIBILITY STRATEGY
====================================================================================================

AI SHOULD:

- Provide extension points via hooks.
- Not hardcode behavior.
- Allow configuration-based behavior.

====================================================================================================
SECTION 114 — FORWARD COMPATIBILITY STRATEGY
====================================================================================================

AI MUST:

- Avoid deprecated methods.
- Avoid undocumented APIs.
- Use official documentation patterns.
- Prepare architecture for further Symfony expansion.

====================================================================================================
SECTION 115 — FINAL VERSION SAFETY CHECK LOOP
====================================================================================================

Before output, AI must verify:

- Is syntax compatible with target?
- Is architecture correct for version?
- Is deprecated pattern avoided?
- Is Domain separated where required?
- Is Context usage safe?
- Is multishop safe?
- Is security enforced?
- Is upgrade path safe?

If ANY mismatch → adjust architecture.

====================================================================================================
END PART 11
====================================================================================================
####################################################################################################
# PRESTASHOP ULTIMATE AI SKILL
# PART 12 — ABSOLUTE ANTI-PATTERN INDEX + GLOBAL PROHIBITIONS + AI CONTROL ENGINE
####################################################################################################

====================================================================================================
SECTION 116 — GLOBAL AI OPERATING CONTRACT
====================================================================================================

From this point forward, the AI generating PrestaShop code must operate under the following
non-negotiable contract:

- Architecture before code.
- Safety before features.
- Compatibility before optimization.
- Clarity before cleverness.
- Explicit before implicit.
- Injection before static.
- Separation before convenience.

If any instruction conflicts with these principles,
the AI must choose the safest architectural path.

====================================================================================================
SECTION 117 — ABSOLUTE PROHIBITION CATALOG
====================================================================================================

The AI MUST NEVER generate:

❌ Raw SQL concatenation  
❌ $_POST direct access  
❌ $_GET direct access  
❌ eval()  
❌ base64_decode for logic  
❌ dynamic include of remote file  
❌ shell_exec / exec  
❌ Direct core file modification  
❌ Unescaped template output  
❌ Inline HTML inside PHP business logic  
❌ Static Context inside Domain  
❌ ObjectModel containing business rules  
❌ Controller performing heavy DB logic  
❌ Query inside loop  
❌ SELECT * on large tables  
❌ Hardcoded shop ID  
❌ Hardcoded language ID  
❌ Hardcoded currency ID  
❌ Overriding Product core casually  
❌ Creating custom entry PHP outside dispatcher  
❌ Returning unvalidated JSON  
❌ Exposing stack trace  
❌ Leaving debug code in production  
❌ Using deprecated API  
❌ Ignoring multishop  
❌ Blocking checkout flow  
❌ Injecting external script silently  
❌ Obfuscated licensing logic  

====================================================================================================
SECTION 118 — ARCHITECTURAL ANTI-PATTERN INDEX
====================================================================================================

118.1 LAYER VIOLATIONS

❌ Controller → DB direct access  
❌ Domain → Context dependency  
❌ Domain → Configuration direct access  
❌ Infrastructure → Calling Controller  
❌ Template → Business logic  

118.2 SERVICE MISUSE

❌ Manual container fetch  
❌ Static service locator  
❌ Circular dependency  
❌ Public services unnecessarily  

118.3 CQRS VIOLATIONS

❌ Writing inside QueryHandler  
❌ Returning Entity directly to template  
❌ Mutable Command objects  
❌ Command without validation  

====================================================================================================
SECTION 119 — SECURITY RED FLAG DETECTOR
====================================================================================================

If generated code contains:

- Unvalidated input
- Missing token validation
- Missing permission check
- Unescaped output
- File upload without MIME validation
- SQL built from raw input
- Missing LIMIT in large dataset
- No shop restriction in multishop table

Then AI MUST regenerate code safer.

====================================================================================================
SECTION 120 — PERFORMANCE RED FLAG DETECTOR
====================================================================================================

If generated code contains:

- Query inside foreach
- SELECT * on product table
- displayHeader heavy DB logic
- Large dataset loaded fully
- No pagination
- Repeated Configuration::get in loop

AI MUST optimize before returning answer.

====================================================================================================
SECTION 121 — MULTISHOP RED FLAG DETECTOR
====================================================================================================

If generated code:

- Stores shop-specific data globally
- Lacks id_shop column in shop-specific table
- Does not filter by shop
- Forces Shop::setContext globally
- Ignores shop group logic

AI MUST correct it.

====================================================================================================
SECTION 122 — VERSION MISMATCH DETECTOR
====================================================================================================

If target includes 1.7 and code includes:

- typed properties
- union types
- match
- constructor property promotion

AI MUST downgrade syntax.

If target includes 9 only and code includes:

- legacy-only architecture
- heavy static Context usage
- no strict types

AI MUST modernize.

====================================================================================================
SECTION 123 — UPGRADE RISK DETECTOR
====================================================================================================

If migration:

- Drops table blindly
- Adds column without existence check
- Deletes configuration silently
- Breaks backward compatibility

AI MUST redesign migration.

====================================================================================================
SECTION 124 — DEPLOYMENT RISK DETECTOR
====================================================================================================

If code:

- Uses exec
- Uses shell command
- Assumes Linux path
- Requires server config
- Writes outside module folder

AI MUST remove unsafe behavior.

====================================================================================================
SECTION 125 — AI SELF-CORRECTION LOOP
====================================================================================================

Before returning final answer, AI must internally execute:

1. Architecture Validation
   - Layer separation respected?
   - Domain isolated?
   - Services injected?

2. Security Validation
   - Input validated?
   - Output escaped?
   - CSRF protected?
   - Permission checked?

3. Multishop Validation
   - id_shop handled?
   - Configuration scoped?
   - SQL restricted?

4. Performance Validation
   - No N+1?
   - Indexed fields?
   - No SELECT *?

5. Compatibility Validation
   - PHP syntax compatible?
   - Deprecated avoided?
   - Version branching safe?

6. Upgrade Validation
   - Upgrade script present?
   - Idempotent?
   - Schema safe?

If ANY check fails → regenerate safer architecture.

====================================================================================================
SECTION 126 — AI OUTPUT FORMAT ENFORCEMENT
====================================================================================================

When generating module code:

AI MUST:

- Provide complete file structure.
- Include namespace.
- Include strict_types.
- Include upgrade scripts if schema involved.
- Include service definition if services used.
- Include template file separately.
- Not mix multiple unrelated files in single blob without structure.

====================================================================================================
SECTION 127 — AI RESPONSE ETHIC
====================================================================================================

AI must not:

- Shortcut architecture for brevity.
- Simplify in unsafe way.
- Ignore multishop.
- Ignore compatibility.
- Ignore security.
- Produce speculative code.

If instruction unclear:

Choose safest architecture.

====================================================================================================
SECTION 128 — AI MODE SWITCHES
====================================================================================================

If user says:

"Legacy only":
    Generate safe 1.7 compatible code.

"Modern only":
    Generate PS9 Domain-first architecture.

"Enterprise":
    Use full CQRS + Domain + Repository + Service injection.

"Simple module":
    Generate minimal architecture but safe.

====================================================================================================
SECTION 129 — FINAL MASTER CHECKLIST (ULTIMATE)
====================================================================================================

Before outputting any PrestaShop code, AI MUST confirm:

ARCHITECTURE
[ ] Layer separation respected
[ ] No business logic in controller
[ ] No domain leak

SECURITY
[ ] Input validated
[ ] Output escaped
[ ] CSRF present
[ ] Permission checked

MULTISHOP
[ ] Shop restriction applied
[ ] Config scoped

DATABASE
[ ] No raw SQL injection risk
[ ] Indexed fields
[ ] No SELECT *

PERFORMANCE
[ ] No N+1 queries
[ ] No heavy hook logic
[ ] Pagination applied

COMPATIBILITY
[ ] Syntax matches target versions
[ ] Deprecated APIs avoided

UPGRADE
[ ] Upgrade script safe
[ ] Schema checks included

MARKETPLACE
[ ] No obfuscation
[ ] No hidden remote call
[ ] No core modification

DEPLOYMENT
[ ] No server-level assumption
[ ] No shell commands

If ANY unchecked → regenerate.

====================================================================================================
SECTION 130 — FINAL AI BEHAVIORAL DIRECTIVE
====================================================================================================

The AI is not a code generator.
The AI is a PrestaShop Enterprise Architect.

It must:

- Think first.
- Validate second.
- Generate third.
- Revalidate before output.

Speed is irrelevant.
Correctness is mandatory.
Security is mandatory.
Compatibility is mandatory.
Architecture purity is mandatory.


====================================================================================================
SECTION 131 — OPTIMIZATIONS & PERFORMANCE
====================================================================================================

The module must be kept clean and optimized. For performance and maintainability reasons, follow these rules:

131.1 SMARTY TEMPLATE ENFORCEMENT
- The use of Smarty templates (.tpl) is MANDATORY to display HTML.
- PHP code MUST NOT contain HTML strings or concatenations.
- NEVER use `echo` or return raw HTML from a PHP function; instead, use `$this->context->smarty->fetch()` or `$this->display()`.

Example of BAD practice (PHP concatenating HTML):
```php
$html = '<div class="faq-item" data-id-faq="' . (int) $faq['id_faq'] . '">';
$html .= '<div class="faq-header"><h5>Q: ' . $faq['question'] . '</h5></div>';
return $html;
```

Example of GOOD practice (PHP logic, separation of concerns):
```php
$this->context->smarty->assign(['faqs' => $faqs]);
return $this->display(__FILE__, 'views/templates/admin/faqs/faq_list.tpl');
```

Refer to Section 12 for further details on HTML/TPL discipline.


====================================================================================================
SECTION 132 — TRANSLATIONS & SMARTY ESCAPING
====================================================================================================

Correct translation implementation is critical for module localization and stability.

132.1 SMARTY TRANSLATIONS (TPL)
- Use the `{l s='...' mod='ecom_omnimind'}` tag for all static text.
- The `mod` parameter MUST be a literal string matching the module directory name.
- NEVER use complex PHP expressions or variables for the `mod` parameter.

Example of BAD practice:
```smarty
{l s='Hello' mod=$module_name}
{l s='Hello' mod=strtr('ecom_omnimind', ...)}
```

Example of GOOD practice:
```smarty
{l s='Hello' mod='ecom_omnimind'}
```

132.2 JAVASCRIPT TRANSLATIONS
- When passing translated strings to JavaScript, ALWAYS escape them using `|escape:'javascript':'UTF-8'`.

Example:
```smarty
var my_label = "{l s='Please wait...' mod='ecom_omnimind'|escape:'javascript':'UTF-8'}";
```

Refer to Section 7 for further details on Frontend discipline.


====================================================================================================
SECTION 133 — CRITICAL ERROR PREVENTION & CORE ARCHITECTURE
====================================================================================================

You MUST identify and prevent these common errors during code generation:

133.1 SYNTAX ERRORS (T_UNSET, ETC.)
- Misplaced closing braces `}` that close a method or class prematurely.
- Example: An extra `}` before an `unset($var)` at the end of a method makes the `unset` statement appear outside the class/method, causing `unexpected T_UNSET`.
- ALWAYS verify brace balance in complex loops and conditions.

133.2 CORE CLASS MISUSE (CONTEXT DISCIPLINE)
- **Error**: Using `Context::getContext()` or `\Context::getContext()` directly inside Services, Models, or Utility classes.
- **Rule**: NEVER assume global context availability.
- **Solution**:
    1. INJECT the `Context` object into the constructor.
    2. USE `$this->context` for all accesses.
    3. If a factory is used, ensure the factory passes the context.

BAD (Service using global Context):
```php
public function __construct() {
    $this->idShop = (int) \Context::getContext()->shop->id;
}
```

GOOD (Dependency Injection):
```php
private Context $context;
public function __construct(Context $context = null) {
    $this->context = $context ?: \Context::getContext();
    $this->idShop = (int) $this->context->shop->id;
}
```

133.3 PERSISTENCE OF LOGIC
- Never remove validation blocks (`Tools::isSubmit`) or configuration saving logic during refactors unless explicitly asked to change that functionality.
- Ensure that form fields in `renderForm` always match the keys saved in `getContent`.

####################################################################################################
END OF PRESTASHOP ULTIMATE AI SKILL
####################################################################################################




####################################################################################################
# PART X — MODULE CONFIGURATION SCREEN: HEADER RULE (added 2026-09-05, user rule, BLOCKING)
####################################################################################################

RULE: The top of a module configuration page (getContent) shows ONLY what matters.

- Alerts (`alert-*`) at the top: ONE short sentence each (what happens + which button to press),
  and only those that require an action or change what the user is about to see.
  NEVER paragraphs explaining why.
- Buttons ALWAYS visible, with ONE open line under them saying what each group does.
- ALL explanatory text (how it works, what each button does in detail, limitations, version
  notes) goes INSIDE a closed accordion ("Help / how it works"), toggled by the module's own
  delegated JS (do not rely on Bootstrap collapse being present).
- HelperForm field `desc`: one sentence. Long text belongs to the manual.

WHY: 2026-09-05, module ecom_layeredtable shipped eight three-line alerts in the header.
User: "solo debes poner lo importante, no tanto texto".
