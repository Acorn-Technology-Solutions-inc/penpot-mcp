# Publishing Checklist

Use this checklist before publishing a new version to PyPI.

## Pre-Release Checklist

### Code Quality
- [ ] All tests passing (`pytest -v`)
- [ ] Functionality tests passing (`python test_functionality.py`)
- [ ] Code formatted (`black src/`)
- [ ] Linting clean (`ruff check src/`)
- [ ] Type checking clean (`mypy src/`)
- [ ] No security vulnerabilities

### Documentation
- [ ] README.md updated
- [ ] CHANGELOG.md updated with version changes
- [ ] API documentation current
- [ ] Examples working
- [ ] Version bumped in `pyproject.toml`

### Version Update
- [ ] Version number updated in `pyproject.toml`
- [ ] Version follows [Semantic Versioning](https://semver.org/)
  - **Major** (x.0.0): Breaking changes
  - **Minor** (0.x.0): New features, backward compatible
  - **Patch** (0.0.x): Bug fixes

### Testing
- [ ] Package builds successfully (`python -m build`)
- [ ] Built distributions verified (`python -m twine check dist/*`)
- [ ] Tested on TestPyPI
- [ ] Installation tested from TestPyPI
- [ ] All MCP tools work correctly

## Publishing Steps

### 1. Clean Previous Builds
```bash
rm -rf dist/ build/ *.egg-info src/*.egg-info
```

### 2. Update Version
Edit `pyproject.toml`:
```toml
version = "1.0.1"  # or appropriate version
```

### 3. Update CHANGELOG
Document changes in `CHANGELOG.md`

### 4. Run All Tests
```bash
python -m pytest -v
python test_functionality.py
python test_mcp_simple.py
```

### 5. Build Package
```bash
python -m build
```

Expected output:
```
Successfully built penpot_mcp-X.Y.Z.tar.gz and penpot_mcp-X.Y.Z-py3-none-any.whl
```

### 6. Verify Package
```bash
python -m twine check dist/*
```

### 7. Test on TestPyPI (Optional but Recommended)
```bash
python -m twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ penpot-mcp
```

### 8. Upload to PyPI
```bash
python -m twine upload dist/*
```

Credentials:
- Username: `__token__`
- Password: Your PyPI API token

### 9. Verify Publication
```bash
# Wait ~1 minute
pip install --upgrade penpot-mcp

# Verify version
python -c "from penpot_mcp import __version__; print(__version__)"

# Check package page
# https://pypi.org/project/penpot-mcp/
```

### 10. Tag Release in Git
```bash
git add pyproject.toml CHANGELOG.md
git commit -m "chore: bump version to X.Y.Z"
git tag vX.Y.Z
git push origin main --tags
```

### 11. Create GitHub Release
- Go to: https://github.com/Acorn-Technology-Solutions-inc/penpot-mcp/releases/new
- Tag: vX.Y.Z
- Title: "Release vX.Y.Z"
- Description: Copy from CHANGELOG.md
- Attach dist files (optional)

## Post-Release

### Documentation Updates
- [ ] Update installation badge if needed
- [ ] Announce on social media
- [ ] Update any external documentation
- [ ] Notify users of breaking changes (if any)

### Monitoring
- [ ] Check PyPI package page
- [ ] Monitor download stats: https://pypistats.org/packages/penpot-mcp
- [ ] Watch for issues on GitHub
- [ ] Respond to user feedback

## Automated Publishing (GitHub Actions)

For automated publishing, ensure:

### Setup
1. GitHub Secret `PYPI_API_TOKEN` is set
2. Workflow file `.github/workflows/release.yml` is configured
3. Tests pass in CI

### Trigger
Create and push a tag:
```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```

GitHub Actions will:
1. Run all tests
2. Build package
3. Publish to PyPI
4. Create GitHub release

## Rollback Procedure

If you need to rollback a release:

### 1. Yank from PyPI
```bash
# You can't delete, but can yank (mark as unavailable)
# Do this via PyPI web interface
```

### 2. Publish Fixed Version
```bash
# Increment version (can't re-upload same version)
# version = "1.0.2"  # Fix the issue
python -m build
python -m twine upload dist/*
```

### 3. Notify Users
- Create GitHub issue
- Update README with known issues
- Announce on communication channels

## Version History

Keep track of releases:

| Version | Date | Changes | PyPI Link |
|---------|------|---------|-----------|
| 1.0.0 | 2024-11-22 | Initial release | [Link](https://pypi.org/project/penpot-mcp/1.0.0/) |

## Troubleshooting

### "File already exists"
- You can't re-upload the same version
- Increment version number and rebuild

### "Invalid or non-existent authentication"
- Check your PyPI token is correct
- Ensure token has upload permissions
- Try regenerating token

### "Package name conflict"
- Name `penpot-mcp` is already taken by you or someone else
- Choose different name in `pyproject.toml`

### "Metadata validation failed"
- Check all required fields in `pyproject.toml`
- Ensure README.md exists and is valid
- Verify license information

## Security Best Practices

- [ ] Never commit PyPI tokens to Git
- [ ] Use environment variables or GitHub Secrets
- [ ] Enable 2FA on PyPI account
- [ ] Use scoped tokens when possible
- [ ] Rotate tokens regularly
- [ ] Review package contents before publishing

## Support

For issues with publishing:
- PyPI Documentation: https://pypi.org/help/
- Python Packaging Guide: https://packaging.python.org/
- GitHub Issues: https://github.com/Acorn-Technology-Solutions-inc/penpot-mcp/issues

---

**Ready to publish?** Follow the checklist above to ensure a smooth release! 🚀
