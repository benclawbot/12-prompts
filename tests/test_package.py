from __future__ import annotations
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build import generate, OUT, SKILL
from install import install, destination


class PackageTests(unittest.TestCase):
    def test_twelve_unique_frameworks(self):
        files = sorted((SKILL / 'references' / 'frameworks').glob('*.md'))
        self.assertEqual([f.name[:2] for f in files], [f'{i:02}' for i in range(1, 13)])
        for path in files:
            text = path.read_text()
            self.assertIn('## Instruction', text)
            self.assertIn('## Avoid', text)
            self.assertGreater(len(text), 450)

    def test_skill_metadata(self):
        text = (SKILL / 'SKILL.md').read_text()
        self.assertTrue(text.startswith('---\n'))
        head = text.split('---', 2)[1]
        self.assertRegex(head, r'(?m)^name: 12-prompts$')
        self.assertRegex(head, r'(?m)^description: .{40,200}$')
        self.assertIn('references/routing.md', text)
        self.assertIn('references/quality.md', text)

    def test_knowledge_bundle_is_current(self):
        self.assertEqual(OUT.read_text(), generate())
        for i in range(1, 13):
            self.assertIn(f'========== Framework {i:02} ==========', generate())

    def test_eval_cases_are_well_formed(self):
        path = ROOT / 'evals' / 'cases.jsonl'
        cases = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
        self.assertGreaterEqual(len(cases), 20)
        self.assertEqual(len(cases), len({c['id'] for c in cases}))
        expected = {f'{i:02}' for i in range(1,13)} | {'none'}
        self.assertTrue(all(c['expected'] in expected and len(c['input'])>15 for c in cases))
        self.assertTrue({f'{i:02}' for i in range(1,13)}.issubset({c['expected'] for c in cases}))

    def test_installer_project_paths_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            for target, directory in [('claude', '.claude'), ('opencode', '.opencode')]:
                dest = install(target, 'project', tmp)
                self.assertEqual(dest, Path(tmp) / directory / 'skills' / '12-prompts')
                self.assertTrue((dest / 'references' / 'frameworks').is_dir())
                self.assertTrue((dest / 'SKILL.md').is_file())
                with self.assertRaises(FileExistsError):
                    install(target, 'project', tmp)
                install(target, 'project', tmp, force=True)
                self.assertTrue((dest / 'SKILL.md').exists())

    def test_installer_dry_run_and_missing_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = install('claude', 'project', tmp, dry_run=True)
            self.assertFalse(dest.exists())
            with self.assertRaises(ValueError):
                destination('opencode', 'project', str(Path(tmp) / 'missing'))


if __name__ == '__main__':
    unittest.main()
