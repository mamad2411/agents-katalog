# Agent instructions (Lexicon harness wiring)

You are writing code that transforms **Avaya CMS** interval data into the
**NICE WFM Import History XML**. Before writing or changing any transformation
code, you MUST:

1. **Read `guides/inferential/QUEUE_glossary.md`** and code in its canonical
   vocabulary. It is the source of truth for meaning.
2. Consult `ontology/canonical_wfm.yaml` (what each field means) and
   `ontology/avaya_cms_dialect.yaml` (how Avaya terms map, and the traps).
3. **HandleTime = talk + hold.** For Avaya: `acdtime + holdtime` (acdtime EXCLUDES
   hold, so add it). For Genesys: `(tTalk + tHeld)/1000`. Never include ACW.
4. **Never let vendor column/metric names** (Avaya: `acdtime`, `acwtime`,
   `holdtime`, `anstime`, `abncalls`, `acceptable`, `slvlabns`, `split`, `logid`;
   Genesys: `tHandle`, `tTalk`, `tAcw`, `queueId`, …) appear in canonical output.
5. For inbound voice, **do not emit `SvcLvlPct`, `BackLog*`, or `RightParty/WrongParty`** fields.

After writing code you MUST make it pass the gate:

```bash
pytest -v                 # semantic + DTD contract tests must be green
python src/sensor.py <your_output.xml>   # must report no drift
```

Do not consider the task done until `pytest` passes and the sensor is clean.
If a contract test fails, fix the mapping — do not weaken the test.

When touching discovery code (`src/lexicon/discover/*`), the gate remains the
same — `pytest -v` must be green. The two E2E regression tests
`tests/lexicon/discover/test_e2e_avaya_cms.py` and
`tests/lexicon/discover/test_e2e_genesys_cloud.py` are load-bearing:
they encode the punchlines this project must deliver (Avaya HandleTime =
acdtime + holdtime; Genesys ms→s + ACW-excluded HandleTime). Do NOT weaken
these tests to make a change pass.
