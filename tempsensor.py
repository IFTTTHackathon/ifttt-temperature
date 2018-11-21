import time, sys, requests
# Systempfad zum den Sensor, weitere Systempfade könnten über ein Array
# oder weiteren Variablen hier hinzugefügt werden.
# 28-02161f5a48ee müsst ihr durch die eures Sensors ersetzen!
sensor = '/sys/bus/w1/devices/28-031683884bff/w1_slave'

def readTempSensor(sensorName) :
    """Aus dem Systembus lese ich die Temperatur der DS18B20 aus."""
    f = open(sensorName, 'r')
    lines = f.readlines()
    f.close()
    return lines

def readTempLines(sensorName) :
    lines = readTempSensor(sensorName)
    # Solange nicht die Daten gelesen werden konnten, bin ich hier in einer Endlosschleife
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = readTempSensor(sensorName)
    temperaturStr = lines[1].find('t=')
    # Ich überprüfe ob die Temperatur gefunden wurde.
    if temperaturStr != -1 :
        tempData = lines[1][temperaturStr+2:]
        tempCelsius = float(tempData) / 1000.0
        tempKelvin = 273 + float(tempData) / 1000
        tempFahrenheit = float(tempData) / 1000 * 9.0 / 5.0 + 32.0
        # Rückgabe als Array - [0] tempCelsius => Celsius...
        return [tempCelsius, tempKelvin, tempFahrenheit]

try:
    while True :
        temp = str(readTempLines(sensor)[0])
        # Mit einem Timestamp versehe ich meine Messung und lasse mir diese in der Console ausgeben.
        print("Temperatur um " + time.strftime('%H:%M:%S') +" drinnen: " + temp + " °C")
        payload = {'sender': 'piZero', 'temp': temp, 'time': time.time()}
        r = requests.post("http://httpbin.org/post", data=payload)
        print()
        print(r.text)
        print()
        # Nach 10 Sekunden erfolgt die nächste Messung
        time.sleep(0.5)
except KeyboardInterrupt:
    # Programm wird beendet wenn CTRL+C gedrückt wird.
    print('Temperaturmessung wird beendet')
except Exception as e:
    print(str(e))
    sys.exit(1)
finally:
    # Das Programm wird hier beendet, sodass kein Fehler in die Console geschrieben wird.
    print('Programm wird beendet.')
    sys.exit(0)
