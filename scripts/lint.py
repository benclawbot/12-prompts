#!/usr/bin/env python3
"""Enforce portable, dependency-free repository structure and prompt hygiene."""
from __future__ import annotations
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / '12-prompts'
EXCLUDE = {'dist', '__pycache__', '.git', '.venv'}


def main() -> int:
    errors: list[str] = []
    for path in ROOT.rglob('*'):
        if not path.is_file() or EXCLUDE.intersection(path.relative_to(ROOT).parts):
            continue
        if path.suffix not in {'.md', '.py', '.txt', '.yml', '.yaml', '.jsonl', '.csv'} and path.name not in {'LICENSE', '.gitignore'}:
            continue
        try:
            content = path.read_text(encoding='utf-8')
        except UnicodeError:
            errors.append(f'{path.relative_to(ROOT)}: not UTF-8')
            continue
        if '\r' in content:
            errors.append(f'{path.relative_to(ROOT)}: CR line ending')
        if not content.endswith('\n'):
            errors.append(f'{path.relative_to(ROOT)}: missing terminal newline')
        for line_no, line in enumerate(content.splitlines(), start=1):
            if line.rstrip() != line:
                errors.append(f'{path.relative_to(ROOT)}:{line_no}: trailing whitespace')
    text = (SKILL / 'SKILL.md').read_text()
    title = re.search(r'^name: ([a-z0-9]+(?:-[a-z0-9]+)*)$', text, re.M)
    description = re.search(r'^description: (.+)$', text, re.M)
    if not title or title.group(1) != '12-prompts':
        errors.append('SKILL.md: invalid or mismatched skill name')
    if not description or not 40 <= len(description.group(1)) <= 200:
        errors.append('SKILL.md: description length must be 40–200 characters for Claude compatibility')
    refs = (SKILL / 'references' / 'routing.md').read_text()
    for num in range(1, 13):
        if f'| {num:02} |' not in refs:
            errors.append(f'routing.md: missing framework {num:02}')
    if errors:
        for error in errors:
            print('ERROR:', error)
        return 1
    print('OK: UTF-8, line endings, skill metadata, and 12 routing entries')
    return 0

if __name__ == '__main__':
    sys.exit(main())
