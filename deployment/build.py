"""
Build script for creating JJ Voice Assistant executables
Run this script to build both CLI and GUI versions
"""

import os
import sys
import shutil
import subprocess


# Get the directory where build.py is located
DEPLOY_DIR = os.path.dirname(os.path.abspath(__file__))
# Root directory is one level up from deployment/
ROOT_DIR = os.path.dirname(DEPLOY_DIR)


def clean_build_dirs():
    """Remove previous build artifacts in root directory"""
    print("🧹 Cleaning previous builds...")
    
    dirs_to_clean = [
        os.path.join(ROOT_DIR, 'build'), 
        os.path.join(ROOT_DIR, 'dist')
    ]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"   Removed {os.path.basename(dir_name)}/")
            except Exception as e:
                print(f"   ⚠️ Could not remove {os.path.basename(dir_name)}/: {e}")
    
    print("✅ Clean complete\n")


def build_executable(spec_file, name):
    """Build executable from spec file"""
    spec_path = os.path.join(DEPLOY_DIR, spec_file)
    print(f"🔨 Building {name}...")
    print(f"   Spec file: {spec_path}")
    
    try:
        # Run pyinstaller from the ROOT_DIR or specify paths
        # Using --distpath and --workpath relative to ROOT_DIR
        # And specifying the spec file in DEPLOY_DIR
        result = subprocess.run(
            [sys.executable, '-m', 'PyInstaller', '--clean', 
             '--distpath', os.path.join(ROOT_DIR, 'dist'),
             '--workpath', os.path.join(ROOT_DIR, 'build'),
             spec_path],
            cwd=ROOT_DIR,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ {name} build successful!\n")
            return True
        else:
            print(f"❌ {name} build failed!")
            # Print last few lines of stderr which usually contains the reason
            print(f"   Error: {result.stderr[-500:]}\n")
            return False
            
    except Exception as e:
        print(f"❌ Error building {name}: {e}\n")
        return False


def get_file_size(filepath):
    """Get human-readable file size"""
    if not os.path.exists(filepath):
        return "Not found"
    
    size_bytes = os.path.getsize(filepath)
    size_mb = size_bytes / (1024 * 1024)
    return f"{size_mb:.1f} MB"


def main():
    """Main build process"""
    print("=" * 60)
    print("🤖 JJ Voice Assistant - Executable Builder")
    print("=" * 60)
    print()
    
    # Check if PyInstaller is installed
    try:
        subprocess.run([sys.executable, '-m', 'PyInstaller', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ PyInstaller not found!")
        print("   Install it with: pip install pyinstaller")
        sys.exit(1)
    
    # Clean previous builds
    clean_build_dirs()
    
    # Build CLI version
    cli_success = build_executable('build_cli.spec', 'CLI Version')
    
    # Build GUI version
    gui_success = build_executable('build_gui.spec', 'GUI Version')
    
    # Summary
    print("=" * 60)
    print("📦 Build Summary")
    print("=" * 60)
    
    cli_path = os.path.join(ROOT_DIR, 'dist', 'jj_voice_assistant_cli.exe')
    gui_path = os.path.join(ROOT_DIR, 'dist', 'jj_voice_assistant_gui.exe')
    
    print(f"\nCLI Version: {'✅ Success' if cli_success else '❌ Failed'}")
    if cli_success:
        print(f"   Location: {cli_path}")
        print(f"   Size: {get_file_size(cli_path)}")
    
    print(f"\nGUI Version: {'✅ Success' if gui_success else '❌ Failed'}")
    if gui_success:
        print(f"   Location: {gui_path}")
        print(f"   Size: {get_file_size(gui_path)}")
    
    print("\n" + "=" * 60)
    
    if cli_success and gui_success:
        print("🎉 All builds completed successfully!")
        print("\n📝 Next steps:")
        print("   1. Test the executables in dist/ folder")
        print("   2. Create .env file next to the .exe files")
        print("   3. Ensure Chrome and Spotify are installed")
        print("   4. Run the executables to verify functionality")
    else:
        print("⚠️ Some builds failed. Check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
