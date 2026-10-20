---
name: terraform-provider
description: How to build and publish a Terraform provider with the Plugin Framework (https://developer.hashicorp.com/terraform/plugin/framework) - project-agnostic. Covers the provider server shape and configuration, resources and data sources, schema attributes and types, plan modifiers and validators, CRUD and Read-based drift detection, ImportState and state handling, diagnostics, timeouts, acceptance testing with terraform-plugin-testing (TF_ACC), local development with dev_overrides, documentation generation with tfplugindocs, and Registry publishing (GPG signing, terraform-registry-manifest.json, GoReleaser). Use when writing or reviewing a Terraform provider resource or data source, adding a new attribute, debugging plan/apply behavior, or setting up provider release automation.
---

# Terraform providers (Plugin Framework)

A provider is a plugin that Terraform talks to over a protocol (gRPC),
translating HCL into API calls and reconciling remote state. The modern
way to write one is the **Plugin Framework**
([docs](https://developer.hashicorp.com/terraform/plugin/framework)),
which supersedes the older SDKv2. Use the Framework for new providers.

## The moving parts

```
main.go                        # serve the provider via providerserver
internal/provider/
  provider.go                  # provider schema + Configure (client setup)
  <name>_resource.go           # one file per resource
  <name>_data_source.go        # one file per data source
internal/client/               # your API client (add an interface for testability)
```

```go
func main() {
    opts := providerserver.ServeOpts{
        Address: "registry.terraform.io/example/example",
        Debug:   false,
    }
    err := providerserver.Serve(context.Background(), New, opts)
    if err != nil { /* log.Fatal */ }
}
```

- **Address** is `registry.terraform.io/<namespace>/<type>`, where
  `<type>` is the repo suffix after `terraform-provider-`. The resource
  prefix is separate; it just has to be unique within the provider.
- The **provider function** (`New`) returns a `provider.Provider` with
  `Schema`, `Resources`, `DataSources`, and `Configure`.

## Resources vs data sources

| | Resource | Data source |
| --- | --- | --- |
| Managed state | yes (CRUD) | no (read-only) |
| Interface | `Create`, `Read`, `Update`, `Delete` | `Read` |
| HCL | `resource "x_y" ...` | `data "x_y" ...` |
| Purpose | creates/owns infrastructure | looks up existing data |

If it doesn't have a lifecycle you manage, it's a data source. If it
does, it's a resource.

## Schema

```go
resp.Schema = schema.Schema{
    MarkdownDescription: "Manages an example widget.",
    Attributes: map[string]schema.Attribute{
        "id": schema.StringAttribute{
            Computed:            true,
            MarkdownDescription: "Server-assigned id.",
        },
        "name": schema.StringAttribute{
            Required:            true,
            MarkdownDescription: "Widget name.",
            Validators:          []validator.String{
                stringvalidator.LengthAtLeast(1),
            },
        },
        "tags": schema.MapAttribute{
            Optional:    true,
            ElementType: types.StringType,
        },
    },
}
```

- Exactly one of `Required`/`Optional`/`Computed` per attribute, with
  the valid combinations (`Optional`+`Computed` for defaults the server
  assigns).
- Use `MarkdownDescription` (shows in Registry docs); it's required in
  practice for a publishable provider.
- Add `Validators` for input rules, `PlanModifiers` for plan-time
  behavior (e.g. `RequiresReplace` when the API can't update a field).
- `Sensitive: true` for secrets — but prefer write-only/ephemeral
  attributes for credentials where the framework version supports them.

## CRUD and state

- `Create` calls the API, then sets the `id` and all computed
  attributes into state.
- `Read` refreshes state from the API. **If the object is gone, call
  `resp.State.RemoveResource(ctx)`** — that's how Terraform detects
  drift and plans a recreate.
- `Update` reconciles changes; only mark a field `RequiresReplace` if
  the API genuinely can't update it.
- `Delete` removes the remote object; treat "already gone" as success.
- Return **diagnostics**, not Go errors: `resp.Diagnostics.Append(...)`
  with `AddError`/`AddAttributeError` so Terraform can attribute the
  problem to a specific attribute.

## Import

Support import so `terraform import` and import blocks work:

```go
func (r *widgetResource) ImportState(ctx context.Context,
    req resource.ImportStateRequest, resp *resource.ImportStateResponse) {
    resource.ImportStatePassthroughID(ctx, path.Root("id"), req, resp)
}
```

For composite ids, split the import id and set each attribute.

## Plan modifiers

| Modifier | Use |
| --- | --- |
| `RequiresReplace()` | force recreation when the field changes |
| `UseStateForUnknown()` | carry an unknown computed value forward (stop spurious `(known after apply)`) |
| `RequiresReplaceIfConfigured()` | replace only when explicitly set |
| `Default`/`DefaultAttribute` | supply defaults (Framework v1.13+) |

`UseStateForUnknown` on computed ids is the usual fix for a plan that
shows a new value on every run.

## Testing

Two layers:

1. **Unit tests** of pure logic (validators, id parsing, client
   mapping) with plain `go test`.
2. **Acceptance tests** with
   [`terraform-plugin-testing`](https://developer.hashicorp.com/terraform/plugin/testing):
   run real `terraform apply`/`refresh`/`destroy` against a real (or
   mocked) API.

```go
func TestWidgetResource(t *testing.T) {
    resource.Test(t, resource.TestCase{
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        Steps: []resource.TestStep{
            {Config: `resource "example_widget" "t" { name = "a" }`,
             Check: resource.TestCheckResourceAttr("example_widget.t", "name", "a")},
        },
    })
}
```

- Acceptance tests are gated on `TF_ACC=1`; without it they skip, so
  `go test ./...` stays offline-safe.
- Use `resource.TestCheckResourceAttr`, `ImportState` steps, and
  `ExpectError` for negative cases. `PlanOnly`/`ExpectNonEmptyPlan` for
  plan behavior.
- `terraform-plugin-testing` can run against a mocked server for
  providers that don't want live-infra tests.

## Docs and release

- Generate docs with [`tfplugindocs`](https://github.com/hashicorp/terraform-plugin-docs)
  (`go generate ./...`), which turns `Description`/`MarkdownDescription`
  and `examples/` into `docs/`. **Never hand-edit `docs/`** — CI should
  fail if it's stale.
- Release via GoReleaser, producing cross-compiled binaries, checksums,
  and GPG signatures, plus `terraform-registry-manifest.json`.
- The Registry requires signed checksums; the GPG key is registered with
  HashiCorp once during the (manual) GitHub App linking step.

## Local dev

Skip `terraform init` and test the provider from source with
`dev_overrides`:

```hcl
# ~/.terraformrc
provider_installation {
  dev_overrides {
    "registry.terraform.io/example/example" = "/path/to/go/bin"
  }
  direct {}
}
```

Then `go build -o $(go env GOPATH)/bin/terraform-provider-example .` and
run `terraform plan`/`apply` directly (init errors under overrides;
that's expected). Use a separate `examples/local/` dir for this.

## Where to look

| File | Covers |
| --- | --- |
| [`references/framework-schema.md`](references/framework-schema.md) | provider/resource/data-source schema, attributes, validators, plan modifiers |
| [`references/crud-and-state.md`](references/crud-and-state.md) | CRUD, Read/drift, import, diagnostics, timeouts, state |
| [`references/acceptance-testing.md`](references/acceptance-testing.md) | terraform-plugin-testing, TF_ACC, mocks, CI |
| [`references/docs-and-publishing.md`](references/docs-and-publishing.md) | tfplugindocs, GoReleaser, GPG, Registry linking |

## What NOT to do

- Don't write a new provider on SDKv2 — use the Plugin Framework.
- Don't return Go errors from CRUD; append diagnostics so Terraform can
  render and attribute them.
- Don't forget to remove state on `Read` when the remote object is gone
  — that's the whole drift-detection mechanism.
- Don't mark every field `RequiresReplace` "to be safe"; it forces
  destroy/recreate and data loss for updatable fields.
- Don't hand-edit generated `docs/` or commit a stale copy — wire
  `tfplugindocs` into CI and fail when the output changes.
- Don't put secrets in plain state-bearing attributes if the framework's
  write-only/ephemeral options can keep them out of state.
