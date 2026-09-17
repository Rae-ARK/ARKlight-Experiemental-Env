# ARKlight Experimental Environment: Architecture v0.002

This was the first documentation pass for this repo, originally
written as a single `docs/ARCHITECTURE.md` -- the same shape
ARKlight's own first architecture doc used, before that repo grew
into the larger multi-folder `docs/Foundational/` /
`docs/Proposals/` / `docs/Backends/` system it uses today (see
[`docs/README.md`](../README.md) for how this repo now mirrors that
same folder convention, scaled down to what this repo actually
needs). This document has now graduated into `docs/Foundational/` as
this repo's own permanent, settled design record -- updated in
place, not deleted, per that folder's own
[`README.md`](README.md).

## Vision

This repo exists to answer one question, scientifically rather than
by proposal:

> Can ARKlight Alpha's IR be genuinely lowered into a native,
> non-Web execution environment, and still work?

Android is the first target environment tried. If the experiment
succeeds, it demonstrates that ARKlight's IR contains enough
platform-independent UI semantics to support a second rendering
target -- not just that "we can generate Kotlin." If it fails, that
failure is itself the useful result: it tells us where the IR's
Web-shaped assumptions actually are.

This is a test of the IR, using Android as the instrument. It is not
a proposal to add a production Android environment to ARKlight.

## Relationship to the parent repo

This repo is a child experiment of
[`Rae-ARK/ARKlight`](https://github.com/Rae-ARK/ARKlight), `alpha`
branch. It consumes that compiler as a dependency (installed
editable into a local venv -- see the root `README.md`) and does not
fork or duplicate its source.

It is **not** the same thing as `arklight`'s existing `android`
subcommand on `alpha`. That subcommand is a packaging backend: it
wraps an already-built `arklight build` output directory (HTML/CSS/
JS) into a native Android app shell via
`androidx.webkit.WebViewAssetLoader`. The HTML is still what
renders; Android just hosts a `WebView` around it. See the parent
repo's `docs/Backends/ANDROID-BACKEND-IMPLEMENTATION.md`.

What this repo tests is different in kind: an environment that skips
HTML entirely and renders the IR's UI-relevant structure with native
Android view primitives (`TextView`, layout containers, `GridLayout`,
...) instead. The Web backend's HTML/CSS/JS output is not this
environment's input, and is not parsed at any point -- only the IR
that produced it is.

## Core principles

- **IR in, native views out.** The environment consumes ARKlight's
  Website IR directly. It does not parse or reverse-engineer HTML,
  CSS, or the Web backend's output.
- **Static UI first.** The first cut targets non-interactive
  structure and content only -- `Text`, `Stack`, `Grid`, and similar
  layout/content nodes lowered to their native Android equivalents.
- **No behavioral runtime, yet.** `State`, `Watch`, `Action`, and any
  form of an ARKVM are explicitly out of scope for this phase. This
  experiment is about the UI half of the IR, not about reproducing
  ARKlight's Web runtime semantics on Android.
- **Semantic styling, not CSS.** The environment lowers ARKlight's
  own styling semantics (as represented in the IR) into Android view
  properties/layout parameters directly. It does not go
  IR → generate CSS → parse CSS → translate to Android -- that path
  is circular and was explicitly rejected during design (see
  "Design history" below).
- **Fail loudly, not silently.** A style property or IR construct
  the environment can't represent natively should be reported
  clearly (e.g. `ARK2041: style property 'X' is not supported by
  the experimental Android environment`), not silently dropped or
  approximated in a way that pretends Android and the Web share a
  layout model.
- **Vocabulary: Environment, not backend.** *Backend* is the
  compilation mechanism; *Environment* is the target execution
  context that mechanism produces for. This keeps the concept open
  to future non-Web environments (Desktop, ...) without treating
  Android as merely "another output format."

## Experimental pipeline

```
ARKlight source
    |
    v
ARK AST
    |
    v
ARK IR                    (arklight's normalized Website IR --
    |                      backend-independent: type/props/children)
    v
UI-relevant IR subset      (this repo's own filtering step: strips
    |                       anything behavioral/interactive, keeps
    |                       structure + static content + styling)
    v
Android Environment        (this repo's own code -- not part of
    |                       arklight's own package tree)
    v
Native Android UI          (TextView, layout containers, GridLayout,
    |                       ...)
    v
Kotlin
    |
    v
Android Views
```

Contrast with the existing, shipped path in the parent repo:

```
ARKlight source -> ... -> Website IR -> HTML Backend -> HTML/CSS/JS
                                             |
                                             v
                                   arklight android (packaging)
                                             |
                                             v
                                 WebView-hosted Android app
```

## Environment interface

Current:
- (none yet -- this repo has not written the Android Environment's
  code. This document defines the target shape before that code is
  written, the same way ARKlight's own first `ARCHITECTURE.md`
  described a Backend Interface before more than the HTML backend
  existed.)

## Implementation staging

Each stage below has a single pass/fail exit question. A stage does
not start until the previous one has an answer recorded (see
"What 'success' means here"). None of these stages reuse or build on
top of `arklight`'s existing `android` subcommand or its
WebView/Gradle packaging template -- that code packages *HTML*
output and shares no structure with what this repo is doing. Every
stage's code lives entirely in this repo, not in the parent repo's
tree.

- **Stage 0 -- Scaffold & IR wiring.** No rendering, no UI, no
  Android at all yet. Establish: (a) this repo's own installable
  package, independent of `arklight`'s source tree; (b) the ability
  to invoke `arklight` as a library against a `.py` site source and
  obtain its in-memory Website IR (not its HTML/CSS/JS output); (c)
  a way to walk and dump that IR (e.g. as JSON) for human inspection.
  Exit question: *can this repo obtain and legibly inspect the IR at
  all, using arklight only as a library dependency?* Nothing here is
  user-visible output -- it's the plumbing every later stage needs.
- **Stage 1 -- Native static UI rendering.** IR structure/content
  only (`Text`, `Stack`, `Grid`, ...) lowered to native Android view
  primitives. Exit question: does the IR's static subset carry
  enough information to reconstruct the same structure natively?
- **Stage 2 -- Native styling/layout mapping.** IR styling semantics
  lowered directly to Android view properties/layout params, per the
  "Semantic styling, not CSS" principle above. Exit question: which
  styling properties have no Android equivalent, and what does that
  imply about the IR's platform-independence?
- **Stage 3 -- Native interaction experiments.** Explicitly a later,
  separate phase; not assumed to be needed. Only attempted once
  Stages 0-2 have recorded results.
- **Stage 4 -- ARKVM decision.** A decision on whether a native
  execution model (`State`/`Watch`/`Action` support) is actually
  warranted, made *after* Stages 0-3, not before. **A candidate
  shape for that decision -- an ARKVM core in C (calling into C++
  libraries internally) exposed across a stable C-ABI FFI, with a
  per-environment implementation hooking into it rather than each
  environment reimplementing the behavioral runtime -- is sketched
  in**
  [`docs/Proposals/ARKVM-FFI-ENVIRONMENT-CONTRACT-PROPOSAL.md`](../Proposals/ARKVM-FFI-ENVIRONMENT-CONTRACT-PROPOSAL.md).
  **Filed there, not here, because it is exactly the kind of
  not-yet-decided idea `docs/Proposals/` exists for -- this section
  stays a placeholder until Stage 4 is actually reached and a
  decision is made one way or the other.**

## Non-goals (for this repo, for now)

- Reproducing ARKlight's full Web runtime on Android.
- An ARKVM, native `State`, `Watch`, or `Action` support.
- Treating this repo's output as a production-ready ARKlight
  environment. It is a scoped experiment with a pass/fail question,
  not a roadmap commitment.
- Parsing HTML/CSS as an implementation strategy, at any stage.

## What "success" means here

This repo's job is to end with a report, not just code, answering:

- Did the IR's UI-relevant subset carry enough information to
  reconstruct the same application structure natively, without
  reference to the HTML output?
- Where did the IR turn out to carry Web-shaped assumptions that
  don't translate (styling properties with no Android equivalent,
  layout behaviors that assume a browser, etc.)?
- What does that imply about how general-purpose the IR actually is,
  independent of whether Android specifically is ever shipped as a
  real ARKlight environment?

That report is the actual deliverable of this repo, evaluated
against this repo's own commit history and experiment logs as they
accumulate.

## Design history

The design discussion this document distills (environment vs.
backend terminology, the "don't treat CSS as the Android backend's
input" argument, the staged 1-4 experimental order above) originated
in this repo's second commit and has been folded into this document
rather than kept as a standalone transcript.
