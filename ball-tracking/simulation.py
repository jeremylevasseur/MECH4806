import time
import csv
import numpy as np
import matplotlib.pyplot as plt
from simple_pid import PID
from pprint import pprint
from utility_functions import printProgressBar

kp = 10
ki = 0.005
kd = 7

pidX = PID(kp, ki, kd)
pidY = PID(kp, ki, kd)

# Setting setpoint
pidX.setpoint = 0
pidY.setpoint = 0

# Setting sample time
pidX.sample_time = 0.01
pidY.sample_time = 0.01

# Setting PID output limits
pidX.output_limits = (-90, 90)
pidY.output_limits = (-90, 90)


# Reading distance data from the CSV file that was 
# generated from the tracking script
with open('./distance_data.csv', "rt", encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',')
    csvData = list(reader)


timeData = []
pidXOutputData = []
pidYOutputData = []

samplesTaken = 0

printProgressBar(samplesTaken, len(csvData), prefix='Progress:', suffix='Complete', length=50)
for i in range(len(csvData)):
    # X distance measurement
    xDistanceMeasurement = float(csvData[i][0])

    # Y distance measurement
    yDistanceMeasurement = float(csvData[i][1])

    # PID X output
    pidXOutput = pidX(xDistanceMeasurement)

    # PID Y output
    pidYOutput = pidY(yDistanceMeasurement)

    # Adding PID outputs to data lists
    pidXOutputData.append(pidXOutput)
    pidYOutputData.append(pidYOutput)
    
    # Adding time to list
    timeData.append(samplesTaken*0.1)

    samplesTaken += 1

    printProgressBar(samplesTaken, len(csvData), prefix='Progress:', suffix='Complete', length=50)

    time.sleep(0.1)

# Plotting data
fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle('PID Outputs')

ax1.plot(timeData, pidXOutputData, 'o-')
ax1.set_ylabel('PID X Output')

ax2.plot(timeData, pidYOutputData, 'o-')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('PID X Output')

plt.show()