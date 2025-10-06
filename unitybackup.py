import os
import argparse
import zipfile
import shutil
from tqdm import tqdm
from pathlib import Path

def is_unity_project(project_dir):
    """Check if a directory is a Unity project by looking for Assets folder."""
    return (project_dir / "Assets").exists()

def clean_temp_folders(project_dir, clean_folders):
    """
    Clean specified temp folders in the project directory.
    
    Args:
    - project_dir: Path to the project directory.
    - clean_folders: List of folder names to clean (e.g., ['Library', 'Temp']).
    """
    to_clean = [f for f in clean_folders if (project_dir / f).exists()]
    if not to_clean:
        print("No temp folders to clean.")
        return True  # Success if nothing to clean
    
    success = True
    for folder in tqdm(to_clean, desc="Cleaning temp folders", unit="folder"):
        try:
            shutil.rmtree(project_dir / folder)
            print(f"Deleted: {folder}")
        except Exception as e:
            print(f"Warning: Could not delete {folder}: {e}")
            success = False
    
    return success

def zip_unity_project(project_dir, output_zip, exclude_patterns=None):
    """
    Zip a Unity project, excluding specified patterns.
    
    Args:
    - project_dir: Path to the project directory.
    - output_zip: Path for the output ZIP file.
    - exclude_patterns: List of patterns to exclude (e.g., ['Library/', 'Temp/']).
    
    Returns:
    - bool: True if zipping succeeded without errors.
    """
    exclude_set = set(exclude_patterns or [])
    success = True
    
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(project_dir):
            # Skip entire dirs if they match exclude patterns
            dirs[:] = [d for d in dirs if not any(d == pat.rstrip('/') for pat in exclude_set)]
            
            # Add files with progress
            file_paths = [os.path.join(root, f) for f in files]
            for file_path in tqdm(file_paths, desc=f"Zipping {project_dir.name}", unit="file"):
                arcname = os.path.relpath(file_path, project_dir)
                try:
                    zf.write(file_path, arcname)
                except Exception as e:
                    print(f"Warning: Could not add {file_path}: {e}")
                    success = False  # Mark as partial failure if any file fails
    
    # Double-check: ZIP should exist and have some content
    if output_zip.exists() and output_zip.stat().st_size > 0:
        return success
    else:
        return False

def main():
    parser = argparse.ArgumentParser(description="Zip Unity projects in a root directory, excluding cache/temp folders.")
    parser.add_argument("root_path", nargs="?", default=".", help="Root path containing Unity projects (default: current dir)")
    parser.add_argument("-c", action="store_true", help="Clean temp folders (Library, Temp, obj, Logs, .git, .vs) before zipping")
    parser.add_argument("-d", action="store_true", help="Delete original project directory after successful zip (WARNING: Irreversible!)")
    args = parser.parse_args()
    
    root_path = Path(args.root_path).resolve()
    if not root_path.exists():
        print(f"Error: Root path '{root_path}' does not exist.")
        return
    
    if args.d:
        confirm = input("WARNING: /d flag will PERMANENTLY DELETE original projects after zipping. Type 'y' to confirm: ")
        if confirm != "y":
            print("Aborted due to confirmation failure.")
            return
    
    if args.c:
        print("Temp cleaning enabled.")
    
    print(f"Root path: {root_path}")
    print("Processing Unity projects...")
    
    unity_projects = [p for p in root_path.iterdir() if p.is_dir() and is_unity_project(p)]
    
    if not unity_projects:
        print("No Unity projects found.")
        return
    
    total_projects = len(unity_projects)
    clean_folders = ["Library", "Temp", "obj", "Logs", ".git", ".vs"]  # Folders to clean if /c
    
    for i, project_dir in enumerate(tqdm(unity_projects, desc="Projects", total=total_projects), 1):
        project_name = project_dir.name
        output_zip = root_path / f"{project_name}.zip"
        
        print(f"\n[{i}/{total_projects}] Processing project: {project_name}")
        
        overall_success = True
        
        # Clean temp folders first if /c
        if args.c:
            print("Starting temp cleanup...")
            clean_success = clean_temp_folders(project_dir, clean_folders)
            if not clean_success:
                print("Temp cleanup had issues, but proceeding with zip...")
            print("Temp cleanup finished.")
        
        # Now zip
        print("Starting zipping...")
        exclude_patterns = ["Library/", "Temp/", "obj/", "Logs/", ".git/", ".vs/"]  # Updated excludes to match clean
        zip_success = zip_unity_project(project_dir, output_zip, exclude_patterns)
        
        if zip_success:
            print(f"Done: {output_zip} created successfully.")
            if args.d:
                try:
                    shutil.rmtree(project_dir)
                    print(f"Deleted original directory: {project_dir}")
                except Exception as e:
                    print(f"Warning: Could not delete {project_dir}: {e}")
                    overall_success = False
        else:
            print(f"Failed to zip {project_name} completely.")
            overall_success = False
    
    print("\nProcessing complete!")

if __name__ == "__main__":
    main()