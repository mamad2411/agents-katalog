---
name: jquery-plugins
description: Use when authoring jQuery plugins, integrating jQuery UI widgets, using jQuery Validation, or evaluating community plugins against safety and API-contract standards.
---

# jQuery Plugins

## Specialization

Author expert-level jQuery plugins using the canonical pattern, integrate jQuery UI and jQuery Validation correctly, and evaluate community plugins against authority, safety, and contract-stability standards — grounded in official jQuery plugin authoring documentation.

## Trigger Conditions

- Authoring a new jQuery plugin with `$.fn.pluginName`.
- Extending jQuery with `$.extend()` or `$.fn.extend()`.
- Integrating jQuery UI widgets (Draggable, Resizable, Dialog, Datepicker, Tabs, Accordion, etc.).
- Implementing jQuery Validation for client-side form rules.
- Evaluating a third-party jQuery plugin for adoption.
- Reviewing an existing plugin for API contract integrity, namespace leaks, or chaining support.

## Scope Boundaries

In scope:

- `$.fn.pluginName` canonical authoring pattern (IIFE wrapper, chainability, default options, destruction method).
- `$.extend()` for utility/namespace plugins; `$.fn.extend()` for element-bound plugins.
- jQuery UI widget factory (`$.widget()`) for stateful widget authoring.
- jQuery Validation integration: rule definition, custom validators, error placement, `submitHandler`.
- Community plugin evaluation criteria.

Out of scope:

- Event binding inside plugins (follow `jquery-events` delegation and namespacing rules).
- AJAX inside plugins (follow `jquery-ajax` security and Deferred patterns).
- Build tooling for npm-published jQuery plugins.

## Inputs

- Plugin purpose, target jQuery version, and expected API surface.
- Options schema and defaults.
- Destruction and cleanup requirements.
- jQuery UI version if widget factory is used.
- Form rule set if jQuery Validation is in scope.

## Required Outputs

- Plugin implementation using canonical IIFE and `$.fn` pattern.
- Public API: initialization, option update, destruction, method invocation.
- Namespace plan: event namespaces, data keys, and CSS class prefixes.
- jQuery UI widget implementation if stateful widget behavior is required.
- jQuery Validation configuration with all custom rule contracts documented.
- Community plugin evaluation report if adopting a third-party plugin.

## Core Patterns

### Canonical Plugin Pattern

```javascript
;(function($) {
  const pluginName = 'myPlugin';
  const defaults = {
    option1: 'value1',
    option2: true
  };

  function Plugin(element, options) {
    this.element = element;
    this.$element = $(element);
    this.settings = $.extend({}, defaults, options);
    this._name = pluginName;
    this.init();
  }

  $.extend(Plugin.prototype, {
    init: function() {
      // Setup — bind events using namespace
      this.$element.on('click.' + this._name, $.proxy(this._onClick, this));
    },
    _onClick: function(event) { /* private */ },
    update: function(options) {
      this.settings = $.extend({}, this.settings, options);
    },
    destroy: function() {
      this.$element.off('.' + this._name);
      this.$element.removeData(this._name);
    }
  });

  $.fn[pluginName] = function(options) {
    return this.each(function() {
      if (!$.data(this, pluginName)) {
        $.data(this, pluginName, new Plugin(this, options));
      }
    });
  };
}(jQuery));
```

**Key rules:**

- Wrap in an IIFE to protect `$` from conflicts.
- Store plugin instance in `.data()` to prevent re-initialization.
- Return `this.each()` to preserve jQuery chainability.
- Namespace all events: `'click.' + pluginName`.
- Implement `destroy()` that unbinds all events and removes data.

### jQuery UI Widget Factory

- Use `$.widget('namespace.widgetName', { ... })` for stateful widgets that need create/destroy lifecycle, option management, and event callbacks.
- Widget factory provides `_create()`, `_destroy()`, `_setOption()` hooks — do not reimplement these manually.
- Trigger widget events via `this._trigger('eventName', event, data)` — consumers bind with `$(el).on('widgetnameeventname', handler)`.
- Always call `this._super()` in overridden methods to preserve inherited behavior.

### jQuery Validation Integration

```javascript
$('#myForm').validate({
  rules: {
    email: { required: true, email: true },
    password: { required: true, minlength: 8 }
  },
  messages: {
    email: { required: 'Email is required', email: 'Enter a valid email' }
  },
  errorPlacement: function(error, element) {
    error.insertAfter(element.closest('.field-wrapper'));
  },
  submitHandler: function(form) {
    // Called only on valid submission — perform AJAX or native submit here
  }
});
```

- Define `submitHandler` — do not rely on default form submission from `.validate()`.
- Always provide `messages` — do not expose default internal error strings to users.
- Use `$.validator.addMethod()` for custom rules; register rules before calling `.validate()`.
- Server-side validation is mandatory — client-side validation is UI convenience only.

### Community Plugin Evaluation Criteria

| Criterion | Pass | Fail |
|---|---|---|
| Repository activity | Commit within 12 months | No commits > 2 years |
| jQuery version compatibility | Explicitly states supported jQuery versions | No version declaration |
| Security advisories | No open CVEs | Known unpatched CVE |
| API stability | Semver versioned | No version, frequent breaking changes |
| Chainability | Returns `this` or jQuery object | Breaks chains |
| Namespace hygiene | Uses plugin namespace for events/data | Pollutes `$.fn` with generic names |
| Destruction support | Has `destroy` or cleanup method | No cleanup |

Reject community plugins that fail two or more criteria. Record the evaluation result and reason code.

## Workflow

1. Determine plugin type: utility (`$.extend`) or element-bound (`$.fn`).
2. Define option schema and defaults.
3. Implement canonical IIFE pattern with chainability and destroy.
4. Namespace all events and data keys.
5. If stateful widget: use `$.widget()` factory.
6. If form validation: configure `.validate()` with `submitHandler` and `messages`.
7. If community plugin: run evaluation criteria and record result.

## Done Criteria

- Plugin is wrapped in IIFE with explicit `jQuery` parameter.
- `.data()` guards against re-initialization.
- `$.fn.pluginName` returns `this.each()`.
- All events use plugin namespace.
- `destroy()` unbinds all events and removes `.data()`.
- jQuery Validation `submitHandler` is defined.
- Community plugin evaluation record exists if third-party plugin was adopted.

## References

- [jQuery Learn: Plugins](https://learn.jquery.com/plugins/)
- [jQuery Learn: Authoring a jQuery Plugin](https://learn.jquery.com/plugins/basic-plugin-creation/)
- [jQuery UI Widget Factory](https://jqueryui.com/widget/)
- [jQuery UI Demos](https://jqueryui.com/demos/)
- [jQuery Validation Docs](https://jqueryvalidation.org)
- [jQuery Validation: $.validator.addMethod()](https://jqueryvalidation.org/jQuery.validator.addMethod/)
