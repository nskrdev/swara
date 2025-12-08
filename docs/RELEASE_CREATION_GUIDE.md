# Creating GitHub Release v1.1.0 - Instructions

This document provides instructions for creating the GitHub release v1.1.0 for the Swara project.

## Option 1: Using GitHub Actions (Recommended - No Authentication Required)

The repository includes a GitHub Action workflow that can create the release automatically.

### Steps:

1. Navigate to https://github.com/nskrdev/swara/actions
2. Click on "Create Release v1.1.0" workflow in the left sidebar
3. Click "Run workflow" button
4. In the confirmation input, type: `create`
5. Click "Run workflow" to start the process

The workflow will:
- Verify the tag v1.1.0 exists
- Create the release with comprehensive notes
- Target the main branch
- Generate additional release notes automatically
- Mark it as the latest release

### Verification:

After the workflow completes successfully:
- Visit https://github.com/nskrdev/swara/releases/tag/v1.1.0
- Verify the release is created with all details

## Option 2: Using the Automated Script

If you have the GitHub CLI (`gh`) installed and authenticated:

```bash
cd /home/runner/work/swara/swara
bash scripts/create-release-v1.1.0.sh
```

The script will automatically:
- Verify the tag exists
- Create the release with proper notes
- Target the main branch
- Generate release notes
- Mark it as the latest release

## Option 3: Using GitHub CLI Manually

```bash
gh release create v1.1.0 \
    --repo nskrdev/swara \
    --title "v1.1.0" \
    --notes-file RELEASE_NOTES_v1.1.0.md \
    --target main \
    --generate-notes \
    --latest
```

## Option 4: Using GitHub Web UI

1. Navigate to https://github.com/nskrdev/swara/releases
2. Click "Draft a new release"
3. Fill in the following:
   - **Choose a tag**: Select or enter `v1.1.0`
   - **Target**: Select `main` branch
   - **Release title**: `v1.1.0`
   - **Description**: Copy content from `RELEASE_NOTES_v1.1.0.md`
   - Check ✅ "Set as the latest release"
   - Check ✅ "Generate release notes" (this will add auto-generated notes)
4. Click "Publish release"

## Release Details

- **Tag**: v1.1.0
- **Title**: v1.1.0
- **Target Branch**: main
- **Summary**: Initial public release
- **Project**: Swara - Intelligent Voice Dictation for Linux
- **Language**: Python 3.10+
- **License**: MIT License

## What Gets Included

The release will include:
- Complete source code (automatic)
- Release notes describing the project
- Key features and technology stack
- Installation instructions
- Usage guidelines
- Privacy information
- System requirements
- Support links

## Post-Release

After creating the release:
1. Verify the release appears at https://github.com/nskrdev/swara/releases/tag/v1.1.0
2. Check that the tag is correctly linked
3. Verify all release notes are properly formatted
4. Test download links for source code archives

## Troubleshooting

### GitHub CLI Not Authenticated

```bash
gh auth login
```

Follow the prompts to authenticate with GitHub.

### Tag Not Found

Verify the tag exists:
```bash
git tag -l
git show v1.1.0
```

If the tag doesn't exist, create it:
```bash
git tag v1.1.0 e3cab49
git push origin v1.1.0
```

### Permission Denied

Ensure you have write access to the repository. You must be a collaborator or owner of the `nskrdev/swara` repository.

## Reference Files

- `.github/workflows/create-release-v1.1.0.yml` - GitHub Action workflow for automated release creation
- `RELEASE_NOTES_v1.1.0.md` - Complete release notes
- `scripts/create-release-v1.1.0.sh` - Automated release creation script (requires gh CLI)
- `docs/RELEASE_CREATION_GUIDE.md` - This guide
- `README.md` - Project documentation
- `LICENSE` - MIT License text

## Notes

- The release targets the `main` branch as specified
- Auto-generated release notes will be included in addition to the custom notes
- The release will be marked as the "latest" release
- All source code at tag v1.1.0 will be automatically packaged as `.tar.gz` and `.zip` archives
