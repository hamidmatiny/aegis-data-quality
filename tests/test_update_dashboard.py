import os
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import update_dashboard as ud  # noqa: E402

BASELINES = """# Review Baselines

- 2026-09-16T12:10:00Z: Reviewed 12 reports.
  - Flagged: `8b015d78-...`, `dcbdfe16-...` (MRR arithmetic contradiction).
  - Clean: `f234c1dd-...`, etc.

- 2026-09-18T12:44:00Z: Reviewed recent fleet reports (`c44a56dd` and `3410edb1`).
  - Clean: no drift.

- 2026-09-18T00:05:00Z: Reviewed recent batch of reports (since last review).
  - Clean: No new reports found in last 24h.

# Schema Rules

- 2026-01-01T00:00:00Z: not an entry, schema section
"""


class ParseTests(unittest.TestCase):
    def test_entries_sorted_newest_first_and_schema_section_ignored(self):
        e = ud.parse_baselines(BASELINES)
        self.assertEqual([x["ts"] for x in e],
                         ["2026-09-18T12:44:00Z", "2026-09-18T00:05:00Z", "2026-09-16T12:10:00Z"])

    def test_counts_never_invented(self):
        e = {x["ts"]: x for x in ud.parse_baselines(BASELINES)}
        self.assertEqual(e["2026-09-16T12:10:00Z"]["reviewed"], 12)
        self.assertEqual(e["2026-09-16T12:10:00Z"]["flagged"], ["8b015d78", "dcbdfe16"])
        self.assertEqual(e["2026-09-18T12:44:00Z"]["reviewed"], 2)
        self.assertIsNone(e["2026-09-18T00:05:00Z"]["reviewed"])

    def test_findings_placeholder_counts_zero(self):
        self.assertEqual(ud.count_findings("# Findings\n\nAppend-only.\n\n_(empty)_\n"), 0)
        self.assertEqual(ud.count_findings("# Findings\n\n## 2026-10-01 MRR\n- delivered\n"), 2)


class RepoDashboardTests(unittest.TestCase):
    def test_refresh_real_repo_dashboard_in_tmp(self):
        tmp = tempfile.mkdtemp()
        try:
            os.makedirs(os.path.join(tmp, "memory"))
            shutil.copy(os.path.join(ROOT, "dashboard.yaml"), tmp)
            with open(os.path.join(tmp, "memory", "review-baselines.md"), "w") as f:
                f.write(BASELINES)
            rc = ud.main(["--root", tmp])
            self.assertEqual(rc, 0)
            out = open(os.path.join(tmp, "dashboard.yaml")).read()
            self.assertIn('updated: "2026-09-18"', out)
            self.assertIn('value: "2026-09-18T12:44:00Z"', out)
            self.assertIn('value: "Active"', out)
            self.assertIn('"2026-09-16T12:10:00Z — 12 reports, flagged 8b015d78, dcbdfe16"', out)
            self.assertNotIn("items: []", out)
            # Untouched sections survive.
            self.assertIn('url: "https://ability.ai"', out)
            # Idempotent second run.
            new, _ = ud.render(out, ud.parse_baselines(BASELINES), 0)
            self.assertEqual(new, out)
        finally:
            shutil.rmtree(tmp)


class SkillCallsScriptTest(unittest.TestCase):
    def test_skill_invokes_script(self):
        for base in ("skill-staging", os.path.join(".claude", "skills")):
            p = os.path.join(ROOT, base, "update-dashboard", "SKILL.md")
            if os.path.exists(p) and "scripts/update_dashboard.py" in open(p).read():
                return
        self.fail("update-dashboard SKILL.md does not call scripts/update_dashboard.py")


if __name__ == "__main__":
    unittest.main()
