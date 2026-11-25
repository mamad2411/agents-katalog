# CLAUDE.md

`AGENTS.md` and `CLAUDE.md` are the same file via symlink. Edit only one of them and avoid duplicate changes.

## Project Identity

`packingsolver3d` is an unofficial Python distribution of two solvers from [PackingSolver](https://github.com/fontanf/packingsolver) by Florian Fontan: `box` (plain three-dimensional bin packing) and `boxstacks` (three-dimensional packing with stacks, nesting, weight-above, stack density, defects and unloading constraints). The upstream C++ libraries are compiled together with a thin pybind11 bridge into one extension module, `packingsolver3d._core`; the Python layer is a value-in / value-out façade that turns a frozen `Instance` into plain values, calls the bridge once, and turns the plain values that come back into a frozen `Result`.

The package name is deliberate: it names the upstream project, so credit stays with it, and it says `3d` so nobody expects the rectangle, guillotine, one-dimensional or irregular solvers. Adding a fifth problem type is a scope change that needs an explicit decision, not an incremental commit.

The design charter, including the reasoning behind every rule below and the amendment that moved the project from bundled executables to an in-process bridge, lives in `mds/DESIGN_CHARTER.md`. Read it before changing the architecture.

## Hard Boundary: The Upstream Submodule

`upstream/packingsolver/` is a git submodule pinned to the commit recorded as `__UPSTREAM_COMMIT__` in `packingsolver3d/config/meta.py`. It is never patched in this repository. The only permitted change to it is moving the version pointer, and every such move must update `__UPSTREAM_COMMIT__` in the same commit. A fix upstream needs goes to `fontanf/packingsolver` as a pull request; until it lands, adapt the bridge or the façade, or document the limitation in the docstring of the affected function.

Build-system adaptations happen from the outside, in the top-level `CMakeLists.txt`: options are forced with `set(... CACHE ... FORCE)` before `add_subdirectory`, and target properties (for example the MSVC runtime) are rewritten after it. Nothing under `upstream/` is edited.

## Non-Negotiable Rules

1. **No Python object owns C++ memory.** The bridge takes plain dicts and returns plain dicts; no upstream object outlives the call, and no handle, pointer, buffer view or reference into solver memory is ever exposed.
2. **Value in, value out.** Public models are frozen dataclasses. There is no mutable session or live solver handle. The one thing that reaches the caller before the solve ends is `progress_callback`, and it only ever receives an immutable `ProgressEvent` (a handful of numbers copied out of the incumbent) and may only stop the solve; no solver object, partial solution or handle crosses over.
3. **Every solve is auditable.** A `Result` always carries its `RunRecord`: problem type, the exact options handed to the bridge, upstream's captured stdout and stderr, and the wall time. Never drop these to make a result smaller.
4. **A solver-reported bound is never relabelled as proven optimal.** `Status.OPTIMAL` requires a bound reported for the requested objective and an achieved value meeting it. Heuristic incumbent, reported bound and proof are three distinct things; keep them distinct in code, tests and docs.
5. **Never build with both LP backends disabled.** The module is built with `PACKINGSOLVER_USE_CLP=OFF PACKINGSOLVER_USE_HIGHS=ON`, recorded in `CMakeLists.txt`, `config/meta.py` (`__LP_SOLVER__`) and `NOTICE.md`. Because upstream defaults the solver name to `CLP` and throws when no matching backend was compiled in, `linear_programming_solver` is set on every call.
6. **Refusals are typed and carry upstream's own message.** Structural problems raise `InvalidInstanceError`; features the `box` model has no notion of raise `UnsupportedFeatureError`; stackability buckets upstream would assemble and then reject raise `StackSemanticsError`; a `std::invalid_argument` from upstream's `InstanceBuilder` surfaces as `InvalidInstanceError` and any other upstream exception as `SolverFailedError` with the partial `RunRecord` attached. Nothing returns an empty solution where an error is due.
7. **Limits are upstream's.** `time_limit` goes to upstream's timer and `memory_limit` to its own memory check. There is no process boundary: a crash inside upstream takes the interpreter with it, and the docstrings say so. Do not add a hidden subprocess or thread-kill layer; callers who need isolation own their worker process. The stagnation watchdog behind `stop_when_unimproved_for` is not such a layer: a side thread that never touches Python and only raises upstream's own stop signal (an end boolean on its timer), exactly what a time limit does.
8. **An objective is always explicit.** `Instance.objective` has no default and `Objective.DEFAULT` (upstream's unset placeholder, which makes `optimize()` return nothing) is refused in `_encode._validate`; never reintroduce a default objective.
8. **No broad `except Exception:`.** Name every expected exception class and justify it inline; in the bridge, let pybind11 translate `std::exception` rather than catching it.
9. Code, comments, docstrings, commit messages, issue and pull-request bodies are in English.
10. Python must run on CPython 3.7 through 3.14 on Linux, macOS and Windows; the bridge must compile with GCC 10+, Clang and MSVC 2022 as C++17.

## Bridge Contract

`packingsolver3d._core` exposes `box_solve(instance, options)` and `boxstacks_solve(instance, options)`. Both take the payload built by `packingsolver3d._encode.instance_payload` and the options built by `packingsolver3d._solve.core_options`, and return `{"output": <upstream Output JSON as a string>, "stdout": str, "stderr": str, "bins": [...], "stop_reason": None | "callback" | "unimproved"}`. Keep the three pieces in step. The options may carry `stop_when_unimproved_for` / `stop_when_unimproved_after` (seconds; the bridge starts a watchdog thread before `optimize()` that flips an end boolean once that long has passed without an incumbent improvement, and joins it after) and one non-JSON entry, `progress_callback`: a Python callable the bridge wires to upstream's `new_solution_callback`; it is called under the GIL with a plain dict (`time, number_of_items, number_of_bins, profit, cost, label`) and a falsy return value or an exception flips an end boolean on upstream's timer (the exception is rethrown after `optimize()` returns). `_solve.solve_instance` wraps the user's callable so events arrive as `ProgressEvent`, exceptions are re-raised unchanged after the solve, and the callable never appears in `RunRecord.options`.

| Payload key | Content |
|---|---|
| `objective` | upstream token, e.g. `bin-packing`, `knapsack`, `default` |
| `bins` | dicts with `x, y, z` plus any of `cost, copies, copies_min, maximum_weight, maximum_stack_density` |
| `items` | dicts with `x, y, z` plus any of `profit, weight, copies, copies_min, rotations, group_id, stackability_id, nesting_height, maximum_stackability, maximum_weight_above` |
| `defects` | dicts with `bin_type_id, x, y, lx, ly` (`boxstacks` only) |
| `unloading_constraint` | upstream token or `None` (`boxstacks` only) |

A key that is absent is not set on the builder, so upstream's own default applies -- the same default its CSV readers use when a column is missing. `copies_min` is therefore `None` on `ItemType`: upstream's `-1` means "every copy is mandatory, except under knapsack where none is", and an explicit `0` makes bin packing return zero bins as the true optimum. Rotation tokens are `XYZ, YXZ, ZYX, YZX, XZY, ZXY`; the bridge computes placed extents from upstream's `ItemType::x(Rotation)` tables. Returned bins carry `bin_type_id, copies, x, y, z, placements, stacks`; placements carry `item_type_id, x, y, z, lx, ly, lz, rotation` plus `stack_id, group_id` for `boxstacks`; stacks carry `stack_id, x, y, lx, ly, lz`.

Two upstream behaviours are encoded in the façade rather than hidden: `tree_search.cpp` buckets item types by `(group_id, stackability_id)` without comparing footprints and `SolutionBuilder::add_item` then throws, so `boxstacks.validate` refuses buckets with no footprint in common (rotation-aware); and at the pinned commit `boxstacks` reads defects but places stacks over them, which the docstrings state and the tests only assert acceptance for.

## Repository Structure

```text
.
|- AGENTS.md -> CLAUDE.md            # symlink; never edit the two separately
|- CLAUDE.md                         # this file
|- README.md                         # unofficial-distribution notice, install, quick start
|- LICENSE                           # this repository, MIT
|- LICENSE-packingsolver             # verbatim upstream MIT
|- NOTICE.md                         # attribution, pinned commit, build options
|- CMakeLists.txt                    # add_subdirectory(upstream) + pybind11_add_module(_core)
|- pyproject.toml                    # build-system (setuptools, pybind11, cmake) + [tool.cibuildwheel]
|- setup.py                          # metadata from config/meta.py; CMakeExtension driving CMakeLists.txt
|- Makefile                          # unified local build / test / package / docs entrypoint
|- pytest.ini
|- requirements.txt                  # runtime: empty on purpose, the package is stdlib-only
|- requirements-build.txt            # setuptools, wheel, build, cmake, pybind11
|- requirements-test.txt
|- requirements-cov.txt             # gcovr, for folding the bridge's C++ coverage into coverage.xml
|- requirements-plot.txt            # plotly, the optional dependency of packingsolver3d.visual
|- requirements-doc.txt
|- codecov.yml
|- .readthedocs.yaml
|- .gitmodules
|- upstream/packingsolver/           # git submodule -> fontanf/packingsolver, pinned; NEVER patched
|- mds/                              # internal design and plan docs
|- packingsolver3d/
|  |- __init__.py                    # public re-exports
|  |- _core.cpp                      # pybind11 bridge: InstanceBuilder -> optimize() -> plain values
|  |- config/meta.py                 # __VERSION__, __UPSTREAM_COMMIT__, __LP_SOLVER__
|  |- model.py                       # Objective, Rotation, ItemType, BinType, Defect, Instance
|  |- result.py                      # Status, Placement, Stack, PackedBin, RunRecord, Result
|  |- errors.py
|  |- _encode.py                     # Instance -> payload, structural validation
|  |- _solve.py                      # shared pipeline: encode, call _core, decode, classify
|  |- box.py                         # validate() + solve() for PackingSolver::box
|  |- boxstacks.py                   # validate() + solve() for PackingSolver::boxstacks
|  `- visual.py                      # plotly figures of a Result, following upstream's visualize_*.py
|- tools/make_figures.py             # regenerates docs/source/_static/figures (HTML + PNG), `make figures`
|- test/                             # pytest; mirrors the package layout; testfile/upstream = upstream's gtest instances
|- docs/                             # sphinx; source/api_doc is generated by `make rst_auto` and committed
`- .github/workflows/
   |- test.yaml                      # build _core + pytest on 3.7-3.14 per OS (cached CMake tree), wheel smoke
   |- release_test.yaml              # full cibuildwheel matrix, no publishing
   |- release.yaml                   # full cibuildwheel matrix + PyPI publish on release
   `- badge.yaml
```

The built module (`packingsolver3d/_core.*.so` / `.pyd`) and the CMake tree (`build/cmake`) are build products and gitignored.

## Where Changes Belong

- A new solver option is a keyword argument of `box.solve` or `boxstacks.solve`, a key in the options dict, a `set_switch` / `read` call in `_core.cpp`, and a test asserting `result.run.options[...]`.
- A new instance field goes into `model.py`, into `_encode.py` (payload key and validation), into the builder calls in `_core.cpp`, into `box.validate` if the `box` model has no notion of it, and into `test/test_encode.py` plus `test/test_core.py`.
- Anything about status classification belongs in `_solve._classify` and must keep rule 4.
- Anything about how upstream is configured or linked belongs in `CMakeLists.txt`; `setup.py` only drives it and `pyproject.toml` only lists what the isolated build needs.

## Local Development

Required tooling: CPython 3.7 to 3.14 (3.12 recommended for development), CMake >= 3.28, a C++17 compiler (GCC 10+, Clang, or MSVC 2022), GNU make, git with submodule support. `pip install -r requirements-build.txt` provides CMake and pybind11 on every platform.

```shell
git clone --recursive https://github.com/HansBug/packingsolver3d.git
cd packingsolver3d
pip install -r requirements-build.txt -r requirements-test.txt -r requirements-cov.txt -r requirements-doc.txt
make build        # cmake configure + build of upstream and the bridge, module placed in packingsolver3d/
make unittest     # pytest -m unittest with coverage; after LINETRACE=1 make build the C++ bridge is included
make rst_auto     # regenerate docs/source/api_doc from the package
make docs         # sphinx html into docs/build
make package      # sdist + wheel into dist/
```

`make help` lists every target and variable. `RANGE_DIR`, `COV_TYPES`, `MIN_COVERAGE`, `WORKERS` and `JOBS` are the supported knobs; do not add targets for tooling this repository does not have (there is no logo, no CLI, no PyInstaller build).

Native build notes: the first configure fetches Boost, HiGHS and six solver libraries through CMake `FetchContent` and needs network access; the build takes several minutes on a workstation. The CMake tree lives in `build/cmake` (override with `PACKINGSOLVER3D_BUILD_DIR`) and is reused across interpreters: `setup.py` drops the cached `Python_*` / `pybind11_*` entries before each configure so switching interpreters only rebuilds the bridge. `make build_clean` removes the tree and the module. `CMAKE_GENERATOR`, `CMAKE_BUILD_PARALLEL_LEVEL` and `PACKINGSOLVER3D_CMAKE_ARGS` are honoured.

## Packaging and Release

Wheels are built with cibuildwheel from `[tool.cibuildwheel]` in `pyproject.toml`; the isolated build environment gets `pybind11` and `cmake` from `[build-system].requires`, and `setup.py` drives `CMakeLists.txt`. Within one cibuildwheel job the shared `build/cmake` tree means the first wheel pays for upstream and the other seven pay for the bridge only; keep that property when touching `setup.py`. auditwheel and delocate repair `_core` like any other extension module. The sdist grafts `upstream/packingsolver` minus `data/`, `test/` and `.git` so a source install can build.

Release and Release Test share one matrix of six native (runner, architecture) pairs: `ubuntu-22.04` x86_64, `ubuntu-22.04-arm` aarch64, `windows-2022` AMD64, `windows-11-arm` ARM64, `macos-14` arm64, `macos-15-intel` x86_64, for CPython 3.7 through 3.14 minus the versions a platform has no official build of (3.7 on Linux arm64 and macOS; 3.7 to 3.10 on Windows ARM64). Nothing is cross-compiled or emulated: every runner builds its own architecture, and the matrix `include` entries only attach the cibuildwheel architecture name and the `uname -m` spelling. i686, ppc64le, s390x, armv7l, riscv64, loongarch64 and wasm32 are deliberately out of the wheel matrix (no realistic audience for a packing solver, hours of QEMU per job, no local reproduction) and are served by the sdist; the decision and its reasoning are recorded in the charter, and a domestic-architecture or browser build is a future item that waits for those ecosystems. The Python 3.7 jobs deliberately install the last cibuildwheel line that still targets cp37; keep `pip install cibuildwheel` unpinned so each interpreter resolves the line it can run. Runner images are the lowest version still offered, to maximise artifact compatibility.

Tests inside cibuildwheel copy `test/` into a scratch directory before running pytest so the installed wheel, not the source tree, is what gets imported.

## Engineering Expectations

- Preserve upstream terminology: objective tokens, rotation names, option names and field names are upstream's, verbatim, parsed through upstream's own stream operators in the bridge.
- Prefer thin wrappers over opinionated abstractions. If upstream exposes a parameter, expose it faithfully as a keyword argument.
- When behaviour is inherited from upstream rather than decided here, say so in the docstring or test, with the upstream file and function when it is not obvious.
- Do not assume Linux. Paths go through `os.path`, encodings are explicit, and the bridge has no platform-specific code.
- Every published number about solver behaviour must be reproducible from a `RunRecord`; do not report measurements without one.

## Python Code Style

- Compatible with CPython 3.7 through 3.14. No `list[str]` or `X | None` annotations, no `match`, no walrus, no `functools.cached_property`, no `dataclasses(slots=True)`, no `typing.Literal`, no `tomllib`. Use `typing.List`, `Optional`, `Tuple`, `Dict`, `Sequence`.
- `UPPER_SNAKE_CASE` constants, `CapWords` classes, `snake_case` everything else. Module-private helpers start with one underscore; private modules do too (`_encode.py`, `_solve.py`, `_core`).
- Public functions and classes have type annotations and reST docstrings with `:param:`, `:return:`, `:raise:` and, where a short one exists, an `Example::` block that doctest could run.
- Standard library first. The runtime has no third-party dependency and should stay that way. Test code may use `hbutils` (`hbutils.testing.TextAligner` is already a fixture); check `hbutils` before writing a generic helper under `test/`.
- Never `except Exception:`; catch the class you expect and say why.
- Frozen dataclasses for public models; keep `__post_init__` to normalisation such as turning sequences into tuples.

## C++ Style for the Bridge

- `_core.cpp` stays a bridge: it builds upstream objects, calls upstream, and copies results out. No solving logic, no caching, no state between calls.
- Use upstream's types (`Length`, `BinPos`, `ItemTypeId`, ...) and upstream's stream operators for tokens; never re-implement a parser upstream already has.
- Release the GIL around `optimize()` and touch no Python object while it is released.
- Collect upstream's log through `parameters.messages_streams` with a per-call `std::ostringstream` and `messages_to_stdout = false`. Never redirect `std::cout` / `std::cerr` (swapping the global stream buffer crashed under concurrent calls); calls from several threads run at the same time and the test suite checks it.
- Capture `std::cout` / `std::cerr` for the duration of the call only, restored by RAII on every exit path.
- Comments explain why, in English, and reference the upstream file when a workaround exists because of it.

## Source distribution check

`tools/try_sdist.sh <image> <sdist.tar.gz>` installs the tarball from source in a clean container (Debian glibc, Alpine musl or bare Ubuntu with its distro Python) and runs the unit tests against the installed package; the `Try sdist` job of `test.yaml` does it for every push, and `make try_sdist IMAGE=...` does it locally (behind this machine's proxy: `DOCKER_ARGS="--network host -e http_proxy=http://127.0.0.1:17777 -e https_proxy=http://127.0.0.1:17777"`). Anything the sdist needs at build time -- a CMake file, a header, a data file -- must be listed in `MANIFEST.in`; the missing `cmake/msvc_runtime.cmake` that broke every source install before 0.0.1 is the reason this check exists.

## Coverage

One `coverage.xml` carries both languages. `pytest-cov` writes the Python part; when the bridge was built with `LINETRACE=1 make build` (CMake option `PS3D_COVERAGE`, `--coverage -O0` on `packingsolver3d/_core.cpp`, GCC/Clang only), `make unittest` runs `gcovr` (from `requirements-cov.txt`) on the gcov data in `build/cmake`, then merges its Cobertura output with pytest-cov's through `gcovr --cobertura-add-tracefile`, rewriting `coverage.xml` and printing one table with the `.py` files and `_core.cpp` side by side. The Linux jobs of `test.yaml` do exactly that and upload the single file to Codecov; wheels are never built instrumented. A new branch in the bridge is expected to show up in that table; if it cannot be reached from Python, it should not exist.

## Upstream Test Cases (developer guide)

`test/testfile/upstream/` holds verbatim copies of the instances upstream's own gtests solve (`data/box/tests/*`, `data/boxstacks/tests/*`, see `SOURCE.md` there), and `test/test_upstream_cases.py` replays each gtest through this package: same files, same parameters (`use_tree_search=True` for `tree_search_test.cpp`, `NOT_ANYTIME_SEQUENTIAL` for `box_test.cpp` / `optimize_test.cpp`), and the comparison `Solution::operator<` uses for the objective (profit for knapsack, cost for variable-sized bin packing, `x_max` for open dimension x, number of bins for bin packing). When the submodule moves, diff upstream's `test/box` and `test/boxstacks` directories and port what changed; do not invent cases there -- hand-written scenarios belong in the other test modules. This is developer material and stays out of the user documentation.

One case carries a note: upstream's `sequential_onedimensional_rectangle_test.cpp` drives that sub-algorithm directly and its reference for the semi-trailer knapsack instance is empty, while the public entry point here is `optimize()`, which packs two of the three items. That case is compared against `solution_optimize.csv`, the certificate upstream's own `packingsolver_boxstacks` executable (built from the pinned commit, `--linear-programming-solver highs`, no time limit) writes on the same files; regenerate it the same way if the submodule moves.

The CSV loader in the test module (`load_case`) maps upstream's columns onto the model: `X, Y, Z, COPIES, COPIES_MIN, PROFIT, WEIGHT` one to one, an absent column or empty cell leaving the field `None`; `ROTATION_XYZ ... ROTATION_ZXY` cells equal to `1` form `rotations` (no rotation column at all means `rotations=None`); `GROUP_ID, STACKABILITY_ID, NESTING_HEIGHT, MAXIMUM_STACKABILITY, MAXIMUM_WEIGHT_ABOVE` and `MAXIMUM_WEIGHT, MAXIMUM_STACK_DENSITY` are the stacking fields; `IS_SEMI_TRAILER_TRUCK=1` plus the `TRACTOR_WEIGHT ... MIDDLE_AXLE_MAXIMUM_WEIGHT` columns become a `SemiTrailerTruck`; `parameters.csv` rows `objective` and `unloading-constraint` are the enum tokens. Promoting this loader to a public `read_csv_instance` is a pending product decision, not something to do in passing.

## Testing Rules

- Tests live under `test/`, mirror the package layout, and are marked `@pytest.mark.unittest`. `make unittest` runs that marker and then the docstring example gate.
- New or changed behaviour comes with tests. A forwarded option is asserted in `result.run.options`; a payload change is asserted against the exact dict in `test/test_encode.py`; a bridge change is asserted through `test/test_core.py` on plain values.
- Tests that run the solver use instances that solve to proven optimality in well under a second; `pytest.ini` sets a 60 s timeout per test. Shared instances are fixtures in `test/conftest.py`.
- Tests must pass on Linux, macOS and Windows without platform guards; there is nothing POSIX-specific left to guard.

## Documentation Structure

`docs/source` follows the same four-section layout as pyfcstm; every page exists in English (`index.rst`) and Chinese (`index_zh.rst`), and the two must say the same thing.

- `tutorials/<topic>/` -- learning paths with one observable success each (`quick_start`, `boxstacks`). A tutorial gives an input, a short code fragment, visible output and a next link; it stops before options and edge cases.
- `how_to/<topic>/` -- task pages for readers who know what they want (`installation`, `budgets`, `visualization`). Developer material (how the upstream test cases are replayed, how the CSV loader maps columns) lives in this file, not in the user documentation.
- `explanations/<topic>/` -- reasoning: `architecture`, `statuses`, and `upstream_behaviours`, which is the single place that lists every upstream behaviour affecting results, each with its evidence (upstream file and function, or a reproducible observation) and what the package does about it.
- `reference/<topic>/` -- fact tables: `model_fields`, `solver_options`, `errors`; the generated API map (`api_doc_en.rst` / `api_doc_zh.rst`, produced by `make rst_auto`) hangs under Reference, not on the home page.
- `benchmarks/<topic>/` -- the capability study: `datasets`, `participants`, `protocol`, `leaderboards`, `gallery`. `leaderboards/index.rst` and `index_zh.rst` are rendered by `tools/make_benchmarks.py` (`make benchmarks`) from `index.rst.in` / `index_zh.rst.in`, whose `.. TABLE:: <key>` lines are replaced by the generated tables; edit the templates, never the rendered pages. The figures under `_static/benchmarks/` are generated the same way; see the Benchmarks section below.
- Each section has a roadmap `index.rst` / `index_zh.rst`; the home pages `index_en.rst` / `index_zh.rst` list the sections with hidden toctrees plus bullet links, and end with `.. include:: api_doc_<lang>.rst`.

Rules: a newly discovered upstream behaviour is added to `explanations/upstream_behaviours` (both languages), to the README section "Behaviours inherited from upstream", and to the docstring of the function it affects, in the same change. A new model field or solver option is added to the reference tables in the same change as the code. Documentation describes what upstream does; it never claims a limitation is fixed here when the package merely refuses or forwards the input. `make docs` (English) and `make docs_zh` must build; warnings other than the pre-existing "document isn't included in any toctree" for `api_doc/index` and the language twin are defects.

## Docstring Example Gate

Every public function, class and module carries an `Example::` block, and every `>>>` example is executed by `pytest --doctest-modules` (`make doctest`; `make unittest` runs the same pass as its second step and folds it into `coverage.xml`). A docstring is a published contract: an example that does not produce the output it claims is a defect to fix, never something to skip.

- There is no known-failure list, and `# doctest: +SKIP` is not used. An example that genuinely cannot run becomes prose or a plain code block instead of a `>>>` block.
- Option flags are pinned to `ELLIPSIS IGNORE_EXCEPTION_DETAIL DONT_ACCEPT_TRUE_FOR_1` (the `sphinx.ext.doctest` defaults); pytest's own default is `ELLIPSIS` alone and setting the option replaces it, so the full set is always listed.
- Examples are deterministic and fast: tiny instances, `time_limit` given, outputs that do not depend on timing. Show the interesting value, not a wall of output; use `...` only where the elided part is noise (paths, long messages).
- Examples are copy-pasteable: every name they use is imported inside the block. `tools/doctest_plugin.py` only moves the working directory to a temporary one; it injects no names.
- Do not pass pytest arguments that leave examples unexecuted (`-k`, `--deselect`, `--ignore`, `-x`, `--maxfail`, `-n`). A green gate only means something if every example ran. `make doctest DOCTEST_SCOPE=packingsolver3d/<module>.py` narrows a run while iterating.
- The gate checks `>>>` blocks only. A wrong sentence passes it; read the prose.

## Python Docstring Style

reStructuredText, PEP 257, Sphinx roles (`:class:`, `:func:`, `:mod:`, `:attr:`). Field lists use `:param name:`, `:return:`, `:raise Class:`; types live in the annotations, not in `:type:` fields. The templates below are the house shape; the existing modules follow them.

Module:

```python
"""
Overview:
    One sentence on what the module is for.

    A paragraph on how it fits: what calls it, what it calls, what it deliberately does not do.

Example::

    >>> from packingsolver3d._solve import core_options
    >>> core_options()
    {'verbosity_level': 0, 'linear_programming_solver': 'highs'}
"""
```

Class (a frozen dataclass here):

```python
@dataclass(frozen=True)
class Stack:
    """
    A vertical pile of items standing on one footprint of a bin floor.

    Only ``boxstacks`` produces stacks; the ``box`` solver places every item independently and reports none.

    :param stack_id: Index of the stack within its bin.
    :param bin_id: Index of the bin the stack sits in.
    :param lz: Total height of the pile.

    Example::

        >>> from packingsolver3d import Stack
        >>> Stack(stack_id=0, bin_id=0, x=0, y=0, lx=20, ly=30, lz=80).lz
        80
    """
```

Function:

```python
def validate(instance: Instance) -> None:
    """
    Refuse instances whose constraints the ``box`` solver would drop in silence.

    Why, in one or two sentences, naming the upstream file or function when the behaviour is upstream's.

    :param instance: The instance to check.
    :raise UnsupportedFeatureError: When the instance needs :mod:`packingsolver3d.boxstacks`.

    Example::

        >>> from packingsolver3d import BinType, Instance, ItemType, box
        >>> box.validate(Instance(bin_types=[BinType(x=10, y=10, z=10)],
        ...                       item_types=[ItemType(x=2, y=2, z=2, stackability_id=0)]))
        Traceback (most recent call last):
            ...
        packingsolver3d.errors.UnsupportedFeatureError: ...
    """
```

Rules: the first line is one sentence in the imperative or a noun phrase; explain why before how; when a behaviour is inherited from upstream, say so and name the upstream location; `Example::` is the last block; private helpers get a short docstring and an example when their behaviour is not obvious (`_classify`, `_number`).

## Code Style Examples

The rules in "Python Code Style" with the shapes that are expected here.

Typing on 3.7 (`typing` generics, `Optional`, comments for local annotations):

```python
def core_options(time_limit: Optional[float] = None) -> Dict[str, Any]:
    options = {'verbosity_level': 0}  # type: Dict[str, Any]
```

Typed refusals with the reason in the message (never a bare `raise ValueError`):

```python
raise StackSemanticsError(
    'item types #{first} and #{second} share group_id {group} and stackability_id {stackability} '
    'but have no footprint in common ({a} vs {b}); upstream stacks them together and then rejects '
    'the stack, so give them distinct stackability_id values'.format(...)
)
```

Catching only what is expected, with the reason inline:

```python
except ValueError as err:
    # std::invalid_argument from InstanceBuilder: the input is at fault.
    raise InvalidInstanceError('{problem_type}: {err}'.format(problem_type=problem_type, err=err))
```

Frozen dataclasses with normalisation confined to `__post_init__`:

```python
def __post_init__(self):
    object.__setattr__(self, 'bin_types', tuple(self.bin_types))
```

Tests: one class per behaviour group, `@pytest.mark.unittest`, fixtures for shared instances, exact expected values (`== {...}`, `== 'X,Y,Z,...'`), and a comment naming the upstream behaviour whenever the expectation is inherited rather than chosen:

```python
@pytest.mark.unittest
class TestValidate:
    def test_rejects_item_stacking(self, stack_instance):
        with pytest.raises(UnsupportedFeatureError) as exc_info:
            box.validate(stack_instance)
        assert 'boxstacks' in str(exc_info.value)
```

Bridge (C++): upstream types and stream operators, `read(dict, key, out)` for optional fields, RAII for anything that must be undone, no logic beyond building, calling and copying.

## Figures

`docs/source/_static/figures/*.{html,png}` are real solves rendered through `packingsolver3d.visual`, regenerated by `make figures` (`tools/make_figures.py`; PNG export needs `kaleido>=1` and a Chrome/Chromium binary, `FIGURES_ARGS=--no-png` skips it) and committed, so that neither the documentation build nor Read the Docs needs the extension, plotly or a browser. Tutorials embed the HTML fragments with `.. raw:: html` (plotly.js from the CDN) and fall back to the PNG in the PDF build; README.md links the PNGs by raw GitHub URL. The drawing conventions are upstream's (`scripts/visualize_box.py`): translucent grey bin, opaque items with black outlines and their type id, the `Pastel` palette, one scene per bin. A figure is regenerated whenever the instance it shows, the solver, or the visual module changes.

## Benchmarks

`docs/source/benchmarks` compares `box.solve` with third-party libraries on three public instance families (`tools/make_benchmarks.py`, data under `tools/benchmarks/`). Rules:

- Third-party results are stored as **placements** in `tools/benchmarks/third_party.json`, never as objective values; `make_benchmarks.py` re-validates every placement (containment, overlap, copies, pose) and recomputes every number in the tables from the instance files. Our own runs are `tools/benchmarks/ours.json`, rewritten by `make benchmarks` (`--solve`, 10 s per case). `test/test_benchmarks_data.py` keeps both files consistent with the checker.
- Instance files: Egeblad-Pisinger and THPACK9 come from the upstream submodule's `data/box`; the ten Martello-Pisinger-Vigo class-9 instances are committed under `tools/benchmarks/instances/mpv_t9/` with `SOURCE.md` (generator parameters, academic-use note). Do not edit them.
- Labels are part of the evidence: `*` only for a value equal to the best bound on the same problem variant, "rotation relaxed" for participants that could not fix the orientation, "reference" for exact codes at their own budget, `invalid` for a placement the checker rejects. A bound is the tightest valid bound available (exact proof, PackingSolver's own bound, volume bound, constructive optimum); never present a solver's incumbent as an optimum.
- The pages describe the participants from their own repositories and papers and name the third-party versions that ran. The adapters that drove the third-party libraries are not part of this repository and the docs say so; do not reference private harnesses or unpublished result files.
- Adding a case or participant means: extend `BENCHMARKS`/`PARTICIPANTS` in `tools/make_benchmarks.py`, add the placements to `third_party.json`, run `make benchmarks`, update the prose of the leaderboard templates and the other pages in both languages where it quotes numbers, and keep README's summary table in step. The rendered leaderboard pages carry a "Generated by" comment on their first line; a page without it has been edited by hand and must be regenerated.

## Documentation Generation

`docs/source/api_doc/` is generated by `make rst_auto` (`auto_rst.py` per module, `auto_rst_top_index.py` for `api_doc_en.rst` / `api_doc_zh.rst`, both copied from pyfcstm) and committed, because `sphinx-multiversion` builds each tag from its own checkout. Regenerate after adding or removing a module, and delete the page of a removed module by hand. `mds/` holds internal plan documents; they are not published.

Markdown paragraphs are written as single lines, not hard-wrapped at a column.

## Commit Message Style

- `type(scope): imperative summary`, lowercase type and scope, no trailing period: `feat(box): expose dual feasible function switch`, `fix(encode): default item copies_min to upstream's -1`, `ci(release): add s390x to the wheel matrix`.
- Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`, `build`. Scopes: `model`, `encode`, `solve`, `core`, `box`, `boxstacks`, `config`, `tests`, `docs`, `ci`, `packaging`, `cmake`, `upstream`. Omit the scope only when the change spans the whole repository.
- Non-trivial commits get a body: one overview sentence, then `-` bullets for concrete changes, tests, compatibility notes.
- Keep `Co-Authored-By:` trailers when applicable.

## Pull Request Workflow

Branch from `main`, open the pull request against `main`, and keep the body in English with three sections: `## Summary`, `## Changes` (bullets) and `## Validation` (the exact `make` targets run and the workflows that passed). A pull request that moves the upstream submodule pointer states the old and new upstream commits and links the upstream changes it picks up.
