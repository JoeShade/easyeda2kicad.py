# easyeda2kicad Chrome Extension

This extension grabs an LCSC part number from JLCPCB or LCSC product pages and asks a
native host to run `easyeda2kicad` to export the symbol, footprint, and 3D model.

## Setup

1. Build or install `easyeda2kicad` in a Python environment that Chrome can access.
2. Edit `chrome_extension/native-host/com.easyeda2kicad.json`:
   - Replace `path` with the absolute path to `easyeda2kicad/native_host.py`.
   - Replace `__EXTENSION_ID__` with the extension ID after you load it.
3. Install the native host manifest:
   - **macOS**: `~/Library/Application Support/Google/Chrome/NativeMessagingHosts/`
   - **Linux**: `~/.config/google-chrome/NativeMessagingHosts/`
   - **Windows**: see the Chrome Native Messaging documentation (registry entry).
4. Load the extension in Chrome:
   - Visit `chrome://extensions`.
   - Enable **Developer mode**.
   - Click **Load unpacked** and select `chrome_extension/`.

## Usage

1. Open a JLCPCB or LCSC product page.
2. Click the extension action button.
3. The extension will send the LCSC part number to the native host, which runs:
   `python -m easyeda2kicad --lcsc_id=<ID> --full`.

The generated symbol, footprint, and 3D model will be written to the default
`~/Documents/Kicad/easyeda2kicad` output folder unless you change the native host
script to pass `--output`.
