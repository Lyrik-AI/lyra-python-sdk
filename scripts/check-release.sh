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
pypi_package="lyriktrip-lyra-python-sdk"
pypi_json_url="https://pypi.org/pypi/${pypi_package}/${version}/json"

python_bin="${PYTHON:-}"
if [[ -z "$python_bin" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    python_bin="python3"
  elif command -v python >/dev/null 2>&1; then
    python_bin="python"
  else
    echo "Missing Python interpreter: set PYTHON, or install python3/python." >&2
    exit 1
  fi
fi

project_version="$(
  "$python_bin" - <<'PY'
from pathlib import Path
import re

match = re.search(r'^version\s*=\s*"([^"]+)"', Path("pyproject.toml").read_text(), re.M)
if not match:
    raise SystemExit("Missing [project].version in pyproject.toml")
print(match.group(1))
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

"$python_bin" - "$tmp_file" <<'PY'
from pathlib import Path
import sys
import zipfile

archive = Path(sys.argv[1])
if not zipfile.is_zipfile(archive):
    raise SystemExit(f"Downloaded archive is not a zip file: {archive}")
PY

echo "Release archive OK: ${archive_url}"

pypi_tmp_file="$(mktemp)"
trap 'rm -f "$tmp_file" "$pypi_tmp_file"' EXIT

pypi_http_code="$(curl -LsS -o "$pypi_tmp_file" -w "%{http_code}" "$pypi_json_url")"

if [[ "$pypi_http_code" != "200" ]]; then
  echo "PyPI release check failed: ${pypi_http_code} ${pypi_json_url}" >&2
  exit 1
fi

"$python_bin" - "$pypi_tmp_file" "$pypi_package" "$version" <<'PY'
from pathlib import Path
import json
import sys

payload = json.loads(Path(sys.argv[1]).read_text())
expected_name = sys.argv[2]
expected_version = sys.argv[3]
info = payload.get("info") or {}
files = payload.get("urls") or []

if info.get("name") != expected_name:
    raise SystemExit(f"PyPI name mismatch: {info.get('name')} != {expected_name}")
if info.get("version") != expected_version:
    raise SystemExit(f"PyPI version mismatch: {info.get('version')} != {expected_version}")
if not files:
    raise SystemExit("PyPI release has no distribution files")
PY

echo "PyPI release OK: ${pypi_json_url}"
