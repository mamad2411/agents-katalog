# apply-spinner

Apply or restore custom spinner verbs to Claude Code settings.

## Usage
```
/my-friends-claude:apply-spinner          # 커스텀 스피너 적용
/my-friends-claude:apply-spinner restore  # 원본 스피너로 복원
```

## Instructions

When this skill is invoked:

### Apply (기본 동작, 인자 없음 또는 `apply`)

1. Read `config/config.json` from the plugin directory and extract `spinnerVerbs.verbs` array
2. Check if `spinnerVerbs.enabled` is `true`
3. Read the user's `~/.claude/settings.json` (create if not exists)
4. If `spinnerVerbs` key already exists in settings.json, back it up by saving the current value as `_spinnerVerbs_backup` in the same file
5. Set `spinnerVerbs` in `~/.claude/settings.json` to an object with `mode` and `verbs` keys
6. Confirm: "스피너 동사가 커스터마이즈되었습니다! Claude Code를 재시작하면 적용됩니다."
7. Show a few example verbs from the applied list

### Restore (인자가 `restore` 또는 `원복`)

1. Read `~/.claude/settings.json`
2. If `_spinnerVerbs_backup` exists, restore `spinnerVerbs` to that value and remove `_spinnerVerbs_backup`
3. If no backup exists, remove the `spinnerVerbs` key entirely (reverts to Claude Code defaults)
4. Confirm: "스피너 동사가 원본으로 복원되었습니다! Claude Code를 재시작하면 적용됩니다."

### Important Notes
- The `spinnerVerbs` setting in `~/.claude/settings.json` accepts an object with `mode` and `verbs` keys
- Format: `"spinnerVerbs": {"mode": "replace", "verbs": ["verb1", "verb2", ...]}`
- `mode` can be `"replace"` (기본값 대체) or `"append"` (기본값에 추가)
- Changes require a Claude Code restart to take effect
- The `_original_mapping` field in config.json is documentation only — do NOT write it to settings.json
- Only write the `verbs` array values to settings.json
- **자동 적용/원복**: 세션 시작 시 자동 적용, 세션 종료 시 자동 원복됩니다. 이 스킬은 수동으로 즉시 적용/원복할 때 사용하세요.
- 자동 적용/원복은 `scripts/spinner-manage.sh`가 처리하며, `session-start.sh`와 `stop.sh` Hook에서 호출됩니다.
