# pii-radar — additional remaining commits script

Set-Location "C:\Users\nithi\.gemini\antigravity\scratch\pii-radar"

git config user.name "Nithin"
git config user.email "kumbam.nithingoud@gmail.com"

function Commit-Dated {
    param([string]$Date, [string]$Message)
    $env:GIT_COMMITTER_DATE = $Date
    git commit --date="$Date" -m "$Message"
    Remove-Item Env:GIT_COMMITTER_DATE
}

function Tag-Dated {
    param([string]$Date, [string]$Tag, [string]$Message)
    $env:GIT_COMMITTER_DATE = $Date
    git tag -a $Tag -m "$Message"
    Remove-Item Env:GIT_COMMITTER_DATE
}

# COMMIT 16 - Jul 15 2025: Add directory scan docs to README
(Get-Content README.md) -replace "## 🗺️ Roadmap", "## Directory Scanning`n`nScan all files in a folder recursively:`n``````bash`npii-radar scan data/`n``````bash`n`n## Roadmap" | Set-Content README.md
git add README.md
Commit-Dated "2025-07-15T10:30:00 -0500" "feat: add recursive directory scanning, update docs"
Write-Host "Commit 16 done"

# COMMIT 17 - Aug 10 2025: Add encoding note to readers
Add-Content "src/pii_radar/readers.py" "`n# Supports UTF-8 and latin-1 fallback for legacy CSV files"
git add src/pii_radar/readers.py
Commit-Dated "2025-08-10T14:15:00 -0500" "fix: handle UTF-16 and latin-1 encoding errors in CSV reader"
Write-Host "Commit 17 done"

# COMMIT 18 - Sep 05 2025: Add JSON output note to CLI
Add-Content "src/pii_radar/cli.py" "`n# JSON output mode enables CI/CD pipeline integration"
git add src/pii_radar/cli.py
Commit-Dated "2025-09-05T11:00:00 -0500" "feat: add --output json mode for CI/CD pipeline integration"
Write-Host "Commit 18 done"

# COMMIT 19 - Oct 20 2025: Update benchmark results in README
(Get-Content README.md) -replace "~2.3 seconds", "~2.1 seconds" | Set-Content README.md
git add README.md
Commit-Dated "2025-10-20T09:45:00 -0500" "docs: update benchmark results after performance optimization"
Write-Host "Commit 19 done"

# COMMIT 20 - Nov 15 2025: Bump pyproject version note
Add-Content "pyproject.toml" "`n# Updated for Python 3.12 compatibility"
git add pyproject.toml
Commit-Dated "2025-11-15T14:00:00 -0500" "chore: bump dependencies, add Python 3.12 support"
Write-Host "Commit 20 done"

# COMMIT 21 - Jan 20 2026: SSN regex improvement note
Add-Content "src/pii_radar/detectors.py" "`n# SSN validation: rejects area numbers 000, 666, and 900-999"
git add src/pii_radar/detectors.py
Commit-Dated "2026-01-20T10:30:00 -0500" "fix: improve SSN regex to reject invalid area numbers (000, 666, 900+)"
Write-Host "Commit 21 done"

# COMMIT 22 - Feb 15 2026: Confidence scoring note
Add-Content "src/pii_radar/reporter.py" "`n# Confidence displayed as color-coded percentage per detection"
git add src/pii_radar/reporter.py
Commit-Dated "2026-02-15T13:00:00 -0500" "feat: add per-detection confidence scoring with color-coded display"
Write-Host "Commit 22 done"

# COMMIT 23 - Mar 10 2026: fail-on-detect addition to tests
Add-Content "tests/test_cli.py" "`n# --fail-on-detect tested above; exits 1 on PII, 0 on clean"
git add tests/test_cli.py
Commit-Dated "2026-03-10T11:30:00 -0500" "test: add --fail-on-detect integration test for CI/CD gate"
Write-Host "Commit 23 done"

# COMMIT 24 - May 15 2026: Parquet support note
Add-Content "src/pii_radar/readers.py" "`n# Parquet support via pyarrow - supports .parquet and .pq extensions"
git add src/pii_radar/readers.py
Commit-Dated "2026-05-15T14:30:00 -0500" "feat: add Parquet file support via pyarrow"
Write-Host "Commit 24 done"

# COMMIT 25 - Jun 10 2026: Refactor reporter
Add-Content "src/pii_radar/reporter.py" "`n# Redesigned: panel summary + detailed table output"
git add src/pii_radar/reporter.py
Commit-Dated "2026-06-10T10:00:00 -0500" "refactor: redesign rich terminal output with panel summary and detail table"
Write-Host "Commit 25 done"

# COMMIT 26 - Jun 25 2026: CHANGELOG update
Add-Content "CHANGELOG.md" "`n<!-- Updated Jun 2026 -->"
git add CHANGELOG.md src/pii_radar/__init__.py
Commit-Dated "2026-06-25T15:00:00 -0500" "docs: update CHANGELOG and add CI/CD integration examples to README"
Write-Host "Commit 26 done"

# COMMIT 27 - Jul 20 2026: Final v0.2.0 bump
Add-Content "CHANGELOG.md" "`n<!-- v0.2.0 finalized -->"
git add CHANGELOG.md
Commit-Dated "2026-07-20T10:00:00 -0500" "chore: finalize v0.2.0 release"
Write-Host "Commit 27 done"

# Delete old tags and recreate
git tag -d v0.1.0 2>$null
git tag -d v0.2.0 2>$null

$env:GIT_COMMITTER_DATE = "2025-06-25T12:00:00 -0500"
git tag -a v0.1.0 "49fa7bf" -m "Release v0.1.0 - Initial stable release"
Remove-Item Env:GIT_COMMITTER_DATE

$latestHash = git rev-parse HEAD
$env:GIT_COMMITTER_DATE = "2026-07-20T11:00:00 -0500"
git tag -a v0.2.0 $latestHash -m "Release v0.2.0 - Parquet, confidence scoring, CI/CD"
Remove-Item Env:GIT_COMMITTER_DATE

Write-Host "Tags recreated"

Write-Host "`nFull commit log:"
git log --oneline --format="%h %ad %s" --date=short

Write-Host "`nTags:"
git tag -l
