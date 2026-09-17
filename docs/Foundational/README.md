# Foundational

## Overview

The permanent design record for this repo -- what this experiment
is, why it exists, and the principles it's held to. Mirrors the role
`docs/Foundational/` plays in the parent repo
([`Rae-ARK/ARKlight`](https://github.com/Rae-ARK/ARKlight)'s own
`docs/Foundational/README.md`): everything here is **settled**, not
aspirational. **Not deletable** -- updated in place as the
experiment progresses, rather than removed.

This repo is small enough, right now, that "Foundational" holds a
single document. That's intentional, not a placeholder gap: per this
repo's own `ARCHITECTURE.md`, "this repo earns that larger structure
later, if and when it needs it; it doesn't start by copying it
wholesale." A folder existing ahead of having many files in it is
the point -- it's where settled design decisions go *when* they
show up, without needing a restructure at that point.

## Index

| File | Covers |
| --- | --- |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Vision, relationship to the parent repo, core principles, the experimental pipeline (`ARKlight source -> ... -> Android Environment -> Kotlin -> Android Views`), the Stage 0-4 implementation staging, non-goals, and what "success" means for this experiment. |

## Contributing

A doc belongs here once a decision it describes is actually in
force for this repo -- not while it's still under discussion. An
idea that hasn't been decided yet (like a candidate shape for Stage
4's ARKVM question) belongs in
[`docs/Proposals/`](../Proposals/README.md) until it graduates.
