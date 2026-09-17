"""Stage 0: obtain arklight's Website IR as a library, not via its
HTML/CSS/JS build output or its `android` packaging subcommand.

NOTE ON THIS FILE'S HONESTY: this repo has not yet inspected
arklight's actual public API surface for reaching the IR
programmatically (as opposed to via its `arklight build` CLI, which
only writes HTML/CSS/JS to disk). The two entry points below are
written against the *most plausible* shape of that API, each wrapped
so a wrong guess fails loudly and specifically rather than silently
falling back to something IR-adjacent (e.g. re-parsing HTML, which
this repo explicitly rejects). Whoever picks up Stage 0 should
confirm the real entry point against arklight's own source
(`alpha` branch) and delete whichever guess turns out unused.

Exit criterion for this file (see docs/Foundational/ARCHITECTURE.md,
Stage 0):
`load_ir()` returns a walkable IR object/tree for a given site
source, and `dump_ir()` can render it as inspectable JSON.
"""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any


class IRLoadError(RuntimeError):
    """Raised when arklight's IR can't be obtained as a library call.

    Deliberately not caught anywhere that would fall back to reading
    `arklight build`'s HTML/CSS/JS output instead -- that fallback
    would violate this repo's "IR in, native views out" principle.
    """


def _import_arklight():
    try:
        return importlib.import_module("arklight")
    except ImportError as exc:
        raise IRLoadError(
            "Could not import 'arklight'. This repo depends on it as an "
            "editable library install (see root README.md) -- it is not "
            "vendored here and is not an automatic dependency of this "
            "package."
        ) from exc


def load_ir(site_source: str | Path) -> Any:
    """Return arklight's in-memory Website IR for `site_source`.

    `site_source` is a path to an ARKlight `.py` site source file --
    the same kind of file passed to `arklight build`. This function
    must return the *IR*, not a build output directory; it must not
    shell out to `arklight build` and then read the resulting HTML.

    TODO(stage-0, unconfirmed against arklight source): the exact
    call here is a guess at arklight's public API. Try, in order,
    whichever of these actually exists on the installed `arklight`
    alpha branch, and prune the rest once confirmed:
      1. `arklight.compile_to_ir(path)`
      2. `arklight.ir.build_ir(path)`
      3. Whatever `arklight`'s own CLI (`arklight/cli.py` or similar)
         calls internally between parsing the AST and invoking the
         HTML backend -- that internal call is the real IR boundary
         and is the thing to import directly.
    """
    site_source = Path(site_source)
    if not site_source.exists():
        raise IRLoadError(f"No such site source file: {site_source}")

    arklight = _import_arklight()

    for attr_path in ("compile_to_ir", "ir.build_ir"):
        obj = arklight
        try:
            for part in attr_path.split("."):
                obj = getattr(obj, part)
        except AttributeError:
            continue
        return obj(site_source)

    raise IRLoadError(
        "None of the guessed arklight entry points "
        "(arklight.compile_to_ir, arklight.ir.build_ir) exist on the "
        "installed arklight package. Confirm the real IR-producing call "
        "in arklight's own source (alpha branch) and update "
        "ir_loader.load_ir() accordingly -- see the TODO in this "
        "function's docstring."
    )


def dump_ir(ir: Any) -> str:
    """Render an IR tree as indented, human-readable JSON.

    Stage 0 only needs this to be legible, not lossless: unknown
    node types are rendered by type name and repr() rather than
    silently dropped, per the "fail loudly, not silently" principle
    in docs/Foundational/ARCHITECTURE.md.
    """

    def default(obj: Any) -> Any:
        node_type = type(obj).__name__
        for attr in ("type", "props", "children"):
            if hasattr(obj, attr):
                return {
                    "_node_type": node_type,
                    **{a: getattr(obj, a) for a in ("type", "props", "children") if hasattr(obj, a)},
                }
        return {"_node_type": node_type, "_repr": repr(obj)}

    return json.dumps(ir, indent=2, default=default)
