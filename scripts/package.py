#!/usr/bin/env python3
"""Create reproducible ZIP packages for the entire repo and Claude custom skill."""
from __future__ import annotations
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
EXCLUDE = {'dist', '__pycache__', '.git', '.pytest_cache', '.venv'}


def make_zip(source: Path, output: Path, prefix: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, 'w', compression=ZIP_DEFLATED) as z:
        for file in sorted(p for p in source.rglob('*') if p.is_file() and not EXCLUDE.intersection(p.relative_to(source).parts) and not p.name.endswith('.pyc')):
            arcname = f'{prefix}/{file.relative_to(source).as_posix()}'
            info = ZipInfo(arcname, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, file.read_bytes())
    print(f'Created {output} ({output.stat().st_size} bytes)')


def main():
    make_zip(ROOT / 'skills' / '12-prompts', DIST / '12-prompts-skill.zip', '12-prompts')
    make_zip(ROOT, DIST / '12-prompts-complete.zip', '12-prompts')


if __name__ == '__main__':
    main()
