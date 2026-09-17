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

## Relationship to `arklight android`

The parent repo already ships an `arklight android` subcommand on
`alpha`. That is a **packaging** backend -- it wraps an existing
`arklight build` HTML/CSS/JS output in a native Android app shell via
`WebView`. This repo is testing something categorically different: an
environment that renders the IR natively, without HTML/WebView at
all. See `docs/Foundational/ARCHITECTURE.md`'s "Relationship to the
parent repo" section for the full distinction.

## What's next

Stage 0 (IR wiring scaffold) is in progress -- see
`src/arklight_native_env/`. A later, not-yet-reached stage (Stage 4,
the ARKVM decision) already has a candidate design worth reading
ahead of time:
[`docs/Proposals/ARKVM-FFI-ENVIRONMENT-CONTRACT-PROPOSAL.md`](docs/Proposals/ARKVM-FFI-ENVIRONMENT-CONTRACT-PROPOSAL.md).
