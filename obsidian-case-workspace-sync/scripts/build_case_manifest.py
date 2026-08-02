#!/usr/bin/env python3
"""Build or refresh a SHA-256 manifest for a case folder without deleting files."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('case_folder', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    base = args.case_folder.resolve()
    out = args.output or base / '_sync_manifest.json'
    now = datetime.now(timezone.utc).isoformat()
    old = {}
    if out.exists():
        try:
            old = {x['relative_path']: x for x in json.loads(out.read_text(encoding='utf-8')).get('files', [])}
        except Exception:
            old = {}
    files = []
    for p in sorted(x for x in base.rglob('*') if x.is_file() and x.resolve() != out.resolve()):
        rel = p.relative_to(base).as_posix()
        stat = p.stat()
        digest = sha256(p)
        prior = old.get(rel, {})
        files.append({
            'relative_path': rel,
            'size': stat.st_size,
            'mtime': datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
            'sha256': digest,
            'first_seen': prior.get('first_seen', now),
            'last_scanned': now,
            'last_read': prior.get('last_read'),
            'sync_status': prior.get('sync_status', 'unreviewed'),
            'workspace_record': prior.get('workspace_record'),
        })
    out.write_text(json.dumps({'generated_at': now, 'case_folder': str(base), 'files': files}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(out)


if __name__ == '__main__':
    main()
