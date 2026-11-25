---
name: zero-downtime-cloud-move
description: "Runbook for moving a live app from one cloud to another (Google Cloud to AWS, AWS to Google Cloud, a PaaS to your own account, or one storage provider to another) without downtime. The agent inventories what is really running, builds the new stack next to the old one, keeps a one-line rollback for every phase, proves the new stack with real workloads before any traffic moves, cuts over with a checklist, watches a fixed window after the switch, copies data with an idempotent job whose second pass must report 0 left, and deletes the old cloud last. Use when someone asks to migrate, move or replatform a production app, switch cloud providers, move a backend, database files or object storage, plan a DNS cutover, or decommission an old cloud account."
---

# Zero-Downtime Cloud Move

Move a live app between clouds while users keep using it. The output is a move that is finished and proven: a written inventory, a phase plan where every phase has a rollback, evidence from real workloads, a cutover log, a watch report, a data copy whose second pass reports 0 left, and an old cloud with nothing running in it.

Five rules. Write them at the top of the plan file and do not trade them away for speed:

1. **Verify, do not remember.** Every fact in the plan (what serves traffic, where DNS points, which settings are live) comes from a command you ran today, with the command next to it.
2. **Parallel, not in place.** The new stack is built next to the old one. The old one keeps serving until the switch and stays intact through the watch window.
3. **One-line rollback per phase.** Before a phase starts, write the single command or single setting that undoes it. If you cannot write it, the phase is too big: split it.
4. **Real workloads before the switch.** Health checks are not proof. Run the product's real jobs end to end on the new stack, including the longest one.
5. **Decommission last.** Nothing in the old cloud is deleted until the watch window is clean and the old side has served zero requests.

The human approves anything that changes production or cannot be undone: the traffic switch, deleting data, deleting old resources, closing accounts. Prepare everything, show the exact command, then wait for the go.

## The five phases

| Phase | What happens | Rollback (one line) | Done when |
| --- | --- | --- | --- |
| 1. Inventory | Write down what is really running, verified live | Nothing changed yet | Every row in `templates/INVENTORY.md` has evidence |
| 2. Decouple | Put each provider-specific dependency behind one switch (a setting or flag), old path left intact | Unset the setting | App runs with the new provider selected and with the old one, same tests pass |
| 3. Build in parallel | Stand up the new stack next to the old one; no user traffic | Delete the new stack; users never saw it | New stack is healthy and reaches the database and every dependency |
| 4. Prove and switch | Real workloads on the new stack, then move traffic, then watch | Point traffic back at the old stack | Watch window clean, old side at 0 requests |
| 5. Copy data and decommission | Idempotent copy with a second pass of 0, then delete the old cloud | Before deletion: switch the reader back. After deletion: none, so it is last | Second pass reports 0, old cloud has no resources for the app |

Copy `templates/MOVE-PLAN.md` into the project and keep it current. It is the single place the human looks.

## Phase 1: inventory first

Do not design the target until you know the source. Fill in `templates/INVENTORY.md` from live commands, not from the README, the diagram or memory.

Find, with evidence for each:

- **Entry points.** Every hostname users or other systems call, what each resolves to, and which load balancer or service answers.
- **Compute.** Every service, the exact revision or image serving traffic, its CPU, memory, scaling limits and request timeout.
- **Configuration.** Every environment variable and secret name on the live revision (names only in the plan; values never leave the secret store).
- **Data.** Databases, object storage (bucket count, object count, total size), queues, caches, cron jobs and scheduled tasks.
- **Outbound dependencies.** Third-party APIs, model providers, email, payments, auth, analytics. Mark which are tied to the old cloud.
- **DNS.** Where the zone is hosted, every record, the TTLs. Export the full zone to a file before touching it.
- **Traffic shape.** Requests over the last 30 days, peak hour, longest request or stream duration, background jobs.
- **Hidden limits.** Request timeouts, body size limits, idle timeouts, cold starts. Compare the longest real request to the target's hard limits before choosing the target service.

Commands that answer these (examples; adapt to the provider):

```bash
# Where does the name point, and how long is it cached?
dig +noall +answer app.example.com A app.example.com AAAA
dig +short NS example.com

# Google Cloud: what serves traffic, and with which settings?
gcloud run services list --format='table(metadata.name,status.url,status.latestReadyRevisionName)'
gcloud run services describe <service> --region <region> --format=json   # env names, limits, timeout
gcloud compute forwarding-rules list
gcloud storage du -s gs://<bucket>

# AWS: the same questions
aws ecs list-services --cluster <cluster>
aws ecs describe-task-definition --task-definition <family>              # env names, limits
aws elbv2 describe-load-balancers
aws s3 ls s3://<bucket> --recursive --summarize | tail -2
```

The inventory is done when a second agent, given only the file, could name every moving part and nothing in production surprises it. Present it to the human with the three biggest risks and the limits that constrain the target choice.

## Phase 2: decouple behind one switch

Most moves fail on the dependency nobody listed: a model API, a search API, a storage client, a queue that only exists in the old cloud. Before building anything new, make each of those swappable.

- Find the narrowest point where the app touches the provider. Often every call goes through one factory or one client module. Put the new provider behind that point with the same interface, so call sites do not change.
- Select the provider with **one setting** (for example `STORAGE_BACKEND=s3`, `MODEL_PROVIDER=<new>`). Leave the old code path intact. The rollback is unsetting that setting.
- Map errors too: throttling and timeouts from the new provider must look like the ones the existing retry logic already handles.
- Prove it with the old provider's credentials **removed from the environment**, so a silent fallback cannot fake a pass.
- Run the full test suite on the base commit and on the branch. The pass and fail lists should be identical; note pre-existing failures instead of hiding them.
- Deploy this change to the **old** stack first. That turns one big move into two small ones: first the dependency (old cloud, new provider), later the compute.

## Phase 3: build the new stack in parallel

- Choose the target service from the inventory's limits, not from habit. If the longest real request is a multi-minute stream, a service with a short hard request cap is out, whatever else it offers.
- Build the image once and push it to the new registry. Port configuration name by name from the inventory.
- **Secrets move from secret store to secret store.** Never through command arguments, shell history, logs, chat or git. Give the workload a role instead of long-lived keys where the platform supports it.
- Set idle and request timeouts to cover the longest real request.
- Request TLS certificates early; validation can take a while and needs DNS records.
- Keep the infrastructure in a script or infrastructure-as-code file, so the stack can be deleted and rebuilt. That script is this phase's rollback.
- The new stack gets a private or provider hostname. No user traffic yet.

Done when the health endpoint is green **and** the app on the new stack reaches the real database and every outbound dependency.

## Phase 4a: verify with real workloads

Run the things users actually do, end to end, against the new stack directly (provider hostname, or a hosts-file override, or a header-routed test path):

- The main job of the product, start to finish, with real inputs. For a document generator: generate real documents. For a shop: a full test order.
- The **longest** path (streams, exports, uploads). Time it and compare with the limits.
- Every write path: check the row landed in the database and the file landed in storage.
- The frontend through its real proxy path, not only the backend alone.
- Auth, payments webhooks (test mode), email, scheduled jobs.

Compare outputs with the old stack where it makes sense. Fix what breaks, redeploy, rerun. Only real workload passes count; record each one in the plan with what ran, how long it took and where the output landed.

## Phase 4b: the cutover checklist

Copy `templates/CUTOVER-CHECKLIST.md`. In short:

Before:
- [ ] Full DNS zone exported to a file. Old values of every record you will change written down.
- [ ] TTL on those records lowered (for example 300 seconds) at least one old TTL before the switch.
- [ ] Certificates issued for every hostname on the new side.
- [ ] Real workload runs from phase 4a recorded and passing on the exact image that will serve.
- [ ] Rollback written as one line and tested where possible (for DNS: the old values, ready to paste).
- [ ] Watch commands for both sides prepared and working now, before the switch.
- [ ] Human said go for this exact switch.

Switch:
- [ ] Change only the records that move traffic. Do not touch mail, verification or third-party records.
- [ ] If there is more than one hostname, flip the API first, verify, then the site.
- [ ] Note the exact time.

After (the watch window):
- [ ] Requests on the new side are arriving and server errors are 0.
- [ ] Requests on the old side fall to 0.
- [ ] One real workload run again through the public hostname.
- [ ] Window length fixed in advance (for example 30 minutes, longer than DNS TTL plus the longest request).

**Rollback rule during the window:** any server error rate above the old baseline, or a failed real workload, means paste the old DNS values back first and investigate second.

Watch commands (examples):

```bash
# AWS: requests and 5xx on the new load balancer, per minute
aws cloudwatch get-metric-statistics --namespace AWS/ApplicationELB --metric-name RequestCount \
  --dimensions Name=LoadBalancer,Value=<lb-id> --start-time <iso> --end-time <iso> --period 60 --statistics Sum
aws cloudwatch get-metric-statistics --namespace AWS/ApplicationELB --metric-name HTTPCode_Target_5XX_Count \
  --dimensions Name=LoadBalancer,Value=<lb-id> --start-time <iso> --end-time <iso> --period 60 --statistics Sum

# Google Cloud: is the old service still getting requests?
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="<service>" AND httpRequest.status>=0' \
  --freshness=30m --format='value(timestamp)' | wc -l

# From outside: which side answers?
dig +short app.example.com && curl -s -o /dev/null -w '%{http_code} %{time_total}s\n' https://app.example.com/health
```

Report the window to the human as numbers: requests on the new side, server errors, requests on the old side.

## Phase 5a: copy data idempotently, second pass must report 0

Databases often stay where they are or move with their own tooling; this section is about files and objects, where silent gaps hide.

- **Switch the writer first.** Put storage behind the one-setting switch from phase 2 and deploy, so new files land in the new store. Then copy the backlog. Copying first and switching later leaves a gap.
- **The copy job must be idempotent:** list the source, skip every object already present in the destination with the same size (or checksum), copy the rest, exit non-zero on any failure. Running it twice must be safe.
- **Run it twice.** The first pass copies. The second pass must report **0 left to copy**. Anything else means writes are still landing on the old side or objects are failing: find out which before moving on.
- **Count both sides.** Source object count must equal destination object count for the copied prefixes: "N of N".
- **Read a real file through the app** on the new store, and request a path that does not exist to confirm it fails cleanly.
- Keep old URLs working: either keep the paths identical or rewrite stored URLs to path form.

Provider tools that already behave this way:

```bash
# AWS S3 destination; rerun until the dry run prints nothing
aws s3 sync s3://<old-bucket> s3://<new-bucket> --only-show-errors
aws s3 sync s3://<old-bucket> s3://<new-bucket> --dryrun | wc -l        # must print 0

# Google Cloud Storage destination
gcloud storage rsync -r gs://<old-bucket> gs://<new-bucket>
gcloud storage rsync -r --dry-run gs://<old-bucket> gs://<new-bucket>

# Any S3-compatible or mixed pair
rclone copy old:<bucket> new:<bucket> --checksum
rclone check old:<bucket> new:<bucket> --one-way                         # must report 0 differences
```

When the source has only an API (a hosted storage product), write the copy script yourself with the same contract, export a manifest from each side (`key<TAB>size` per line) and run:

```bash
python3 scripts/manifest_diff.py source.tsv dest.tsv    # prints "N of N copied, 0 left" and exits 0, or lists what is missing and exits 1
```

## Phase 5b: decommission last

Only after the watch window is clean, the old side has served zero requests, and the second pass reported 0:

1. Back up anything that exists only in the old cloud (buckets, exports, logs you need) and verify the backup opens.
2. Delete in dependency order: services first, then load balancers and forwarding rules, proxies, certificates, static IPs, then storage, then secrets.
3. List what is left with the provider's own inventory commands. The target is zero resources for this app.
4. Remove now-unused credentials and settings from the app and the secret store.
5. Leave untouched anything in the same account that belongs to another product. Name it in the report.
6. Deleting data and closing accounts is the human's call, every time.

```bash
# Google Cloud: what is still there?
gcloud run services list; gcloud compute forwarding-rules list; gcloud compute addresses list; gcloud storage ls
# AWS: what is still there?
aws ecs list-services --cluster <cluster>; aws elbv2 describe-load-balancers; aws s3 ls
```

## Report

Close with a short report the human can read in a minute:

```
Moved: <app> from <old> to <new> on <date>, app live throughout.
Phases: 5 of 5 done. Rollbacks used: <n>.
Before the switch: <n> real workloads end to end on the new stack, longest <duration>.
Watch window (<minutes> min): <n> requests on new, <n> server errors, <n> requests on old.
Data: <N> of <N> objects copied, second pass <0> left.
Old cloud: <n> resources left for this app. Left on purpose: <list or none>.
Open: <anything the human must do>.
```

## Do not

- Do not edit the live stack in place to "save a step". Parallel or not at all.
- Do not start a phase without its one-line rollback written down.
- Do not count a green health check as verification.
- Do not switch traffic, delete data, delete resources or close accounts without the human's go for that exact action.
- Do not put secret values in arguments, logs, plans, commits or chat.
- Do not touch DNS records you are not moving, and never change a zone you have not exported.
- Do not delete the old side during the watch window, even if everything looks fine.
- Do not report "copied" from the first pass. The second pass and the counts are the evidence.
