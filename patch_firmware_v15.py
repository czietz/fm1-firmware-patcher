#!/usr/bin/env python3
"""Patch the FM-1 V15 firmware file to fix detuning and remove aftertouch."""

import argparse
import hashlib
import sys
from pathlib import Path


ORIGINAL_FIRMWARE_VERSION = "V15"
EXPECTED_INPUT_SHA256 = (
    "DB1642B2B6FA5C2CCCB11FFD13878068BB28601678D3644049F99DC40E7EDB8A"
)
EXPECTED_OUTPUT_SHA256 = (
    "4638959B842A3318CD161F7D2A3964ADD52428DC93C26B1471944CDFC4FE3FAE"
)

# Each tuple contains: file offset, bytes expected in the original, replacement bytes.
PATCHES = (
    (0, bytes.fromhex("a27b2f0c"), bytes.fromhex("48003f69")),
    (69, bytes.fromhex("3ba5"), bytes.fromhex("71b8")),
    (17428, bytes.fromhex("68e0e70f"), bytes.fromhex("5c07718a")),
    (17460, bytes.fromhex("7f8416e1"), bytes.fromhex("a85efa95")),
    (36866, bytes.fromhex("4f8d"), bytes.fromhex("f2c5")),
    (149344, bytes.fromhex("97c9d896"), bytes.fromhex("25480097")),
    (160538, bytes.fromhex("bb49"), bytes.fromhex("44a6")),
    (173608, bytes.fromhex("cf5c"), bytes.fromhex("f74b")),
)


def sha256(data: bytes) -> str:
    """Return the uppercase SHA-256 digest of data."""
    return hashlib.sha256(data).hexdigest().upper()


def apply_patches(data: bytes) -> bytes:
    """Apply all patches after verifying their original bytes are present."""
    patched = bytearray(data)
    for offset, original, replacement in PATCHES:
        end = offset + len(original)
        if end > len(patched) or patched[offset:end] != original:
            raise ValueError(
                "unexpected bytes at offset "
                f"0x{offset:X}: expected {original.hex()}, "
                f"found {bytes(patched[offset:end]).hex()}"
            )
        patched[offset:end] = replacement
    return bytes(patched)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Apply the FM-1 oscillator detune and the 'no aftertouch' fixes to the "
            "original FM-1.fwsc V15 firmware file."
        ),
        epilog=(
            f"The input file must be the original FM-1 {ORIGINAL_FIRMWARE_VERSION} "
            "firmware image."
        ),
    )
    parser.add_argument(
        "input",
        type=Path,
        help=f"original FM-1.fwsc {ORIGINAL_FIRMWARE_VERSION} firmware file",
    )
    parser.add_argument("output", type=Path, help="patched output file")
    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit()
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        input_data = args.input.read_bytes()
    except OSError as exc:
        print(f"error: cannot read input file {args.input}: {exc}", file=sys.stderr)
        return 1

    input_digest = sha256(input_data)
    if input_digest != EXPECTED_INPUT_SHA256:
        print(
            f"error: input file hash mismatch\n"
            f"expected: {EXPECTED_INPUT_SHA256}\n"
            f"found:    {input_digest}",
            file=sys.stderr,
        )
        return 1

    try:
        output_data = apply_patches(input_data)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    output_digest = sha256(output_data)
    if output_digest != EXPECTED_OUTPUT_SHA256:
        print(
            f"error: patched output hash mismatch\n"
            f"expected: {EXPECTED_OUTPUT_SHA256}\n"
            f"found:    {output_digest}",
            file=sys.stderr,
        )
        return 1

    try:
        args.output.write_bytes(output_data)
    except OSError as exc:
        print(f"error: cannot write output file {args.output}: {exc}", file=sys.stderr)
        return 1

    print(f"wrote patched firmware to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
