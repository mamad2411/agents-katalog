---
name: Ruby
description: Write expressive Ruby with blocks, metaprogramming, and idiomatic patterns.
metadata: {"clawdbot":{"emoji":"💎","requires":{"bins":["ruby"]},"os":["linux","darwin","win32"]}}
---

# Ruby Development Rules

## Blocks and Procs
- `do...end` for multi-line, `{}` for single line — convention, both work
- `yield` calls the block — `block_given?` checks if block passed
- `&block` captures block as Proc — can store, pass around, call later
- Lambda checks argument count, Proc doesn't — lambda returns from lambda, Proc returns from enclosing method
- `->` is stabby lambda syntax — `add = ->(a, b) { a + b }`

## Methods
- Last expression is implicit return — no `return` needed unless early exit
- `?` suffix for boolean methods — `empty?`, `valid?`, convention not enforcement
- `!` suffix for dangerous methods — usually mutates in place or raises instead of returning nil
- Parentheses optional — omit for DSLs and zero-arg, use for clarity with arguments
- `*args` splat for variable arguments — `**kwargs` for keyword arguments

## Truthiness
- Only `nil` and `false` are falsy — `0`, `""`, `[]` are truthy
- `||=` for memoization — `@user ||= fetch_user` caches on first call
- `&&` and `||` return actual values — not booleans, useful for defaults
- `nil?` checks nil specifically — `blank?` is Rails (nil, empty, whitespace)

## Symbols vs Strings
- Symbols are immutable, interned — same `:name` is same object everywhere
- Symbols for keys, identifiers — strings for text content
- Symbol keys in hashes: `{ name: "Ruby" }` — shorthand for `{ :name => "Ruby" }`
- `to_sym` and `to_s` convert — but don't convert user input to symbols (memory leak)

## Collections
- `each` for iteration — `map` for transformation
- `select`/`reject` for filtering — return new array
- `find` returns first match — `nil` if none, not exception
- `reduce`/`inject` for accumulation — `[1,2,3].reduce(0) { |sum, n| sum + n }`
- `compact` removes nils — `flatten` collapses nested arrays

## Classes
- `attr_accessor` for getter and setter — `attr_reader` read-only, `attr_writer` write-only
- `initialize` is constructor — instance variables start with `@`
- `self.method` for class methods — or `class << self` block for multiple
- Inheritance with `<` — `class Dog < Animal`
- Modules for mixins — `include` adds instance methods, `extend` adds class methods

## Metaprogramming
- `method_missing` catches undefined calls — always define `respond_to_missing?` too
- `define_method` creates methods dynamically — takes name and block
- `send` calls method by name — `obj.send(:method_name, args)`
- Open classes: can add methods to any class — use responsibly, prefer refinements
- `class_eval` and `instance_eval` — change self for block evaluation

## Scope
- `def`, `class`, `module` create scope gates — block variables leak in older Ruby, not anymore
- Constants are UPPERCASE — looked up lexically then by inheritance
- `::` for namespacing — `Module::Class::CONSTANT`
- Global variables `$` are code smell — avoid except built-ins like `$stdout`

## Common Mistakes
- `==` for equality, `equal?` for identity — opposite-ish of Java
- String interpolation only in double quotes — `"Hello #{name}"` not `'Hello #{name}'`
- Modifying while iterating is allowed — but confusing, prefer `map`/`select` to build new
- Ranges: `1..5` includes 5, `1...5` excludes — three dots exclude end
- `require` vs `require_relative` — relative for same project, require for gems

## Gems and Bundler
- `Gemfile` lists dependencies — `bundle install` installs them
- `Gemfile.lock` pins versions — commit it for reproducible builds
- `bundle exec` runs with bundled gems — avoids version conflicts
- Semantic versioning: `~> 2.1` allows 2.x — `>= 2.1, < 3.0` equivalent
