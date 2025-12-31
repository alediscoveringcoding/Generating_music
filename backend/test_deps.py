#!/usr/bin/env python
"""
Test script - verifică dacă toate dependențele necesare sunt instalate
"""

import sys

print("=" * 60)
print("🎵 AI Music Generator - Dependency Check (Python 3.9)")
print("=" * 60)
print(f"Python Version: {sys.version}")
print()

# Test imports
dependencies = {
    "FastAPI": "fastapi",
    "Uvicorn": "uvicorn",
    "TensorFlow": "tensorflow",
    "note-seq": "note_seq",
    "pretty_midi": "pretty_midi",
    "pydantic": "pydantic",
    "numpy": "numpy",
}

print("Checking dependencies...")
print("-" * 60)

all_ok = True
for name, module in dependencies.items():
    try:
        mod = __import__(module)
        version = getattr(mod, '__version__', 'unknown')
        print(f"✅ {name:20} - OK ({version})")
    except ImportError as e:
        print(f"❌ {name:20} - MISSING: {e}")
        all_ok = False

print("-" * 60)

if all_ok:
    print("\n✅ All core dependencies are installed!")
    print("\n📝 To start the server, run:")
    print("   python main.py")
else:
    print("\n❌ Some dependencies are missing. Check errors above.")
    sys.exit(1)
