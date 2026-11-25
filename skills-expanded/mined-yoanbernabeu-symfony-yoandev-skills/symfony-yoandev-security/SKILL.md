---
name: symfony-yoandev-security
description: >-
  Authentication and authorisation on a Symfony project: the User entity and user
  providers, the firewall, native access_token authentication for a JSON API with
  revocable opaque tokens, roles and role_hierarchy for zones, Voters for anything
  depending on the object acted on, access_control plus #[IsGranted], and hardening —
  login throttling, password hashing, strength and breach checks, rate limiting, CSRF.
  Use this skill whenever someone asks to add login or a login form, register users,
  protect a page or a route, restrict or secure my API, add an API key or token
  authentication, add roles or an admin area, work out who can do what, make it so only
  the author can edit or delete their own review, hide a button unless the user may
  click it, check permissions, write a Voter, log a user in from code, log out,
  impersonate another user, stop brute-force attempts on the login form, or fix "Cannot
  resolve argument $user", "Full authentication is required", "Access Denied", "Invalid
  CSRF token", or a 401 on an endpoint that should be open. Also use it before writing
  any endpoint that reads the current user.
---

# Security

> **Tier: core the moment the application has users** — the wiring check, one firewall, roles for zones and voters for objects. The hardening table is core too; `#[RateLimit]` beyond login is on demand.

Who the request is, and what that lets them do. Two questions, two mechanisms — and the
first is the one people skip.

## First: is security actually wired?

On a freshly generated project it is not. The recipe ships a firewall with no
authenticator and a `users_in_memory` provider: no `User` entity, no way to log in,
nothing for `#[CurrentUser]` to resolve. Thirty seconds to check — an empty
authenticator list alongside `users_in_memory` is the untouched skeleton state:

```bash
php bin/console debug:firewall main          # authenticators, provider, stateless or not
grep -A3 'providers:' config/packages/security.yaml
```

Check before writing the endpoint: `mine(#[CurrentUser] User $user)` 500s with *"requires
the `$user` argument that could not be resolved"* and says nothing about a missing
provider, and `?User $user` turns that crash into a silent `null`, which is worse.

**Three things are needed and none is optional:**

1. an entity implementing `UserInterface` (plus `PasswordAuthenticatedUserInterface` if
   it has a password);
2. a provider pointing at it, referenced by the firewall;
3. an **authenticator** on it — `form_login`, `json_login`, `access_token`. A provider
   only *loads* a user, it never authenticates one: a firewall with a provider and no
   authenticator lets nobody in, quietly.

**Say this rather than routing around it.** Two workarounds appear on their own; both are
worse than the missing feature:

| Workaround | Why it is refused |
|---|---|
| Taking a `userId` in the request payload | Not authentication — the caller is telling you who they are, and anyone can send another id. It spreads, too: every service downstream now trusts an unauthenticated value. |
| Adding an entity provider *only* so `loginUser()` greens the functional tests | `loginUser()` writes a token straight into the token storage and never runs an authenticator. The suite goes green while production still has no way to log in — green tests over an unreachable feature is the expensive kind of wrong. |

The honest answer is "this needs a User entity and a login mechanism first, here is what
that involves" — not an endpoint that appears to work.

## The three pieces

```php
class User implements UserInterface, PasswordAuthenticatedUserInterface
{
    /** @var list<string> */
    #[ORM\Column]
    private array $roles = [];

    /** @return list<string> */
    public function getRoles(): array
    {
        return array_values(array_unique([...$this->roles, 'ROLE_USER']));
    }
    // getUserIdentifier() returns the unique email column; the rest is maker output
}
```

`ROLE_USER` is added in the getter, not stored, so no row can be missing it, and
`getUserIdentifier()` must be stable and unique — it is what lands in the session and in
every token. `eraseCredentials()` was removed from `UserInterface` in Symfony 8.0
(deprecated in 7.3); on 6.4–7.x implement it empty. `make:user` generates the right
shape for the installed version.

```yaml
security:
    password_hashers:
        Symfony\Component\Security\Core\User\PasswordAuthenticatedUserInterface: 'auto'
    providers:
        app_users:
            entity: { class: App\Entity\User, property: email }
    firewalls:
        dev:
            pattern: ^/(_profiler|_wdt|assets)/
            security: false
        main:
            lazy: true
            provider: app_users
            form_login: { login_path: app_login, check_path: app_login, enable_csrf: true }
            logout: { path: app_logout }
            login_throttling: { max_attempts: 5, interval: '15 minutes' }
```

**One firewall for the application**, plus `dev`, an exclusion rather than a boundary.
Several firewalls mean several security contexts, and a user authenticated in one is
anonymous in the other — the bug people lose an afternoon to. The one legitimate second
firewall is a **stateless** one for a token API on its own path prefix: different
mechanism, and it must not create a session. `password_hashers: auto` picks the best
algorithm the platform offers and, with `needsRehash()` at login, migrates hashes as
that improves; naming bcrypt or argon2id freezes the decision in a file nobody revisits.

## Roles for zones, Voters for objects

| Question | Mechanism |
|---|---|
| "Is this person allowed into the admin area, the billing section?" | A role, and `role_hierarchy` |
| "Can this person edit *this* review?" | A Voter |

The line is whether the answer depends on the target object. It usually does, and a
role-shaped answer to an object-shaped question is how `ROLE_REVIEW_OWNER` gets invented
— a role per row, which no hierarchy can express. **Controllers and templates name
actions, never roles:** `#[IsGranted(ReviewVoter::EDIT, subject: 'review')]`, not
`ROLE_MODERATOR`, so the rule lives in one class instead of being copied into every
controller that checks a role.

`subject: 'review'` names the **controller argument**; the resolved object is what the
voter receives. This is the one case where a controller resolves an entity
(`Review $review`, the EntityValueResolver) instead of handing an id to the service: the
voter runs before the action, so the object has to exist before the service is called.
The action still passes `$review->getId()` to the service, which reloads for free from
the identity map (`symfony-yoandev-architecture`). Omit it and the voter is called with `null`, `supports()` returns false,
every voter abstains — and an all-abstain decision is **denied**, because
`allow_if_all_abstain` defaults to `false` (verified by execution). So the symptom is a
403 on an action that should have been allowed, and the cause is an attribute that looks
correct. It fails closed, which is the right direction; it is still a bug.

The attribute does not replace `access_control`; they fail differently. `access_control`
is the **net** — one rule per URL zone, applied before the controller is resolved, so a
new action in a protected controller is covered without anyone remembering; rules run
top to bottom and **only the first match applies**, so `^/` goes last. `#[IsGranted]` is
the **precision** — this action, this object, and the only one of the two that can
express "the author". Only `#[IsGranted]` leaks the day someone adds a method and
forgets the attribute; only `access_control` cannot express ownership at all.

## The Voter

```php
<?php

declare(strict_types=1);

namespace App\Security\Voter;

use App\Entity\Review;
use App\Entity\User;
use Symfony\Component\Security\Core\Authentication\Token\TokenInterface;
use Symfony\Component\Security\Core\Authorization\AuthorizationCheckerInterface;
use Symfony\Component\Security\Core\Authorization\Voter\Vote;
use Symfony\Component\Security\Core\Authorization\Voter\Voter;

/** @extends Voter<self::EDIT|self::DELETE, Review> */
final class ReviewVoter extends Voter
{
    public const EDIT = 'REVIEW_EDIT';
    public const DELETE = 'REVIEW_DELETE';

    public function __construct(private readonly AuthorizationCheckerInterface $checker)
    {
    }

    protected function supports(string $attribute, mixed $subject): bool
    {
        return \in_array($attribute, [self::EDIT, self::DELETE], true) && $subject instanceof Review;
    }

    protected function voteOnAttribute(string $attribute, mixed $subject, TokenInterface $token, ?Vote $vote = null): bool
    {
        if (!($user = $token->getUser()) instanceof User) {
            return false;
        }

        if ($this->checker->isGranted('ROLE_MODERATOR')) {
            return true;
        }

        if ($subject->getAuthor() !== $user) {
            $vote?->addReason('Only the author may act on their own review.');

            return false;
        }

        return self::DELETE !== $attribute || !$subject->isPublished();
    }
}
```

The fourth parameter `?Vote $vote = null` exists from **Symfony 7.3**; on 6.4–7.2 the
signature ends at `TokenInterface $token` and adding the parameter is a fatal signature
error. Read `vendor/symfony/security-core/Authorization/Voter/Voter.php` before writing
it — that file is the source of truth, not this one. `$vote?->addReason()` is what the
profiler and `AccessDecision::getMessage()` display, turning "Access Denied" into a
sentence. Role checks go through `AuthorizationCheckerInterface`, never
`$token->getRoleNames()`: the token holds raw roles and `role_hierarchy` is applied by
the checker, so reading the token makes `ROLE_ADMIN` stop implying `ROLE_MODERATOR`.
Type-hinting the interface rather than `Security` also keeps the voter stubbable without
a kernel.

## Hardening

Each line answers a specific attack; none is optional.

| Measure | Without it |
|---|---|
| `login_throttling` on the firewall | The login form is an online password-guessing oracle. Needs `symfony/rate-limiter` |
| `password_hashers: auto` | An algorithm frozen by whoever wrote the file first |
| `#[Assert\PasswordStrength]` on registration and password-change DTOs | Accounts secured by `azerty123` |
| `#[Assert\NotCompromisedPassword]` | Credential stuffing works on day one |
| `#[RateLimit]` beyond login | Password reset, registration, search and export are all abusable, and `login_throttling` covers none of them |

`#[RateLimit]` is `Symfony\Component\HttpKernel\Attribute\RateLimit`, added in **Symfony
8.1**. It needs `symfony/rate-limiter` **and** a limiter declared under
`framework.rate_limiter` whose name it references — alone, it throws "Rate limiter … does
not exist" at request time. Before 8.1, inject the generated
`RateLimiterFactoryInterface` and consume explicitly.

## CSRF

The Form component handles it: every form gets a `_token` field, validated on submit —
nothing to write. Outside forms (a POST link, a fetch call, an inline delete button) put
`#[IsCsrfTokenValid('delete-review', tokenKey: '_token')]` on the action beside its
`#[Route]` — Symfony 7.1+; before that, call `isCsrfTokenValid()` in the controller.

**A JSON API needs CSRF only when it authenticates by cookie**, because CSRF exists to
counter the browser attaching cookies to cross-site requests by itself. A stateless API
reading `Authorization: Bearer …` is not exposed — the browser never adds that header on
its own. A session-backed JSON endpoint called from your own front end absolutely is.

## When it does not behave

| Symptom | Cause |
|---|---|
| `Cannot resolve argument $user` on `#[CurrentUser]`, or `?User $user` always null | No user provider, or the route is not behind an authenticated firewall. Check `debug:firewall` |
| `Full authentication is required` | `access_control` matched a rule an anonymous request cannot satisfy — often `^/` placed above `^/login` |
| Access Denied where the voter should grant | `subject:` missing on `#[IsGranted]`, so the voter got `null` and `supports()` said no |
| The voter is never called | `supports()` returns false: wrong attribute string, or an unexpected subject class |
| 401 on an endpoint that should be public | Needs an explicit `PUBLIC_ACCESS` rule above the catch-all |
| `Invalid CSRF token` on a form that has one | Stateless CSRF (default since 7.2) needs its Stimulus controller loaded in the browser |
| `ROLE_ADMIN` stops implying the roles below it | Roles read off the token instead of through the authorization checker |
| Test user logs in but the app 403s | `loginUser()` bypasses authenticators; roles come from the entity, not the firewall |

## Reference files

| File | When to read it |
|---|---|
| `references/api-authentication.md` | A token-authenticated API: `access_token`, revocable opaque tokens in the database, the handler, testing it |
| `references/voters-and-roles.md` | Writing or unit-testing a Voter, designing `role_hierarchy`, `access_control` ordering, `is_granted` in Twig |
| `references/hardening.md` | Throttling, password constraints, rate limiting, CSRF details, programmatic login, logout and impersonation |
