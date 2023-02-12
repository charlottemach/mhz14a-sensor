#!/usr/bin/env python3
import time
import serial

class CO2Sensor():
  request = [0xff, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79]

  def __init__(self, port='/dev/ttyS0'):
    self.serial = serial.Serial(
        port = port,
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
    )

  def get(self):
    self.serial.write(bytearray(self.request))
    response = self.serial.read(9)
    if len(response) == 9:
      current_time = time.strftime('%H:%M:%S', time.localtime())
      response = bytearray(response)
      return {"time": current_time, "ppa": (response[2] << 8) | response[3], "temp": response[4]}
    return -1

  def get_average(self, duration):
    values = []
    while duration != 0:
      values.append(self.get().get("ppa"))
      duration -= 1
      time.sleep(1)
    return sum(values) // len(values)


def main():
  sensor = CO2Sensor()
  while True:
    #print(sensor.get())
    #time.sleep(10)
    print(sensor.get_average(6))


if __name__ == '__main__':
  main()
