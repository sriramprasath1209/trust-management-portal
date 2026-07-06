<#
Simple prerequisite checker for Windows.
It checks for Python and Node.js and offers to install them via winget if available.
Run as Administrator for automatic installs.
#>

function Check-Command($cmd) {
    $null -ne (Get-Command $cmd -ErrorAction SilentlyContinue)
}

Write-Host "Checking prerequisites for Trust Management Portal..."

$python = Check-Command python
$node = Check-Command node

if ($python) { Write-Host "Python found:"; python --version }
else { Write-Host "Python not found." }

if ($node) { Write-Host "Node.js found:"; node --version }
else { Write-Host "Node.js not found." }

if ($python -and $node) {
    Write-Host "All core prerequisites found. You can run the app using the Start shortcut.";
    exit 0
}

# Attempt to use winget if present
$winget = Check-Command winget
if (-not $winget) {
    Write-Host "winget not found. Please install Python (https://www.python.org/downloads/) and Node.js (https://nodejs.org/) manually."
    Pause
    exit 1
}

$consent = Read-Host "Some prerequisites are missing. Install missing items via winget now? (Y/N)"
if ($consent -notin @('Y','y')) { Write-Host "Skipped automatic install."; exit 1 }

if (-not $python) {
    Write-Host "Installing Python via winget..."
    winget install --exact --id Python.Python.3 -e
}
if (-not $node) {
    Write-Host "Installing Node.js LTS via winget..."
    winget install --exact --id OpenJS.NodeJS.LTS -e
}

Write-Host "Installation commands issued. Please reopen a new terminal for environment variable changes to take effect.";
Pause
exit 0
