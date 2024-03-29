# FW Tool

Tool for unpack, optimize and repack firmware for music
players based on Hiby OS, MTouch and Fiio system (non-Android)

## Supported players:
- AGPTEK Rocker / Benjie T6
- Cayin N3 / N3 Pro
- Cayin N8
- Fiio M3 Pro `(not tested)`
- Fiio M3K `(not tested)`
- Fiio M5 `(not tested)`
- HiBy R2
- HiBy R3 / R3 Pro
- Hidizs AP60 / AP60 II / AP60 Pro
- Hidizs AP80 / AP80 Pro / AP80 Pro X
- Shanling M0 `(not tested)`
- Shanling M1
- Shanling M2s
- Shanling M2x `(not tested)`
- Shanling M3s
- Shanling M5s `(not tested)`
- Tempotec V1 / V1-A
- xDuoo X3 II
- xDuoo X20

## WARNING:
All modifications are use at your own risk. I can't be
sure the modified FW will not brick your device,
especially the players marked as `not tested`.

## NOTE:
First of all you should to choose your player model, path
to `*.upt`, `*.bin` or `*.fw` update file and mode in the
head of program.

## DEPENDENCIES:
- Linux-based system
- Python >= 3.6
- Install modules with bash:
  - sudo apt-get install liblzo2-dev
  - sudo apt-get install optipng
  - sudo apt-get install gcc-mipsel-linux-gnu
  - sudo apt install mtd-utils
  - pip3 install PyQt5
  - pip3 install pycdlib
  - pip3 install python-lzo
  - pip3 install ubi_reader

## Run
run `FW-tool.desktop` file.
