# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CircuitPython firmware for an Adafruit Feather RP2040 RFM95 soil sensor node. The device wakes from deep sleep every hour, reads soil moisture/temperature via I2C (Adafruit Seesaw), checks battery voltage, and transmits a msgpack-encoded payload over LoRa (RFM9x) with ACK. It then returns to deep sleep.

## Hardware

- Adafruit Feather RP2040 RFM95 (board: `adafruit_feather_rp2040_rfm9x`)
- Adafruit I2C Soil Moisture Sensor (Seesaw, addr `0x36`, STEMMA QT)
- 3.7V 2000mAh Li-ion battery + solar charging

## Deployment

There is no build step. Deploy by copying files to the `CIRCUITPY` USB drive that appears when the board is connected. CircuitPython automatically runs `code.py` on boot.

```bash
# Copy everything to the device (adjust /media/... to your mount point)
cp code.py /media/$USER/CIRCUITPY/
cp -r lib/ /media/$USER/CIRCUITPY/
cp settings.toml /media/$USER/CIRCUITPY/
```

`.mpy` files (`lib/seesaw.mpy`, `lib/adafruit_bus_device/*.mpy`) are pre-compiled CircuitPython bytecode — do not convert these to `.py`.

## Configuration

Runtime config lives in `settings.toml` (on the device root). Access via `os.getenv()`:

```toml
DEVICE_NUM = 1
```

`settings.toml` should not be committed — keep a `settings.toml.example` instead.

## Development Environment

`uv` manages dev-only Python dependencies (type stubs for IDE support — nothing runs on the desktop):

```bash
uv sync
```

## Architecture

**`code.py`** — entry point. Orchestrates the wake → check battery → read sensor → transmit → sleep cycle.

**`lib/battery_monitor.py`** — reads battery voltage from analog pin A3 (voltage divider, 0–3.3V scaled ×2). Blinks the D13 LED to signal charge state (1 blink = full, 2 = mid, 3 = low). Triggers deep sleep on low battery.

**`lib/lora_sender.py`** — wraps `adafruit_rfm9x`. Initializes the RFM9x over SPI using board pins `RFM_CS`/`RFM_RST`. Serializes the payload dict (plus `device_num`) with msgpack and calls `send_with_ack()`. LoRa config: 915 MHz, SF7, BW 125 kHz, CR 4/5, CRC on, 3 ACK retries.

**`lib/seesaw.mpy`** — Adafruit Seesaw library (I2C soil moisture + temperature).

**Data shape sent over LoRa:**
```python
{"device_num": int, "data": {"soil": float, "temp": float, "battery": float}}
```
