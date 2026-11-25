---
name: nuget-package-propertychanged-sourcegenerator
description: Use when working with C# properties that need INotifyPropertyChanged notifications.
metadata:
  homepage: "https://github.com/canton7/PropertyChanged.SourceGenerator"
  version: "PropertyChanged.SourceGenerator 1.1.2"
  last-updated: "2026-10-30"
  generated-by: "gpt-6.1-terra"
---

# PropertyChanged.SourceGenerator

## Prerequisite

Assume the project already has `PropertyChanged.SourceGenerator` installed. If a compiler error suggests the package is missing, check the affected project's dependencies. If it is absent, ask the user for approval before installing it with `dotnet add <project.csproj> package PropertyChanged.SourceGenerator`.

## Why this package is useful

Annotated fields replace repetitive property setters, equality checks, and notification calls, reducing boilerplate. Dependent-property notifications and hooks keep related behavior close to the properties.

## Usage

Use a `partial` class and put `[Notify]` on backing fields:

```csharp
using PropertyChanged.SourceGenerator;

public partial class PersonViewModel
{
    [Notify] private string _firstName = "";
    public string DisplayName => $"Hello, {FirstName}";
}
```

The generator supplies missing `INotifyPropertyChanged` infrastructure. By default, `_firstName` becomes a public `FirstName` property with public accessors. Its setter compares values using `EqualityComparer<T>.Default` and raises notifications only when the value differs. Use the generated property rather than its backing field when notifications are needed.

Use `[Notify("GivenName")]` to override a property name, or `[Notify(Setter.Private)]` to restrict its setter. XML documentation placed before `[Notify]` is copied to the generated property.

### Dependent properties

In the example, changing `FirstName` also notifies `DisplayName`. Automatic detection requires getters to read properties on the same instance, not backing fields; it does not observe properties on other objects.

When dependencies cannot be inferred, put `[DependsOn(nameof(FirstName))]` on the dependent property, or `[Notify, AlsoNotify(nameof(DisplayName))]` on the source backing field.

Use property names, not field names. `[DependsOn(...)]` replaces automatic detection for that property, so list all intended dependencies; empty `[DependsOn]` disables automatic detection for it. These attributes raise notifications, not assignments or recalculations of stored property values.

### Change hooks

Define an ordinary method in the same partial class using the generated property name. Supported property hooks are `OnFirstNameChanged()` or `OnFirstNameChanged(string oldValue, string newValue)`. For a hook reached through a dependent-property notification, the old value can be `default(T)`.

Before-change notifications are opt-in: the class or a base class must implement `INotifyPropertyChanging`. Its property hooks are `OnFirstNameChanging()` or `OnFirstNameChanging(string oldValue)`.

## Notes

The generator does not rewrite existing property setters. It supports existing notification implementations and base classes; if generation fails with a base class, inspect the diagnostic and its event-raising method signature before adding duplicate infrastructure.

## Further reference

The [project homepage](https://github.com/canton7/PropertyChanged.SourceGenerator) covers details intentionally omitted here: `[IsChanged]` tracking, type-wide hooks, inherited dependency handling, supported base-class event-raising signatures, virtual properties, forwarding attributes with `[PropertyAttribute]`, `.editorconfig` customization, and version-specific build compatibility or workarounds. Consult it only when the task needs those details.

Do not fetch the homepage for information already covered here.
