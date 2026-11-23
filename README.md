# 🌱 RP2040 Soil Sensor 💧

The RP2040 Soil Sensor is an RFM95 enabled soil sensor package to monitor garden beds temperature and soil moisture. The 
system is powered by a 3.7V 2000mAh lithium-ion battery and can be charged with a solar panel. 

The system is designed to be low power and can run for months on a single charge. The system wakes from low power sleep 
mode every 3 hours to take readings and transmit data to the RFM receiver. Using the RFM95 long range modem provides 
ultra-long range spread spectrum communication and high interference immunity whilst minimizing current consumption.

Because packet size is limited, the system uses MessagePack to encode the data before sending it to the RFM receiver. 
The RFM receiver can then decode the data and relay it to the API server.

This system does not use true LoRaWAN protocols, but instead uses a custom protocol to send data to the RFM receiver. 
The RFM receiver can then relay the data to an API server.

## Hardware

- [Adafruit Feather RP2040 RFM95](https://www.adafruit.com/product/5714)
- [I2C Soil Moisture Sensor](https://www.adafruit.com/product/4026)
- [Lithium-ion Battery -3.7V 2000mAh](https://www.digikey.com/en/products/detail/adafruit-industries-llc/2011/6612469)
- Solar Panel with 5V 3.5W Continuously Charging

## Software

- [CircuitPython 10.2.1](https://circuitpython.org/board/adafruit_feather_rp2040_rfm9x/)

## Packet format

Payloads are msgpack-encoded. The gateway receives and decodes this structure:

```python
import msgpack
from io import BytesIO

msgpack.pack({
    "device_num": 2,          # int — from DEVICE_NUM in settings.toml
    "data": {
        "temp":    77.54,     # float — °F
        "soil":    350,       # int   — raw capacitance count
        "battery": 3.97,      # float — volts
    }
}, stream=BytesIO())
```

## Author

- [Tom Camp](https://github.com/Tom-Camp)

## License

This Project is licensed under the AGPL-3.0 License - see the [LICENSE](LICENSE) file for details.