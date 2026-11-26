"""Texts From Your Future Self -- make.fun entry (program/v1).

Writes a single text message from the entrant's future self to
/output/entry.txt: 122 characters, UTF-8, one line, no trailing newline.

The joke: future-you urgently warns present-you to delete a tweet --
not the mean one, the boring one -- because that is the one they read
out at your funeral. The misdirection (mean vs. boring) is the twist,
and the funeral detail is what makes the warning feel like it comes
from someone who has already seen how the story ends. It needs no
setup, no context, and no second read: the whole joke arrives inside
the text itself, in the voice of a future self who is embarrassed on
your behalf.

Standard library only. No network, no local imports, no reads or
writes outside the harness output directory. Deterministic: the same
bytes on every run.
"""

import os
import sys

TEXT = (
    "Hey, it's you from 2042. Delete that tweet. "
    "Not the mean one \u2014 the boring one. "
    "It's the one they read out at your funeral."
)


def fail(message):
    sys.exit("entry rejected: " + message)


def check(text):
    if not isinstance(text, str):
        fail("entry is not text")
    if not text.strip():
        fail("entry is blank")
    if text != text.strip():
        fail("entry has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        fail("entry must be a single line")
    if not 1 <= len(text) <= 200:
        fail("entry must be 1-200 characters, got %d" % len(text))
    if "  " in text:
        fail("entry contains a double space")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        fail("entry contains a control character")
    non_ascii = sorted({ch for ch in text if ord(ch) > 127})
    if non_ascii != ["\u2014"]:
        # The em dash is the entry's only non-ASCII character, on
        # purpose: any other one would mean the line drifted from
        # the text the joke was written in.
        fail("entry has unexpected non-ASCII characters: %r" % non_ascii)
    if "2042" not in text or "funeral" not in text:
        fail("entry lost its future-self punchline")
    try:
        return text.encode("utf-8")
    except UnicodeEncodeError:
        fail("entry is not UTF-8 encodable")


def main():
    data = check(TEXT)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as handle:
        handle.write(data)
    with open(path, "rb") as handle:
        written = handle.read()
    if written != data:
        fail("entry.txt does not match the entry text")
    print("wrote %s (%d chars, %d bytes)" % (path, len(TEXT), len(data)))


if __name__ == "__main__":
    main()
