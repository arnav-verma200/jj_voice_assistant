# Building Executables - Developer Guide

This guide is for developers who want to build the Windows executables from source.

## Prerequisites

1. **Install all dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure the app works in development**:
   ```bash
   python src/main.py
   ```
   Test all features before building.

## Building

### Quick Build (Both Versions)

Run the automated build script:

```bash
python deployment/build.py
```

This will:
- Clean previous builds
- Build CLI version (`jj_voice_assistant_cli.exe`)
- Build GUI version (`jj_voice_assistant_gui.exe`)
- Report file sizes
- Place executables in `dist/` folder

### Manual Build (Individual Versions)

**CLI Version**:
```bash
cd deployment
pyinstaller --clean build_cli.spec
```

**GUI Version**:
```bash
cd deployment
pyinstaller --clean build_gui.spec
```

## Testing

### 1. Basic Functionality Test

Run the executables from `dist/` folder:

```bash
cd dist
.\jj_voice_assistant_cli.exe
```

Test each feature:
- Voice input (all modes)
- Spotify control
- YouTube playback
- WhatsApp messaging
- Volume control
- Browser commands

### 2. Clean Environment Test

**Important**: Test on a machine without Python installed!

Options:
- Create a new Windows user account
- Use a Windows VM
- Ask someone without Python to test

This ensures all dependencies are properly bundled.

### 3. Dependency Check

Verify these work in the executable:
- ✅ Chrome opens correctly
- ✅ Spotify controls work
- ✅ Microphone input works
- ✅ Webcam for volume control works
- ✅ .env file is read from exe directory
- ✅ Chrome sessions persist

## Troubleshooting Build Issues

### Issue: "Module not found" at runtime

**Solution**: Add the module to `hiddenimports` in the spec file.

Example:
```python
hiddenimports=[
    'your_missing_module',
    # ... other imports
],
```

### Issue: MediaPipe models not found

**Solution**: Add MediaPipe data files to spec file:
```python
datas=[
    ('path/to/mediapipe/models', 'mediapipe/models'),
],
```

### Issue: Large executable size

**Expected**: 200-300 MB is normal for this app.

To reduce size (optional):
- Use `upx=True` (already enabled)
- Remove unused features
- Use one-folder mode instead of one-file

### Issue: Slow startup

**Solution**: Use one-folder mode instead of one-file.

In spec file, change:
```python
exe = EXE(
    pyz,
    a.scripts,
    # Remove these lines for one-folder mode:
    # a.binaries,
    # a.zipfiles,
    # a.datas,
    ...
)

# Add this for one-folder mode:
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='jj_voice_assistant_cli',
)
```

## Distribution Package

### Creating Release Package

1. **Build both executables**:
   ```bash
   python deployment/build.py
   ```

2. **Create distribution folder**:
   ```
   jj_voice_assistant_v1.0.0/
   ├── jj_voice_assistant_cli.exe
   ├── jj_voice_assistant_gui.exe
   ├── docs/
   │   └── SETUP_GUIDE.txt
   ├── .env.example
   └── README.txt (simplified version)
   ```

3. **Create README.txt** (simplified):
   ```
   JJ Voice Assistant v1.0.0
   
   Quick Start:
   1. Read docs/SETUP_GUIDE.txt
   2. Install Chrome and Spotify
   3. Run jj_voice_assistant_cli.exe or jj_voice_assistant_gui.exe
   
   Full documentation: https://github.com/yourusername/jj-voice-assistant
   ```

4. **Zip the folder**:
   ```bash
   # PowerShell
   Compress-Archive -Path jj_voice_assistant_v1.0.0 -DestinationPath jj_voice_assistant_v1.0.0.zip
   ```

### GitHub Release

1. **Create a tag**:
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```

2. **Create release on GitHub**:
   - Go to Releases → New Release
   - Select the tag (v1.0.0)
   - Title: "JJ Voice Assistant v1.0.0"
   - Description: Release notes (features, fixes, known issues)
   - Upload the ZIP file
   - Publish release

3. **Update README.md**:
   - Update the releases link
   - Add version badge (optional)

## Version Management

Update version in these files:
- `README.md` (if version is mentioned)
- Release notes
- Git tag

## Code Signing (Optional)

To avoid Windows Defender warnings:

1. **Purchase a code signing certificate** (~$100-500/year)
   - DigiCert
   - Sectigo
   - Others

2. **Sign the executable**:
   ```bash
   signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com jj_voice_assistant_cli.exe
   ```

**Note**: This is optional but recommended for professional distribution.

## Automated Builds with GitHub Actions (Optional)

Create `.github/workflows/build.yml`:

```yaml
name: Build Executables

on:
  release:
    types: [created]

jobs:
  build:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Build executables
      run: python deployment/build.py
    
    - name: Upload to release
      uses: actions/upload-release-asset@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        upload_url: ${{ github.event.release.upload_url }}
        asset_path: ./dist/jj_voice_assistant_cli.exe
        asset_name: jj_voice_assistant_cli.exe
        asset_content_type: application/octet-stream
```

This automatically builds and uploads executables when you create a release.

## Tips

- **Test thoroughly** before releasing
- **Document known issues** in release notes
- **Provide clear error messages** for missing dependencies
- **Keep build scripts updated** as you add features
- **Version your releases** consistently

## Support

For build issues:
- Check PyInstaller documentation
- Search existing issues on GitHub
- Open a new issue with build logs
