---
language: zh
type: AI Agent Guidance
note: lyra-python-sdk repository guidance.
---

# lyra-python-sdk Agent Rules

## Release Rule

- Any change to public SDK behavior, exported models, client namespaces, dependencies, or installation docs must update `[project].version` in `pyproject.toml`.
- Release tags must match the project version exactly as `vX.Y.Z`.
- After pushing a release tag, run `scripts/check-release.sh X.Y.Z` and confirm the proxied GitHub archive is downloadable.
- PyPI releases use the distribution name `lyriktrip-lyra-python-sdk`; the Python import package remains `lyra`.
- Consumer projects should use the proxied archive URL format: `lyriktrip-lyra-python-sdk @ https://proxy.cbotomo.com/https://github.com/Lyrik-AI/lyra-python-sdk/archive/refs/tags/vX.Y.Z.zip`.
- Do not document a tag as released until `scripts/check-release.sh X.Y.Z` passes.
