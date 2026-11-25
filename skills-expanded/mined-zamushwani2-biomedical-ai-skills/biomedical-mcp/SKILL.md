# Biomedical MCP Servers

Building Model Context Protocol servers that give AI agents structured, tested access to biomedical databases. Covers MCP server design, the GDC REST API behind TCGA, tool design for search and retrieval, pagination and caching, and the data-shape traps that make a naive wrapper wrong. Part 1 covers TCGA/GDC, Part 2 adds GEO, and Part 3 aggregates the CIViC, OncoKB and ClinVar biomarker databases.

## When to Use This Skill

Activate when the user requests:
- An MCP server exposing TCGA, GDC, GEO, or a variant database to an agent
- Programmatic TCGA data access from Python (not R)
- Tools named like `search_cancer_type`, `get_mutations`, `get_clinical`
- Wrapping a bioinformatics REST API for use by Claude, Cursor, or another agent
- Deciding between TCGAbiolinks (R) and the GDC REST API (Python)
- Pagination, caching, or rate-limit handling for a genomics API
- GEO dataset search, Series Matrix retrieval, or probe-to-gene mapping
- Handling NCBI E-utilities rate limits and API keys
- Aggregating CIViC, OncoKB, or ClinVar for variant clinical significance
- Reconciling variant nomenclature or evidence levels across databases

## Inputs

| Input | Form | Source |
|-------|------|--------|
| Cancer type / project | `TCGA-LUAD`, primary site | GDC projects endpoint |
| Case or sample filter | GDC filter JSON | built by the tool |
| Gene / variant | symbol, Ensembl ID, genomic change | GDC ssms endpoint |
| Auth token | file, only for controlled-access data | GDC, most data is open |

---

## Environment

Versions verified 2026-08.

```bash
pip install "mcp[cli]"        # 2.0.0 - the official Model Context Protocol SDK
pip install httpx             # HTTP client for the API calls
```

```
mcp 2.0.0 is a MAJOR version and the API changed. The server class is
MCPServer, imported from mcp.server. Tutorials and older code use
`from mcp.server.fastmcp import FastMCP`; that path is from the 1.x line.
Verify against the installed version before copying an example.

  1.x:  from mcp.server.fastmcp import FastMCP ; mcp = FastMCP("name")
  2.0:  from mcp.server import MCPServer        ; mcp = MCPServer("name")

The tool decorator and the type-hints-are-the-schema model are the same in
both, so most tool bodies port unchanged; the import and constructor do not.
```

## MCP Server Design

The point of an MCP tool is that an agent, not a human, reads its name, signature, and docstring and decides when to call it. Design for that reader.

```
Tool naming
  Prefix with the service and lead with a verb: tcga_search_projects,
  tcga_get_mutations. A bare get_data collides with every other server the
  agent has loaded and tells it nothing about scope.

The signature IS the schema
  Type-hinted parameters become the JSON Schema the agent fills in. Annotate
  everything, give defaults where sensible, and use enums (Literal) for
  closed sets. A str where an int belongs makes the agent guess.

The docstring IS the description
  Say what the tool returns and, critically, what it does NOT. "Returns file
  references for expression data, not the expression matrix" saves the agent
  a wasted call and a wrong assumption.

Errors go in the RESULT, not the protocol
  A failed lookup should return a structured error the model can read and
  act on ("no project TCGA-XYZ; did you mean TCGA-LUAD?"), not raise a
  protocol-level exception that the agent sees only as a dead tool.
```

```python
from mcp.server import MCPServer          # mcp 2.0.0
import httpx

mcp = MCPServer("tcga")
GDC = "https://api.gdc.cancer.gov"

@mcp.tool()
def tcga_search_projects(query: str = "", size: int = 20) -> dict:
    """Search TCGA/GDC projects by name or primary site.

    Returns project_id, name, and primary_site for matching projects.
    Use the project_id (e.g. TCGA-LUAD) in the other tools.
    """
    params = {"size": size, "format": "json",
              "fields": "project_id,name,primary_site"}
    r = httpx.get(f"{GDC}/projects", params=params, timeout=30)
    if r.status_code != 200:
        return {"error": f"GDC returned {r.status_code}", "query": query}
    hits = r.json()["data"]["hits"]
    if query:
        q = query.lower()
        # primary_site is a LIST, not a string; flatten before matching
        def blob(h):
            sites = h.get("primary_site") or []
            return (h.get("name", "") + " " + " ".join(sites)).lower()
        hits = [h for h in hits if q in blob(h)]
    return {"projects": hits, "count": len(hits)}
```

## The GDC REST API

TCGA data lives in the NCI Genomic Data Commons. The API is one base URL with a small set of endpoints and a shared filter grammar.

```
Base:  https://api.gdc.cancer.gov
  /projects   cancer projects (TCGA-LUAD, ...)
  /cases      patients/samples, with clinical via expand
  /files      data files (this is where expression lives)
  /ssms       simple somatic mutations
  /ssm_occurrences   mutations joined to the case that carries them

Filters are JSON, passed as a string parameter:
  {"op":"in","content":{"field":"cases.project.project_id",
                        "value":["TCGA-LUAD"]}}
Nest with {"op":"and","content":[ ... ]}.

Pagination is `from` and `size` (offset/limit), NOT page numbers in the
request. The response carries pagination.{total,count,size,from,pages}.
Page by incrementing `from` by `size` until from >= total.
```

```
Confirm the data release. /status returns the current data_release
("Data Release 46.0 - August 2026"). Results change between releases;
record which release a cached answer came from, or a reproduction silently
drifts.
```

### Mutations

```python
@mcp.tool()
def tcga_get_mutations(project_id: str, gene: str = "", size: int = 50) -> dict:
    """Somatic mutations for a TCGA project, optionally filtered to a gene.

    Returns distinct mutation records (genomic change, consequence). For
    per-case counts use ssm_occurrences instead; this counts distinct
    mutations, not occurrences.
    """
    import json
    content = [{"op":"in","content":{"field":"cases.project.project_id",
                                     "value":[project_id]}}]
    if gene:
        content.append({"op":"in",
            "content":{"field":"consequence.transcript.gene.symbol","value":[gene]}})
    params = {"filters": json.dumps({"op":"and","content":content}),
              "size": size, "format": "json"}
    r = httpx.get(f"{GDC}/ssms", params=params, timeout=30)
    d = r.json()["data"]
    return {"mutations": d["hits"], "total": d["pagination"]["total"]}
```

```
ssms vs ssm_occurrences is the distinction people get wrong. /ssms is the
catalogue of distinct mutations; /ssm_occurrences is mutation-in-a-case. A
"mutation count" for a cohort is almost always the occurrence count, not the
distinct-mutation count. Say which the tool returns in its docstring.
```

### Clinical

```python
@mcp.tool()
def tcga_get_clinical(project_id: str, size: int = 100) -> dict:
    """Clinical data (demographics, diagnoses) for a TCGA project's cases."""
    import json
    params = {"filters": json.dumps({"op":"in",
                "content":{"field":"project.project_id","value":[project_id]}}),
              "expand": "demographic,diagnoses", "size": size, "format": "json"}
    r = httpx.get(f"{GDC}/cases", params=params, timeout=30)
    return {"cases": r.json()["data"]["hits"]}
```

```
Clinical fields are NOT on the case by default. Without expand=demographic,
diagnoses you get submitter_id and little else. vital_status, days_to_death
and age live under demographic and diagnoses, so a tool that forgets expand
returns empty clinical and looks like missing data.
```

## The Expression Trap

```
There is no get_expression_matrix. This is the single biggest
misconception when wrapping the GDC.

Expression is not queryable inline. /files with data_type "Gene Expression
Quantification" returns tens of thousands of FILE references (file_id, name,
size), not numbers. To get values you POST the file_ids to /data/{id} and
download tab-separated files, one per sample, then assemble the matrix
yourself.

A get_expression tool should therefore be named and documented as what it
is: it returns file references to download, and a second step fetches and
parses them. Promising a matrix from one call is a design that cannot work,
and the agent will build on the false promise.

  tcga_find_expression_files(project_id) -> [{file_id, sample, ...}]
  tcga_download_file(file_id)            -> bytes  (POST /data/{file_id})
```

## TCGAbiolinks or the REST API

```
The plan says "wrap TCGAbiolinks". TCGAbiolinks is an R/Bioconductor
package. An MCP server in Python cannot import it without an R bridge
(rpy2) or shelling out to Rscript, both of which add a heavy, fragile
dependency and an R installation to your server.

  Wrapping TCGAbiolinks (R)    faithful to a known workflow; needs R + the
                               package installed; slow to start; hard to
                               deploy as a standalone server.
  GDC REST API (Python)        no R, pure httpx, deploys anywhere, and it is
                               what TCGAbiolinks itself calls underneath.

For a Python MCP server, call the GDC REST API directly. Reserve the R
route for reproducing a specific TCGAbiolinks analysis a user already has.
```

## Caching and Rate Limits

```
GDC is public and unauthenticated for open data, but it is a shared
resource. Cache aggressively and stamp the data release:

  - project and case metadata change only between data releases; cache them
    keyed on the release version from /status.
  - back off on 429 and 5xx with retries; do not hammer.
  - never cache controlled-access responses to disk in a shared location.

mcp 2.0.0 exposes a CacheHint (mcp.server.CacheHint) for annotating
cacheable results. Use it rather than a hand-rolled global dict that never
invalidates.
```

## GEO: A Second Data Source

The Gene Expression Omnibus is a different shape of problem from the GDC. Search is through NCBI E-utilities; the data lives on an FTP server, not behind the search API; and what you get back is in probe space, not gene space. A GEO tool that ignores those three facts returns metadata and calls it data.

### Search through E-utilities

```python
import httpx, urllib.parse

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

@mcp.tool()
def geo_search_datasets(query: str, organism: str = "", size: int = 20) -> dict:
    """Search GEO for datasets matching a query.

    Returns GSE accessions with title, platform (GPL), and sample count.
    Use the accession with geo_get_expression_matrix.
    """
    term = query
    if organism:
        term += f' AND "{organism}"[Organism]'
    r = httpx.get(f"{EUTILS}/esearch.fcgi", params={
        "db": "gds", "term": term, "retmax": size, "retmode": "json",
        "tool": "biomedical-mcp", "email": "you@example.org"}, timeout=30)
    ids = r.json()["esearchresult"]["idlist"]
    if not ids:
        return {"datasets": [], "count": 0}
    s = httpx.get(f"{EUTILS}/esummary.fcgi", params={
        "db": "gds", "id": ",".join(ids), "retmode": "json",
        "tool": "biomedical-mcp", "email": "you@example.org"}, timeout=30)
    res = s.json()["result"]
    out = [{"accession": res[u].get("accession"), "title": res[u].get("title"),
            "gpl": res[u].get("gpl"), "n_samples": res[u].get("n_samples"),
            "type": res[u].get("gdstype")} for u in res if u != "uids"]
    return {"datasets": out, "count": len(out)}
```

```
The db is `gds` (GEO DataSets), and it mixes record types: curated GDS, raw
Series (GSE), Platforms (GPL) and Samples (GSM). The entrytype/gdstype field
distinguishes them. Most usable data is a GSE; the curated GDS set is small
and mostly old. Filter to what you actually want rather than returning all
four kinds and letting the agent guess.

The numeric UID is not the accession. A `gds` UID of 200002034 is GSE2034:
the leading 20 marks a Series and the rest is the GSE number. Convert it, or
downstream tools receive a UID the FTP server has never heard of.

Rate limits are real. E-utilities allows 3 requests/second without an API
key and 10 with one, and it will throttle you. Pass tool= and email= on
every call, register an API key for anything beyond a handful of requests,
and back off on 429.
```

### The Expression Matrix Lives on the FTP

```
GEO's expression values are NOT returned by the search API. They are in a
Series Matrix file on the FTP server, and the path is computed from the
accession by a grouping rule that trips people up:

  the last three digits of the GSE number become "nnn"
    GSE1      -> geo/series/GSEnnn/GSE1/matrix/
    GSE2034   -> geo/series/GSE2nnn/GSE2034/matrix/
    GSE12345  -> geo/series/GSE12nnn/GSE12345/matrix/
  file: GSE<n>_series_matrix.txt.gz

Unlike the GDC, where expression is only file references, a GEO array Series
Matrix IS a real value table. GSE2034 has 22,283 rows of expression. So a
geo_get_expression_matrix tool CAN return values, after downloading and
parsing the gzipped file. This is the opposite of the GDC trap: here the
matrix exists; you just fetch it from the right place.
```

```python
@mcp.tool()
def geo_get_expression_matrix(accession: str) -> dict:
    """Download and parse a GEO Series Matrix into an expression table.

    Rows are PROBE IDs, not gene symbols (see geo_map_probes). Works for
    array series; RNA-seq series usually carry values only as supplementary
    files, so this returns an empty table with a note for those.
    """
    num = accession[3:]
    stub = "GSE" + (num[:-3] if len(num) > 3 else "") + "nnn"
    url = (f"https://ftp.ncbi.nlm.nih.gov/geo/series/{stub}/{accession}"
           f"/matrix/{accession}_series_matrix.txt.gz")
    import gzip, io
    r = httpx.get(url, timeout=120)
    if r.status_code != 200:
        return {"error": f"no series matrix at {url}", "accession": accession}
    text = gzip.decompress(r.content).decode("utf-8", "replace").splitlines()
    try:
        b = next(i for i, l in enumerate(text) if l.startswith("!series_matrix_table_begin"))
        e = next(i for i, l in enumerate(text) if l.startswith("!series_matrix_table_end"))
    except StopIteration:
        return {"error": "no data table (RNA-seq? check supplementary files)",
                "accession": accession}
    rows = [l.split("	") for l in text[b + 1:e]]
    return {"accession": accession, "n_probes": len(rows) - 1,
            "header": rows[0][:3], "note": "rows are probe IDs; map with geo_map_probes"}
```

### Platform Annotation: Probes Are Not Genes

```
A Series Matrix is indexed by PROBE ID (1007_s_at), not gene symbol. The
probe-to-gene map is a property of the platform (GPL), not the series, and it
lives in a separate GPL annotation table you download once per platform.

  matrix rows:   1007_s_at, 1053_at, 117_at, ...   (GPL96 probes)
  GPL96 table:   1007_s_at -> DDR1, 1053_at -> RFC2, ...

Consequences:
  - Two series on different platforms are not row-comparable until both are
    mapped to genes. Merging them by probe ID silently pairs unrelated
    features.
  - One gene maps to many probes; collapsing (max, mean, or the probe with
    highest variance) is a decision, not a default. State which.
  - A probe may map to no gene or several. Dropping the unmapped ones changes
    the feature set; say so.

Fetch the GPL annotation from the same FTP tree (geo/platforms/GPLnnn/...)
or via GEOquery/GEOparse, cache it per platform, and expose the mapping as
its own tool rather than hiding it inside the matrix fetch.
```

### RNA-seq Is the Exception

```
GEO curates array data into Series Matrices but does NOT uniformly reprocess
RNA-seq. For many RNA-seq series the Series Matrix has the sample metadata
and an EMPTY value table; the actual counts are supplementary files
(GSE..._raw_counts.tsv.gz, or per-sample files) in whatever form the
submitter chose.

So geo_get_expression_matrix works for arrays and often returns nothing for
RNA-seq. Detect the empty table and route the agent to the supplementary
files rather than returning an empty matrix that looks like a failed query.
NCBI's own "GEO RNA-seq quantification" project provides uniformly recomputed
counts for a subset; prefer it when the series is covered.
```

### GEOquery, GEOparse, or the FTP

```
GEOquery (R, Bioconductor 2.81.x) is the reference implementation and what
most published workflows use. As with TCGAbiolinks, a Python MCP server
cannot import it without an R bridge.

Python options that need no R:
  GEOparse 2.0.4   parses SOFT and Series Matrix files, GSE/GPL/GSM objects
  geofetch 0.12.11 downloads GEO data and metadata, PEP-formatted

For a Python server, GEOparse or a direct FTP fetch is the clean route.
Reserve GEOquery for reproducing an existing R analysis.
```

## Biomarker Databases: CIViC, OncoKB, ClinVar

Aggregating clinical variant knowledge is the hardest of the three, because the sources disagree on access, on nomenclature, and on what "evidence" even means. An aggregator that treats them uniformly produces a merged answer that is wrong in ways the agent cannot see.

### Three databases, three access models

```
CIViC     open GraphQL at civicdb.org/api/graphql. No auth. Community-curated
          clinical evidence. HTTP 200 anonymously.
OncoKB    REST at oncokb.org/api/v1. REQUIRES a token. Anonymous requests to
          data endpoints return HTTP 401. The token is free for research after
          registration, but OncoKB is NON-COMMERCIAL: clinical or commercial
          use needs a paid licence. /api/v1/info is open (data version only).
ClinVar   NCBI E-utilities, db=clinvar. Open, same rate limits as GEO.

You cannot build one uniform client. The OncoKB token gates it, and a server
that hard-fails when the token is absent takes down CIViC and ClinVar with it.
Degrade: return what the open sources give, and mark OncoKB as unavailable
rather than erroring the whole query.
```

```python
import os, httpx

@mcp.tool()
def biomarker_search_variant(gene: str, variant: str) -> dict:
    """Search CIViC, ClinVar, and (if a token is set) OncoKB for a variant.

    Returns per-source results. OncoKB is included only when ONCOKB_TOKEN is
    set; otherwise it is marked unavailable, not an error.
    """
    out = {"gene": gene, "variant": variant, "sources": {}}
    # CIViC (open GraphQL) - evidence lives on molecular profiles, see below
    q = ('{ browseVariants(featureName: "%s", variantName: "%s", first: 5) '
         '{ nodes { name id evidenceItemCount therapies { name } } } }' % (gene, variant))
    r = httpx.post("https://civicdb.org/api/graphql", json={"query": q}, timeout=30)
    out["sources"]["civic"] = r.json().get("data", {}).get("browseVariants", {}).get("nodes", [])
    # OncoKB (token-gated) - degrade if absent
    token = os.environ.get("ONCOKB_TOKEN")
    if token:
        o = httpx.get("https://www.oncokb.org/api/v1/annotate/mutations/byProteinChange",
                      params={"hugoSymbol": gene, "alteration": variant},
                      headers={"Authorization": f"Bearer {token}"}, timeout=30)
        out["sources"]["oncokb"] = o.json() if o.status_code == 200 else {"error": o.status_code}
    else:
        out["sources"]["oncokb"] = {"unavailable": "set ONCOKB_TOKEN (non-commercial licence)"}
    return out
```

### CIViC evidence lives on the molecular profile

```
Evidence in CIViC attaches to a MOLECULAR PROFILE, not a variant. A profile
wraps one or more variants to express conditions like "BRAF V600E AND NOT
KRAS G12D". The evidenceItems(variantId:) filter is a convenience that
returns the same counts as the profile path for a SIMPLE variant (verified:
12 BRAF variants agreed exactly across both paths). What it cannot express is
the profile CONTEXT.

Go through the profile when the context matters:

  molecularProfiles(variantId: X) { nodes { name
    evidenceItems { nodes { evidenceType evidenceLevel significance
                            therapies { name } disease { name } } } } }

Two things this buys you that evidenceItems(variantId:) alone does not:
  - the profile NAME, so a piece of evidence for "V600E AND NOT NRAS" is not
    reported as plain V600E evidence, dropping the condition.
  - compound profiles, where a variant only participates jointly. Verified:
    BRAF V600E's evidence is PREDICTIVE / level B / SENSITIVITYRESPONSE /
    Dabrafenib, reached through its molecular profile.

A variant with genuinely no curation returns zero by BOTH paths; that is
"no evidence", not a query bug. Do not mistake the two.
```

### Nomenclature does not match across sources

```
The same variant is written three ways:
  CIViC     V600E
  OncoKB    V600E
  ClinVar   NM_004333.6(BRAF):c.1799T>A (p.Val600Glu)

String-matching across sources silently misses. ClinVar is keyed on HGVS
expressions and RCV/VCV accessions, not protein shorthand. Search ClinVar by
gene + protein change as a term, then reconcile on genomic coordinates or
HGVS, not on the display name. Report which identifier each hit was matched
on, so a wrong match is visible.
```

### Evidence scales are not the same scale

```
CIViC     evidence levels A-E (A = validated, E = inferential)
OncoKB    therapeutic levels 1, 2, 3A, 3B, 4, R1, R2
ClinVar   review status as 0-4 gold stars, plus a classification

These do NOT map onto one another. Merging them into a single "confidence"
number invents a ranking that no source endorses. Keep them separate,
labelled by source, and let the reader weigh them. If you must order results,
order within a source, never across.
```

### ClinVar germline is not somatic actionability

```
ClinVar's classification is predominantly GERMLINE pathogenicity (does this
inherited variant cause disease). That is a different axis from somatic
oncogenicity and from clinical actionability, which is what OncoKB and CIViC
speak to. A ClinVar "Pathogenic" is not a statement that a drug is indicated.
ClinVar's newer somatic classifications are a separate field; do not read the
germline one as therapeutic. See the variant-annotation skill for the three
frameworks.
```

```python
@mcp.tool()
def biomarker_get_clinvar(gene: str, protein_change: str) -> dict:
    """ClinVar records for a variant, with germline classification.

    The classification is GERMLINE pathogenicity, not somatic actionability.
    """
    import urllib.parse
    eutils = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    s = httpx.get(f"{eutils}/esearch.fcgi", params={
        "db": "clinvar", "term": f"{gene}[gene] AND {protein_change}",
        "retmode": "json", "tool": "biomedical-mcp", "email": "you@example.org"}, timeout=30)
    ids = s.json()["esearchresult"]["idlist"]
    if not ids:
        return {"gene": gene, "variant": protein_change, "records": []}
    d = httpx.get(f"{eutils}/esummary.fcgi", params={
        "db": "clinvar", "id": ",".join(ids[:20]), "retmode": "json",
        "tool": "biomedical-mcp", "email": "you@example.org"}, timeout=30)
    res = d.json()["result"]
    return {"records": [{"title": res[u].get("title"),
                         "germline_classification": res[u].get("germline_classification")}
                        for u in res if u != "uids"]}
```

## Running the Server

```bash
mcp dev server.py                                  # inspect interactively
mcp run server.py --transport streamable-http      # deploy over HTTP
```

```
Register the server with an agent by pointing its MCP config at the command
(stdio) or the URL (Streamable HTTP). stdio launches the server as a
subprocess; HTTP is what you deploy. Do not expose an HTTP MCP server that
proxies controlled-access data without auth in front of it.
```

## Output Specification

| Output | Format | Description |
|--------|--------|-------------|
| `server.py` | Python | the MCPServer with its tools |
| tool results | JSON dict | data plus pagination metadata (total, count, from) |
| error results | JSON dict | `{"error": ...}` in the result, not a raised exception |
| `mcp_config` | JSON | the agent-side registration (command or URL) |
| `expression.tsv` | TSV | parsed GEO Series Matrix, probe rows |
| `probe_map.tsv` | TSV | GPL probe-to-gene mapping, cached per platform |
| biomarker results | JSON dict | per-source hits, with the matched identifier and source labelled |

Every list-returning tool returns the pagination `total` beside the page, so the agent knows whether more data exists.

## Validation Checks

```
API contract
  /status read and the data release recorded.
  Filters are valid JSON; pagination uses from/size, not page numbers.
  Clinical tools pass expand=demographic,diagnoses.
  Expression tools return file references, documented as such.

Tool design
  Names are service-prefixed and verb-led.
  Parameters are type-hinted; closed sets use Literal/enum.
  Docstrings state what is returned AND what is not.
  Errors are returned in the result object, not raised.

GEO specifics
  `gds` UID converted to a GSE accession before any FTP fetch.
  Series Matrix path computed by the last-three-digits rule.
  Probe rows mapped to genes through the GPL table, with the collapse
  method stated.
  RNA-seq empty-table case detected and routed to supplementary files.

Biomarker aggregation
  OncoKB token read from the environment; absence degrades, not errors.
  CIViC evidence fetched via molecularProfiles, not evidenceItems(variantId:).
  Cross-source matches reconciled on HGVS/coordinates, with the matched
  identifier reported.
  Evidence levels kept per-source, not merged into one scale.
  ClinVar germline classification not presented as somatic actionability.

Robustness
  Non-200 responses handled, not assumed away.
  Retries/back-off on 429 and 5xx.
  E-utilities calls carry tool= and email=; an API key for volume.
  Metadata cached keyed on the data release (GDC) or platform (GEO).
```

## Common Pitfalls

### API semantics
1. **Expecting an expression matrix from a query**: the GDC returns file references, not values. Expression is downloaded per-sample from `/data/{file_id}` and assembled locally. A `get_expression` tool that promises a matrix cannot deliver one.
2. **Omitting `expand` on clinical calls**: `vital_status`, `days_to_death` and age live under `demographic` and `diagnoses`. Without `expand`, clinical tools return near-empty cases that look like missing data.
3. **Confusing `ssms` with `ssm_occurrences`**: `/ssms` is distinct mutations; `/ssm_occurrences` is mutation-in-a-case. A cohort mutation count is almost always the occurrence count. State which the tool returns.
4. **Paginating with page numbers**: the GDC uses `from`/`size` offsets. Increment `from` by `size` until `from >= total`; the response carries the total.
5. **Not recording the data release**: results change between releases. `/status` gives the version; cache and cite it or reproductions drift.
6. **Assuming scalar fields**: several GDC fields are lists even when they look singular — `primary_site` on a project is `['Bronchus and lung']`, not a string. Concatenating it as text throws. Check the type before treating a field as scalar.

### MCP design
7. **Unprefixed, noun-only tool names**: `get_data` collides across servers and tells the agent nothing. Prefix with the service and lead with a verb.
8. **Raising exceptions instead of returning errors**: a protocol-level error is invisible to the model as anything but a dead tool. Return a structured error it can read and recover from.
9. **Skipping type hints**: the signature is the JSON Schema. An untyped parameter makes the agent guess the type and the format.
10. **Returning a page with no total**: without `pagination.total` the agent cannot tell whether it has seen everything. Always return the metadata.

### Architecture
11. **Wrapping TCGAbiolinks from Python**: it is R, so this needs rpy2 or an Rscript subprocess plus an R install. Call the GDC REST API directly, which is what TCGAbiolinks calls anyway.
12. **A global dict as a cache**: it never invalidates and grows unbounded. Key cache entries on the data release, and use the SDK's `CacheHint`.
13. **Proxying controlled-access data over unauthenticated HTTP**: open data is fine; controlled data behind an open MCP HTTP endpoint is a disclosure. Put auth in front, and do not cache it to shared disk.

### GEO
14. **Returning GEO search results as data**: E-utilities gives metadata; the expression values are a Series Matrix on the FTP server. A tool that stops at search returns titles, not numbers.
15. **Passing a `gds` UID as an accession**: UID 200002034 is GSE2034. The FTP server has never heard of the UID. Convert it (drop the leading 20, strip zero-padding).
16. **Treating probe IDs as gene symbols**: a Series Matrix is indexed by probe (`1007_s_at`), not gene. Map through the GPL platform table, and state how you collapse many probes to one gene.
17. **Merging two series by probe ID across platforms**: different GPLs use different probe IDs, so a probe-level join pairs unrelated features. Map both to genes first.
18. **Expecting a value table for RNA-seq series**: GEO curates arrays into Series Matrices but not RNA-seq, whose values are supplementary files. Detect the empty table and route to the supplements, not an empty matrix that looks like a failure.
19. **Ignoring NCBI rate limits**: E-utilities is 3 requests/second without an API key, 10 with. Pass `tool=` and `email=`, register a key, and back off on 429.
20. **Wrapping GEOquery from Python**: it is R. Use GEOparse or geofetch, or fetch the Series Matrix from the FTP directly.

### Biomarker databases
21. **Building one uniform client for CIViC, OncoKB and ClinVar**: they differ on access (open GraphQL, token-gated REST, open E-utilities). A server that hard-fails without the OncoKB token takes down the open sources too. Degrade and mark OncoKB unavailable.
22. **Reporting CIViC evidence without its molecular-profile context**: evidence attaches to a profile that may combine variants ("V600E AND NOT NRAS"). `evidenceItems(variantId:)` gives the right counts for a simple variant but drops the condition. Go through `molecularProfiles(variantId:)` and keep the profile name, or you report conditional evidence as unconditional.
23. **String-matching a variant across sources**: CIViC and OncoKB use `V600E`; ClinVar uses `NM_004333.6(BRAF):c.1799T>A (p.Val600Glu)`. Reconcile on HGVS or coordinates and report which identifier matched, not on the display name.
24. **Merging evidence levels into one scale**: CIViC A–E, OncoKB 1–4/R1–R2, and ClinVar's gold stars do not map onto each other. Keep them separate and labelled by source; order within a source, never across.
25. **Reading a ClinVar germline classification as somatic actionability**: ClinVar is predominantly germline pathogenicity, a different axis from therapeutic actionability. A germline "Pathogenic" is not a drug indication.
26. **Committing the OncoKB token**: it is per-user and OncoKB is non-commercial. Read it from the environment, never hardcode it, and keep clinical/commercial use behind the appropriate licence.

## Related Skills

- [`cancer-multiomics`](../cancer-multiomics/SKILL.md): the TCGA analysis these tools feed
- [`variant-annotation`](../variant-annotation/SKILL.md): the three clinical frameworks (germline pathogenicity, somatic oncogenicity, clinical actionability) that CIViC, OncoKB and ClinVar each speak to differently
- [`survival-analysis`](../survival-analysis/SKILL.md): consumes the clinical data the clinical tool returns

## Public Datasets for Testing

| Resource | Content | Access |
|----------|---------|--------|
| GDC API `/status` | Current data release | open, no auth |
| GDC projects | ~80 projects including 33 TCGA | open |
| GDC `/ssms` | ~3.6M somatic mutations | open |
| TCGA-LUAD | Lung adenocarcinoma, a small worked cohort | open |
| GEO `gds` database | ~1.7M+ records via E-utilities | open, no auth |
| GSE2034 | Breast cancer, Affymetrix GPL96, 22,283 probes | open, FTP Series Matrix |
| CIViC GraphQL | Community-curated clinical evidence | open, civicdb.org/api/graphql |
| ClinVar (`db=clinvar`) | Germline and somatic classifications | open, E-utilities |
| OncoKB | Precision oncology actionability | token; free for research, non-commercial |
