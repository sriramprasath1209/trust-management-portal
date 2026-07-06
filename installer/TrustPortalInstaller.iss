; Inno Setup script for Trust Management Portal
[Setup]
AppName=Trust Management Portal
AppVersion=1.0
DefaultDirName={pf}\Trust Management Portal
DefaultGroupName=Trust Management Portal
OutputDir=..uild
OutputBaseFilename=TrustPortalSetup
Compression=lzma
SolidCompression=yes

[Files]
; Copy the entire project (parent directory) into the installation folder, excluding installer outputs and large runtime folders
Source: "..\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion; Excludes: "installer\*; .git\*; node_modules\*; .venv\*"

[Icons]
Name: "{group}\Start Trust Management Portal"; Filename: "{app}\start.bat"; WorkingDir: "{app}"
Name: "{group}\Open Backend API Docs"; Filename: "{sys}\cmd.exe"; Parameters: "/c start http://localhost:8000/docs"

[Run]
; Optionally offer to check/install prerequisites by running the bundled PowerShell script (requires user consent/admin)
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -NoProfile -File \"{app}\\installer\\install_prereqs.ps1\""; Description: "Run prerequisite check (recommended)"; Flags: postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
