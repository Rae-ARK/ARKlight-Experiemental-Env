# ARKlight Experimental Environment

An experiment, not a product: can [ARKlight](https://github.com/Rae-ARK/ARKlight)
Alpha's compiler IR be genuinely lowered into a native, non-Web
execution environment and still work? Android is the first target.

Full scope, principles, and the pipeline this repo is testing:
[`docs/Foundational/ARCHITECTURE.md`](docs/Foundational/ARCHITECTURE.md).
See [`docs/README.md`](docs/README.md) for the full documentation
index (mirrors the parent repo's `Foundational/`/`Proposals/` folder
convention, scaled to what this repo needs).

## Status

No environment code has been written yet. This repo currently holds
only the experiment's design/architecture doc, plus one unsettled
proposal for a later stage. Check `docs/Foundational/ARCHITECTURE.md`
for the planned staged order, and `docs/README.md` for the full
documentation index.

### v1 scope: non-stateful only

**v1 of this experiment is Stages 0-3: static UI structure, styling/
layout, and (if reached) interaction experiments -- all still
non-stateful.** `State`/`Watch`/`Action`/any ARKVM (Stage 4) is a
**v2+ concern**, not part of v1's pass/fail question. Nailing the
non-stateful UI/UX lowering is the whole job for v1; the ARKVM
decision doesn't need to be made, or even leaned toward, for v1 to
succeed or fail on its own terms. See "Implementation staging" in
`docs/Foundational/ARCHITECTURE.md` for the full Stage 0-4 breakdown.

## Setup

This repo depends on the ARKlight compiler (`alpha` branch) as a
library, installed editable into its own virtual environment -- it
does not vendor or fork ARKlight's source.

```bash
git clone https://github.com/Rae-ARK/ARKlight.git
cd ARKlight
git checkout alpha

python3 -m venv .venv
source .venv/bin/activate

# ARKlight is GPLv3+ with additional attribution terms (see its LICENSE).
# A source build (pip install -e .) requires accepting those terms:
ARKLIGHT_ACCEPT_LICENSE=1 pip install -e .
```

This installs the `arklight` package and CLI. Verify with:

```bash
arklight --version
arklight build examples/hello_site/site.py -o /tmp/ark_test --no-open
```

Verified against `alpha` HEAD (currently `v0.0641`; `arklight
--version` reports `0.641`): the install and the `hello_site` build
both complete cleanly, producing `index.html`, `about.html`,
`styles.css`, and `arklight.js`. For reference, `main` is currently
at `v0.54.0` ("alpha catch-up") -- this repo tracks `alpha`
specifically, not `main`, since `alpha` is where the IR this repo
consumes is furthest along.

## Relationship to `arklight android`

The parent repo already ships an `arklight android` subcommand on
`alpha`. That is a **packaging** backend -- it wraps an existing
`arklight build` HTML/CSS/JS output in a native Android app shell via
`WebView`. This repo is testing something categorically different: an
environment that renders the IR natively, without HTML/WebView at
all. See `docs/Foundational/ARCHITECTURE.md`'s "Relationship to the
parent repo" section for the full distinction.

## Relationship to `carklight` and `.arklight`

[`Rae-ARK/C_ARKlight`](https://github.com/Rae-ARK/C_ARKlight)
("carklight") is a separate, downstream project: a C port of a
settled ARKlight baseline, consumed through a stable C ABI. Its
[`docs/ADDENDUM.md`](https://github.com/Rae-ARK/C_ARKlight/blob/main/docs/ADDENDUM.md)
proposes `.arklight` -- a real, versioned, on-disk binary IR file
format (closer to a `.pyc` or LLVM bitcode than a wire payload) that
any language frontend could emit and that `carklight` loads directly,
dispatching to a target backend from it.

That `.arklight` binary IR output **is not built yet** -- carklight's
own staging (`docs/IMPLEMENTATION.md`) has it as Stage 7, the last
stage, not yet marked implemented (Stages 0-6 are). Until it exists,
this repo keeps consuming ARKlight's in-memory IR directly as a
Python library dependency (see Setup above), which works fine for
everything this repo needs today. Once `.arklight` ships, it's a
candidate alternative ingestion path worth revisiting -- reading a
sealed `.arklight` file instead of importing `arklight` as a live
Python dependency -- but that's a later-stage question, not something
v1 is blocked on or needs to decide now.

## What's next

Stage 0 (IR wiring scaffold) is in progress -- see
`src/arklight_native_env/`. A later, not-yet-reached stage (Stage 4,
the ARKVM decision, v2+) already has a candidate design worth reading
ahead of time:
[`docs/Proposals/ARKVM-FFI-ENVIRONMENT-CONTRACT-PROPOSAL.md`](docs/Proposals/ARKVM-FFI-ENVIRONMENT-CONTRACT-PROPOSAL.md).
