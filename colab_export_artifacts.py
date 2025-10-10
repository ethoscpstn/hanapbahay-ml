# ========================================
# Run this cell in your Colab notebook to export artifacts
# Copy and paste this entire code into a new Colab cell
# ========================================

from google.colab import files
import os
import shutil

# Find where your artifacts are actually stored
print("Searching for artifact files...")

# Check common locations
possible_paths = [
    "/content/hanapbahay_artifacts/",
    "/content/artifacts/",
    "./artifacts/",
    "/content/"
]

artifact_dir = None
for path in possible_paths:
    if os.path.exists(path):
        # Check if model_latest.joblib exists in this directory
        model_path = os.path.join(path, "model_latest.joblib")
        meta_path = os.path.join(path, "meta.json")

        if os.path.exists(model_path) and os.path.exists(meta_path):
            artifact_dir = path
            print(f"✓ Found artifacts in: {path}")
            break

# If not found in those locations, search for the files
if artifact_dir is None:
    print("\nSearching entire /content/ directory...")
    for root, dirs, files in os.walk("/content"):
        if "model_latest.joblib" in files and "meta.json" in files:
            artifact_dir = root
            print(f"✓ Found artifacts in: {root}")
            break

if artifact_dir is None:
    print("\n❌ ERROR: Could not find model_latest.joblib and meta.json")
    print("\nPlease run the training cells first to generate the model!")
    print("Look for the cell that saves artifacts (Cell 26 or 28 in your notebook)")
else:
    print(f"\n📁 Artifact directory: {artifact_dir}")
    print("Files found:")
    for f in os.listdir(artifact_dir):
        if f.endswith(('.joblib', '.json', '.pkl')):
            size = os.path.getsize(os.path.join(artifact_dir, f))
            print(f"  - {f} ({size:,} bytes)")

    # Create a clean export directory
    export_dir = "/content/hanapbahay_export"
    os.makedirs(export_dir, exist_ok=True)

    # Copy files to export directory
    print(f"\n📦 Copying files to {export_dir}...")
    shutil.copy2(os.path.join(artifact_dir, "model_latest.joblib"), export_dir)
    shutil.copy2(os.path.join(artifact_dir, "meta.json"), export_dir)

    # Create zip file
    print("🗜️  Creating zip file...")
    shutil.make_archive("/content/hanapbahay_artifacts", "zip", export_dir)

    print("\n✅ Ready to download!")
    print("=" * 50)

    # Download the zip file
    files.download("/content/hanapbahay_artifacts.zip")

    print("\n📥 Download started!")
    print("\nNext steps:")
    print("1. Extract hanapbahay_artifacts.zip")
    print("2. Copy model_latest.joblib and meta.json to:")
    print("   c:\\xampp\\htdocs\\public_html\\ml_service\\artifacts\\")
