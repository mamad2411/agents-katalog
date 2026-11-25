---
name: greybox
description: >
  Test a target with test logins for each type of user, the interface documentation and a
  description of how the system fits together, but without the source code. Use when someone
  says grey box, greybox, gray box, "authenticated testing", "we can give you test
  accounts", "we have API docs", "logged in as each role", or /redteam:greybox. This is the
  usual level on paid work, so use it as the default when the level has not been stated but
  logins exist.
---

# Testing with part access

You have working logins for every type of user, a description of the programming interface,
and a picture of how the system is built. You do not have the source code.

This is the level most paid work happens at, and it buys the most per day. You stop guessing
at things the client could have told you in ten minutes, and you spend the time on the areas
where the serious problems actually are.

Read `../pentest/SKILL.md` first if the engagement has not been scoped. Permission still
comes before traffic.

## What to insist on before starting

- **Two accounts for every type of user.** Two administrators, two staff, two customers. One
  each is not enough, because a large share of real findings is one customer reaching
  another customer's data, and that cannot be tested with a single account. If the client
  offers one account per type, explain what will go untested and ask again.
- **An account with nothing enabled**, and one that has been suspended or has lapsed. These
  two find a surprising amount, because expiry and suspension are usually checked in one
  place and forgotten everywhere else.
- **The interface documentation**, whatever form it takes.
- **A description of how the system fits together**, even a whiteboard photograph. You need
  to know what sits between the internet and the application, and which parts talk to each
  other.
- **If the system serves more than one company or team, two separate tenants.** Isolation
  between customers cannot be tested from inside one of them.

Never test with a real person's account, even if offered.

## The order of work

Run the phase files in order:

1. `../pentest/phases/00-permission-and-scope.md`
2. `../pentest/phases/02-public-information.md`, kept short. Still do the certificate logs
   and the secret scanning, because clients rarely know what they have leaked.
3. `../pentest/phases/03-mapping.md`, but walk the whole application as every type of user.
   This is the step where part access earns its money.
4. `../pentest/phases/04-automated-checks.md`, running the logged-in scan once for each type
   of user rather than once in total. What a scanner sees as an administrator is a different
   application from what it sees as a customer.
5. `../pentest/phases/05-manual-testing.md`, in the order given there. All of it is now in
   reach.
6. `../pentest/phases/07-proving-impact.md` onwards.

## Where to spend the time

With logins in hand, two areas produce most of the serious findings. Give them more than
half the testing time.

**Permission checks.** Four questions, asked against every address you listed while mapping,
not just the interesting-looking ones:

1. Can a low-privilege user call something meant for an administrator, by calling the
   address directly instead of clicking the button that is hidden from them?
2. Can customer A read, change or delete customer B's records by changing an identifier?
   Every kind of object, every method, not just the first one that worked.
3. Can a user reach another company's or team's data by swapping the identifier wherever it
   appears, including inside a token or a header?
4. Can a user set a field they should not control by adding it to a request body? A role, a
   balance, an owner, a price.

Use a proxy add-on that repeats every request as every other user to cover the ground, then
confirm every flag by hand before it becomes a finding.

**Business rules.** Work from the lifecycle you wrote while mapping. Prices, quantities,
negative numbers, discounts applied twice, steps skipped, the same action fired twice at the
same instant, refunds that leave the customer with the goods and the money. There is no tool
for this and it is where the highest-severity findings usually are.

## What part access still cannot reach

Say this in the report rather than letting it pass silently:

- Code that is hard to reach by clicking, including logic behind switches that are off
- Encryption mistakes, which look identical from outside
- Out-of-date components whose versions are not visible from the running system
- A missing permission check on an address that nothing in the interface ever calls, and
  which you therefore never found while mapping
- Anything in the build pipeline

If the client wants those covered, they need to hand over the source. Point them at
`../whitebox/SKILL.md` and at the cost difference in
`../pentest/phases/01-access-decision.md`.

## The coverage note

Shorter than the outside-only one, but still needed. Name the types of user you tested as,
because that defines the coverage of the permission testing, and name the areas above that
part access cannot see.
