"""Mutation regression tests for the shipped standards-loading graph.

Run: python scripts/test_standards_integration.py
These verify document wiring; they do not simulate an LLM or compile a target app.
"""

from contextlib import redirect_stdout
import importlib.util
import io
from pathlib import Path
import re
import shutil
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True
SPEC = importlib.util.spec_from_file_location("check_docs", ROOT / "scripts/check-docs.py")
CHECKS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKS)


class StandardsWiringTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="dev-skills-standards-test-")
        self.addCleanup(self.temp.cleanup)
        self.fixture = Path(self.temp.name)
        shutil.copytree(ROOT / "skills", self.fixture / "skills")
        CHECKS.ROOT = self.fixture
        CHECKS.failures.clear()

    def failures(self):
        CHECKS.failures.clear()
        with redirect_stdout(io.StringIO()):
            CHECKS.check_standards_integration()
        return list(CHECKS.failures)

    def edit(self, name, change):
        path = self.fixture / name
        path.write_text(change(path.read_text(encoding="utf-8")), encoding="utf-8")

    def test_intact_package_passes(self):
        self.assertEqual(self.failures(), [])

    def test_removed_shared_configuration_is_detected(self):
        self.edit("skills/rules/entry-protocol.md", lambda text: "\n".join(
            line for line in text.splitlines()
            if not line.startswith("| `docs/agents/coding-standards.md`")
        ))
        self.assertIn("coding standards is a configured input", self.failures())

    def test_removed_gate_section_is_detected(self):
        self.edit("skills/rules/entry-protocol.md", lambda text: re.sub(
            r"#### Standards Gate\n.*?(?=#### Tracker Conventions)", "", text, flags=re.S
        ))
        self.assertIn("the shared Standards Gate anchor exists", self.failures())

    def test_missing_original_is_detected(self):
        (self.fixture / "skills/ruoyi-plus-dev/references/ry-coding.md").unlink()
        self.assertIn("the profile reaches the packaged original rules", self.failures())

    def test_unreachable_retained_original_is_detected(self):
        for name in ("SKILL.md", "REFERENCE.md"):
            self.edit(f"skills/ruoyi-plus-dev/{name}", lambda text: text.replace(
                "](references/ry-coding.md)", "](references/unregistered-source.md)"
            ))
        self.assertIn("the profile reaches the packaged original rules", self.failures())

    def test_removed_workflow_gate_is_detected(self):
        self.edit("skills/implement/REFERENCE.md", lambda text: text.replace(
            "../rules/entry-protocol.md#standards-gate", "../rules/entry-protocol.md"
        ))
        self.assertIn("implement links the Standards Gate", self.failures())

    def test_removed_child_read_is_detected(self):
        for name in ("tdd", "review"):
            with self.subTest(skill=name):
                self.edit(f"skills/{name}/REFERENCE.md", lambda text: "\n".join(
                    line for line in text.splitlines()
                    if not (line.startswith("- [ ]") and "docs/agents/coding-standards.md" in line)
                ))
                self.assertIn(f"{name} sub-agents re-read the standards configuration", self.failures())

    def test_setup_prose_does_not_mask_incomplete_generated_block(self):
        self.edit("skills/setup-project/REFERENCE.md", lambda text: re.sub(
            r"### Coding standards\n.*?(?=<!-- Multi-repo only:)", "", text, flags=re.S
        ))
        self.assertIn("the generated agent block includes the standards pointer", self.failures())


if __name__ == "__main__":
    unittest.main()
