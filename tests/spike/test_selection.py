#!/usr/bin/env python3
"""
Day 0 Spike Test: Context Capture

Tests context capture in different applications:
- Brave browser
- VSCode
- Ghostty terminal
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from swara_core import capture_context, get_logger
import time

logger = get_logger("test_selection")


def test_selection_capture():
    """Test selection capture"""
    print("\n" + "=" * 60)
    print("SELECTION CAPTURE TEST")
    print("=" * 60)
    print("\nInstructions:")
    print("1. Select some text in any application")
    print("2. Press Enter within 5 seconds")
    print("3. Check if the selection was captured")
    print("\nStarting in 3 seconds...")
    time.sleep(3)

    for i in range(3):
        print(f"\nTest {i + 1}/3")
        print("Select text now and press Enter...")
        input()

        start = time.time()
        context = capture_context()
        elapsed = (time.time() - start) * 1000  # Convert to ms

        print(f"\n  Capture time: {elapsed:.2f}ms")

        if context.selected_text:
            print(f"  ✓ Selection captured: {len(context.selected_text)} chars")
            print(f"  ✓ Active window: {context.active_window}")
            print(f"  ✓ Preview: {context.selected_text[:100]}...")
        else:
            print("  ✗ No selection found")

        print()
        time.sleep(1)


def test_apps():
    """Test selection in different apps"""
    print("\n" + "=" * 60)
    print("APPLICATION-SPECIFIC TESTS")
    print("=" * 60)

    apps_to_test = [
        ("Brave Browser", "Select text in browser (e.g., from a webpage)"),
        ("VSCode", "Select text in code editor"),
        ("Ghostty Terminal", "Select text in terminal"),
    ]

    for app_name, instruction in apps_to_test:
        print(f"\n--- Testing {app_name} ---")
        print(instruction)
        print("Press Enter when ready...")
        input()

        context = capture_context()

        if context.selected_text:
            print(f"✓ Selection captured")
            print(f"  - App detected: {context.active_window}")
            print(f"  - Length: {len(context.selected_text)} chars")
        else:
            print(f"✗ No selection captured")

        print()


def main():
    print("\n" + "=" * 60)
    print("SWARA - CONTEXT CAPTURE SPIKE TEST")
    print("=" * 60)

    print("\nThis test will verify that context capture works correctly")
    print("in different applications.\n")

    try:
        test_selection_capture()
        test_apps()

        print("\n" + "=" * 60)
        print("TEST COMPLETE")
        print("=" * 60)
        print("\nResults:")
        print("- Review the output above")
        print("- Note which apps work well")
        print("- Note which apps need special handling")
        print()

    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n\nError during test: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
