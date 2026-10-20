---
name: opentofu-iac
description: Write and review OpenTofu/Terraform infrastructure code without the failures that make a state untouchable or take a service down: for_each keys unknown until apply, resources that already exist and must be imported rather than re-created, configuration baked into user_data that rebuilds the machine on every change, certificate validation records that collide, and secrets that leak through a printed command. Use when writing or reviewing .tf files, standing up or migrating an environment, adopting existing infrastructure into state, or before any apply that touches something serving traffic.
---

# OpenTofu / Terraform — Skill for AI Coding Agents

Target: OpenTofu 1.7+ / Terraform 1.7+, any provider. `import` and `moved` work
from Terraform 1.5; everything else here assumes 1.7, and the one block that
needs it says so where it appears.

This skill is written from a post-mortem. Every rule below corresponds to a
failure that actually happened while an agent built a small production
environment: a state that could not be touched, a certificate that would not
validate, four machine rebuilds in one afternoon, and an operator locked out of
his own box. None of it was exotic. All of it is documented somewhere the agent
did not look.

Sources:
- https://opentofu.org/docs/language/
- https://developer.hashicorp.com/terraform/language/meta-arguments/for_each
- https://developer.hashicorp.com/terraform/language/block/import
- https://developer.hashicorp.com/terraform/language/block/moved
- https://developer.hashicorp.com/terraform/language/block/removed
- https://developer.hashicorp.com/terraform/language/style
- https://developer.hashicorp.com/terraform/language/tests
- https://github.com/terraform-aws-modules/terraform-aws-acm
- https://github.com/antonbabenko/pre-commit-terraform

---

## When to use

- Writing or reviewing any `.tf` / `.tofu` file.
- Standing up a new environment, or migrating one to new infrastructure.
- Before running `apply` against anything that already serves traffic.
- Adopting infrastructure that exists but is not yet in the state.

Do NOT use for: application deployment recipes, container orchestration, or
cloud questions unrelated to infrastructure-as-code.

---

## Rule 0 — read the reference implementation first

If the organisation already has a working infrastructure repository, open it
**before** designing anything. Not after the design is challenged. Not after the
first failure.

The failure mode is specific and expensive: the agent invents a mechanism, the
reviewer rejects it, the agent invents a second one, and the answer was in a
file that took thirty seconds to open. In the session this skill comes from that
happened seven times in one day.

What to open, in order:
1. The deploy recipe of a comparable project — it shows what the infrastructure
   is expected to leave behind.
2. The instance bootstrap of a comparable environment — it shows what a machine
   must have before anything is deployed to it.
3. The variables file of a comparable environment — it shows which values are
   pinned and which are left to the provider.

If a mechanism is not in any of them, only then design it. And say so.

---

## Rule 1 — `for_each` keys are known at plan time

The most common way to render a state untouchable.

A `for_each` map's **keys** must be resolvable during the plan. Only its
**values** may arrive at apply. Iterate over an attribute of a resource that
does not exist yet and every operation fails — including operations that have
nothing to do with that resource, such as an `import` of something else.

```hcl
# WRONG — the keys come from a certificate that does not exist yet
resource "dns_record" "validation" {
  for_each = {
    for option in aws_acm_certificate.this.domain_validation_options :
    option.domain_name => option
  }
  name = each.value.resource_record_name
}
```

```hcl
# RIGHT — keys from configuration, values from the resource
resource "dns_record" "validation" {
  for_each = toset(var.certificate_names)

  name = one([
    for option in aws_acm_certificate.this.domain_validation_options :
    option.resource_record_name if option.domain_name == each.key
  ])
}
```

One trap worth knowing: the same code **works** while the resource already
exists in the state and **fails** the day it is recreated. A green plan is not
proof — it may only mean that nothing on that path has been rebuilt yet.

There is a widely repeated claim that `try()` and `can()` misbehave with unknown
values where `lookup()` does not. The official documentation of `try` says only
that it catches *dynamic* errors, and says nothing about unknown values, so this
skill does not turn it into a rule. Treat it as unverified: if a `for_each`
fails and the keys look static, check what the expression actually resolves to
rather than swapping functions on faith.

The error message suggests `-target` as a workaround. Do not adopt it as a
habit: it applies part of the graph and leaves drift nobody is looking at.

---

## Rule 2 — a resource that already exists is imported, never re-created

Claiming a name that exists fails the apply. Deleting it first "so the apply can
create it" takes the service down for the length of the gap.

Prefer the declarative block — it lives in the repository, is visible in the
plan, and survives the next person:

```hcl
import {
  to = cloudflare_dns_record.apex
  id = "<zone-id>/<record-id>"
}
```

`tofu import` on the command line does the same thing and leaves no trace. Use
it only for a genuine one-off, and write down that you did.

For refactors, two more blocks replace state surgery:

```hcl
# any supported version
moved { from = aws_instance.a to = aws_instance.b }

# OpenTofu 1.7+ / Terraform 1.7+ — will not parse on anything older
removed {
  from = aws_instance.retired
  lifecycle { destroy = false }
}
```

`removed` is the newest of the three: Terraform 1.7.0 (17 January 2024,
"`removed` block for refactoring modules") and OpenTofu 1.7.0 ("Add support for
a `removed` block that allows users to remove resources or modules from the
state without destroying them"), both quoted from their own changelogs. On an
older engine the file fails to parse — there is no graceful degradation, so
check the version before reaching for it.

Large public modules keep a `migrations.tf` per version holding exactly these
`moved` blocks, so that upgrading never destroys anything. Copy the habit.

---

## Rule 3 — configuration does not live in the machine's bootstrap

Anything rendered into `user_data` becomes part of the instance's identity.
Adding one VPN client, one SSH key or one allowed address then rebuilds the
machine and takes every session on it down with it.

Put in the bootstrap only what a machine needs to *exist*: hostname, packages,
the runtime the deploy assumes, ownership of the deploy directory. Everything
that changes on a human timescale is read at runtime:

- **Instance tags via the metadata service** — no credentials on the box, and a
  tag change is an in-place update. Requires the instance metadata tags option
  to be enabled.
- **A parameter store or object read on a timer** — needs an identity on the
  machine, scales past the tag size limit.
- **A configuration management run decoupled from the apply** — heaviest, but
  the only one that handles genuinely complex state.

Whatever the source, the reader must **fail closed**: metadata that cannot be
read is not the same as "no clients configured", and treating it as such locks
everyone out on a transient error.

```bash
# fails closed: unreadable metadata changes nothing
keys="$(imds tags/instance)" || exit 0
```

---

## Rule 4 — the machine must arrive with what the deploy assumes

An environment that applies cleanly and then cannot be deployed to is not
finished.

Write the contract down, in both directions:

| The infrastructure guarantees | The deploy expects |
|---|---|
| Container runtime installed and running | It can build an image |
| Deploy directory owned by the deploy user | It can clone without elevation |
| Managed database reachable from this host only | It creates its own schema and user |
| Operator keys installed | A human can get in when it breaks |

Every line of that table is a line of bootstrap code, and every one of them was
learned by watching a deploy die on it.

---

## Rule 5 — certificates validated through a DNS provider you also manage

Three failures, all avoidable:

1. **A wildcard and its bare name produce the same validation record.** Keyed by
   domain name, two entries collide into one and the plan cannot expand. Public
   certificate modules expose a de-duplicated list precisely for this; consume
   it instead of re-deriving it.
2. **Two certificates for the same domain ask for the same record name.** Before
   creating it, check whether it exists and what it holds. If the value matches,
   import it — the environments can share it. If it differs, taking it over will
   break the other certificate's next renewal, and that is a decision, not a
   detail.
3. **The value carries a trailing dot** that the cloud emits and the DNS
   provider does not store, so the plan never converges. `trimsuffix(value, ".")`.

And before designing any of it, **find out whether a certificate is needed at
all**. If a proxy fronts the origin, its TLS mode decides: a strict mode
validates the origin certificate, a lax one does not. One request against a name
the current certificate does not cover answers the question in thirty seconds —
a `526` back means strict.

---

## Rule 6 — secrets: encrypted in the repository, never in the clear

Committing the ciphertext and keeping the key out of the repository beats an
ignored plaintext file: an ignore rule does not cover what is already tracked,
and a file that only exists on one laptop is one laptop away from being lost.

**And encrypting the repository is only half the problem: the state holds the
same secrets in the clear.** A password passed to a database, a generated key, a
value read from a secret store — they all land in the state file, whatever care
was taken with the input. Two consequences:

- The state backend needs encryption at rest and an access policy at least as
  tight as the secrets inside it. A bucket anyone in the account can read is a
  bucket where every password lives.
- OpenTofu encrypts the state itself since 1.7.0 — end-to-end, with key
  providers for a passphrase or a managed key service — so the backend never
  sees the plaintext. It is the only measure that survives a misconfigured
  bucket.

Two more hazards specific to encrypted variable files:

- **The decrypt step overwrites the plaintext.** If someone edited the plaintext
  and never encrypted it, that edit disappears silently, and the next apply
  propagates the loss to real infrastructure. Run the status check that compares
  both before decrypting, and never chain decrypt into an apply blindly.
- **Deploy tooling prints the command it failed on.** A token interpolated into
  a repository URL ends up in the terminal and the log at the worst moment. Use
  the tool's secret placeholder, and clean the credential out in a `finally` so
  a failure cannot leave it behind.

---

## Rule 7 — one directory per environment

Separate directories with their own state and their own credentials are the only
arrangement that isolates access. Workspaces share authentication by design; the
documentation says so plainly.

Extract a module when something is instantiated in more than one shape. A root
configuration used once is not a module, it is a root configuration.

---

## Pre-apply checklist

Run through this before every apply that touches something serving traffic.

1. `tofu validate` passes.
2. The plan is **read**, not skimmed. Count the destroys and name each one.
3. Nothing in the plan is a surprise. A resource you did not expect to change is
   a signal that the state and the world disagree.
4. Anything being created that might already exist has been checked against the
   provider's API first.
5. If the plan replaces an instance, you know what that instance is currently
   serving.
6. Secrets are in sync: the encrypted file and the plaintext agree.
7. You can say, in one sentence, what will be different afterwards.

---

## The rebuild test

An environment is finished when it can be destroyed and stood up again with
nothing done by hand:

```
tofu apply
<deploy> seed      # only for projects that own a database
<deploy> deploy
```

If any step needs an import, an SSH session to run a command, or a manual edit
on the machine, the design is not finished — write down which step, and fix
that rather than documenting the workaround.

Note the middle step is conditional. A project with no entities, no repositories
and no schema of its own has nothing to seed; giving it a seed recipe produces
an elaborate mechanism guarding an empty room.

---

## Report format

When reviewing an infrastructure change, report only what is wrong:

```
<file>:<line> — <what breaks, in one sentence>
  Trigger: <the conditions under which it breaks>
  Fix:     <the change, concretely>
```

No inventory of what is correct. A review exists to produce work.

---

## Anti-patterns

- Designing a mechanism without opening the reference implementation.
- Reporting a check as verified when the test could not have distinguished pass
  from fail. If the assertion would have succeeded either way, it proved nothing.
- `for_each` over a resource attribute.
- Importing on the command line and leaving no trace in the repository.
- Rendering anything into `user_data` that changes more often than the machine.
- Applying to production from a branch that has not been merged.
- Calling something cosmetic before finding out where it comes from.
