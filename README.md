# Wii Play Tanks Co-op Mission 12 Mod

This patch modifies the **Tanks! Practice Mod** for the North American revision of *Wii Play* so that the original two-player co-op mode behaves like this:

- Co-op begins normally on Mission 1.
- Choosing **Start over** jumps directly to Mission 12.
- Missions retain the original Wii Play graphics, layouts, enemy placement, and tank behavior.
- Only the original 20 two-player missions are used.

The patch has been tested in Dolphin. A real-Wii test requires an original Wii Play disc, the Homebrew Channel, and Riivolution.

## What this repository contains

- `patch_coop.py` — patches the original Practice Mod module.
- `.gitignore` — prevents disc images and extracted Nintendo files from being committed accidentally.

This repository does **not** contain Wii Play, a disc image, Nintendo assets, a patched `main.dol`, or the original Practice Mod binary.

## Requirements

- Your own original NTSC-U *Wii Play* disc: `RHAE01`, revision 1.
- [Tanks! Practice Mod](https://kataryn.com/tanks-practice-mod/), version 1.0.3.
- Python 3.
- For a real Wii: Homebrew Channel and Riivolution.

## Create the co-op module

1. Download and extract Tanks! Practice Mod 1.0.3.
2. Find this file inside the extracted mod:

   `wiiplay/100_inject_101/modules/m_play.bin`

3. Download `patch_coop.py` from this repository.
4. Open Command Prompt in the folder containing the script and run:

   ```text
   python patch_coop.py "C:\path\to\m_play.bin"
   ```

5. The script creates `m_play.coop.bin` beside the original file.
6. Keep a backup of the original `m_play.bin`.
7. Rename `m_play.coop.bin` to `m_play.bin` and replace the Practice Mod copy with it.

The patcher verifies the exact source-file checksum before making changes. It stops without producing a patch if the wrong version is supplied.

## Install on a real Wii

1. Back up the SD card.
2. Copy the Practice Mod's `riivolution` and `wiiplay` folders to the SD-card root.
3. Merge the folders if they already exist and replace the older Practice Mod files when prompted.
4. Insert the SD card and your original Wii Play disc into the Wii.
5. Start the Homebrew Channel, then launch Riivolution.
6. Enable **Tanks Practice Mod** and select **Launch**.
7. Start a two-player Tanks game. It begins on Mission 1; **Start over** loads Mission 12.

Do not install this as a WAD. It does not need to modify the Wii System Menu.

## Dolphin

Dolphin can run a test image rebuilt from your own disc dump. This repository intentionally does not provide an ISO, WBFS, RVZ, or other game image.

## Compatibility

The patch is designed specifically for:

- Game ID: `RHAE01`
- Region: NTSC-U / USA
- Revision: 1
- Tanks! Practice Mod source module SHA-256:
  `40bf57ebc329951f512369aeabd6c2a127b36febc25f04aca5ea01fed0d3d1d3`

## Credits

- Nintendo created Wii Play and Tanks.
- The mission-selector foundation comes from the Tanks! Practice Mod and its contributors.
- This repository contains only an independently created patching script and documentation.

Wii, Wii Play, and related names are trademarks of Nintendo. This project is unofficial and is not affiliated with or endorsed by Nintendo.
