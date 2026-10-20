# ICTServe Development Guidelines

**System**: ICTServe v3.5.0 (True Hybrid Architecture)  
**Framework**: Laravel 12.40.1, PHP 8.2.12  
**Standards**: ISO/IEC/IEEE 15288, 12207, 29148, 42010, ISO 8000, ISO/IEC 27701, WCAG 2.2 AA, OWASP ASVS L2, MyGOV Digital Service Standards v2.1.0  
**Last Updated**: December 3, 2025  
**Documentation**: D00-D17 (System Overview → Queue Management)

---

## System Architecture Overview

ICTServe operates as a **True Hybrid Architecture** internal platform for MOTAC staff (v3.5.0):

### Core Architecture Components

- **Guest Access**: Quick submission forms without login (tracked via status tokens)
- **Authenticated Access**: Staff login via Laravel Breeze 2.3.8 with self-registration (@motac.gov.my)
- **Google Workspace SSO**: Optional OAuth 2.0 login (Laravel Socialite 5.x) for @motac.gov.my accounts
- **Admin Panel**: Filament 4.1.10 for `admin` and `superuser` roles with 2FA (TOTP) for superuser
- **Dual Audit System**:
  - Owen-it Laravel Auditing v14.x (field-level compliance audit, 7-year retention)
  - Spatie Activity Log v4.x (user activity logging for operations)
- **Real-time Communication**: Laravel Reverb 1.6.2 WebSocket server + Laravel Echo 2.2.6 client
- **Performance Monitoring**: Laravel Pulse 1.3.0 (admin/superuser only, 7-day retention)
- **API Authentication**: Laravel Sanctum 4.0 (token-based API with abilities and expiration)
- **Debugging**: Laravel Telescope 5.x (superuser only, unrestricted access)

### Key Architectural Principles

1. **Hybrid Data Association**: Nullable `user_id` FK in `helpdesk_tickets` and `loan_applications`
   - If `Auth::check()` === true: Link submission to `user_id`
   - If false: `user_id` = NULL, fallback to `submitter_email`
   - Email notifications always sent to `submitter_email`

2. **True Hybrid User Flow**:
   - **Staff Option A**: Login → My Dashboard → Auto-fill forms → View history
   - **Staff Option B**: Quick access → Guest forms → Manual entry → Token tracking
   - **Admin/Superuser**: Filament panel → Process tickets/loans → Monitor performance

3. **Security Layers**:
   - CSRF protection for all forms
   - Rate limiting (60 req/min for guest routes, 60 req/min for API)
   - reCAPTCHA Enterprise (invisible mode) for guest forms
   - ClamAV virus scanning for file uploads
   - 2FA (TOTP) for superuser accounts
   - Token hashing (SHA-512) for approval and status tokens

---

## Code Quality Standards

### PHP Standards (PHP 8.2.12)

#### Strict Typing Declaration
**ALWAYS** start PHP files with strict type declaration:

```php
<?php

declare(strict_types=1);
```

**Frequency**: 100% of analyzed PHP files follow this pattern.
**Compliance**: ISO/IEC/IEEE 5055 (Software Quality)

#### Type Hints

Use explicit type hints for all parameters and return types:

```php
public function handle(Request $request, Closure $next): Response
{
    // Implementation
}

private function calculateDepth(?InternalComment $comment): int
{
    // Implementation
}
```

**Pattern**: All methods have explicit return types, nullable types use `?` prefix.

#### Constructor Property Promotion (PHP 8.2)

Use constructor property promotion for dependency injection:

```php
public function __construct(
    private readonly SecurityMonitoringService $securityMonitoring,
    private readonly EmailNotificationService $emailService,
) {}
```

**Frequency**: 100% of service classes use this pattern.
**Note**: Use `readonly` for immutable dependencies.

#### Match Expressions

Prefer `match` over `switch` for value returns:

```php
return match ($operator) {
    '=' => $entityValue == $expectedValue,
    '>' => $entityValue > $expectedValue,
    'in' => in_array($entityValue, (array) $expectedValue),
    default => false,
};
```

### Naming Conventions

#### Class Names

- **Services**: `{Purpose}Service` (e.g., `EmailNotificationService`, `SLAManagementService`)
- **Middleware**: `{Purpose}Middleware` (e.g., `SecurityMonitoringMiddleware`)
- **Volt Components**: `kebab-case` filenames (e.g., `ticket-form.blade.php`)
- **Filament Resources**: `{Model}Resource` (e.g., `HelpdeskTicketResource`)
- **Enums**: PascalCase (e.g., `LoanStatus`, `TicketPriority`)

#### Method Names

- **Public methods**: Descriptive verbs (e.g., `sendTicketCreatedNotification`, `calculateDueDates`)
- **Volt Actions**: Variables storing closures (e.g., `$save`, `$increment`, `$submit`)
- **Boolean methods**: Start with `is`, `has`, `can` (e.g., `isGuestSubmission`, `canApprove`)

#### Variable Names

- **Descriptive names**: `$ticketNumber`, `$submitterEmail`, `$approvalToken`
- **Collections**: Plural nouns (e.g., `$tickets`, `$applications`)
- **Single items**: Singular nouns (e.g., `$ticket`, `$application`)

### Documentation Standards

#### PHPDoc Blocks

Include PHPDoc with traceability to requirements:

```php
/**
 * HelpdeskTicket Model - Enhanced with Hybrid Architecture Support
 *
 * Supports both guest submissions (no user_id) and authenticated submissions.
 * Integrates with asset loan system for cross-module functionality.
 *
 * @see D03 Software Requirements Specification - Requirement 1, 2
 * @see D04 Software Design Document - Hybrid Architecture
 * @see D09 Database Documentation - helpdesk_tickets table
 *
 * @property int|null $user_id Nullable FK for hybrid support
 * @property string|null $guest_email Email for guest submissions
 */
```

#### Attributes (PHP 8+)

Prefer native Attributes over PHPDoc annotations:

```php
#[Override]
public function render(): View
{
    // ...
}

#[Computed(persist: true)]
public function stats(): array
{
    // ...
}
```

---

## Architectural Patterns

### Service Layer Pattern

#### Service Class Structure

```php
<?php

declare(strict_types=1);

namespace App\Services\Helpdesk;

class HelpdeskService
{
    public function __construct(
        private readonly EmailNotificationService $emailService,
        private readonly SLAManagementService $slaService,
    ) {}

    public function createTicket(array $data): HelpdeskTicket
    {
        // Orchestrate business logic
        // 1. Validate data
        // 2. Create ticket
        // 3. Send notifications
        // 4. Calculate SLA
    }
}
```

**Pattern Frequency**: All business logic extracted to service classes.
**Compliance**: ISO/IEC/IEEE 42010 (Architecture Description)

### Hybrid Data Association Pattern

**CRITICAL**: ICTServe uses nullable `user_id` FK for hybrid guest/authenticated support (D03 SRS-DATA-001, D04 §4.1, D09 §5.3):

```php
// In HelpdeskTicket model (app/Models/HelpdeskTicket.php)
public function isGuestSubmission(): bool
{
    return $this->user_id === null;
}

public function getSubmitterEmail(): string
{
    return $this->user_id 
        ? $this->user->email 
        : $this->submitter_email; // Note: field name is submitter_email, not guest_email
}

public function getSubmitterName(): string
{
    return $this->user_id 
        ? $this->user->name 
        : $this->submitter_name;
}

// In service layer (app/Services/Helpdesk/HelpdeskService.php)
public function createTicket(array $data): HelpdeskTicket
{
    $ticket = new HelpdeskTicket();
    
    if (Auth::check()) {
        // Authenticated staff submission
        $ticket->user_id = Auth::id();
        $ticket->submitter_name = Auth::user()->name;
        $ticket->submitter_email = Auth::user()->email;
        $ticket->submitter_phone = Auth::user()->phone;
        $ticket->submitter_division_code = Auth::user()->department?->code;
        $ticket->submitter_grade = Auth::user()->grade;
    } else {
        // Guest submission
        $ticket->user_id = null;
        $ticket->submitter_name = $data['submitter_name'];
        $ticket->submitter_email = $data['submitter_email'];
        $ticket->submitter_phone = $data['submitter_phone'];
        $ticket->submitter_division_code = $data['submitter_division_code'];
        $ticket->submitter_grade = $data['submitter_grade'] ?? null;
    }
    
    // Common fields
    $ticket->ticket_number = $this->generateTicketNumber();
    $ticket->form_reference_code = 'PK.(S).MOTAC.07.(L1)'; // Official form code
    $ticket->category = $data['category'];
    $ticket->priority = $data['priority'];
    $ticket->description = $data['description'];
    $ticket->status = TicketStatus::Open;
    $ticket->status_token_hash = $this->tokenService->generateStatusToken();
    
    $ticket->save();
    
    // Trigger dual audit logging
    activity('helpdesk')
        ->performedOn($ticket)
        ->causedBy(Auth::user())
        ->log('Ticket created');
    
    return $ticket;
}
```

**Database Schema** (D09 §5.3):

- `user_id`: bigint, FK nullable → users.id (NULL for guest, NOT NULL for authenticated)
- `submitter_*`: Always populated (from user profile if authenticated, from form if guest)
- `form_reference_code`: VARCHAR(50), stores official form code (e.g., 'PK.(S).MOTAC.07.(L1)')
- `status_token_hash`: VARCHAR(128), SHA-512 hash for guest status checking

**Requirements**:

- D03 SRS-DATA-001 (Hybrid Data Association)
- D03 SRS-AUTH-001 (Dual Entry Model)
- D03 SRS-FORM-001 (Auto-fill Data)
- D04 §4.1 (Helpdesk Module Design)
- D09 §5.3 (helpdesk_tickets table)

### Livewire & Volt Component Patterns

#### Volt Functional API (Preferred)

For UI components, use the Volt Functional API:

```php
<?php

use App\Models\HelpdeskTicket;
use function Livewire\Volt\{state, rules, mount};

state(['subject' => '', 'description' => '', 'ticketId']);

rules([
    'subject' => 'required|min:5|max:255',
    'description' => 'required|min:10',
]);

$submit = function () {
    $this->validate();
    
    HelpdeskTicket::create([
        'subject' => $this->subject,
        'description' => $this->description,
        'user_id' => Auth::id(), // Nullable for hybrid support
    ]);
    
    $this->redirect(route('helpdesk.success'));
};

?>

<div>
    <input wire:model="subject" type="text" />
    <textarea wire:model="description"></textarea>
    <button wire:click="submit">Submit</button>
</div>
```

#### Class-Based Volt

For complex components requiring extensive lifecycle management:

```php
<?php

use Livewire\Volt\Component;
use Livewire\Attributes\Layout;

new #[Layout('layouts.app')] class extends Component {
    public string $subject = '';
    public string $description = '';
    
    public function mount(): void
    {
        if (Auth::check()) {
            // Auto-fill from user profile
            $this->subject = Auth::user()->default_subject ?? '';
        }
    }
    
    public function submit(): void
    {
        $this->validate([
            'subject' => 'required|min:5',
            'description' => 'required|min:10',
        ]);
        
        // Create ticket with hybrid support
    }
}
?>
```

### Middleware Pattern

#### Security Middleware

```php
<?php

declare(strict_types=1);

namespace App\Http\Middleware;

class SecurityMonitoringMiddleware
{
    public function __construct(
        private readonly SecurityMonitoringService $securityMonitoring
    ) {}

    public function handle(Request $request, Closure $next): Response
    {
        if ($this->securityMonitoring->isIpBlocked($request->ip())) {
            abort(429, 'Too Many Requests');
        }

        return $next($request);
    }
}
```

---

## Security Patterns

### Input Validation

#### Livewire Validation

Use the `#[Validate]` attribute or `rules()` method:

```php
use Livewire\Attributes\Validate;

#[Validate('required|string|max:1000')]
public string $comment = '';

// Or using rules() method
rules(['comment' => 'required|string|max:1000']);
```

#### Pattern Detection

Use regex patterns within Service classes to detect threats:

```php
if (preg_match($sqlPattern, $input)) {
    $this->security->logSuspiciousActivity('SQL Injection', $context);
    throw new SecurityException('Suspicious input detected');
}
```

### Authorization Checks

#### Policy Usage

Always use Policies via the `authorize` method:

```php
// In Volt component
$delete = function (HelpdeskTicket $ticket) {
    $this->authorize('delete', $ticket);
    $ticket->delete();
};

// In controller
public function destroy(HelpdeskTicket $ticket)
{
    $this->authorize('delete', $ticket);
    $ticket->delete();
    return redirect()->route('helpdesk.index');
}
```

### Logging Security Events

#### Structured Logging

```php
Log::channel('security')->warning('Suspicious Activity', [
    'user_id' => Auth::id(),
    'ip' => $request->ip(),
    'action' => 'file_upload_blocked',
    'reason' => 'Invalid file type',
]);
```

---

## Data Handling Patterns

### Collection Processing

#### Map Transformations

```php
return $tickets->map(fn (HelpdeskTicket $ticket) => [
    'number' => $ticket->ticket_number,
    'status' => $ticket->status->label(),
    'submitter' => $ticket->getSubmitterName(),
]);
```

### Eager Loading

#### Deep Relationships

Prevent N+1 queries by loading relationships upfront:

```php
$tickets = HelpdeskTicket::with([
    'user',
    'division',
    'category',
    'comments.user',
    'attachments',
])->paginate(15);
```

### Hybrid Data Queries

#### Guest vs Authenticated Filtering

```php
// Get all tickets for current user (authenticated or guest)
public function getUserTickets(): Collection
{
    if (Auth::check()) {
        return HelpdeskTicket::where('user_id', Auth::id())->get();
    }
    
    // Guest: use session token or email
    $email = session('guest_email');
    return HelpdeskTicket::whereNull('user_id')
        ->where('guest_email', $email)
        ->get();
}
```

---

## Frontend Patterns (Alpine.js)

### State Management

#### Entangle

Sync server-side state with client-side state:

```html
<div x-data="{ open: @entangle('isOpen') }">
    <div x-show="open">...</div>
</div>
```

### Accessibility Enhancer Pattern

#### Focus Management

```javascript
document.addEventListener('livewire:navigated', () => {
    // Reset focus to top of main content on navigation
    document.getElementById('main-content')?.focus();
});
```

---

## Localization Patterns

### Translation Keys

#### Namespaced Keys

```php
__('helpdesk.ticket_created_success')
__('loan.application_submitted')
__('common.motac_full_name')
```

### Bilingual Content

#### Fallback Pattern

```php
'category' => $ticket->category?->name_en ?? 'N/A',
'division' => $user->division?->name_ms ?? 'Tiada',
```

---

## Testing Patterns

### Component Testing (Volt)

#### Volt Test Structure

**Note**: For PHPUnit 12, use PHP 8 attributes (`#[Test]`) instead of PHPDoc `@test` annotations.

```php
use Livewire\Volt\Volt;
use PHPUnit\Framework\Attributes\Test;

#[Test]
public function authenticated_user_can_create_ticket(): void
{
    // For Pest-style tests, use:
    // test('authenticated user can create ticket', function () {
    $user = User::factory()->create();

    Volt::test('helpdesk.ticket-form')
        ->actingAs($user)
        ->set('subject', 'Test Ticket')
        ->set('description', 'Test description')
        ->call('submit')
        ->assertHasNoErrors();

    $this->assertDatabaseHas('helpdesk_tickets', [
        'subject' => 'Test Ticket',
        'user_id' => $user->id,
    ]);
});

test('guest can create ticket without login', function () {
    Volt::test('helpdesk.ticket-form')
        ->set('subject', 'Guest Ticket')
        ->set('description', 'Guest description')
        ->set('guest_email', 'guest@example.com')
        ->call('submit')
        ->assertHasNoErrors();

    $this->assertDatabaseHas('helpdesk_tickets', [
        'subject' => 'Guest Ticket',
        'user_id' => null,
        'guest_email' => 'guest@example.com',
    ]);
});
```

**Pattern**: Setup → Volt::test → Action → Assertion.

---

## Performance Patterns

### Query Optimization

#### Attribute Scopes

Use PHP 8 Attributes for global scopes:

```php
#[ScopedBy(ActiveScope::class)]
class HelpdeskTicket extends Model
{
    // ...
}
```

### Caching Strategies

#### Computed Properties

Use the `#[Computed]` attribute with caching:

```php
use Livewire\Attributes\Computed;

#[Computed(persist: true, seconds: 3600)]
public function metrics(): array
{
    return $this->service->calculateMetrics();
}
```

---

## Error Handling Patterns

### Validation Errors

#### Flash Messages

```php
session()->flash('error', __('messages.operation_failed'));
return;
```

### Exception Handling

#### Service Layer

```php
public function createTicket(array $data): HelpdeskTicket
{
    try {
        DB::beginTransaction();
        
        $ticket = HelpdeskTicket::create($data);
        $this->emailService->sendTicketCreatedNotification($ticket);
        
        DB::commit();
        return $ticket;
    } catch (\Exception $e) {
        DB::rollBack();
        Log::error('Ticket creation failed', [
            'error' => $e->getMessage(),
            'data' => $data,
        ]);
        throw new TicketCreationException('Failed to create ticket', 0, $e);
    }
}
```

---

## Code Organization Principles

### Single Responsibility

- **Services**: Business logic orchestration
- **Volt Components**: UI logic and state management
- **Controllers**: Routing and HTTP response handling (minimal logic)
- **Models**: Data representation and relationships

### Dependency Injection

All dependencies injected via constructor in Classes, or resolved via `app()`/method injection in Functional Volt.

---

## Common Idioms

### Null-Safe Operator

```php
$ticket->user?->name ?? 'Guest User'
$application->approver?->email ?? 'No approver'
```

### Match Expressions

```php
$statusColor = match ($status) {
    LoanStatus::Approved => 'green',
    LoanStatus::Pending => 'yellow',
    LoanStatus::Rejected => 'red',
    default => 'gray',
};
```

---

## Accessibility Standards (WCAG 2.2 AA)

### Implementation Patterns

- **Livewire Loading**: Use `wire:loading.attr="aria-busy"` to indicate processing states
- **Focus Trap**: Use Alpine's `x-trap` for modals
- **Semantic HTML**: Use proper heading hierarchy (`h1` → `h2` → `h3`)
- **Color Contrast**: Minimum 4.5:1 for text, 3:1 for UI components
- **Touch Targets**: Minimum 44x44 pixels for interactive elements
- **Keyboard Navigation**: All interactive elements accessible via keyboard

### ARIA Attributes

```html
<button 
    wire:click="submit" 
    aria-label="{{ __('Submit ticket') }}"
    aria-busy="false"
    wire:loading.attr="aria-busy=true"
>
    {{ __('Submit') }}
</button>
```

---

## Dual Audit System (D09 §4.6, §4.7, D11 §8)

ICTServe implements a **mandatory dual audit system** for compliance and operational monitoring:

### Owen-it Laravel Auditing v14.x (Compliance Audit)

**Purpose**: Field-level audit trail for PDPA 2010 compliance with 7-year retention (D09 §4.6).

**Features**:

- Tracks old/new values for all auditable fields
- Immutable records (cannot be updated or deleted)
- IP address hashing for privacy
- Automatic retention policy enforcement

```php
<?php

declare(strict_types=1);

namespace App\Models;

use OwenIt\Auditing\Contracts\Auditable;
use Illuminate\Database\Eloquent\Model;

class HelpdeskTicket extends Model implements Auditable
{
    use \OwenIt\Auditing\Auditable;
    
    /**
     * Fields to include in audit trail
     * @see D09 §4.6 - Compliance audit requirements
     */
    protected $auditInclude = [
        'status',
        'priority',
        'assigned_admin_id',
        'category',
        'sla_due_at',
    ];
    
    /**
     * Exclude sensitive fields from audit
     */
    protected $auditExclude = [
        'status_token_hash', // Security token
    ];
    
    /**
     * Generate audit tags for categorization
     */
    public function generateTags(): array
    {
        return [
            'helpdesk',
            'ticket:' . $this->ticket_number,
            'priority:' . $this->priority->value,
        ];
    }
}
```

**Database Table**: `audits` (D09 §4.6)

- `id`: bigint PK
- `user_type`: string (morphable)
- `user_id`: bigint (morphable)
- `event`: string (created, updated, deleted)
- `auditable_type`: string (morphable)
- `auditable_id`: bigint (morphable)
- `old_values`: JSON (previous field values)
- `new_values`: JSON (new field values)
- `url`: string (request URL)
- `ip_address`: string (hashed for privacy)
- `user_agent`: string
- `tags`: string (comma-separated)
- `created_at`: timestamp (immutable)

### Spatie Activity Log v4.x (Operations Audit)

**Purpose**: User activity logging for operational dashboards and real-time monitoring (D09 §4.7).

**Features**:

- High-level activity descriptions
- Subject and causer tracking
- Custom properties for context
- Log name categorization

```php
<?php

declare(strict_types=1);

namespace App\Models;

use Spatie\Activitylog\Traits\LogsActivity;
use Spatie\Activitylog\LogOptions;
use Illuminate\Database\Eloquent\Model;

class HelpdeskTicket extends Model
{
    use LogsActivity;
    
    /**
     * Configure activity logging
     * @see D09 §4.7 - Operations audit requirements
     */
    public function getActivitylogOptions(): LogOptions
    {
        return LogOptions::defaults()
            ->logOnly(['status', 'priority', 'assigned_admin_id'])
            ->logOnlyDirty() // Only log changed attributes
            ->dontSubmitEmptyLogs()
            ->useLogName('helpdesk') // Categorize logs
            ->setDescriptionForEvent(fn(string $eventName) => match($eventName) {
                'created' => 'Ticket created',
                'updated' => 'Ticket updated',
                'deleted' => 'Ticket deleted',
                default => "Ticket {$eventName}",
            });
    }
    
    /**
     * Tap into activity before saving
     */
    public function tapActivity(Activity $activity, string $eventName): void
    {
        $activity->properties = $activity->properties->merge([
            'ticket_number' => $this->ticket_number,
            'submitter_email' => $this->submitter_email,
            'is_guest' => $this->isGuestSubmission(),
        ]);
    }
}
```

**Manual Activity Logging**:

```php
// In service layer or controller
activity('helpdesk')
    ->performedOn($ticket)
    ->causedBy(Auth::user())
    ->withProperties([
        'action' => 'status_changed',
        'old_status' => $oldStatus,
        'new_status' => $newStatus,
    ])
    ->log('Ticket status changed from ' . $oldStatus . ' to ' . $newStatus);
```

**Database Table**: `activity_log` (D09 §4.7)

- `id`: bigint PK
- `log_name`: string (category)
- `description`: text (human-readable)
- `subject_type`: string (morphable)
- `subject_id`: bigint (morphable)
- `causer_type`: string (morphable)
- `causer_id`: bigint (morphable)
- `properties`: JSON (custom data)
- `event`: string (nullable)
- `batch_uuid`: UUID (for batch operations)
- `created_at`: timestamp

### Unified Audit Log Viewer (Filament)

**Location**: `app/Filament/Pages/UnifiedAuditLog.php`

**Features**:

- Combined view of compliance audits and activity logs
- Filtering by date range, user, action type, entity
- Export to CSV/PDF
- Real-time updates via Laravel Reverb
- Restricted to `superuser` role only

```php
// Access control
public static function canAccess(): bool
{
    return Auth::user()?->hasRole('superuser') ?? false;
}
```

**Requirements**:

- D03 SRS-ADM-002 (Role-based access control)
- D09 §4.6 (Compliance audit)
- D09 §4.7 (Operations audit)
- D11 §8 (Security design)

---

## Real-time Communication (Laravel Reverb)

### Broadcasting Events

```php
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;

class TicketUpdated implements ShouldBroadcast
{
    public function __construct(
        public HelpdeskTicket $ticket
    ) {}
    
    public function broadcastOn(): array
    {
        return [
            new PrivateChannel('admin.tickets'),
            new PrivateChannel('user.' . $this->ticket->user_id),
        ];
    }
}
```

### Client-side Listening (Laravel Echo)

```javascript
Echo.private(`user.${userId}`)
    .listen('TicketUpdated', (e) => {
        console.log('Ticket updated:', e.ticket);
        // Update UI
    });
```

---

## API Authentication (Laravel Sanctum)

### Token Generation

```php
$token = $user->createToken('api-token', [
    'read:tickets',
    'write:tickets',
])->plainTextToken;
```

### Token Validation

```php
// In routes/api.php
Route::middleware(['auth:sanctum', 'ability:read:tickets'])
    ->get('/tickets', [ApiTicketController::class, 'index']);
```

---

## Laravel Pulse Performance Monitoring (v3.5.0)

**Purpose**: Real-time application performance monitoring for `admin` and `superuser` roles (D00 §4, D03 SRS-ADM-007).

### Configuration

**Installation** (already included in v3.5.0):

```bash
composer require laravel/pulse
php artisan vendor:publish --provider="Laravel\Pulse\PulseServiceProvider"
php artisan migrate
```

**Access Control** (`app/Providers/PulseServiceProvider.php`):

```php
<?php

declare(strict_types=1);

namespace App\Providers;

use Illuminate\Support\Facades\Gate;
use Laravel\Pulse\PulseServiceProvider as BasePulseServiceProvider;

class PulseServiceProvider extends BasePulseServiceProvider
{
    /**
     * Restrict Pulse access to admin and superuser only
     * @see D03 SRS-ADM-007
     */
    public function boot(): void
    {
        Gate::define('viewPulse', function ($user) {
            return $user->hasAnyRole(['admin', 'superuser']);
        });
    }
}
```

### Monitored Metrics

1. **Slow Queries** (>500ms threshold)
2. **Queue Job Metrics** (success/failure rates, processing times)
3. **Request Response Times** (average, p95, p99)
4. **Server Health** (CPU, memory, disk usage)
5. **Cache Hit/Miss Rates**
6. **Exception Tracking**

### Data Retention

- **Retention Period**: 7 days (configurable in `config/pulse.php`)
- **Automatic Pruning**: Daily via scheduled command
- **Storage**: `pulse_entries`, `pulse_values`, `pulse_aggregates` tables (D09 §4.1)

### Dashboard Access

**URL**: `/pulse`  
**Roles**: `admin`, `superuser` only  
**Features**:

- Real-time metrics updates
- Historical trend charts
- Drill-down into specific queries/jobs
- Export capabilities

## Laravel Sanctum API Authentication (v3.5.0)

**Purpose**: Token-based API authentication for future mobile apps and external integrations (D00 §4, D03 SRS-ADM-008).

### Token Generation

```php
<?php

declare(strict_types=1);

namespace App\Services\Api;

use App\Models\User;
use Laravel\Sanctum\PersonalAccessToken;

class ApiTokenService
{
    /**
     * Create API token with abilities
     * @see D03 SRS-ADM-008
     */
    public function createToken(User $user, string $name, array $abilities = ['*']): string
    {
        $token = $user->createToken($name, $abilities, now()->addDays(30));
        
        // Log token creation for audit
        activity('api')
            ->performedOn($user)
            ->causedBy($user)
            ->withProperties([
                'token_name' => $name,
                'abilities' => $abilities,
                'expires_at' => now()->addDays(30),
            ])
            ->log('API token created');
        
        return $token->plainTextToken;
    }
    
    /**
     * Revoke token
     */
    public function revokeToken(PersonalAccessToken $token): void
    {
        activity('api')
            ->performedOn($token->tokenable)
            ->causedBy(Auth::user())
            ->withProperties([
                'token_name' => $token->name,
            ])
            ->log('API token revoked');
        
        $token->delete();
    }
}
```

### API Routes with Abilities

```php
// routes/api.php
Route::middleware(['auth:sanctum', 'ability:read:tickets'])
    ->get('/tickets', [ApiTicketController::class, 'index']);

Route::middleware(['auth:sanctum', 'ability:write:tickets'])
    ->post('/tickets', [ApiTicketController::class, 'store']);

Route::middleware(['auth:sanctum', 'ability:read:loans'])
    ->get('/loans', [ApiLoanController::class, 'index']);

Route::middleware(['auth:sanctum', 'ability:admin:all'])
    ->group(function () {
        Route::get('/admin/stats', [ApiAdminController::class, 'stats']);
        Route::post('/admin/config', [ApiAdminController::class, 'updateConfig']);
    });
```

### Available Abilities

- `read:tickets` - View helpdesk tickets
- `write:tickets` - Create/update helpdesk tickets
- `read:loans` - View loan applications
- `write:loans` - Create/update loan applications
- `admin:all` - Full admin access (admin/superuser only)

### Rate Limiting

**Configuration** (`bootstrap/app.php`):

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->throttleApi('60,1'); // 60 requests per minute
})
```

## Google Workspace SSO (Optional, v3.5.0)

**Purpose**: OAuth 2.0 authentication for @motac.gov.my accounts (D00 §4, D03 SRS-AUTH-005).

### Configuration

**Installation**:

```bash
composer require laravel/socialite
```

**Environment Variables** (`.env`):

```env
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_REDIRECT_URI=https://ictserve.motac.gov.my/auth/google/callback
```

### Service Implementation

```php
<?php

declare(strict_types=1);

namespace App\Services\Auth;

use App\Models\User;
use Laravel\Socialite\Facades\Socialite;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;

class GoogleSsoService
{
    /**
     * Redirect to Google OAuth
     */
    public function redirectToGoogle(): \Symfony\Component\HttpFoundation\RedirectResponse
    {
        return Socialite::driver('google')
            ->scopes(['email', 'profile'])
            ->redirect();
    }
    
    /**
     * Handle Google callback
     * @see D03 SRS-AUTH-005
     */
    public function handleGoogleCallback(): User
    {
        $googleUser = Socialite::driver('google')->user();
        
        // Validate @motac.gov.my domain
        if (!Str::endsWith($googleUser->getEmail(), '@motac.gov.my')) {
            throw new \Exception('Only @motac.gov.my accounts are allowed');
        }
        
        // Find or create user
        $user = User::where('email', $googleUser->getEmail())->first();
        
        if (!$user) {
            // Auto-create account for new Google users
            $user = User::create([
                'name' => $googleUser->getName(),
                'email' => $googleUser->getEmail(),
                'google_id' => $googleUser->getId(),
                'email_verified_at' => now(),
                'password' => Hash::make(Str::random(32)), // Random password
                'role' => 'staff',
            ]);
            
            activity('auth')
                ->performedOn($user)
                ->log('Account auto-created via Google SSO');
        } else {
            // Link Google account to existing user
            $user->update(['google_id' => $googleUser->getId()]);
            
            activity('auth')
                ->performedOn($user)
                ->causedBy($user)
                ->log('Google account linked');
        }
        
        return $user;
    }
}
```

### Login UI Component

```blade
{{-- resources/views/components/auth/google-login-button.blade.php --}}
<a href="{{ route('auth.google.redirect') }}" 
   class="flex items-center justify-center gap-2 px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50"
   aria-label="{{ __('Sign in with Google') }}">
    <svg class="w-5 h-5" viewBox="0 0 24 24">
        {{-- Google logo SVG --}}
    </svg>
    <span>{{ __('Sign in with Google') }}</span>
</a>
```

## Best Practices Summary

1. **Strict Typing**: `declare(strict_types=1)` in all files (100% compliance)
2. **Volt First**: Use Volt for all new UI components (functional API preferred)
3. **Service Layer**: Extract logic to Services, keep components light (single responsibility)
4. **Hybrid Support**: Always check `Auth::check()` for guest/authenticated logic (nullable `user_id` FK)
5. **Validation**: Validate inputs server-side using `rules()` or Form Requests
6. **Authorization**: Check policies before actions (use `$this->authorize()`)
7. **Localization**: Use translation keys for all text (bilingual BM/EN support)
8. **Testing**: Write feature tests for all critical paths using `Volt::test()` or PHPUnit
9. **Accessibility**: Ensure WCAG 2.2 AA compliance (keyboard, screen reader, 4.5:1 contrast)
10. **Security**: Sanitize outputs, validate inputs, log suspicious activities
11. **Audit Trail**: Use dual audit system (Owen-it + Spatie) for all critical operations
12. **Real-time**: Use Laravel Reverb for WebSocket notifications (admin dashboard)
13. **Documentation**: Include traceability to D00-D17 requirements in PHPDoc
14. **Performance**: Eager load relationships, cache computed properties, monitor with Pulse
15. **API Security**: Use Sanctum tokens with abilities, enforce rate limiting
16. **Form Codes**: Include official form reference codes (e.g., 'PK.(S).MOTAC.07.(L1)')
17. **Token Security**: Use SHA-512 hashing for all tokens (status, approval)
18. **Database**: Use nullable `user_id` FK pattern for hybrid data association
19. **Monitoring**: Leverage Laravel Pulse for performance insights (admin/superuser only)
20. **SSO**: Support Google Workspace SSO as optional authentication method

---

## Compliance Checklist

Before committing code, verify:

- [ ] Strict typing declaration present
- [ ] All methods have explicit return types
- [ ] PHPDoc blocks include D00-D17 traceability
- [ ] Hybrid data association handled correctly (nullable `user_id`)
- [ ] Authorization policies checked
- [ ] Input validation implemented
- [ ] Audit logging configured (dual system)
- [ ] Translation keys used (no hardcoded text)
- [ ] WCAG 2.2 AA compliance verified
- [ ] Tests written and passing
- [ ] Laravel Pint formatting applied
- [ ] PHPStan analysis passing (level 5+)

---

## References

- **D00**: System Overview (v3.5.0)
- **D03**: Software Requirements Specification (v3.5.0)
- **D04**: Software Design Document (v3.5.0)
- **D09**: Database Documentation (v3.5.0)
- **D10**: Source Code Documentation (v3.5.0)
- **D12-D14**: UI/UX Design Guides (v3.5.0)
- **ISO/IEC/IEEE 15288**: Systems and software engineering
- **ISO/IEC/IEEE 12207**: Software life cycle processes
- **ISO/IEC/IEEE 29148**: Requirements engineering
- **WCAG 2.2 AA**: Web Content Accessibility Guidelines
- **OWASP ASVS L2**: Application Security Verification Standard

---

**Version**: 3.5.0  
**Last Updated**: December 3, 2025  
**Maintained By**: BPM MOTAC Development Team
