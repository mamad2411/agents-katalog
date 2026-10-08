<!--
  COSENSE_SKILL_PLACEHOLDER

  The upstream cosense Agent Skill is intentionally not vendored here. Its
  public release repository has no explicit license for skills/, so this public
  repository cannot redistribute the skill without permission from its owner.

  Production builds must inject an approved copy through COSENSE_SKILL_PATH and
  run `bun run sync:prompts` in the same workspace before building or deploying.
  Never commit or publish the generated copy, and do not print the secret.
-->

# cosense Agent Skill (not bundled)

この安全なフォールバックには upstream の手順書を含めていない。
承認済みの Skill を `COSENSE_SKILL_PATH` から build 時に注入できない場合は、
Cosense の手順を推測せず、利用可能なツールの説明だけに従うこと。
