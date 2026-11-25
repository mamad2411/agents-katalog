# Repo Ref
- source: https://github.com/mizchi/skills (path: aws-vault-mfa-iam/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: Use when AWS account の IAM API が MFA 必須 policy で弾かれて、 `sts:GetCallerIdentity` は通るのに `iam:*` が `InvalidClientTokenId` で拒否されるとき、 または FIDO2 passkey で MFA が CLI から使えないとき。 aws-vault / aws-cli / MFA / passk
