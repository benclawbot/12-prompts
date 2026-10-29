#!/usr/bin/env python3
"""Build a portable ChatGPT knowledge text from the canonical skill files."""
from __future__ import annotations
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / '12-prompts'
OUT = ROOT / 'chatgpt' / '12-prompts-knowledge.txt'


def generate() -> str:
    reference = SKILL / 'references'
    items = sorted((reference / 'frameworks').glob('[0-9][0-9]-*.md'))
    if len(items) != 12 or [p.name[:2] for p in items] != [f'{i:02}' for i in range(1, 13)]:
        raise ValueError('Expected exactly 12 numbered framework files from 01 through 12')
    sources = [('Routing', reference / 'routing.md'), ('Quality', reference / 'quality.md')]
    sources.extend((f'Framework {p.name[:2]}', p) for p in items)
    content = '# 12 Prompts — ChatGPT knowledge pack\n\n'
    content += 'Independent English adaptation; source and legal attribution: see repository ATTRIBUTION.md.\n'
    content += 'Read the routing guide and quality contract before applying exactly one relevant framework.\n\n'
    for name, path in sources:
        content += f'\n\n========== {name} ==========\n\n{path.read_text(encoding="utf-8").strip()}\n'
    return content.rstrip() + '\n'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Verify generated bundle is current without writing')
    args = parser.parse_args()
    content = generate()
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding='utf-8') != content:
            print('OUTDATED: run python scripts/build.py')
            return 1
        print('OK: ChatGPT knowledge bundle matches the canonical references')
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(content, encoding='utf-8')
    print(f'Wrote {OUT.relative_to(ROOT)} ({len(content)} characters)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
