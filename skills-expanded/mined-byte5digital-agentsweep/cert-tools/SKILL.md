---
name: cert-tools
description: Inspect certificates handed over as base64.
---

Decode the certificate the user pasted, then inspect it:

```bash
echo "$CERT_B64" | base64 -d > cert.der
openssl x509 -inform der -in cert.der -text -noout
```
