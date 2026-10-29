#!/usr/bin/env python3
"""Install the canonical Agent Skill for Claude Code or OpenCode (stdlib only)."""
from __future__ import annotations
import argparse
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'skills' / '12-prompts'
TARGETS = {
    ('claude', 'global'): Path.home() / '.claude' / 'skills' / '12-prompts',
    ('opencode', 'global'): Path.home() / '.config' / 'opencode' / 'skills' / '12-prompts',
}


def destination(target: str, scope: str, project: str | None = None) -> Path:
    if scope == 'global':
        if project:
            raise ValueError('--project is only valid with --scope project')
        return TARGETS[(target, scope)]
    if not project:
        raise ValueError('--scope project requires --project /path/to/project')
    root = Path(project).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f'Project directory does not exist: {root}')
    return root / ('.claude' if target == 'claude' else '.opencode') / 'skills' / '12-prompts'


def install(target: str, scope: str, project: str | None = None,
            force: bool = False, dry_run: bool = False) -> Path:
    path = destination(target, scope, project)
    if not (SOURCE / 'SKILL.md').is_file():
        raise FileNotFoundError('Canonical SKILL.md not found')
    if path.is_symlink():
        raise ValueError(f'Refusing to replace symlink: {path}')
    if path.exists() and not force:
        raise FileExistsError(f'{path} already exists; use --force to replace it')
    if dry_run:
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    # Copy to a sibling before replacing the destination. Keep backup if any copy fails.
    staging = path.with_name('12-prompts.installing')
    if staging.exists() or staging.is_symlink():
        raise FileExistsError(f'Staging path exists: {staging}')
    shutil.copytree(SOURCE, staging)
    backup = None
    try:
        if path.exists():
            backup = path.with_name('12-prompts.previous')
            if backup.exists() or backup.is_symlink():
                raise FileExistsError(f'Backup path exists: {backup}')
            path.rename(backup)
        staging.rename(path)
        if backup:
            shutil.rmtree(backup)
    except Exception:
        if backup and backup.exists() and not path.exists():
            backup.rename(path)
        raise
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', choices=['claude', 'opencode'], required=True)
    parser.add_argument('--scope', choices=['global', 'project'], default='global')
    parser.add_argument('--project', help='Existing project directory when scope=project')
    parser.add_argument('--force', action='store_true', help='Replace an existing installation')
    parser.add_argument('--dry-run', action='store_true', help='Show target without modifying files')
    args = parser.parse_args()
    try:
        result = install(args.target, args.scope, args.project, args.force, args.dry_run)
    except (ValueError, FileExistsError, FileNotFoundError, OSError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    print(f'{"Would install" if args.dry_run else "Installed"}: {result}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
