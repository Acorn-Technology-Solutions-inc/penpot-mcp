# Publishing Penpot MCP to PyPI

This guide walks you through publishing the Penpot MCP package to PyPI (Python Package Index).

## Prerequisites

1. **PyPI Account**: Create accounts on both:
   - Production PyPI: https://pypi.org/account/register/
   - Test PyPI: https://test.pypi.org/account/register/ (for testing)

2. **API Tokens**: Generate API tokens for both accounts:
   - PyPI: https://pypi.org/manage/account/token/
   - Test PyPI: https://test.pypi.org/manage/account/token/

3. **Install Build Tools**:
   ```bash
   pip install --upgrade build twine
   ```

## Step-by-Step Publishing Process

### Step 1: Verify Package Configuration

Ensure `pyproject.toml` is properly configured:

```bash
# Check the package configuration
cat pyproject.toml
```

Key fields to verify:
- ✅ `name = "penpot-mcp"`
- ✅ `version = "1.0.0"`
- ✅ `description` is clear
- ✅ `readme = "README.md"` exists
- ✅ `requires-python = ">=3.11"`
- ✅ All dependencies listed
- ✅ Entry point configured: `penpot-mcp = "penpot_mcp.server:main"`

### Step 2: Clean Previous Builds

```bash
# Remove old build artifacts
rm -rf dist/ build/ *.egg-info

# Verify clean state
ls -la
```

### Step 3: Build the Package

```bash
# Build source distribution and wheel
python -m build

# You should see output like:
# Successfully built penpot_mcp-1.0.0.tar.gz and penpot_mcp-1.0.0-py3-none-any.whl
```

This creates two files in `dist/`:
- `penpot_mcp-1.0.0.tar.gz` (source distribution)
- `penpot_mcp-1.0.0-py3-none-any.whl` (wheel)

### Step 4: Test with TestPyPI (Recommended)

Before publishing to production PyPI, test on TestPyPI:

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# You'll be prompted for:
# Username: __token__
# Password: <your TestPyPI API token>
```

**Test the installation:**

```bash
# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ penpot-mcp

# Test it works
python -c "from penpot_mcp import __version__; print(__version__)"
python -m penpot_mcp --help
```

### Step 5: Publish to Production PyPI

Once testing is successful:

```bash
# Upload to production PyPI
python -m twine upload dist/*

# You'll be prompted for:
# Username: __token__
# Password: <your PyPI API token>
```

### Step 6: Verify Publication

```bash
# Wait a minute, then install from PyPI
pip install penpot-mcp

# Verify it works
python -c "from penpot_mcp import __version__; print(__version__)"
```

Visit your package page:
- https://pypi.org/project/penpot-mcp/

## Using GitHub Actions for Automated Publishing

For automated publishing on release, the `.github/workflows/release.yml` is already configured.

### Setup GitHub Secrets

1. Go to: `https://github.com/Acorn-Technology-Solutions-inc/penpot-mcp/settings/secrets/actions`

2. Add these secrets:
   - `PYPI_API_TOKEN` - Your PyPI API token
   - `DOCKER_USERNAME` - Your Docker Hub username (optional)
   - `DOCKER_PASSWORD` - Your Docker Hub password (optional)

### Create a Release

```bash
# Tag a new version
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Or create a release through GitHub UI
# Go to: https://github.com/Acorn-Technology-Solutions-inc/penpot-mcp/releases/new
```

The GitHub Action will automatically:
1. Run all tests
2. Build the package
3. Publish to PyPI
4. Build and push Docker image

## Configuration with PyPI Token

### Option 1: Using `.pypirc` File

Create `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = <your PyPI API token>

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = <your TestPyPI API token>
```

Then upload without prompts:

```bash
python -m twine upload dist/*
```

### Option 2: Using Environment Variables

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=<your PyPI API token>

python -m twine upload dist/*
```

## Updating the Package

To publish a new version:

### 1. Update Version Number

Edit `pyproject.toml`:

```toml
version = "1.0.1"  # Increment version
```

### 2. Update CHANGELOG

Document what changed in version 1.0.1

### 3. Build and Upload

```bash
# Clean old builds
rm -rf dist/

# Build new version
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

### 4. Create Git Tag

```bash
git add pyproject.toml CHANGELOG.md
git commit -m "chore: bump version to 1.0.1"
git tag v1.0.1
git push origin main --tags
```

## Versioning Guidelines

Follow [Semantic Versioning](https://semver.org/):

- **Major** (1.x.x): Breaking changes
- **Minor** (x.1.x): New features, backward compatible
- **Patch** (x.x.1): Bug fixes

Examples:
- `1.0.0` → `1.0.1` (bug fix)
- `1.0.1` → `1.1.0` (new features)
- `1.1.0` → `2.0.0` (breaking changes)

## Troubleshooting

### Issue: "File already exists"

You can't re-upload the same version. Options:
1. Delete from PyPI (not recommended)
2. Increment version number (recommended)

### Issue: "Invalid authentication"

Check your API token:
- Must start with `pypi-` for PyPI
- Must start with `pypi-` for TestPyPI
- No extra spaces or characters

### Issue: "Package name already taken"

If `penpot-mcp` is taken, choose a different name:
- `penpot-mcp-server`
- `mcp-penpot`
- `penpot-model-context-protocol`

Update in `pyproject.toml`:
```toml
name = "penpot-mcp-server"
```

### Issue: "Missing required metadata"

Ensure all required fields in `pyproject.toml`:
- `name`
- `version`
- `description`
- `readme`
- `requires-python`
- `license`

## Post-Publication Checklist

After publishing:

- [ ] Verify package page: https://pypi.org/project/penpot-mcp/
- [ ] Test installation: `pip install penpot-mcp`
- [ ] Test functionality: `python -m penpot_mcp`
- [ ] Update README badges with PyPI version
- [ ] Announce on social media/forums
- [ ] Update documentation with installation instructions

## Security Best Practices

1. **Never commit API tokens** to Git
2. **Use environment variables** or GitHub Secrets
3. **Rotate tokens** regularly
4. **Use scoped tokens** (package-specific)
5. **Enable 2FA** on PyPI account

## Package Statistics

After publication, you can track:
- Downloads: https://pypistats.org/packages/penpot-mcp
- Dependencies: https://libraries.io/pypi/penpot-mcp
- Security: https://snyk.io/advisor/python/penpot-mcp

## Quick Reference Commands

```bash
# Build package
python -m build

# Check package
python -m twine check dist/*

# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*

# Test installation
pip install penpot-mcp

# Verify version
python -c "from penpot_mcp import __version__; print(__version__)"
```

## Additional Resources

- **PyPI Help**: https://pypi.org/help/
- **Python Packaging Guide**: https://packaging.python.org/
- **Twine Documentation**: https://twine.readthedocs.io/
- **Build Documentation**: https://build.pypa.io/

---

**Ready to publish?** Follow the steps above to make `pip install penpot-mcp` available to everyone! 🚀
