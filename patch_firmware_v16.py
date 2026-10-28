#!/usr/bin/env python3
"""Patch the FM-1 V16 firmware file to remove aftertouch."""

import argparse
import hashlib
import sys
from pathlib import Path


ORIGINAL_FIRMWARE_VERSION = "V16"
EXPECTED_INPUT_SHA256 = (
    "D017FB65E70ACA97EE29D944470C3515A74581DF5C0576BF70DE917C7B2B61D5"
)
EXPECTED_OUTPUT_SHA256 = (
    "CC825CAF8CF3214F684533168724EF0D80D85F24216BEFE8F65EA2E865F2CE55"
)

# Each tuple contains: file offset, bytes expected in the original, replacement bytes.
PATCHES = (
    (0, bytes.fromhex("2ca86fc3"), bytes.fromhex("c9dbc783")),
    (69, bytes.fromhex("db47"), bytes.fromhex("2df5")),
    (17428, bytes.fromhex("bec2e07c"), bytes.fromhex("9e5640c1")),
    (17460, bytes.fromhex("6eb917e3"), bytes.fromhex("dcae7ee5")),
    (148306, bytes.fromhex("5618"), bytes.fromhex("a850")),
    (293518, bytes.fromhex("e4"), bytes.fromhex("b5")),
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
            "Apply the 'no aftertouch' fix to the original FM-1.fwsc V16 "
            "firmware file."
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
