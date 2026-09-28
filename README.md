# M-VAVE FM-1 firmware patcher

This script applies multiple changes to the firmware of the M-VAVE FM-1 synthesizer:

* Fixes the [implementation of oscillator detune](https://www.elektronauts.com/t/m-vave-fm-1/252170/191) to match Dexed.
* Removes the reaction to MIDI aftertouch messages – which cause an unexpected strong vibrato.
* Makes the oscilloscope display on the main screen dark blue to make it stand out more.
* Makes the selection cursor on the FX screen green (purely as a visual indicator that custom FW is running).

Usage: `python patch_firmware.py FM-1.fwsc FM-1-fixed.fwsc`

The resulting firmware file `FM-1-fixed.fwsc` must not be distributed, as it is under copyright by M-VAVE.

---

## Disclaimer

**Install at your own risk!**

The firmware is running stable for me. The changes are localized, and don’t modify the size of the firmware, its memory consumption or its processing time. Hence, I consider them quite low risk. The risk is more about the flashing procedure in general (also applies to stock firmware): If the updater or the FM-1 crash during the firmware flashing, recovery could require hardware tools.

---

## Requirements

* Python
* The original **V15** firmware, available under “PC Firmware” on [M-VAVE’s download page](http://www.cuvave.com/download).
* The firmware upgrade utility **M-UPGRADE**, available under “PC Software” on [M-VAVE’s download page](http://www.cuvave.com/download).
* The **V14 firmware upgrade** utility, available under “Major Update” on [M-VAVE’s download page](http://www.cuvave.com/download).

---

## Installation

* Patch the V15 firmware with the Python script: `python patch_firmware.py FM-1.fwsc FM-1-fixed.fwsc`
* M-UPGRADE won’t directly let you upgrade from stock firmware V15 to the changed version, because it thinks both are identical. 
* Thus, use the V14 firmware upgrade utility to downgrade to V14 first.
* Then, use the standalone M-UPGRADE to apply my firmware `FM-1-fixed.fwsc`.
* In case you want to go back to stock V15, you can use the same procedure (downgrade to V14, then upgrade) again.

---

## Thanks

* Kris Naphtali for making me aware of the detune issue and encouraging me along the way.
* Anhang Li for a [partial reverse-engineering of older firmware](https://github.com/AL-255/FM-1-RE/) that served as a good starting point.
* [Andrey Grigoryev](https://github.com/kagaimiq/) for the tools that deal with firmware files for the SoC that M-VAVE uses.
* M-VAVE for making this fun and affordable device.

---

## License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit of the public at large and to the detriment of our heirs and successors. We intend this dedication to be an overt act of relinquishment in perpetuity of all present and future rights to this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>