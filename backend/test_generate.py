#!/usr/bin/env python
"""Quick test of music generation"""

import sys
import traceback

try:
    print("=" * 60)
    print("Testing Music Generator...")
    print("=" * 60)
    
    from music_generator import get_generator
    
    print("✅ Import successful")
    
    gen = get_generator()
    print("✅ Generator initialized")
    print(f"   Generator object: {gen}")
    
    print("\n🎵 Attempting to generate music...")
    file_path, metadata = gen.generate_music('electronic')
    
    print("✅ Music generated successfully!")
    print(f"   File: {metadata['filename']}")
    print(f"   Genre: {metadata['genre']}")
    print(f"   Size: {metadata['file_size']} bytes")
    print(f"   Path: {file_path}")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)
