# ARKlight Experimental Environment Documentation

This folder is the documentation index for this repo. Start here,
then follow the links below into the subfolder for the topic you
need.

This structure deliberately mirrors the folder convention the parent
repo, [`Rae-ARK/ARKlight`](https://github.com/Rae-ARK/ARKlight)
(`alpha` branch), uses in its own `docs/` -- `Foundational/` for the
permanent, settled record and `Proposals/` for unsettled, not-yet-
decided ideas -- scaled down to the two folders this repo actually
needs right now, rather than copying the parent's full folder set
(`Backends/`, `Implementation/`, `version history/`, ...) wholesale.
Per this repo's own `ARCHITECTURE.md`: "this repo earns that larger
structure later, if and when it needs it." Folders can be added here
the same way, if and when this repo's docs actually need them.

## Philosophy

The principles `docs/Foundational/ARCHITECTURE.md` holds this repo
to, in brief (see that document for the full statement of each):

- **IR in, native views out.** No parsing or reverse-engineering
  HTML/CSS/JS -- only ARKlight's own Website IR, consumed as a
  library.
- **Static UI first, behavior later.** `State`/`Watch`/`Action`/any
  ARKVM are explicitly out of scope until Stage 4, and Stage 4 is a
  decision made *after* Stages 0-3 have results, not before. In
  version terms: **v1 is Stages 0-3, non-stateful only; Stage 4's
  ARKVM decision is a v2+ concern.**
- **Semantic styling, not CSS.** IR styling semantics lower directly
  to native view properties; no IR-to-CSS-to-native round trip.
- **Fail loudly, not silently.** An unsupported IR construct is
  reported clearly, never silently dropped or approximated.
- **Environment, not backend.** *Backend* is the compilation
  mechanism; *Environment* is the native target it produces for --
  vocabulary kept deliberately open to more than just Android.

## Folder Guide

Each subfolder has its own `README.md` with a fuller overview and
index -- the summaries below are quick pointers, not the source of
truth.

### [`docs/Foundational/`](Foundational/README.md) -- permanent

The core reading for what this experiment is, why it exists, and the
principles above. **Not deletable** -- updated in place as the
experiment progresses.

| File | Covers |
| --- | --- |
| [`ARCHITECTURE.md`](Foundational/ARCHITECTURE.md) | Vision, relationship to the parent repo, core principles, the experimental pipeline, the Stage 0-4 implementation staging, non-goals, and what "success" means for this experiment. |

### [`docs/Proposals/`](Proposals/README.md) -- unsettled

Speculative design ideas not yet decided or acted on -- distinct
from `Foundational/`'s settled, permanent record. Removed or
graduated into `Foundational/` once a decision is made.

| File | Covers |
| --- | --- |
| [`ARKVM-FFI-ENVIRONMENT-CONTRACT-PROPOSAL.md`](Proposals/ARKVM-FFI-ENVIRONMENT-CONTRACT-PROPOSAL.md) | Candidate shape for the Stage 4 ARKVM decision: a C-core ARKVM (free to use C++ internally) exposed across a stable C-ABI FFI as an environment interface contract, with each native environment implementing that contract rather than reimplementing the reactive runtime itself. **Not accepted -- Stage 4 hasn't been reached.** |

## Contributing

A new document goes in `Foundational/` only once it describes
something already decided and in force. Anything still under
consideration -- including a not-yet-reached later stage's candidate
design -- goes in `Proposals/` until it graduates or is rejected.
