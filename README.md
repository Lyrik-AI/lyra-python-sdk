# lyra-python-sdk

Typed Python SDK for the LyrikTrip Lyra/DataPipe domain API.

## Install from GitHub source archive

```bash
pip install "lyra-python-sdk @ https://github.com/Lyrik-AI/lyra-python-sdk/archive/refs/tags/v0.1.0.zip"
```

## Development

```bash
uv run --project . pytest tests -q
```

Python import name stays short and stable:

```python
from lyra import AsyncLyraClient
```
