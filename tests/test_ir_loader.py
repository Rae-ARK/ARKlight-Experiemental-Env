"""Stage 0 tests.

These deliberately do not require `arklight` to be installed, since
this repo does not vendor or auto-install it (see root README.md).
What Stage 0 must guarantee regardless of whether arklight is present:
missing-file and missing-dependency cases fail loudly with a specific
IRLoadError, never silently or via an HTML-parsing fallback.
"""

from pathlib import Path

import pytest

from arklight_native_env.ir_loader import IRLoadError, dump_ir, load_ir


def test_missing_site_source_raises_ir_load_error(tmp_path: Path) -> None:
    missing = tmp_path / "does_not_exist.py"
    with pytest.raises(IRLoadError):
        load_ir(missing)


def test_dump_ir_handles_unknown_node_type() -> None:
    class FakeIRNode:
        def __init__(self) -> None:
            self.type = "Text"
            self.props = {"content": "hello"}
            self.children: list = []

    rendered = dump_ir(FakeIRNode())
    assert "Text" in rendered
    assert "hello" in rendered


def test_dump_ir_falls_back_to_repr_for_opaque_objects() -> None:
    rendered = dump_ir(object())
    assert "_repr" in rendered
