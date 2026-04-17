import os, subprocess
import psutil

def main():
    osname = os.name
    if(osname == "posix"):
        print("LINUX! :)")
        err, msg = subprocess.getstatusoutput('cat /sys/class/thermal/thermal_zone0/temp')
        temp = int(msg) / 1000
        print(f"Temp: {temp}ºC")
        cpu = psutil.cpu_percent()
        print(f"CPU: {cpu}%")
        temp = psutil.sensors_temperatures()
        print(f"New Temp {temp}")

    elif(osname == "nt"):
        print("WINDOWS :(")

if __name__ == "__main__":
    main()

