---
name: mj-product
description: "Majordomus product: The domains; One feature; The features; Features against interfaces; The providers; Validate the model."
argument-hint: "[request]"
---
<!-- GENERATED FILE — DO NOT EDIT DIRECTLY
     Source: module:product; regenerate with `majordomus generate`
     Generator: majordomus-cli 1.2.0 -->

# Majordomus `product`

The capabilities the Majordomus registry declares in its module `product`. Choose the one that answers the request below — or, without one, the person's last request about `product` — call it through its MCP tool, and report what it answers, as it answered:

$ARGUMENTS

| Capability | What it is | MCP tool | Command line | Effect |
|---|---|---|---|---|
| `product.domains` | The domains | `majordomus_product_domains` | `majordomus product domains` | reads |
| `product.feature` | One feature | `majordomus_feature` | `majordomus product show` | reads |
| `product.features` | The features | `majordomus_features` | `majordomus product list` | reads |
| `product.matrix` | Features against interfaces | `majordomus_product_matrix` | `majordomus product matrix` | reads |
| `product.providers` | The providers | `majordomus_providers` | `majordomus product providers` | reads |
| `product.validate` | Validate the model | `majordomus_product_validate` | `majordomus product validate` | reads |

A capability that *changes* something runs only when the person asked for that change: call it once, and if it is refused or its outcome is not known, report that as it is and do not try again by another way. One that *reads* may be called whenever the request needs it.

Without the Majordomus MCP server attached, run the command line form from the repository root; `--help` shows its arguments. What each capability accepts and answers is defined once, in its declaration: `majordomus capabilities describe <id>`, or the MCP tool's own description. This file is derived from the registry and says nothing the declarations do not.
