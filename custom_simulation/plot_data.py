import numpy as np
import matplotlib.pyplot as plt


def plotPidOutputAndBallPositionTimeseries(coordinate, time, positionData, pidData):
    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.suptitle(str(coordinate) + ' Coordinate Position And PID Response')

    ax1.plot(time, positionData, '.-')
    ax1.set_ylabel('Ball ' + str(coordinate) + ' Position (m)')

    ax2.plot(time, pidData, '.-')
    ax2.set_ylabel(str(coordinate) + ' PID Output')
    
    ax2.set_xlabel('Time (s)')

    plt.show()

def plotBallPositionTimeseries(coordinate, time, positionData):
    fig, ax = plt.subplots()
    ax.plot(time, positionData)
    ax.set(
        xlabel='Time (s)',
        ylabel='Ball ' + str(coordinate) + ' Position (m)',
        title=str(coordinate) + ' Coordinate Position vs. Time')
    ax.grid()
    fig.savefig(str(coordinate) + "-position-data.png")
    plt.show()