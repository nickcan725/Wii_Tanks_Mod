"""Create the Wii Play Tanks Mission-12 co-op module.

The source file must be m_play.bin from Tanks! Practice Mod 1.0.3.
No Wii Play game data is included with this script.
"""

from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path
from struct import pack, unpack_from

EXPECTED_SHA256 = "40bf57ebc329951f512369aeabd6c2a127b36febc25f04aca5ea01fed0d3d1d3"


def extended_command(kind: int, destination: int, source: int) -> bytes:
    return bytes([kind]) + bytes.fromhex("ff ff fe") + pack(">II", destination, source)


def internal_command(kind: int, destination: int, source: int) -> bytes:
    return bytes([kind]) + destination.to_bytes(3, "big") + pack(">I", source)


def patch_module(source_path: Path, output_path: Path) -> None:
    data = bytearray(source_path.read_bytes())
    actual_hash = sha256(data).hexdigest()
    if actual_hash != EXPECTED_SHA256:
        raise SystemExit(
            "Unsupported m_play.bin.\n"
            f"Expected SHA-256: {EXPECTED_SHA256}\n"
            f"Actual SHA-256:   {actual_hash}"
        )
    if data[:8] != b"Kamek\0\0\2":
        raise SystemExit("The input is not a supported Kamek module.")

    code_size = unpack_from(">I", data, 0x0C)[0]
    if code_size != 0xCCA04:
        raise SystemExit("Unexpected Kamek code size.")
    command_start = 0x20 + code_size

    # Use the original selector's BSS value as a persistent flag.
    # First co-op setup: Mission 1. Later Start over resets: Mission 12.
    selector_offset = 0x570
    selector_flag_offset = 0xCCA18
    selector = bytes.fromhex(
        "3C A0 00 00"  # lis r5, selector_flag@ha
        "38 A5 00 00"  # addi r5, r5, selector_flag@l
        "80 05 00 00"  # lwz r0, 0(r5)
        "2C 00 00 00"  # cmpwi r0, 0
        "40 82 00 14"  # bne already_used
        "38 00 00 01"  # li r0, 1
        "90 05 00 00"  # stw r0, 0(r5)
        "38 80 00 00"  # li r4, 0 (Mission 1)
        "48 00 00 08"  # b store_mission
        "38 80 00 0B"  # already_used: li r4, 11 (Mission 12)
        "90 9E 00 08"  # store_mission: stw r4, 8(r30)
        "38 00 00 13"  # restore the original mission-limit value
        "4E 80 00 20"  # blr
    )
    selector_file_offset = 0x20 + selector_offset
    data[selector_file_offset : selector_file_offset + len(selector)] = selector

    # Remove relocations that would alter the replacement selector and remove
    # the original single-player hook. All unrelated commands remain intact.
    commands = data[command_start:]
    kept = bytearray()
    position = 0
    while position < len(commands):
        beginning = position
        kind = commands[position]
        destination = int.from_bytes(commands[position + 1 : position + 4], "big")
        position += 4
        if destination == 0xFFFFFE:
            destination = int.from_bytes(commands[position : position + 4], "big")
            position += 4
        command_source = int.from_bytes(commands[position : position + 4], "big")
        position += 4
        if kind in (35, 36, 37, 38):
            position += 4
        raw = commands[beginning:position]

        overwrites_selector = selector_offset <= destination < selector_offset + len(selector)
        original_single_player_hook = (
            kind == 65
            and destination == 0x8026549C
            and command_source == selector_offset
        )
        if not overwrites_selector and not original_single_player_hook:
            kept += raw

    data[command_start:] = kept
    data += internal_command(6, selector_offset + 2, selector_flag_offset)
    data += internal_command(4, selector_offset + 6, selector_flag_offset)
    data += extended_command(65, 0x8026552C, selector_offset)
    data += extended_command(32, 0x80265534, 0x809E0008)

    output_path.write_bytes(data)
    print(f"Created: {output_path}")
    print(f"SHA-256: {sha256(data).hexdigest()}")


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Practice Mod 1.0.3 m_play.bin")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output path (default: m_play.coop.bin beside the source)",
    )
    arguments = parser.parse_args()
    output = arguments.output or arguments.source.with_name("m_play.coop.bin")
    patch_module(arguments.source, output)


if __name__ == "__main__":
    main()
