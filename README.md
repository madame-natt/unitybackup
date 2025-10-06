# UnityBackup.py - Unity Project Backup and Cleanup Tool

## Overview
`unitybackup.py` is a Python script designed to backup Unity projects by creating ZIP archives of them, while optionally cleaning temporary/cache folders beforehand and deleting the original directories after a successful backup. This is useful for archiving projects, freeing up disk space, and ensuring clean backups without bloat from Unity's generated files.

**Key Features:**
- Automatically detects Unity projects (subdirectories containing an `Assets` folder).
- Excludes common temp/cache folders during zipping (e.g., `Library/`, `Temp/`, etc.).
- Progress bars for cleaning, zipping, and overall processing (powered by `tqdm`).
- Optional pre-zip cleanup of temp folders.
- Optional deletion of originals post-zip (with safety confirmation).

**⚠️ Important Warnings:**
- using `/-` (delete originals)—this is irreversible.
- Cleaning `.git/` or `.vs/` removes version control history or IDE settings.
- Close Unity Editor before running to avoid file locks.
- Test on a small project directory first.

## Requirements
- **Python**: 3.7+ (tested on 3.12).
- **Dependencies**: 
  - `tqdm` (for progress bars): Install via `pip install tqdm`.
- No other external tools needed (uses built-in `zipfile`, `shutil`, `pathlib`).

## Installation
1. Clone or download this repository (or just save the script as `unitybackup.py`).
2. Install dependencies:
   ```
   pip install tqdm
   ```
3. Ensure Python is in your PATH.

## Usage
Run the script from the command line (e.g., Command Prompt, PowerShell, or terminal).

### Basic Syntax
```
python unitybackup.py [root_path] [/c] [/d]
```

- **`root_path`** (optional positional argument): Path to the directory containing Unity projects (default: current directory `.`).
- **`-c`** (flag): Enable temp folder cleanup before zipping.
- **`-d`** (flag): Delete original project directories after successful zipping (requires "YES" confirmation).

### Examples
1. **Basic backup (zip projects in current directory):**
   ```
   python unitybackup.py
   ```
   - Zips each Unity project into `{project_name}.zip` in the current folder.

2. **Backup with cleanup (current directory):**
   ```
   python unitybackup.py /c
   ```
   - Cleans `Library/`, `Temp/`, `obj/`, `Logs/`, `.git/`, `.vs/` before zipping.

3. **Backup a specific folder with cleanup and delete:**
   ```
   python unitybackup.py "C:\MyUnityProjects" /c /d
   ```
   - Processes projects in `C:\MyUnityProjects`, cleans temp files, zips, then deletes originals.

4. **Just cleanup (no zipping):**
   - The script always zips if projects are found. For cleanup-only, use `/c` without further actions, or modify the script.

### Output
- ZIP files are created in the root path (e.g., `MyProject.zip`).
- Progress bars show:
  - Overall project processing.
  - Per-project temp cleaning (if `/c`).
  - Per-project file zipping.
- Logs success/failures and warnings (e.g., locked files).

## Options Details
| Flag | Description | Default |
|------|-------------|---------|
| `/c` | Clean temp folders before zipping: Deletes `Library/`, `Temp/`, `obj/`, `Logs/`, `.git/`, `.vs/` recursively if they exist. Shows progress. Proceeds to zip even on partial failures. | Off |
| `/d` | **Dangerous!** Deletes the entire original project directory after a successful zip (ZIP exists, has content, no errors). Prompts for "YES" confirmation. | Off |

- **Exclude Patterns (always applied during zip):** `Library/`, `Temp/`, `obj/`, `Logs/`, `.git/`, `.vs/`.
- **Project Detection:** Scans immediate subdirectories for those containing `Assets/`. For deeper nesting, edit the `unity_projects` line in the script.

## Troubleshooting
- **Permission Errors:** Run as admin or close Unity/IDE.
- **No Projects Found:** Ensure subfolders have `Assets/`.
- **Large Projects:** Zipping may take time; progress bar helps track.
- **Customization:** Edit `clean_folders` or `exclude_patterns` lists in the script for more/less aggressive cleaning.
- **Nested Projects:** Change `root_path.iterdir()` to `root_path.rglob('*')` and filter for dirs with `Assets/`.

## License
MIT License – Feel free to use/modify/share. Created for Unity developers' convenience.

## Contributing
Suggestions or pull requests welcome! Report issues if you encounter bugs.

---

*Last updated: October 06, 2025*
