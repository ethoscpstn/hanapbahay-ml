"""
Check which notebook/model version is currently being used
"""
import json
import os
from datetime import datetime

# Path to current model metadata
META_PATH = os.path.join(os.path.dirname(__file__), 'artifacts', 'meta.json')

print("=" * 60)
print("HanapBahay ML Model Information")
print("=" * 60)

if os.path.exists(META_PATH):
    with open(META_PATH, 'r') as f:
        meta = json.load(f)

    version = meta.get('version', 'Unknown')
    created = meta.get('created_utc', 'Unknown')
    features = meta.get('features', [])

    print(f"\n📦 Model Version: {version}")
    print(f"📅 Created: {created}")
    print(f"🔢 Number of Features: {len(features)}")
    print(f"\n📋 Features Used:")
    for i, feat in enumerate(features, 1):
        print(f"   {i}. {feat}")

    # Parse date
    try:
        dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
        print(f"\n⏰ Model Age: Created on {dt.strftime('%B %d, %Y at %I:%M %p UTC')}")
    except:
        pass

    print("\n" + "=" * 60)
    print("Notebook Files Found:")
    print("=" * 60)

    # Check for notebook files by searching the parent directory
    parent_dir = os.path.dirname(os.path.dirname(__file__))
    print(f"\nSearching in: {parent_dir}\n")

    notebooks_found = []
    try:
        for file in os.listdir(parent_dir):
            if file.endswith('.ipynb'):
                nb_path = os.path.join(parent_dir, file)
                size = os.path.getsize(nb_path)
                modified = datetime.fromtimestamp(os.path.getmtime(nb_path))
                notebooks_found.append({
                    'name': file,
                    'path': nb_path,
                    'size': size,
                    'modified': modified
                })

        if notebooks_found:
            for nb in notebooks_found:
                print(f"📓 {nb['name']}")
                print(f"   Size: {nb['size']:,} bytes ({nb['size']/1024:.1f} KB)")
                print(f"   Modified: {nb['modified'].strftime('%B %d, %Y at %I:%M %p')}")

                # Compare with model creation time
                try:
                    model_dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    if nb['modified'] < model_dt:
                        print(f"   ✅ Modified BEFORE model creation")
                        print(f"   → LIKELY USED to create current model")
                    else:
                        print(f"   ℹ️  Modified AFTER model creation")
                        print(f"   → This is a newer version")
                except:
                    pass
                print()
        else:
            print("   ❌ No .ipynb files found")
    except Exception as e:
        print(f"   Error: {e}")

    print("\n" + "=" * 60)
    print("💡 Tips:")
    print("=" * 60)
    print("• The model was created on:", created[:10])
    print("• Compare this date with your notebook modification dates")
    print("• The notebook modified BEFORE this date was likely used")
    print("\n• To use a different notebook:")
    print("  1. Open the desired .ipynb file in Colab")
    print("  2. Run all training cells")
    print("  3. Export artifacts (run the download cell)")
    print("  4. Replace files in ml_service/artifacts/")

else:
    print("\n❌ ERROR: meta.json not found!")
    print(f"Expected location: {META_PATH}")

print("\n" + "=" * 60)
