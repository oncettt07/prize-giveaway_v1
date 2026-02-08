import os
import shutil

# Remove old unused folders
folders_to_remove = ['admin', 'public']

for folder in folders_to_remove:
    folder_path = os.path.join(os.path.dirname(__file__), folder)
    if os.path.exists(folder_path):
        print(f"Removing {folder_path}...")
        shutil.rmtree(folder_path)
        print(f"[OK] Removed {folder}")
    else:
        print(f"[SKIP] {folder} not found")

print("\n[DONE] Cleanup complete!")
print("Please open: file:///C:/Users/User/.gemini/antigravity/scratch/prize-giveaway/index.html")
