# ARKVM as a C Core with an FFI Environment Interface Contract

## Status

**Proposed. Not accepted, not scheduled.** This repo's own
`docs/Foundational/ARCHITECTURE.md` is explicit that Stage 4 (the
ARKVM decision) is made *after* Stages 0-3 have recorded results,
not before -- and Stages 1-3 haven't been started yet. This document
exists so the idea isn't lost, not to jump the staging order it's
filed against.

- **Type:** Architecture / runtime proposal
- **Scope:** The Stage 4 question only -- "is a native execution
  model (`State`/`Watch`/`Action`) warranted, and if so, what shape
  does it take?" Does not touch Stages 0-3 (IR wiring, static
  rendering, styling/layout mapping), which this proposal assumes
  are already answered by the time Stage 4 is reached.
- **Initial target environment:** Android (this repo's existing
  first target), but the whole point of the shape proposed below is
  that the core shouldn't need to know that.

## Framing note

This is deliberately not a proposal to build an ARKVM. It's a
proposal for *what shape the decision should take*, if and when
Stage 4 says yes. `ARCHITECTURE.md` already lists Stage 4 as a real
future gate; leaving it as a single unexamined line item risks the
decision defaulting, by inertia, to "write it directly inside the
Android environment" the day Stage 4 arrives -- the one shape that
would make a second environment (Desktop, ...) mean rewriting the
same behavioral runtime a second time. This document exists so that,
*when* Stage 4 is reached, there's already a considered alternative
on the table instead of only the path of least resistance.

---

## 1. Summary

Split the eventual ARKVM into two things that don't need to know
much about each other:

1. **The ARKVM core.** A single implementation of the
   `State`/`Watch`/`Action` execution model -- the reactive graph,
   dependency tracking, action dispatch -- written in **C**, free to
   call into C++ libraries internally for anything that genuinely
   benefits from them (containers, string handling, whatever), but
   presenting a **plain C ABI** at its outer boundary. This is the
   "common work" mentioned in the prompt this document answers:
   logic that has nothing to do with any specific platform and
   should exist exactly once.
2. **A per-environment implementation** (Android first) that links
   against the ARKVM core across that C-ABI boundary and supplies
   the platform-specific half: turning ARKVM's "update this node's
   text" call into an actual `TextView.setText()`, and turning a
   real Android tap event into a call back into the core.

The two sides only ever talk to each other through a single,
explicit, versioned contract -- the **Environment Interface
Contract** -- crossed via **FFI**. Neither side needs to be written
in the other's language, and a second environment (Desktop, ...)
implements that same contract instead of reimplementing the
reactive graph.

```
              +-------------------------------+
              |         ARKVM core (C)         |
              |  State / Watch / Action graph  |
              |     -- the "common work" --    |
              +----------------+----------------+
                               |
                   Environment Interface Contract
                        (C-ABI, versioned)
                               |
              +----------------+----------------+
              |                                 |
   +----------v----------+          +-----------v----------+
   |  Android environment  |          |  (future) Desktop env |
   |  JNI/NDK glue,         |          |  its own FFI glue,     |
   |  TextView/GridLayout/  |          |  GTK or whatever this  |
   |  ... real views         |          |  repo's Desktop target |
   |                         |          |  ends up being         |
   +-------------------------+          +-------------------------+
```

---

## 2. Motivation

`ARCHITECTURE.md` already draws one version of this line for the
*rendering* half of the problem -- "Semantic styling, not CSS":
ARKlight's styling semantics get lowered directly to Android view
properties, never round-tripped through CSS as an intermediate
format, because that path is circular and platform-blind in the
wrong direction.

The same shape of problem shows up one layer down once `State`,
`Watch`, and `Action` enter the picture (Stage 4). If the reactive
graph that resolves `Watch` dependencies and dispatches `Action`
handlers is written *inside* the Android environment's own code --
in Kotlin, say, using Android-specific data structures -- then a
second environment doesn't get to reuse any of it. It has to
re-derive the same dependency-tracking and dispatch logic in
whatever language that environment happens to be written in, and
now there are two implementations of "what does `Watch` mean" that
have to be kept in sync by hand. That's exactly the kind of
duplication `ARCHITECTURE.md`'s "Vocabulary: Environment, not
backend" principle is trying to keep this repo's design honest
about -- Android is *a* environment, not *the* environment, and the
common work shouldn't quietly assume otherwise.

Separating the reactive core from the rendering environment behind
an explicit, language-neutral boundary means:

- The behavioral semantics (`State`/`Watch`/`Action`) get **one**
  implementation, not one per environment.
- A new environment's job shrinks to "implement this fixed contract
  in whatever's natural on this platform" -- which is a much smaller
  and more honestly scoped task than "reimplement a reactive VM."
- The core can be reasoned about, and tested, entirely independent
  of any specific platform's view system -- closer in spirit to how
  this repo's own Stage 0 (`ir_loader.py`) already keeps IR loading
  independent of any rendering step.

---

## 3. Terminology

**ARKVM core** -- the single, platform-independent implementation of
the `State`/`Watch`/`Action` execution model. Written in C at its
public boundary; may use C++ internally for its own implementation
details, but nothing on the other side of the FFI boundary is
allowed to depend on that.

**Environment Interface Contract** -- the fixed set of C function
signatures/structs that make up the boundary between the ARKVM core
and any environment implementation. This is the artifact this
proposal is actually asking to be designed carefully, since it's the
one thing every future environment has to agree to.

**Environment implementation** -- a specific platform's code
(Android/Kotlin+JNI first) that implements the "environment side" of
the contract (rendering primitives, event delivery) and calls into
the ARKVM core for the "core side" (reactive evaluation, action
dispatch). This is a sibling concept to, but distinct from, this
repo's Stage 1-2 static-rendering work -- Stage 1-2 lower IR
directly to native views with no behavioral runtime involved at all;
this proposal only matters once Stage 4 introduces one.

**FFI boundary** -- the actual mechanism a given environment uses to
call a C-ABI shared library from its native language: JNI/NDK on
Android, a native module on Desktop, etc. Each environment owns its
own glue code for this; the ARKVM core neither knows nor cares which
one is in use.

---

## 4. Why a C ABI specifically

A few properties make a plain C ABI the right boundary here, rather
than a C++ ABI or a higher-level RPC/serialization boundary:

- **C++ has no stable, cross-compiler ABI.** Name mangling, STL
  container layout, and exception-handling internals all vary by
  compiler and version. A C++ class exposed directly across an FFI
  boundary ties every environment's toolchain to the exact compiler
  the core was built with. A plain `extern "C"` surface sidesteps
  this entirely -- which is exactly why the core is allowed to *use*
  C++ internally but must not *expose* it.
- **Every relevant environment can already call C.** JNI on Android
  is a C API by construction; Kotlin/Java reach it via
  `System.loadLibrary` + `native` method declarations. Whatever this
  repo's eventual Desktop environment turns out to be almost
  certainly has an equally direct C-calling story. A C boundary is
  the actual lowest common denominator, not a novel one.
- **It keeps the "fail loudly" principle enforceable at the
  boundary.** `ARCHITECTURE.md`'s "Fail loudly, not silently"
  principle (an `ARK2041`-style reported error for anything the
  environment can't represent) works cleanly with a small, explicit,
  versioned C function/struct surface -- it's much harder to keep
  that discipline over an implicit, evolving C++ interface.

---

## 5. Contract shape (sketch, not a spec)

This is illustrative only -- the real shape is a design task for
whoever actually reaches Stage 4, not something this proposal is
trying to lock in prematurely. The point is the *kind* of split, not
these exact names.

Calls the ARKVM core exposes, for an environment to drive it:

```c
/* Opaque handle; the environment never reaches into this. */
typedef struct ArkvmInstance ArkvmInstance;

ArkvmInstance *arkvm_create(const uint8_t *ir_blob, size_t ir_len);
void            arkvm_destroy(ArkvmInstance *vm);

/* Environment tells the core a real user event happened. */
void arkvm_dispatch_event(ArkvmInstance *vm,
                           uint32_t node_id,
                           ArkvmEventKind kind,
                           const ArkvmEventPayload *payload);
```

Calls the environment supplies, for the core to drive rendering (a
vtable/struct of function pointers registered at `arkvm_create`
time, following the same shape ARKlight's own backend-interface
placeholder in `ARCHITECTURE.md`'s "Environment interface" section
is left open for):

```c
typedef struct ArkvmEnvironmentCallbacks {
    void (*update_text)(uint32_t node_id, const char *new_text, void *env_ctx);
    void (*set_visible)(uint32_t node_id, bool visible, void *env_ctx);
    void (*report_unsupported)(uint32_t node_id,
                                const char *ark_error_code,
                                const char *message,
                                void *env_ctx);
    /* ... one entry per Stage-4-in-scope capability, added
       deliberately and one at a time, not speculatively. */
} ArkvmEnvironmentCallbacks;
```

Each side only needs to know this contract, never the other side's
internals -- the core never includes a single Android header, and
the Android environment never reaches into the core's reactive-graph
data structures.

---

## 6. Relationship to this repo's existing staging

This proposal is strictly downstream of, and does not change, Stages
0-3:

- Stage 0's `ir_loader.py` still owns getting the IR out of
  `arklight` as a library call. Nothing about this proposal changes
  that boundary or requires it to move out of Python.
- Stages 1-2 (static rendering, styling/layout mapping) have no
  ARKVM involvement at all, by `ARCHITECTURE.md`'s own "No
  behavioral runtime, yet" principle -- this proposal only becomes
  relevant once Stage 4 is actually reached.
- Whatever crosses from the Python-side IR loading into a C ARKVM
  core (a serialized IR blob, most plausibly) is itself an open
  question this proposal deliberately leaves to Stage 4, not
  something worth designing prematurely here.

This also means adopting this shape is a bigger commitment than
anything shipped so far: it introduces a second implementation
language (C, plus whichever C++ libraries the core ends up using)
into a repo that has, to date, been Python-only. That's exactly why
this belongs in `docs/Proposals/`, not `docs/Foundational/`, until
Stage 4 actually says yes.

---

## 7. Open questions

- **IR transfer format.** How does the IR (or the Stage-4-relevant
  behavioral subset of it) actually cross from the Python process
  that loads it into the C ARKVM core -- an in-process embed, a
  serialized blob over a defined format, a separate process
  entirely? Left open; affects the shape of `arkvm_create` above.
- **Threading / event-loop ownership.** Android has its own main-
  thread/UI-thread rules; a future Desktop environment will have its
  own. Does the ARKVM core own no threading opinions at all and
  simply require the environment to call it in a consistent way, or
  does the contract need an explicit threading clause? Left open.
- **Memory ownership across the boundary.** Who frees what, and
  when, for anything passed across `ArkvmEnvironmentCallbacks` --
  particularly strings. A real spec needs an explicit answer here;
  this sketch doesn't attempt one.
- **Contract versioning.** If the contract itself needs to change
  once a second environment exists, how is that negotiated --
  a version field in `arkvm_create`, separate contract headers per
  major version, something else? Left open.

## 8. Non-goals

- This document does not decide that Stage 4 will happen at all.
  `ARCHITECTURE.md`'s own "Non-goals" section still applies in full:
  an ARKVM is explicitly out of scope until Stages 0-3 have recorded
  results.
- This is not a proposal to change this repo's existing language
  (Python) for Stages 0-3, or the parent `arklight` compiler's own
  implementation language, in any way.
- This is not a proposal to reproduce ARKlight's Web runtime
  semantics natively -- same non-goal `ARCHITECTURE.md` already
  states, unaffected by which shape a native runtime eventually
  takes.
- This is not a finished interface spec. Section 5 is illustrative;
  the real contract is a task for whoever actually picks up Stage 4.

## 9. What would make this "accepted"

Per `docs/Proposals/README.md`'s own contributing rule: Stages 0-3
recording results, Stage 4 being reached on `ARCHITECTURE.md`'s own
terms, and a maintainer choosing this shape (or a revised version of
it) over the alternative of writing the reactive runtime directly
inside the Android environment. At that point this document's
content -- reshaped by whatever Stage 4's actual findings are --
graduates into `docs/Foundational/`, and this file is removed or
left as a one-line pointer, matching how the parent repo's own
`docs/Proposals/` folder handles acceptance.
