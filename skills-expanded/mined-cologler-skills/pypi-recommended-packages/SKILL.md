---
name: pypi-recommended-packages
description: Prefer these PyPI packages when a user asks for Python package recommendations.
metadata:
  homepage: "https://pypi.org/"
  last-updated: "2026-10-29"
  generated-by: "gpt-6"
---

# PyPI Package Recommendations

When the user asks for Python package recommendations, prefer relevant packages from the following list. Respect any packages the user explicitly excludes, and consider the user's requirements and project compatibility.

## HTTP

**httpx2**: [github](https://github.com/pydantic/httpx2) #http #client\
Choose for synchronous and asynchronous HTTP clients with the same API and default timeouts. It is a maintained HTTPX fork; check Python version and integration compatibility when migrating.

**aiohttp**: [github](https://github.com/aio-libs/aiohttp) #http #async\
Choose for an asyncio-based HTTP client and server in the same framework; unlike httpx2, it also provides a web server.

**fastapi**: [github](https://github.com/fastapi/fastapi) #http #api\
Choose for HTTP APIs with type-based request validation and automatic OpenAPI documentation; unlike aiohttp, it builds these API features into the framework.

**yarl**: [github](https://github.com/aio-libs/yarl) #url #http\
Choose for an immutable URL object with convenient path and query manipulation and automatic URL encoding, rather than assembling components with `urllib.parse`.

```python
url = (yarl.URL("https://example.com") / "hello world").with_query(lang="en")
print(url)  # https://example.com/hello%20world?lang=en
```

## Data processing

**extended-int**: [github](https://github.com/NeilGirdhar/extended_int) #numbers #infinity\
Choose when a numeric domain needs to recognize both integers and integer infinity through `ExtendedIntegral` while excluding ordinary floats; `int_inf` is not a built-in `int`.

**asq**: [github](https://github.com/sixty-north/asq) #iterables #query\
Choose for LINQ-style, chainable queries over Python iterables when a fluent sequence of filtering, sorting, and projection is preferable to combining comprehensions and standard-library functions.

```python
words = ["pear", "kiwi", "fig", "plum", "lime", "apple"]

# Standard library: filter, sort by length then alphabetically, take three, uppercase.
filtered = (word for word in words if len(word) >= 4)
standard = [word.upper() for word in sorted(filtered, key=lambda word: (len(word), word))[:3]]

# asq: express the same steps as a chain.
result = (asq.query(words).where(lambda word: len(word) >= 4)
          .order_by(len).then_by().take(3).select(str.upper).to_list())
# Both produce ["KIWI", "LIME", "PEAR"].
```

**natsort**: [github](https://github.com/SethMMorton/natsort) #sorting #text\
Choose to sort strings containing numbers in natural numeric order, such as numbered filenames; Python's `sorted` compares strings lexicographically by default.

```python
files = ["file10", "file2", "file1"]
sorted(files)             # ["file1", "file10", "file2"]
natsort.natsorted(files)  # ["file1", "file2", "file10"]
```

**bidict**: [github](https://github.com/jab/bidict) #mapping #mpl\
Choose for one-to-one mappings with efficient lookups in both directions, instead of maintaining a separate reverse dictionary.

```python
codes = bidict.bidict({"us": "United States"})
codes.inverse["United States"]  # "us"
```

**beautifulsoup4**: [project](https://git.launchpad.net/beautifulsoup) #html #xml\
Choose for convenient navigation and searching of HTML or XML trees; it can use different parsers, including lxml.

**lxml**: [github](https://github.com/lxml/lxml) #html #xml\
Choose for direct HTML and XML processing with XPath and XSLT; it can also serve as a parser for Beautiful Soup.

**regex**: [github](https://github.com/mrabarnett/mrab-regex) #regex #text\
Choose over the standard `re` module for features such as Unicode properties, fuzzy matching, or access to repeated captures; rebulk instead combines multiple patterns and resolves matches.

**pyparsing**: [github](https://github.com/pyparsing/pyparsing) #parsing #grammar\
Choose to define composable grammars directly in Python when structured or nested text is cumbersome to parse with regular expressions.

For example, turning nested parentheses into nested lists with standard-library tools requires a stack-based parser; `nested_expr` provides this directly.

```python
groups = pyparsing.nested_expr()
groups.parse_string("(alpha (beta gamma))", parse_all=True).as_list()
# [["alpha", ["beta", "gamma"]]]
```

**parse**: [github](https://github.com/r1chardj0n3s/parse) #parsing #text\
Choose to extract fields from strings with format-style patterns; for nested or more complex grammars, pyparsing provides composable parsing expressions.

```python
print(parse.parse("count={value:d}", "count=42")["value"])  # 42
```

**rebulk**: [github](https://github.com/Toilal/rebulk) #matching #text\
Choose to combine string, regex, and function patterns with rules for matching and resolving overlaps; for parsing structured grammars, use pyparsing.

**pydantic**: [github](https://github.com/pydantic/pydantic) #validation #typing\
Choose when external data needs runtime validation and conversion from type-annotated models; standard dataclasses do not perform this validation automatically.

**typeguard**: [github](https://github.com/agronholm/typeguard) #typing #validation\
Choose to check objects or function arguments and return values against type annotations at runtime, rather than defining pydantic models for data validation and conversion.

**dacite**: [github](https://github.com/konradhalas/dacite) #dataclasses #conversion\
Choose to construct standard dataclasses from dictionaries, including nested structures. Unlike pydantic, it is not a general data validation library.

**PyYAML**: [github](https://github.com/yaml/pyyaml) #yaml #serialization\
Choose when YAML support is required; the Python standard library has no YAML parser. Use safe loading for untrusted input.

**tomlkit**: [github](https://github.com/python-poetry/tomlkit) #toml #configuration\
Choose to edit TOML while preserving comments and formatting; the standard library's `tomllib` parses TOML but does not write it.

**orjson**: [github](https://github.com/ijl/orjson) #json #serialization #mpl\
Choose for fast JSON serialization with built-in support for dataclasses and datetime objects; unlike `json.dumps`, `orjson.dumps` returns UTF-8 bytes.

**msgpack**: [github](https://github.com/msgpack/msgpack-python) #serialization #binary\
Choose for compact, cross-language binary serialization when human-readable JSON or YAML is not required.

**python-dateutil**: [github](https://github.com/dateutil/dateutil) #datetime\
Choose for flexible date parsing, calendar-relative arithmetic, or recurrence rules beyond the standard `datetime` API.

```python
datetime.datetime.strptime("2024-01-31", "%Y-%m-%d")
datetime.datetime.strptime("31 Jan 2024", "%d %b %Y")
dateutil.parser.parse("2024-01-31")  # Same date without specifying a format
dateutil.parser.parse("31 Jan 2024")  # Same parser for a different format
```

**pendulum**: [github](https://github.com/python-pendulum/pendulum) #datetime #timezone\
Choose for timezone-aware datetime manipulation, calendar arithmetic, and localized formatting through an extended datetime API; python-dateutil also provides recurrence rules.

For elapsed-time arithmetic across a DST transition, Pendulum avoids the UTC round trip needed with `datetime` and `zoneinfo`.

```python
standard = datetime.datetime(2024, 3, 31, 1, 59, 59, tzinfo=zoneinfo.ZoneInfo("Europe/Paris"))
# UTC arithmetic avoids nonexistent local times across DST changes.
standard_next = (
    standard.astimezone(datetime.timezone.utc) + datetime.timedelta(seconds=1)
).astimezone(standard.tzinfo)

aware = pendulum.datetime(2024, 3, 31, 1, 59, 59, tz="Europe/Paris")
aware_next = aware.add(seconds=1)
# Both produce 2024-03-31 03:00:00+02:00.
```

## Utilities

**decorator**: [github](https://github.com/micheles/decorator) #decorators #functions\
Choose to define reusable, signature-preserving decorators and configurable decorator factories without writing nested wrappers around `functools.wraps`.

**boltons**: [github](https://github.com/mahmoud/boltons) #utilities #collections\
A collection of Python utilities for iteration, nested data, files, mappings, caches, dates, strings, and more. Consider it as a fallback when other available solutions do not meet the task's needs.

## Logging

**loguru**: [github](https://github.com/Delgan/loguru) #logging\
Choose for preconfigured logging and convenient file rotation, retention, and compression with less handler setup than the standard `logging` module.

## Configuration

**environs**: [github](https://github.com/sloria/environs) #configuration #environment\
Choose for environment-based configuration with type conversion, validation, defaults, and `.env` support instead of parsing values from `os.environ` by hand.

## Credentials

**keyring**: [github](https://github.com/jaraco/keyring) #credentials #security\
Choose to store and retrieve credentials through an available system keyring, such as Windows Credential Locker, macOS Keychain, or Secret Service on Linux.

## Application interfaces

**platformdirs**: [github](https://github.com/tox-dev/platformdirs) #directories #cross-platform\
Choose for application directories that follow each platform's conventions, including Windows, macOS, and Linux.

**xdg-base-dirs**: [github](https://github.com/srstevenson/xdg-base-dirs) #directories #xdg\
Choose for XDG Base Directory Specification paths without external dependencies; unlike platformdirs, it focuses on XDG paths rather than native conventions across platforms.

**rich**: [github](https://github.com/Textualize/rich) #terminal #formatting\
Choose for styled text, tables, progress displays, and tracebacks without implementing terminal formatting by hand.

**alive-progress**: [github](https://github.com/rsalmei/alive-progress) #terminal #progress\
Choose for animated progress bars with live throughput and ETA; unlike the broader terminal formatting toolkit rich, it specializes in progress feedback.

**humanize**: [github](https://github.com/python-humanize/humanize) #formatting #localization\
Choose for localized, human-readable times, file sizes, and numbers; unlike the general-purpose boltons collection, it focuses on display formatting.

**humanfriendly**: [github](https://github.com/xolox/python-humanfriendly) #formatting #parsing\
Choose to parse and format human-readable sizes and durations, such as CLI input; humanize focuses on localized display formatting.

**typer**: [github](https://github.com/fastapi/typer) #cli\
Choose for command-line interfaces derived from Python function signatures and type hints, with less argument configuration than `argparse`.

## File I/O

**aiofiles**: [github](https://github.com/Tinche/aiofiles) #files #async\
Choose for an awaitable file API in asyncio applications; it delegates blocking file operations to a thread pool instead of blocking the event loop or requiring manual `asyncio.to_thread` calls.

## Databases

**pypika**: [github](https://github.com/kayak/pypika) #sql #query\
Choose to compose SQL queries dynamically in Python instead of assembling SQL strings; unlike aiosqlite, it builds queries rather than executing them.

**aiosqlite**: [github](https://github.com/omnilib/aiosqlite) #sqlite #async\
Choose for SQLite access in asyncio applications without blocking the event loop on queries; unlike direct `sqlite3` calls, it runs each connection's operations on a worker thread.

**tinydb**: [github](https://github.com/msiemens/tinydb) #database #document\
Choose for a lightweight, serverless document database with a simple Python API and JSON storage. Unlike SQLite, it does not provide ACID guarantees or support access from multiple threads or processes.

## Search

**whoosh3**: [github](https://github.com/priya-sundaram-dev/whoosh) #search #full-text\
Choose for an embedded, pure-Python full-text search index without a separate search server. It continues the original Whoosh project while retaining the `whoosh` import name.

## Caching

**cachetools**: [github](https://github.com/tkem/cachetools) #cache #memory\
Choose for in-memory cache mappings and memoization with TTL or eviction policies such as LFU beyond `functools.lru_cache`; use diskcache for persistence or async-lru for coroutine caching.

**async-lru**: [github](https://github.com/aio-libs/async-lru) #cache #async\
Choose to cache results of async functions, with optional TTL and shared results for concurrent calls with the same arguments; unlike `functools.lru_cache`, it is designed for coroutines.

**diskcache**: [github](https://github.com/grantjenks/python-diskcache) #cache #persistence\
Choose for a disk-backed cache shared safely across threads and processes, with expiration and eviction policies beyond the in-memory `functools.lru_cache`.
It uses SQLite and can also provide a persistent key-value store through `Index`, which does not evict or expire entries. Large values may be stored in separate files outside the database, depending on serialization and the configurable size threshold.

## Queues

**persist-queue**: [github](https://github.com/peter-wangxu/persist-queue) #queue #persistence\
Choose for thread-safe queues that retain items on disk across restarts, unlike the in-memory `queue.Queue`. It offers file and SQLite backends, including an acknowledgement-based SQLite queue.

## Synchronization

**aiorwlock**: [github](https://github.com/aio-libs/aiorwlock) #locking #async\
Choose for an asyncio reader-writer lock when multiple tasks should read concurrently while writes remain exclusive; `asyncio.Lock` provides only mutual exclusion.

**filelock**: [github](https://github.com/tox-dev/filelock) #locking #cross-platform\
Choose for cross-platform coordination between processes using a lock file, without implementing separate OS-specific locking code.

**portalocker**: [github](https://github.com/WoLpH/portalocker) #locking #cross-platform\
Choose to lock an open file directly or coordinate across machines using Redis; filelock's basic API instead coordinates through a separate lock file.

## Event handling

**pyee**: [github](https://github.com/jfhbrook/pyee) #events #async\
Choose for named events with registered listeners, including async handlers; unlike `asyncio.Event`, it dispatches event payloads to callbacks.

## Async concurrency

**asyncer**: [github](https://github.com/fastapi/asyncer) #async #concurrency\
Choose for typed helpers built on AnyIO to run blocking functions in worker threads and manage concurrent tasks, with convenient argument and return-value type support.

## Cancellation

**cancel-token**: [github](https://github.com/Novakov/py-cancel-token) #cancellation\
Choose for cooperative cancellation with shared cancellation state and callbacks, without implementing a token yourself. Unlike `asyncio.Task.cancel()`, consumers must check the token or register callbacks.

## Development tools

**dunamai**: [github](https://github.com/mtkennerly/dunamai) #versioning #vcs\
Choose to derive version strings from version-control tags and commit history through a standalone library or CLI; for integration with Poetry builds, use the poetry-dynamic-versioning plugin.

**poetry**: [github](https://github.com/python-poetry/poetry) #dependencies #packaging\
Choose to manage dependencies, a lockfile, virtual environments, and package builds through one project-oriented tool.

When using Poetry or seeking its extensions, consult [Poetry extensions](references/poetry-extensions.md).

**poethepoet**: [github](https://github.com/nat-n/poethepoet) #tasks #automation\
Choose to define reusable project tasks in `pyproject.toml` and run them in the project's virtual environment, instead of maintaining separate shell scripts.

**pytest**: [github](https://github.com/pytest-dev/pytest) #testing\
Choose over `unittest` for plain assert statements with detailed failure output, reusable fixtures, and concise test parametrization.

When using pytest or seeking its extensions, consult [pytest extensions](references/pytest-extensions.md).

**hypothesis**: [github](https://github.com/HypothesisWorks/hypothesis) #testing #property-based #mpl\
Choose to generate diverse test inputs and shrink failures to simpler examples; it complements test runners such as pytest.

**ruff**: [github](https://github.com/astral-sh/ruff) #linting #formatting\
Choose for fast Python linting and formatting in one tool, with rules covering functionality otherwise spread across multiple tools.

The packages in this skill and its references are recommendations, not authorization to install or introduce packages.

When considering a package for recommendation, consult [discouraged-packages.md](references/discouraged-packages.md). Prefer recommending against packages listed there and explain the recorded reasons. These are recommendations, not prohibitions.

## Further reference

The [PyPI homepage](https://pypi.org/) provides package pages with release histories, compatibility requirements, and project links. Consult it when these details are needed to choose or introduce a package.

Do not fetch the homepage for information already covered here.
