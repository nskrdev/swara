# GitHub Actions Workflows

This directory contains GitHub Action workflows for the Swara project.

## Available Workflows

### Create Release v1.1.0

**File**: `create-release-v1.1.0.yml`

**Purpose**: Automates the creation of GitHub release v1.1.0 for the Swara project.

**Trigger**: Manual workflow dispatch (must be triggered manually from GitHub Actions UI)

**How to Use**:

1. Navigate to the [Actions tab](https://github.com/nskrdev/swara/actions) in the repository
2. Select "Create Release v1.1.0" from the workflows list
3. Click "Run workflow"
4. In the confirmation prompt, type `create` (case-sensitive)
5. Click "Run workflow" to start the process

**What it Does**:

1. ✅ Checks out the repository code
2. ✅ Verifies that tag `v1.1.0` exists
3. ✅ Creates a GitHub release with:
   - Tag: `v1.1.0`
   - Title: `v1.1.0`
   - Target branch: `main`
   - Comprehensive release notes describing the project
   - Auto-generated release notes from commits
   - Marked as the latest release

**Requirements**:

- The tag `v1.1.0` must exist in the repository
- User must have write permissions to create releases
- Workflow requires `contents: write` permission (automatically granted)

**Safety**:

- Requires explicit confirmation by typing `create` to prevent accidental releases
- Validates tag existence before attempting to create release
- Will fail gracefully if the release already exists

**Output**:

Upon successful completion, a new release will be available at:
https://github.com/nskrdev/swara/releases/tag/v1.1.0

## Workflow Syntax

All workflows in this directory follow GitHub Actions syntax version 3.
- Uses `actions/checkout@v4` for repository checkout
- Uses `softprops/action-gh-release@v1` for release creation
- Runs on `ubuntu-latest` runner

## Troubleshooting

### Workflow doesn't appear in Actions tab

- Ensure the workflow file is committed to the `main` branch or the current branch
- Workflow files must be in `.github/workflows/` directory
- File must have `.yml` or `.yaml` extension

### "Tag not found" error

- Verify the tag exists: `git tag -l`
- Push the tag if missing: `git push origin v1.1.0`

### Permission errors

- Ensure you have write access to the repository
- Check that the workflow has `contents: write` permission

## Related Files

- `../docs/RELEASE_CREATION_GUIDE.md` - Comprehensive guide for creating releases
- `../RELEASE_NOTES_v1.1.0.md` - Full release notes for v1.1.0
- `../scripts/create-release-v1.1.0.sh` - Command-line script alternative
