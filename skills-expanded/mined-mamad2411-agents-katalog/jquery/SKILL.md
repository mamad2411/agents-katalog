---
name: jquery
description: >
  jQuery best practices for maintaining legacy codebases and planning migration
  to vanilla JavaScript. Use this skill when working on projects that use jQuery,
  optimizing jQuery performance, or incrementally replacing jQuery with modern
  browser APIs. Covers DOM manipulation, event handling, AJAX, plugins, and
  migration patterns.
license: MIT
metadata:
  author: skillbox
  version: "1.0"
  category: frontend
  tags: jquery, javascript, dom, legacy, migration
---

# jQuery Best Practices

## When jQuery Is Still Appropriate

Use jQuery when maintaining an existing codebase that depends on it or when supporting very old browsers. Do not introduce jQuery into new projects because vanilla JavaScript now covers every jQuery use case.

## DOM Manipulation

Cache selectors. Every `$(selector)` call traverses the DOM.

```javascript
// Bad: three DOM lookups
$('#panel').addClass('active');
$('#panel').text('Welcome');
$('#panel').show();

// Good: one lookup, chained
const $panel = $('#panel');
$panel.addClass('active').text('Welcome').show();
```

Use `.find()` to scope queries within a cached parent:

```javascript
const $form = $('#signup-form');
const $email = $form.find('input[name="email"]');
```

Minimize DOM writes. Build HTML in bulk, then insert once:

```javascript
// Bad: reflow on every iteration
users.forEach(u => $('#list').append('<li>' + u.name + '</li>'));

// Good: single insert
const html = users.map(u => '<li>' + $('<span>').text(u.name).prop('outerHTML') + '</li>').join('');
$('#list').append(html);
```

Use `.text()` for user-provided content to prevent XSS. Only use `.html()` for trusted content.

## Event Handling and Delegation

Use event delegation for dynamic content. Attach handlers to a stable parent element.

```javascript
// Bad: breaks when new items are added
$('.delete-btn').on('click', function() { /* ... */ });

// Good: delegated on stable parent
$('#item-list').on('click', '.delete-btn', function() {
  $(this).closest('.item').remove();
});
```

Use namespaced events to safely remove your handlers without affecting others:

```javascript
$('#modal').on('click.myPlugin', '.close', closeModal);
$('#modal').off('.myPlugin'); // removes only your handlers
```

## AJAX

Use `$.ajax()` for full control. Set global defaults for common headers.

```javascript
$.ajaxSetup({
  headers: { 'X-CSRFToken': $('meta[name="csrf-token"]').attr('content') },
  timeout: 10000,
});

$.ajax({
  url: '/api/orders',
  method: 'POST',
  contentType: 'application/json',
  data: JSON.stringify({ items: cart.getItems() }),
  success: function(order) { window.location.href = '/orders/' + order.id; },
  error: function(jqXHR) { showErrors(jqXHR.responseJSON?.errors); },
});
```

## Plugin Patterns

Return `this` for chaining. Accept options with sensible defaults.

```javascript
(function($) {
  $.fn.smoothCollapse = function(options) {
    var settings = $.extend({ speed: 300, easing: 'swing' }, options);
    return this.each(function() {
      var $trigger = $(this).find('[data-trigger]');
      var $content = $(this).find('[data-content]');
      $trigger.on('click', function() {
        $content.slideToggle(settings.speed, settings.easing);
      });
    });
  };
})(jQuery);

$('.collapsible').smoothCollapse({ speed: 200 });
```

## Performance

Detach elements before making many changes, then reattach:

```javascript
var $list = $('#large-list').detach();
$list.find('li').addClass('processed');
$list.appendTo('#container'); // single reflow
```

Prefer CSS classes over `.show()`/`.hide()` for toggling visibility:

```javascript
$el.toggleClass('is-hidden'); // faster than $el.toggle()
```

## Migration: jQuery to Vanilla JS

Replace incrementally, one pattern at a time.

```javascript
// Selectors
$('.item')          → document.querySelectorAll('.item')
$('#main')          → document.getElementById('main')

// DOM manipulation
$el.addClass('on')  → el.classList.add('on')
$el.text('Hi')      → el.textContent = 'Hi'

// Delegated events
$('#list').on('click', '.item', fn)
→ document.getElementById('list').addEventListener('click', e => {
    const item = e.target.closest('.item');
    if (item) fn.call(item, e);
  })

// AJAX
$.get('/api/data')  → fetch('/api/data').then(r => r.json())

// Animation
$el.fadeOut(300)    → el.animate([{opacity:1},{opacity:0}], {duration:300})
                       .finished.then(() => el.style.display = 'none')
```

## jQuery UI Alternatives

| jQuery UI | Modern Replacement |
|---|---|
| Datepicker | `<input type="date">` or Flatpickr |
| Dialog | `<dialog>` element |
| Sortable | SortableJS |
| Autocomplete | Headless UI Combobox |
| Tooltip | Floating UI |

```html
<!-- Native dialog replaces jQuery UI Dialog -->
<dialog id="confirm">
  <p>Are you sure?</p>
  <form method="dialog">
    <button value="cancel">Cancel</button>
    <button value="confirm">Confirm</button>
  </form>
</dialog>
<script>
  const d = document.getElementById('confirm');
  d.showModal();
  d.addEventListener('close', () => { if (d.returnValue === 'confirm') doAction(); });
</script>
```

## Common Pitfalls

Do not mix jQuery and vanilla references without converting: use `$el[0]` to get raw DOM or `$(el)` to wrap. Do not use `$(document).ready()` -- use `defer` on script tags instead. Do not store data with `.attr('data-*')` when it is only needed in JS -- use `.data()` or a Map.
