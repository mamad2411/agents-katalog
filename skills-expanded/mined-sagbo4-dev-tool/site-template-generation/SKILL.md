---
name: site-template-generation
description: Builds a client website as a template with its own back office: the content contract, design tokens by trade in both light and dark, a motion system driven by one intensity scalar, an administration surface where the client edits text, images, colours, hours and legal facts without touching code, authenticated and rate limited, a message inbox fed by the contact form, legal pages generated from the company's real facts and never invented, an installable offline-capable shell with push notifications, and the gate a template passes before it counts as finished. Use when building a portfolio or a showcase site, a reusable site template, or any client site that must stay editable after delivery.
license: MIT
metadata:
  category: dev-skills
  version: 2.0.0
  depends_on: [engineering-core]
  outputs: [content-contract, token-profile, motion-spec, admin-surface, admin-security-report, legal-fact-sheet, completion-gate-report]
---

# Site Template Generation

A site built for a client is delivered twice: once as a page, and once as
something the client can still run a year later without calling anyone. This
skill builds the second. The template is fixed and written by hand; a site is an
instance of it, produced from a content file that the client's own back office
writes. What a person would want to change lives in that file, and what the file
does not hold is a defect rather than a shortcut.

## 1. Four artefacts, kept apart

```
template    components, layout, routing, behaviour. Written once, reused for
            every instance. Contains no client fact and no visual literal.
content     one structured file holding every string, image, colour, hour and
            contact detail a human would want to change. One instance of the
            site is one content file.
tokens      the visual vocabulary: two palettes, type scale, spacing, radius,
            motion intensity. Declared as data in the content file, consumed by
            the template as custom properties.
back office the authenticated surface that writes the content file, stores the
            uploads and holds the messages. It is part of the delivery, not a
            developer tool the client is told to avoid.
```

The separation is testable: a value found in a component and not in the content
file fails the gate in section 17, whatever it is. The reverse is equally firm:
logic never enters the content file, because the back office writes that file
and a client editing text must not be able to break the build.

## 2. Two kinds, and what actually differs

| | portfolio | showcase |
|---|---|---|
| Owner | one person trading under their own name | a company with a legal identity |
| Shape | one page, anchored sections, one scroll | several pages, one per intent |
| Voice | first person, personal | third person, institutional |
| Proof | gallery, results, testimonials | services, references, credentials |
| Action | a message | a quotation request |
| Legal | the pages the person's activity requires | legal notice, terms, privacy, cookies, all of them |
| Back office | the same one | the same one |

The kind is decided before anything is written: it changes the content contract,
the navigation, the number of routes and the legal surface. It does not change
the back office, which is the same surface over a different contract.

## 3. The content contract

Fixed per kind, not improvised per project. One fixed contract is what lets a
single back office, a single validator and a single handover serve every
instance. Field by field: `resources/content-contract.md`.

```
root        site, brand, theme, nav, ui, sections, contact, forms, legal, seo,
            pwa
required    refused at load with a named field, never silently defaulted
optional    absent means the section does not render at all, not that it
            renders empty
arrays      ordered, may be empty, and the template renders the empty case
            without a broken frame
alt text    a content field on every image, never a constant in a component
strings     every word a visitor reads, including headings, button labels,
            empty states and the 404 page
```

The content file is read at runtime from a writable data directory, not
imported into the bundle, because the back office writes it while the site runs.
It is parsed once and re-read when its modification time changes.

## 4. The shape every instance shares

A generated site is not a one-off. It joins a fleet, and a fleet is maintained
by tools that do not know which instance they are looking at: a verification
that has to change every field, a backup that has to find the data, an operator
opening an unfamiliar project at two in the morning.

So three things are fixed. They are the smallest set that lets one tool serve
every instance, and everything outside them stays the trade's decision.

### Where things live

```
data/content.json     the instance's content, the only file the back office
                      writes, the only file a backup must carry
data/                 everything else a running instance writes, and nothing a
                      developer edits: uploads, sessions, messages, history
lib/                  the loader, the contract, the tokens, the security
app/                  routes, following the framework's own convention
public/               what is served unchanged
```

No `src/` wrapper: it adds a level that carries no meaning here, and two
instances that disagree about it cannot share a script. The framework's config
keeps the framework's own extension.

### What the custom properties are called

```
--color-<token>       every palette key, kebab-cased: --color-accent,
                      --color-border-strong, --color-focus-ring
--font-display        --font-text
--size-<step>         the type scale
--space-<name>        --radius-<name>
--motion-duration     --motion-easing, --motion-intensity, --motion-lift
```

An abbreviation saves six characters once and costs a rename everywhere. A tool
that measures contrast reads these names; a template that spells them otherwise
is not measurable by it, and an unmeasurable palette is how white on white
ships.

### How the back office talks to the server

Four endpoints, JSON, session in an http-only cookie, the CSRF token in
`<meta name="csrf-token">` on every admin page and sent back as
`x-csrf-token`. Every one refuses without a session before it does anything
else.

```
GET  /api/admin/fields    -> { ok, fields: [ { path, label, kind, changes,
                              hint?, pattern?, options?, min?, max?, step?,
                              item?: [ { key, kind, options? } ] } ] }
GET  /api/admin/content   -> { ok, content }
PUT  /api/admin/content      { patch: { "dotted.path": value } }
                          -> { ok } or { ok: false, error } naming the field
POST /api/admin/login        { password } -> { ok } or { ok: false, error }
```

`/api/admin/fields` is the piece that is easy to leave out and expensive to
add later. It is the field map as data, and it has two readers: the handover
document that lists what the client can change, and any verification that has
to change every field and watch the change arrive. Without it, a checker has to
crawl the back office and know its routes and its markup, so it only ever works
against the instance it was written for. With it, one script checks every site
in the fleet, including the ones that do not exist yet.

The rest of the admin surface is the template's own: more endpoints, other
routes, a different arrangement of the forms. Only these four are promised.

## 5. Tokens, by trade, in both themes

The trade decides the values; the component only reads them. A palette is
always a pair: light and dark are both delivered, both measured, and the visitor
chooses.

```
theme.palettes.light   the full palette
theme.palettes.dark    the full palette again, not a filter over the first
theme.type             one display family, one text family, a scale ratio
theme.radius           sm, md, lg, pill
theme.spacing          unit, section, and the page width
theme.motion           intensity between 0 and 1, base duration, easing
theme.density          compact | regular | airy
```

Dark is not an inversion. A dark palette that is the light one with the
lightness flipped produces grey text on charcoal and an accent that glows. Each
palette is authored and measured on its own. The profiles per trade, the pairs
that must be measured and the two border tokens are in
`resources/trade-profiles.md`.

The theme resolves in this order: the visitor's stored choice, then the system
preference, then light. The stored choice is applied before first paint, so the
page never flashes the wrong theme.

## 6. Motion is chosen by trade, not only scaled

Two values in the content file decide every movement on the site.

```
theme.motion.signature   which effects exist at all, named after the trade
theme.motion.intensity   how far and how fast those effects go, 0 to 1
```

A scalar alone produces the same site twice, once faster. The signature is what
makes a coach's page and an electrician's page move differently in kind:

| Signature | Trades | Effects it turns on |
|---|---|---|
| energetic | coaching, fitness, dance | entrance, reveal, stagger, counters, parallax, lift |
| creative | photography, design, architecture | entrance, reveal, stagger, parallax, lift |
| crafted | artisan food, ceramics, florists | entrance, reveal, stagger, counters, lift |
| technical | building trades, industrial services | reveal, lift |
| clinical | medical, legal, accounting | reveal |

```
entrance   the first screen assembles once on load, title then subtitle then
           actions, and never again
reveal     a section fades and rises as it enters the viewport, once
stagger    the items of a list follow one another rather than arriving as a
           block, which is the effect that makes a page feel alive
counters   a figure counts up to its value when it becomes visible, keeping any
           suffix the content wrote
parallax   the hero image moves slower than the page, on transform only
lift       cards and buttons rise under the pointer
```

The intensity scales all of them and zero disables all of them.
`prefers-reduced-motion: reduce` forces zero whatever the content file says, and
a browser without JavaScript shows everything, because the hidden state is
applied by the script and never by the stylesheet.

A stagger that decorates the container instead of its items is not a stagger.
The delay belongs on each item, with its index, or nothing moves in sequence and
the page looks static however high the intensity is set. Both reference
implementations shipped that defect once; the gate now checks it.

The technique ladder, the components and what must never move:
`resources/motion-system.md`.

## 7. The page uses its width

A site that centres one column of text inside sixty percent of a wide screen
looks like a document, not like a business. The layout is decided per section,
not once for the whole page.

```
full bleed    the hero, section backgrounds, image bands, the footer. They span
              the viewport
wide          cards, galleries, service grids, figures. They use the page width
              token, which is wide, and grow their column count with it
readable      long prose and legal pages only, capped around 70 characters,
              because a 200 character line is unreadable at any screen size
asymmetric    a two column section is rarely 50/50; the weight follows the
              content, and the grid states the ratio
```

Centring a narrow column is a decision made for text, never a default applied to
everything.

## 8. The back office

The client changes their site from a browser, signed in, without a developer and
without a rebuild. This surface is part of the deliverable.

| Section | What it edits | Writes |
|---|---|---|
| Content | every visitor facing string, section by section, in the order of the page | the content file |
| Media | upload, replace, delete an image, with its alt text required | the uploads directory and the content file |
| Theme | both palettes, the motion intensity, the density | the content file |
| Hours and contact | address, telephone, email, opening hours, social links | the content file |
| Legal | the legal facts and the clauses the counsel provided | the content file |
| Messages | the inbox of the contact form: read, unread, archived | the message store |
| Notifications | the browser subscription that receives a new message | the subscription store |
| Identity | the favicon, the installed icons, the social preview | the uploads and the content file |
| Security | the password of this account | the credential store, and every session |
| History | the previous versions, and a return to any of them | the content file, after snapshotting the present one |
| Help | what each section does, in the client's words | nothing |

Rules the surface obeys:

```
one contract    the form is generated from the content contract, so a new
                field appears in the back office without new admin code
validated       every write is validated against the contract on the server;
                a rejected write names the field and changes nothing
atomic          the content file is written to a temporary file and renamed, so
                a crash mid-write never leaves a half file
never logic     the client edits values, never expressions, never markup beyond
                a declared inline subset
visible effect  every field in the back office changes something the client can
                see, which is verified by changing it, not by intending it
reversible      every write snapshots the state it replaces, and any snapshot
                can be restored in one action. A client who cannot undo will
                not touch their own site
guiding         the surface says what is still missing, computed from the
                content, and links to where each one is fixed
their words     nothing here addresses a developer. A command, a file path or
                an environment variable shown to a client is a defect: name the
                installer instead, and put the command in the handover
```

## 9. Getting in: authentication and rate limiting

The back office is the highest value target on the site and is built as one.
`admin-console`, `authentication-security`, `session-security` and
`rate-limiting` govern; the specifics for this surface are in
`resources/admin-security.md`.

```
credential      one account, password hashed with a memory hard function and a
                per-account salt. No password in the repository, in the content
                file or in an environment variable in plain text. Set out of
                band the first time, changed from the back office afterwards,
                with the current one required and a minimum length enforced on
                the server
session         a random token, stored hashed server side with an expiry, in an
                httpOnly SameSite cookie, Secure outside development. Signing
                out deletes the record, not only the cookie
rate limit      the login endpoint is limited per address and per account, with
                a lockout window after repeated failures, and the same answer
                and the same timing for a wrong password and an unknown account
csrf            every state changing request carries a token bound to the
                session, checked on the server
protected       every admin route and every admin endpoint checks the session
                on the server. Hiding a link is not access control
uploads         type checked by extension and by content, size capped, name
                generated, stored outside any executable path, and no SVG
public limits   the contact endpoint is rate limited too, or the inbox becomes
                a spam folder on the first crawl
body size       refused before it is parsed, because a request body is read
                whole before anything validates it
record          every privileged action appended to an audit log: who signed
                in, what was written, what was uploaded, what was deleted, what
                was refused. No password, no token, no message body in it
```

The browser is the second half of this. A site that hands the visitor no policy
relies entirely on the server being perfect:

```
policy          a Content-Security-Policy with a nonce issued per request, so
                that a script which reaches the page, however it got there, does
                not run. `style-src` keeps stylesheets locked; style attributes
                carry values and are allowed
headers         nosniff, a referrer policy, frame protection, a permissions
                policy naming what the site does not use, and HSTS
no cache        the back office and every endpoint are `no-store`, in the
                browser and in anything between
```

Anything a signed in client types that ends up inside a style or a script is
validated where it is written and escaped where it is used. A colour is a
colour, a length is a length, and a font family is a list of names. Without
that, the back office is a stored cross-site scripting hole aimed at every
visitor, and the client is one phishing away from it. Both reference
implementations shipped that hole once; `resources/admin-security.md` carries
the patterns.

## 10. The contact form has a destination

A form that posts into nothing is the most common broken thing on a client site.
The message is stored on the server, shown in the back office, and announced.

```
stored      validated, then written to the message store with its timestamp,
            its source page and the visitor's declared fields
shown       the Messages section lists unread first, with read and archive
            actions, and a count the client sees on arrival
announced   a push notification to the subscribed browser, when the client has
            subscribed, and an email when the instance is configured for one
never lost  if the announcement fails, the message is already stored, and the
            failure is logged rather than swallowed
answered    the visitor sees a success state that says when to expect a reply,
            or a failure state that gives the direct address
```

## 11. Legal pages are built from facts, and never invented

A legal page is a statement about a real company. The template assembles it from
the facts that company provided.

```
provided     rendered
missing      rendered as a visible, unmistakable marker naming the missing
             fact, never as a plausible invention
structural   the headings and the connective sentences of a notice may be
             templated, because they carry no claim
obligation   any clause that binds, a warranty, a withdrawal period, a
             jurisdiction, a mediator, is taken from the company's own document
             or left marked for its counsel
```

Never assert a registration number, a VAT identifier, an insurance policy, a
professional certification, a capital amount, a mediator or a hosting provider
that was not given: that is not a placeholder, it is a false legal statement
published under the client's name. A site with unresolved markers may be
reviewed and staged; it may not be announced as delivered. Page by page:
`resources/legal-fact-sheet.md`.

## 12. Accessibility, responsive, and the pages nobody designs

Applied while building, not audited afterwards.

```
mobile first  designed at 360px, then widened; no horizontal scroll at any
              supported width
targets       44px minimum for anything tapped, which includes a telephone
              number in a header, an email address in a footer and the brand
              link. A link is not exempt because it looks like text
identity      the business name is why anyone reads a header. When the row is
              too tight for the name, the number and the menu, the name takes a
              row of its own and the number becomes a call button. Truncating
              the name to an ellipsis is not a compromise, it is a loss
navigation    a navigation that does not fit becomes a menu, never a wrapping
              row. The button says what it controls and whether it is open, the
              panel is reachable and dismissible by keyboard, Escape closes it
              and focus returns to the button
contrast      measured on both palettes, 4.5:1 for text, 3:1 for the boundary
              of a control and for large text
keyboard      every action reachable and operable, focus visible on both
              themes, order following the reading order
semantics     landmarks, one h1 per page, headings that descend without gaps,
              a skip link
forms         a real label per field, errors announced and tied to their field,
              never colour alone
motion        prefers-reduced-motion removes movement rather than shortening it
targets       44px minimum for anything tapped
404           designed, in the site's own tokens and both themes, with its
              words in the content file and a way back that is not the browser
              button. A default framework 404 is an unfinished site
offline       the offline page is designed the same way, for the same reason
```

## 13. Installable, offline, and able to notify

```
manifest    generated from the content file: name, short name, description,
            theme and background colour from the tokens, icons from the media
            the client uploaded
service     a service worker that serves the shell and the uploaded media from
worker      cache, falls back to the offline page for a navigation it cannot
            reach, and never caches the back office or an API response
install     the install prompt is offered, not forced, and the site works
            identically when it is declined
push        one subscription per client browser, VAPID keys held as server
            configuration, a notification on a new message, an unsubscribe that
            actually deletes the record
degrade     every one of these is optional at runtime. A browser without
            service workers, or a visitor who refuses notifications, gets the
            whole site minus the extra
```

## 14. Being found

A site nobody finds is not delivered. Three files, all generated from the
content file so that an instance changing its address does not keep announcing
the old one:

```
robots.txt      generated; the back office and the endpoints disallowed; the
                sitemap named at the instance's own address
sitemap.xml     the routes this instance actually serves, including the legal
                slugs, and no route it does not
structured data one block naming the business, its type, its address, the area
                it says it covers and the services it lists. Every value comes
                from the content file, and a value that is absent is left out
```

The address of the site is a field the client owns, validated as an absolute
origin. It decides the sitemap, the canonical links and every share preview, so
an instance still announcing an example domain is an unfinished instance, and
the back office says so.

Nothing here may state what the site does not. An opening hour that cannot be
mapped, an award nobody entered, a rating nobody gave: left out. Structured
data claiming what the pages do not is the same false claim as an invented
legal fact, with a penalty attached.

## 15. What the runtime must provide

The back office, the uploads, the inbox, the rate limits and the push
subscriptions all need a server. That is a consequence of the deliverable, not a
preference, and it changes what the project is.

```
runtime      a server process, not a static export
storage      the content file, the uploads, the messages, the sessions, the
             subscriptions and the rate limit counters live in a writable data
             directory, or in a database when the instance outgrows files. The
             choice is recorded with the threshold that would change it
secrets      the password hash, the push keys and the session secret are server
             configuration, never in the repository and never in the bundle
backup       the data directory is what a restore needs, and the handover says
             so with the command. A backup is untested until a restore has been
             performed: take one, remove the directory, restore it, and load the
             site
retention    what the privacy page promises about how long a message is kept is
             enforced by the software, not by an intention. A period stated and
             not applied is a false statement in a published document
audit        the log lives in the data directory with everything else, and is
             part of what a backup carries
deployment   the handover states how the site is started, restarted and
             updated, and what happens to the data directory in each case
```

## 16. Prohibitions

- No demonstration content inside a component: no name, no photograph, no
  telephone number, no address, no price.
- No colour, radius, duration or font literal inside a component.
- No single palette: a site without a measured dark theme is not finished.
- No invented legal fact, registration number, insurance, certification,
  testimonial or client reference.
- No real person's identity, photograph or contact details used as sample data.
- No admin field that is not wired, and no admin route whose protection is a
  hidden link rather than a server side check.
- No login endpoint without a rate limit, and no public form endpoint without
  one either.
- No contact form that posts into nothing.
- No instance that departs from the shared shape of section 4: a private file
  layout, private custom property names, or a private admin contract. Each one
  is a tool that stops working on the next site.
- No form without a declared method: the fallback is GET, and GET puts a
  password or a visitor's message into the URL, the log and the Referer.
- No command, file path or environment variable shown to the client inside
  the back office.
- No structured data, sitemap entry or preview that claims something the
  site does not say on a page a visitor can read.
- No framework default 404.
- No optional section that renders an empty frame when its block is absent.
- No template declared finished before the gate in section 17 passes whole.

## 17. The completion gate

Twenty nine checks. All twenty nine pass, or the template is not finished.

```
1   every visitor facing string, image, colour, hour and contact detail
    resolves from the content file, verified by searching the components for
    literals and for the instance's own facts, and finding none
2   every required field is refused at load with a message naming the field
3   every optional block absent removes its section cleanly, verified on a
    content file with all of them removed
4   changing one token changes the rendered site, verified by changing one
5   both palettes measured on the rendered page, in the browser, reading the
    custom properties the stylesheet actually resolves, not the colours
    written in the content file; every required pair passing, both themes.
    A palette that is only read and not measured is how white on white ships
6   the theme toggle works, persists, respects the system preference and does
    not flash the wrong theme on load
7   the motion signature of the trade is visible: the effects it names happen,
    the ones it does not name do not, a staggered list arrives in sequence
    rather than as a block, and prefers-reduced-motion removes all of it
8   the layout uses the page width: no section centred in a narrow column
    except prose, and no horizontal scroll from 360px upward
9   every field the back office offers is changed, the public pages are read to
    see the change arrive, and the original value is put back; the content file
    then matches what it was, byte for byte. Not a sample: every field. The
    pages read are the ones the instance's sitemap declares and the fields are
    the ones `/api/admin/fields` publishes, so the check cannot quietly skip a
    page nobody remembered to add to a list, nor a field nobody rendered with
    the attribute a scraper was looking for
10  every field can be emptied and set again, and no two fields hold the same
    fact
11  an upload is accepted, rejected by type, rejected by size, and its alt text
    is required
12  the login is rate limited, verified by exceeding it and seeing the refusal;
    the session is server side; signing out invalidates it; an admin endpoint
    called without a session is refused
13  the password can be changed from the back office with the current one, and
    doing so ends every session
14  a contact submission arrives in the inbox, is counted unread, and the
    visitor sees the success state
15  every legal page the kind requires exists, is generated from the facts, and
    marks visibly every fact not provided
16  the 404 and the offline pages are the site's own, in both themes
17  the navigation is operable at 360px as a menu, with its button naming what
    it controls, Escape closing it and focus returning; the business name is
    readable at that width, and nothing tapped is under 44px
18  the favicon and the installed icons come from the content file, and
    changing them in the back office changes what the browser shows
19  the manifest is served, the service worker registers, the site works with
    the service worker unregistered and with notifications refused
20  every route is looked at, at 360px, in both themes, with no clipped text
21  the security headers are served, the policy carries a nonce, a value typed
    into a style field cannot close the tag, and a request body over the limit
    is refused before it is parsed
22  a backup is taken, the data directory removed, the backup restored and the
    site loaded; the retention the privacy page states is applied; every
    privileged action appears in the audit log
23  the dependencies carry no known vulnerability at the version pinned, and
    the handover names the day that was checked
24  the handover lists every back office field, the data directory, the backup
    command, and the secrets the instance needs
25  no form can submit by GET: every form declares its method, verified by
    reading the rendered markup, because a form without one falls back to GET
    and writes a password or a visitor's message into the URL, the server log
    and the Referer header
26  a page loaded without JavaScript says so where a form would have been, and
    points at a way to make contact that still works
27  the back office says what is left to do, computed from the content and not
    remembered: a fact still missing, an image still from the model, an address
    still unset. Every item a client can act on carries the link to where it is
    done, and fixing one closes it without anyone marking it done
28  nothing inside the back office asks the client to run a command, edit a
    file or set a variable. What only the installer can do names the installer
    and says to ask them. The commands belong in the handover
29  the shared shape of section 4 holds: the content file at its agreed path,
    the custom properties under their agreed names, and the four endpoints
    answering their agreed shapes, `/api/admin/fields` included. Verified by
    running a check written against another instance, not against this one. An
    instance nothing but its own scripts can check is a maintenance cost that
    grows with the fleet
```

## 18. Protocol

1. Establish the kind, portfolio or showcase, the trade, and the legal identity
   of the owner. The kind decides the contract, the routes and the legal
   surface.
2. Collect the facts that only the client has: legal identity, contact details,
   hours, services, prices, images and their rights. Record what is missing
   rather than filling it.
3. Fix the content contract for the kind, and write the loader that refuses a
   missing required field by name.
4. Author both palettes for the trade, measure every required pair, and set the
   motion intensity. Express every visual value as a token.
5. Build the public template against the contract: full width where the content
   is not prose, both themes, the motion system, the 404 and the offline page.
6. Build the back office: the sections of section 8, generated from the
   contract, with server side validation and atomic writes.
7. Secure the way in: password hash, server side sessions, rate limits on login
   and on the public form, a CSRF token, upload validation. Then try to get in
   without a session and confirm it fails.
8. Wire the contact form to the inbox, with the notification path and the
   failure path.
9. Generate the legal pages from the fact sheet, marking visibly every fact not
   yet provided.
10. Add the manifest, the service worker and the push subscription, each
    degrading to nothing when refused.
11. Produce the example content file with clearly fictional data, and run the
    site from it.
12. Run the twenty nine point gate in section 17, whole. Fix and re-run what a fix
    touched.
13. Write the handover: the field map, the data directory, the backup command,
    the secrets, and how the site is started and updated.

## 19. Auto-critique

Score from 0 to 5: the content contract holds everything a human would want to
change, both palettes are authored and measured, the motion system is driven by
the intensity rather than sprinkled, the layout uses the width it is given, the
back office actually writes what it shows and is protected on the server with a
rate limited way in, the contact form reaches an inbox, the legal pages are
built from provided facts with the missing ones marked, and the accessibility
rules were applied while building.

Threshold: no axis below 4, average at least 4.5. An admin route protected only
by a hidden link, a login endpoint without a rate limit, a contact form that
posts into nothing, a back office field that is not wired, or one invented legal
statement scores 0 overall: the first three are the ways this kind of site is
actually broken into or silently loses business, and the last two make the
delivery false.

## 20. Interfaces

- Upstream: `engineering-core`, `template-selection` when the work starts from
  an existing template rather than a blank page.
- Lateral: `design-system` for the token structure, `ui-ux-engineering` for the
  rendered experience, `frontend-engineering` for the implementation,
  `animation` for the motion the intensity scalar drives,
  `design-authenticity` so the result does not read as a generic default,
  `admin-console` for the back office, `authentication-security` and
  `session-security` for the way in, `rate-limiting` for the login and the
  public form, `input-validation` for every write, `file-handling` for the
  uploads, `backend-engineering` for the endpoints, `data-privacy` for what the
  privacy and cookie pages must state and for how long a message is kept,
  `accessibility-testing` for the verification, `seo-engineering` for the
  metadata, `deployment-engineering` and `backup-recovery` for the data
  directory.
- Downstream: `code-review-protocol`, `security-audit` on the admin surface,
  then `client-handover` with the field map and the operational instructions.
- Run by: the site-template-engineer agent, and the frontend-engineer when a
  template instance is being produced.
