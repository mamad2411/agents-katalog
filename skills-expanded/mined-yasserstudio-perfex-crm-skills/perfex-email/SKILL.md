---
name: perfex-email
description: Use whenever the user is sending, rendering, or debugging transactional email in a Perfex CRM module — `$this->emails_model->send_simple_email`, `send_mail_template`, email template files under `views/emails/`, admin-recipient fallback chains (`my_module_admin_email` → `contact_form_notification_email` → `smtp_email`), retry queues with exponential backoff stored in `tbl<module>_email_retries`, or cron-driven retry processing via `register_cron_task()` / `after_cron_run`. Also trigger when the user says "my Perfex email isn't sending", "send_simple_email returns false", "email failed but the user saw a success page", "SMTP error in my module", "email retry queue", "why didn't my notification email go out", or "email template merge fields". Reinforces the rule that email failure must never break the user flow — always try/catch and enqueue on failure.
license: MIT
metadata:
  author: yasserstudio
  version: "1.5.0"
---

# Perfex Email System

You are a Perfex CRM email engineer. Your job is to send transactional email reliably from inside modules — using `send_simple_email` correctly, rendering email-client-safe templates, falling back gracefully when admin recipients aren't configured, and queueing retries for transient SMTP failures so the user flow never breaks.

Perfex has an email templates system (Setup → Email Templates) and a simple-send helper for ad-hoc messages. For module-owned emails that don't need user-editable templates, `send_simple_email` is the right primitive.

## The 3 send paths

| Primitive | When to use |
|---|---|
| `$this->emails_model->send_simple_email($to, $subject, $body)` | Module-owned emails, admin notifications |
| `send_mail_template('slug', ...)` | User-editable templates registered via `register_merge_fields` |
| Raw `$this->email` (CI library) | Don't. Use one of the above. |

## send_simple_email pattern

```php
public function notify_admin($contact_id, $event) {
    $this->load->model('emails_model');

    $to = $this->admin_email();
    if (!$to) return;

    $data = [
        'contact_name' => get_contact_full_name($contact_id),
        'event'        => $event,
    ];

    $body = $this->_render_email_template('admin_notification', $data);

    try {
        $sent = $this->emails_model->send_simple_email(
            $to,
            _l('my_module_admin_notification_subject'),
            $body
        );
        if (!$sent) {
            $this->enqueue_email_retry($to, $subject, $body, $data);
        }
    } catch (Throwable $e) {
        log_message('error', 'my_module: send failed: ' . $e->getMessage());
        $this->enqueue_email_retry($to, $subject, $body, $data);
    }
}
```

**Email failures MUST NOT fail the user flow.** Wrap in try/catch, log the error, continue. The user already completed their action — don't punish them because SMTP blipped.

## Admin-recipient fallback chain

When sending "notify the admin", fall back through configured options:

```php
private function admin_email() {
    return get_option('my_module_admin_email')
        ?: get_option('contact_form_notification_email')
        ?: get_option('smtp_email')
        ?: null;
}
```

Remember: `get_option('key') ?: fallback` — never pass a default as a second arg.

## Render email template with merge

Put templates in `modules/my_module/views/emails/`. Use inline styles and table layout — Gmail strips `<style>` blocks, `<div>` grids break in Outlook.

```php
private function _render_email_template($template, array $data = []) {
    extract($data);
    ob_start();
    include(__DIR__ . '/../views/emails/' . $template . '.php');
    return ob_get_clean();
}
```

Template example (`views/emails/admin_notification.php`):
```html
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:24px;">
    <tr><td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background:#fff;border-radius:8px;padding:32px;font-family:Arial,sans-serif;">
            <tr><td>
                <h1 style="margin:0 0 16px 0;font-size:20px;color:#111;">
                    New event from <?= htmlspecialchars($contact_name) ?>
                </h1>
                <p style="margin:0;color:#333;line-height:1.5;">
                    <?= htmlspecialchars($event) ?>
                </p>
            </td></tr>
        </table>
    </td></tr>
</table>
```

Always `htmlspecialchars()` user data. A newline in a name isn't a security issue but a `<script>` tag in one is.

## Retry queue pattern

SMTP can transiently fail. Don't drop the email — enqueue it:

### Schema

```sql
CREATE TABLE `tblmymodule_email_retries` (
    `id`            INT NOT NULL AUTO_INCREMENT,
    `to_email`      VARCHAR(191) NOT NULL,
    `subject`       VARCHAR(255) NOT NULL,
    `body`          LONGTEXT NOT NULL,
    `context_json`  TEXT NULL,
    `attempts`      TINYINT NOT NULL DEFAULT 0,
    `last_error`    TEXT NULL,
    `next_try_at`   DATETIME NOT NULL,
    `created_at`    DATETIME NOT NULL,
    PRIMARY KEY (`id`),
    KEY `idx_next_try` (`next_try_at`, `attempts`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Enqueue

```php
private function enqueue_email_retry($to, $subject, $body, $context = []) {
    $this->db->insert(db_prefix() . 'mymodule_email_retries', [
        'to_email'     => $to,
        'subject'      => $subject,
        'body'         => $body,
        'context_json' => json_encode($context),
        'attempts'     => 0,
        'next_try_at'  => date('Y-m-d H:i:s', strtotime('+5 minutes')),
        'created_at'   => date('Y-m-d H:i:s'),
    ]);
}
```

### Process via cron

Register with `register_cron_task()` — it runs after core cron tasks and makes the dependency explicit (see `perfex-module-dev`):

```php
// module_name.php
register_cron_task('my_module_process_email_retries');

function my_module_process_email_retries() {
    $CI =& get_instance();
    $CI->load->model('my_module/my_module_model');
    $CI->my_module_model->process_email_retries();
}
```

In the model:
```php
public function process_email_retries() {
    $this->load->model('emails_model');

    // Prune > 7 days old
    $this->db->where('created_at <', date('Y-m-d H:i:s', strtotime('-7 days')));
    $this->db->delete(db_prefix() . 'mymodule_email_retries');

    // Grab up to 50 due, attempts < 5
    $this->db->where('next_try_at <=', date('Y-m-d H:i:s'));
    $this->db->where('attempts <', 5);
    $this->db->order_by('next_try_at', 'ASC');
    $this->db->limit(50);
    $queue = $this->db->get(db_prefix() . 'mymodule_email_retries')->result();

    foreach ($queue as $row) {
        try {
            $sent = $this->emails_model->send_simple_email($row->to_email, $row->subject, $row->body);
            if ($sent) {
                $this->db->where('id', $row->id)->delete(db_prefix() . 'mymodule_email_retries');
            } else {
                $this->_bump_retry($row, 'send_simple_email returned false');
            }
        } catch (Throwable $e) {
            $this->_bump_retry($row, $e->getMessage());
        }
    }
}

private function _bump_retry($row, $error) {
    $next_attempt = $row->attempts + 1;
    // Exponential backoff: 5min, 15min, 1h, 6h, 24h
    $backoffs = [5, 15, 60, 360, 1440];
    $minutes = $backoffs[min($next_attempt - 1, count($backoffs) - 1)];
    $this->db->where('id', $row->id)->update(db_prefix() . 'mymodule_email_retries', [
        'attempts'    => $next_attempt,
        'last_error'  => $error,
        'next_try_at' => date('Y-m-d H:i:s', strtotime("+{$minutes} minutes")),
    ]);
}
```

Cap at 5 attempts. After that, alert the admin (another email!) or leave for manual review via the prune-at-7-days rule.

## Email language fallback

Perfex resolves which language to use for email templates in this order:

1. **Customer language** — if the recipient is a customer/contact, uses their profile language
2. **Staff language** — if the recipient is staff, uses their configured language
3. **Lead language** — leads use the system default language
4. **System default** — fallback when no recipient-specific language is set

If a template is empty for the resolved language, Perfex falls back to the system default language. If that's also empty, the email is **skipped** (not sent with a blank body).

Templates can be disabled per-language in **Setup → Email Templates** — a disabled template for a specific language means that notification won't fire for users configured to that language.

Two traps in how `App_mail_template::prepare()` does this:

- **Non-English template rows don't exist until an admin opens Setup → Email Templates.** Core inserts the per-language rows lazily on that page visit (the source comment says so). On a fresh install that skipped it, every non-English recipient silently gets the English template. Part of your module's install checklist: visit that page once per install.
- **Picking the template row does not switch CI's language.** `prepare()` selects the `tblemailtemplates` row for the recipient's language but never calls `$this->lang->load()` for it. Any `_l()` you use while building merge-field values runs in the *current request's* language — the staff member's, or the cron's default. A French customer gets a French template body with English labels in your merge fields. If a merge field needs translated text, look the string up explicitly for the recipient's language (load the file with `$CI->lang->load('my_module/my_module', $recipient_language)` into a scratch array, or keep a per-language map) rather than calling `_l()`.

## SMTP configuration check

If a dev environment has no SMTP configured, `send_simple_email` silently returns false. In a module's activation hook, warn:
```php
if (!get_option('smtp_host')) {
    set_alert('warning', 'My Module: SMTP is not configured. Emails will queue but never send.');
}
```

## Common SMTP pitfalls

The most common reason `send_simple_email` returns `false` or throws has nothing to do with your code — it's SMTP configuration. Know these before you debug application logic:

### 1. `smtp_host` / `smtp_port` mismatch gives misleading errors

The `Setup → Settings → Email` form accepts any value. If `smtp_host` is right but port is wrong, CI's email library throws generic "SMTP connection failed" errors that look like network problems. **Always verify** host/port against the provider's docs (Gmail: 587 TLS, Office365: 587 TLS, AWS SES: 587 TLS on regional endpoint). Port 25 almost never works on shared hosting — blocked outbound.

### 2. Enable `smtp_debug` during initial setup

Perfex has two mail engines, chosen at **Setup → Settings → Email → Mail Engine** (`mail_engine` option: `codeigniter` — the default — or `phpmailer`). `App_mailer` branches on it. There is no `mail_debug` key in either.

- **PHPMailer engine:** in `application/config/email.php`
  ```php
  $config['smtp_debug']   = 2;        // 0 off · 1 commands · 2 commands+data · 3 +connection · 4 low-level
  $config['debug_output'] = 'error_log';   // or 'html' / 'echo' — 'html' leaks the SMTP conversation into the page
  ```
  This surfaces the actual SMTP conversation. Set back to `0` before going live. With the CodeIgniter engine selected these keys do nothing.
- **CodeIgniter engine:** no config switch; call `$this->email->print_debugger()` after a failed send (pitfall 4 below).

If you can't tell why nothing changes, check which engine is selected first. Note `email.php` reads `get_option('smtp_*')` at load time — the Setup → Settings → Email values, not hardcoded ones — so a wrong value there survives config edits.

### 3. Gmail / Workspace: DMARC rejects `From:` spoofing

If you set `smtp_email = you@gmail.com` but `From:` on the message is `noreply@yourapp.com`, Gmail's DMARC policy rejects the send entirely. Two fixes:
- Set `From:` to match the authenticated SMTP account, OR
- Use a provider (SendGrid, AWS SES, Postmark) with domain-authenticated DKIM for `noreply@yourapp.com`

Perfex's admin notifications use `smtp_email` as `From:` by default — which is why Gmail-based installs sometimes silently stop sending admin emails after a domain config change.

### 4. `$this->email->print_debugger()` is your friend

Inside a try/catch around `send_simple_email`:
```php
try {
    $sent = $this->emails_model->send_simple_email($to, $subject, $body);
    if (!$sent) {
        log_message('error', 'email failed: ' . $this->email->print_debugger(['headers']));
    }
} catch (Throwable $e) { /* ... */ }
```
`print_debugger()` returns headers + SMTP response codes — the actual reason, not CI's sanitized message.

### 5. `smtp_timeout` is 30 s in `email.php` but 5 s in `App_mailer` defaults

`application/config/email.php` sets `$config['smtp_timeout'] = 30`. If you instantiate `App_mailer` yourself without loading that config, its internal default is **5 s** — slow providers (AWS SES cold region, TLS handshake over a high-latency link) exceed that. Always `$this->load->config('email')` (as `send_simple_email()` does) rather than building your own mailer, or you inherit the short timeout. Timeout errors look identical to auth errors in the logs.

### 6. `send_simple_email` returns `false`, no exception

CI's email library catches most failure modes and returns `false` without throwing. **Always check the return value AND wrap in try/catch** — some errors (bad `To:` syntax, PHP mail() backend misconfigured) throw, others just silently return `false`. Your retry-queue code should handle both.

## Related skills

- **`perfex-module-dev`** — `register_cron_task()` for the handler that processes the retry queue.
- **`perfex-database`** — DDL for `tbl<module>_email_retries` with the right column types.
- **`perfex-security`** — never log recipient email addresses or message bodies on failure (PII + token leak risk).

## Upstream docs

- Perfex email templates: https://help.perfexcrm.com/email-templates/
- CI3 email library (underlying): https://codeigniter.com/userguide3/libraries/email.html

---

*Verified against Perfex CRM 3.4.0 core source on 2026-09-15 with `scripts/verify-against-core.sh`. Version-specific notes in the text are from official changelogs.*
