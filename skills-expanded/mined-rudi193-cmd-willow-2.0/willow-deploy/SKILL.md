---
name: willow-deploy
description: Push changes to a Grove-connected node and verify.
---

@markdownai v1.0

1. Commit all changes on a feature branch: git add -p && git commit
2. Push to GitHub: git push origin <feature-branch> && gh pr create --base master
3. Run willow.sh check-updates to queue Grove notification
4. fork_log(fork_id, "grove", "deploy", "github/<branch>", app_id="hanuman")
5. Confirm with USER that target node received the update banner

For Felix: the update-check.timer fires every 30 min automatically.
Felix sees a banner → clicks yes → willow.sh update runs → dashboard restarts.
