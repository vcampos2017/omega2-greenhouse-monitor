from OmegaExpansion import oledExp
from OmegaExpansion import onionI2C

import time

HIH7130_ADDR = 0x27
READ_REG = 0x00

def read_hih7130(i2c):
    data = i2c.readBytes(HIH7130_ADDR, READ_REG, 4)

    # Humidity: 14-bit
    humidity = ((((data[0] & 0x3F) << 8) + data[1]) * 100.0) / 16383.0

    # Temp: 14-bit (top 14 bits of bytes 2/3)
    temp_raw = ((data[2] << 8) + (data[3] & 0xFC)) >> 2
    cTemp = (temp_raw / 16384.0) * 165.0 - 40.0
    fTemp = cTemp * 1.8 + 32.0

    return humidity, cTemp, fTemp

def oled_write(line, text):
    oledExp.setCursor(line, 0)
    oledExp.write(text[:20])  # OLED is narrow; trim for safety

def main():
    oledExp.driverInit()

    i2c = onionI2C.OnionI2C(0)
    i2c.setVerbosity(0)

    while True:
        try:
            humidity, cTemp, fTemp = read_hih7130(i2c)

            now = time.strftime("%H:%M:%S")
            oled_write(0, now)
            oled_write(1, "RH: %5.2f%%" % humidity)
            oled_write(2, "Temp: %5.2f C" % cTemp)
            oled_write(3, "Temp: %5.2f F" % fTemp)

            print(now, "RH=%.2f%%" % humidity, "C=%.2f" % cTemp, "F=%.2f" % fTemp)

        except Exception as e:
            # Keep running; show error briefly
            oled_write(0, time.strftime("%H:%M:%S"))
            oled_write(1, "I2C read error")
            oled_write(2, str(e)[:20])
            print("ERROR:", e)

        time.sleep(5)

if __name__ == "__main__":
    main()