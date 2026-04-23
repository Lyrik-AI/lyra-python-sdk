# lyra-python-sdk

Typed Python SDK for the LyrikTrip Lyra/DataPipe domain API.

## Install from proxied GitHub source archive

```bash
pip install "lyra-python-sdk @ https://proxy.cbotomo.com/https://github.com/Lyrik-AI/lyra-python-sdk/archive/refs/tags/v0.1.1.zip"
```

## Release rule

Every public SDK behavior, exported model, client namespace, dependency, or installation-doc change must:

1. Bump `[project].version` in `pyproject.toml`.
2. Create and push the matching `vX.Y.Z` git tag.
3. Verify the proxied GitHub archive after publishing:

```bash
scripts/check-release.sh 0.1.1
```

## Development

```bash
uv run --project . pytest tests -q
```

Python import name stays short and stable:

```python
from lyra import AsyncLyraClient
```
