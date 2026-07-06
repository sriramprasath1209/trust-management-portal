Trust Management Portal — Windows Single-Click Installer

This folder contains an Inno Setup script and a small PowerShell prereq checker to produce a single-click installer (EXE) for Windows.

Files
- `TrustPortalInstaller.iss` — Inno Setup script. Place this file in `installer/` and compile it with Inno Setup Compiler (ISCC.exe).
- `install_prereqs.ps1` — Optional PowerShell script the installer can run after install to check for Python/Node and offer installation via `winget`.

Build steps
1. Install Inno Setup: https://jrsoftware.org/isinfo.php
2. Open `TrustPortalInstaller.iss` in Inno Setup Compiler or run from command line: `"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" TrustPortalInstaller.iss`
3. The compiled installer EXE will be created in `..\build\` (relative to the `installer` folder).

Usage notes
- The installer copies the project into `C:\Program Files\Trust Management Portal` by default.
- The installer creates a Start menu shortcut that runs `start.bat` to launch backend and frontend.
- The installer will not bundle Python or Node.js. Use the optional `install_prereqs.ps1` step (it attempts to use `winget` to install missing items).
- After installing, run the Start shortcut. The first run will create a `.venv` and install Python packages (this requires internet access).

Advanced: unattended installs
- You can customize `TrustPortalInstaller.iss` or pass Inno Setup command-line parameters to change `DefaultDirName`, `AppVersion`, and output filename.

If you want, I can:
- Create a `docker-compose.yml` instead (simpler for server deployments), or
- Generate a compiled installer for you if you confirm the target Windows architecture and whether you want prerequisites bundled.
