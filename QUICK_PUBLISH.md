# Quick Publishing Guide

**TL;DR**: How to publish Penpot MCP to PyPI in 5 minutes.

## Prerequisites (One-time Setup)

1. **Create PyPI account**: https://pypi.org/account/register/
2. **Generate API token**: https://pypi.org/manage/account/token/
3. **Install tools**: `pip install build twine`

## Publishing Steps

### 1. Update Version

Edit `pyproject.toml`:
```toml
version = "1.0.1"  # Increment appropriately
```

### 2. Update Changelog

Add changes to `CHANGELOG.md`

### 3. Build

```bash
rm -rf dist/
python -m build
```

### 4. Upload

```bash
python -m twine upload dist/*
```

Enter:
- Username: `__token__`
- Password: `<your PyPI token>`

### 5. Verify

```bash
pip install --upgrade penpot-mcp
python -c "from penpot_mcp import __version__; print(__version__)"
```

## Done! 🎉

Your package is now available at:
```bash
pip install penpot-mcp
```

---

## Testing First (Recommended)

Before publishing to production PyPI, test on TestPyPI:

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test install
pip install --index-url https://test.pypi.org/simple/ penpot-mcp
```

---

## Automated Publishing

### Via GitHub Release

1. Add PyPI token to GitHub Secrets as `PYPI_API_TOKEN`
2. Create and push a tag:
   ```bash
   git tag v1.0.1
   git push origin v1.0.1
   ```
3. GitHub Actions automatically publishes to PyPI

---

## Common Issues

**"File already exists"**
→ Increment version number (can't re-upload same version)

**"Authentication error"**
→ Check PyPI token is correct and has upload permissions

**"Invalid metadata"**
→ Warning only, package will still upload

---

## Full Documentation

See [docs/PUBLISHING.md](docs/PUBLISHING.md) for complete guide with:
- Detailed steps
- Troubleshooting
- Security best practices
- Version management
- GitHub Actions setup

---

## Quick Reference

```bash
# Build
python -m build

# Check
python -m twine check dist/*

# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*

# Install
pip install penpot-mcp
```

---

**Need help?** See [PUBLISHING_CHECKLIST.md](PUBLISHING_CHECKLIST.md) for complete checklist.
