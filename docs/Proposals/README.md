# Proposals

## Overview

Speculative, not-yet-decided design ideas for this repo -- put
forward for consideration, but not yet acted on. A file lands here
once someone has sketched the shape of an idea, but before it has
been picked up as something this repo is actually doing.

## Why this is separate from `docs/Foundational/`

Same rationale the parent repo's `docs/Proposals/README.md` gives
for its own split, applied at this repo's (much smaller) scale:
`docs/Foundational/` is the permanent, settled record of what this
experiment *is* and how it's already decided to run. Filing an
unsettled idea next to `ARCHITECTURE.md` would blur that line -- a
reader in `Foundational/` should be able to trust that everything
there reflects the experiment as it actually stands, not something
still under consideration.

Concretely, for this repo: `ARCHITECTURE.md`'s own "Implementation
staging" section is explicit that **Stage 4 (the ARKVM decision) is
a decision made *after* Stages 0-3, not before**. Anything written
about what a native execution model *could* look like is, by that
document's own rule, exactly the kind of thing that cannot yet live
in `Foundational/` as settled fact. It lives here instead, until
Stage 4 is actually reached and a real decision -- built, rejected,
or rewritten -- gets made.

## What belongs here

- Candidate designs for a not-yet-reached stage (e.g. what Stage 4's
  ARKVM might look like), filed early so the idea isn't lost, without
  pretending the decision has already been made.
- Ideas that would change this repo's principles or pipeline if
  accepted, put up for scrutiny before any code is written against
  them.

## What doesn't

- Anything already described as settled in `ARCHITECTURE.md` --
  that belongs in `docs/Foundational/`.
- Experiment logs, stage results, or pass/fail answers as stages are
  actually completed -- those belong recorded against this repo's
  own commit history and experiment logs, per `ARCHITECTURE.md`'s
  "What success means here" section, not in a proposal doc.

## Index

| File | Covers |
| --- | --- |
| [`ARKVM-FFI-ENVIRONMENT-CONTRACT-PROPOSAL.md`](ARKVM-FFI-ENVIRONMENT-CONTRACT-PROPOSAL.md) | Candidate shape for the Stage 4 ARKVM decision: a single ARKVM core written in C (itself free to call into C++ libraries internally) exposed across a stable, versioned C-ABI FFI boundary as an **environment interface contract**, with each native environment (Android first, others later) as a separate, per-platform implementation that hooks into that contract instead of reimplementing behavioral-runtime semantics itself. **Not accepted -- Stage 4 hasn't been reached yet; this is only a sketch for when it is.** |

## Contributing

If you add a new proposal, add a row for it in the table above. When
an idea here is actually decided -- accepted, rejected, or reshaped
-- move its outcome into `docs/Foundational/ARCHITECTURE.md` (if
it's now settled) or into this repo's experiment logs (if it's a
recorded stage result), and update or remove the entry here rather
than leaving it to go stale.
