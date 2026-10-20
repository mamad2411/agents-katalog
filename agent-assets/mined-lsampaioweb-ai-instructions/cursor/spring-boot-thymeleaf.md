---
description: "Spring Boot Thymeleaf contract for page controllers, templates, form binding, fragments, and static assets."
globs: "**/pom.xml,**/*PageController.java,**/src/main/resources/templates/**/*.html,**/src/main/resources/static/**"
alwaysApply: false
---

# Spring Boot Thymeleaf Contract

These rules apply when an application serves server-rendered HTML with
Thymeleaf. REST JSON APIs stay in the controller contract. Form validation
error handling stays in the exception contract. Message bundles and locale
resolution stay in the i18n contract. Lombok ownership of form-bean annotations
stays in the Lombok contract. CSRF for browser forms stays in the Security
contract when Security is present.

Applications that ship HTML pages must meet this contract.

## Dependency

- Add `spring-boot-starter-thymeleaf` only when the application renders HTML
  pages.
- Keep a one-line purpose comment above the dependency (pom contract).

## Page controllers

- Use `@Controller` for server-rendered pages. Never use `@RestController` for
  HTML views.
- Name classes `<Feature>PageController` (architecture contract). Never use a
  bare `PageController` or a `*PageRoutes` name for feature pages.
- Keep page controllers thin: bind input, call a service interface, choose a
  view name or redirect. Do not put business rules in the controller or in the
  template.
- Return a logical view name (for example `task/form`) or a redirect
  (`redirect:/tasks`). Do not write HTML from Java.

## Templates and static assets

- Put templates under `src/main/resources/templates/`.
- Put CSS, JavaScript, and other static files under `src/main/resources/static/`.
- Reference static assets with Thymeleaf link expressions such as
  `th:href="@{/css/style.css}"` and `th:src="@{/js/script.js}"`.
- Prefer feature-oriented template paths (for example `task/form.html`) over a
  flat dump of unrelated pages in the templates root when the app has multiple
  features.

## Forms

- Use mutable form-backing classes with `@Getter` and `@Setter` for binder
  population (Lombok contract). Do not use records or `@Data` for form beans.
- Bind with `th:object` and `th:field`.
- Annotate form posts with `@Valid` and accept `BindingResult`. On field errors,
  re-render the same view. On success, use the Post-Redirect-Get pattern
  (`redirect:…`) (exception contract).
- Show field errors with `th:errors` / `#fields.hasErrors` (and optional error
  CSS classes). Do not convert MVC field errors into the REST JSON error
  envelope.

## Internationalization in templates

- Resolve every user-visible template string (page titles, headings, labels,
  buttons, empty-state text, column headers) with Thymeleaf message expressions
  (`#{…}`) backed by the i18n bundles.
- Keep validation constraint messages on message keys (for example
  `{task.title.required}`), not inline English.
- Do not hardcode English (or any locale) UI copy in HTML templates for real
  apps.

## Fragments and AJAX

- Use Thymeleaf fragments (`template :: fragmentName`) when the response should
  be a partial HTML snippet (AJAX / htmx-style updates).
- Full-page navigations return a plain view name without a fragment selector.
- Keep fragment markup in the same feature template that owns the full page when
  practical.

## Security interaction

- When Spring Security is present, keep CSRF enabled for browser form posts
  (Security contract) and include the CSRF token in forms.
- Do not disable CSRF solely because Thymeleaf is in use.

## Forbidden

- Never render HTML from a `@RestController`.
- Never name an MVC page controller `PageController` or `*PageRoutes` when a
  feature-specific `<Feature>PageController` name is available.
- Never put business logic in Thymeleaf templates.
- Never hardcode user-visible UI copy in templates; use `#{…}` keys.
- Never use `@Data` or records for mutable form-backing objects.
- Never skip `BindingResult` handling on `@Valid` form posts.
- Never use Thymeleaf templates as the response body for REST JSON APIs.
