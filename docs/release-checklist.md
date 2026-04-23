# lyra-python-sdk Release Checklist

## Scope

Use this checklist whenever the public SDK behavior, exported models, client namespaces, dependencies, packaging metadata, or installation docs change.

## Checklist

1. Update `pyproject.toml`:
   - bump `[project].version`
   - keep the PyPI distribution name as `lyriktrip-lyra-python-sdk`
2. Update install docs:
   - README archive URL
   - any consumer examples that reference the release version
3. Run local verification:
   - `uv lock --project .`
   - `uv run --project . pytest tests -q`
   - `uv build`
4. Verify built metadata:
   - wheel and sdist report `Name: lyriktrip-lyra-python-sdk`
   - wheel still imports as `lyra`
5. Commit release changes to `main`
6. Create or move the matching git tag:
   - `git tag -f vX.Y.Z`
   - `git push origin main`
   - `git push --force origin vX.Y.Z`
7. Let GitHub Actions publish to PyPI:
   - workflow: `.github/workflows/publish-pypi.yml`
   - environment: `pypi`
8. Verify the published artifacts:
   - `scripts/check-release.sh X.Y.Z`
   - confirm PyPI JSON shows the expected version and files
9. Update downstream consumers to the new archive URL if needed:
   - `lyriktrip.com/apps/api/pyproject.toml`
   - corresponding lock files

## Notes

- Trusted Publishing is configured on PyPI for:
  - repository `Lyrik-AI/lyra-python-sdk`
  - workflow `publish-pypi.yml`
  - environment `pypi`
- `skip-existing: true` is enabled in the publish workflow so a tag re-push does not fail after the files already exist on PyPI.
