#!/usr/bin/env python3
"""
Day 0 Spike Test: Text Injection with ydotool

Tests text injection strategies in different applications:
- Simple typing
- Special characters
- Replace selected text
- Speed tests
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from swara_core import inject_text, Context, get_logger
import time

logger = get_logger("test_injection")


def test_simple_typing():
    """Test simple text typing"""
    print("\n" + "=" * 60)
    print("SIMPLE TYPING TEST")
    print("=" * 60)
    print("\nThis will type: 'Hello from Swara!'")
    print("Make sure you have a text field focused.")
    print("Starting in 5 seconds...")
    time.sleep(5)

    test_text = "Hello from Swara!"
    print(f"\nTyping: {test_text}")

    start = time.time()
    success = inject_text(test_text)
    elapsed = (time.time() - start) * 1000

    if success:
        print(f"✓ Typed successfully in {elapsed:.2f}ms")
    else:
        print(f"✗ Typing failed")


def test_special_characters():
    """Test special characters and punctuation"""
    print("\n" + "=" * 60)
    print("SPECIAL CHARACTERS TEST")
    print("=" * 60)

    test_cases = [
        "Test with punctuation: Hello, World!",
        "Test with quotes: \"Hello\" and 'World'",
        "Test with symbols: $100 @user #hashtag",
        "Test with newline:\nSecond line here",
    ]

    for i, test_text in enumerate(test_cases, 1):
        print(f"\nTest {i}/{len(test_cases)}")
        print(f"Text: {repr(test_text)}")
        print("Focus a text field and press Enter...")
        input()

        success = inject_text(test_text)

        if success:
            print("✓ Typed successfully")
        else:
            print("✗ Typing failed")

        time.sleep(1)


def test_selection_replacement():
    """Test replacing selected text"""
    print("\n" + "=" * 60)
    print("SELECTION REPLACEMENT TEST")
    print("=" * 60)
    print("\nInstructions:")
    print("1. Type some text: 'original text'")
    print("2. Select ALL of that text")
    print("3. Press Enter")
    print("4. The selected text should be replaced")
    print("\nPress Enter when ready...")
    input()

    # Create context with selection
    context = Context(
        selected_text="original text", selection_length=13, active_window="test"
    )

    replacement = "REPLACED TEXT"
    print(f"\nReplacing with: {replacement}")
    print("(Your selected text should be replaced)")

    time.sleep(2)
    success = inject_text(replacement, context)

    if success:
        print("✓ Replacement attempted")
        print("Check if the text was actually replaced correctly")
    else:
        print("✗ Replacement failed")


def test_speed():
    """Test typing speed"""
    print("\n" + "=" * 60)
    print("TYPING SPEED TEST")
    print("=" * 60)

    test_lengths = [10, 50, 100, 200]

    for length in test_lengths:
        test_text = "a" * length
        print(f"\nTyping {length} characters...")
        print("Focus a text field and press Enter...")
        input()

        start = time.time()
        success = inject_text(test_text)
        elapsed = (time.time() - start) * 1000

        if success:
            chars_per_sec = length / (elapsed / 1000)
            print(
                f"✓ {length} chars in {elapsed:.2f}ms ({chars_per_sec:.0f} chars/sec)"
            )
        else:
            print(f"✗ Failed")

        time.sleep(1)


def test_apps():
    """Test in different applications"""
    print("\n" + "=" * 60)
    print("APPLICATION-SPECIFIC TESTS")
    print("=" * 60)

    apps_to_test = [
        ("Brave Browser", "Open a text field in browser"),
        ("VSCode", "Open an empty file"),
        ("Ghostty Terminal", "Open terminal"),
    ]

    test_text = "Testing in this app!"

    for app_name, instruction in apps_to_test:
        print(f"\n--- Testing {app_name} ---")
        print(instruction)
        print(f"Will type: {test_text}")
        print("Press Enter when ready...")
        input()

        success = inject_text(test_text)

        if success:
            print(f"✓ Typing succeeded")
        else:
            print(f"✗ Typing failed")

        time.sleep(1)


def main():
    print("\n" + "=" * 60)
    print("SWARA - TEXT INJECTION SPIKE TEST")
    print("=" * 60)

    print("\nThis test will verify that text injection works correctly")
    print("with ydotool in different scenarios.\n")

    print("IMPORTANT: Make sure ydotool is installed and you are")
    print("in the 'input' group. Restart your session if you just")
    print("added yourself to the group.\n")

    try:
        test_simple_typing()
        test_special_characters()
        test_selection_replacement()
        test_speed()
        test_apps()

        print("\n" + "=" * 60)
        print("TEST COMPLETE")
        print("=" * 60)
        print("\nResults:")
        print("- Review which tests passed/failed")
        print("- Note any apps that need special handling")
        print("- Verify typing speed is acceptable")
        print()

    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n\nError during test: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
