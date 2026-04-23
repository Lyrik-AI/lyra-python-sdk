#!/usr/bin/env bash
set -euo pipefail

version="${1:-}"

if [[ -z "$version" ]]; then
  echo "Usage: scripts/check-release.sh X.Y.Z" >&2
  exit 2
fi

tag="v${version}"
repo_url="https://github.com/Lyrik-AI/lyra-python-sdk"
archive_url="https://proxy.cbotomo.com/${repo_url}/archive/refs/tags/${tag}.zip"

project_version="$(
  python - <<'PY'
from pathlib import Path
import tomllib

data = tomllib.loads(Path("pyproject.toml").read_text())
print(data["project"]["version"])
PY
)"

if [[ "$project_version" != "$version" ]]; then
  echo "Version mismatch: pyproject.toml has ${project_version}, expected ${version}" >&2
  exit 1
fi

if ! git ls-remote --exit-code --tags origin "refs/tags/${tag}" >/dev/null; then
  echo "Missing remote tag: ${tag}" >&2
  exit 1
fi

tmp_file="$(mktemp)"
trap 'rm -f "$tmp_file"' EXIT

http_code="$(curl -LsS -o "$tmp_file" -w "%{http_code}" "$archive_url")"

if [[ "$http_code" != "200" ]]; then
  echo "Archive request failed: ${http_code} ${archive_url}" >&2
  exit 1
fi

python - "$tmp_file" <<'PY'
from pathlib import Path
import sys
import zipfile

archive = Path(sys.argv[1])
if not zipfile.is_zipfile(archive):
    raise SystemExit(f"Downloaded archive is not a zip file: {archive}")
PY

echo "Release archive OK: ${archive_url}"
