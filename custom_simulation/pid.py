from simple_pid import PID

class PID_Controller():
    def __init__(self, kp, ki, kd, sampleTime, outputLowerLimit, outputUpperLimit):
        self.pid = PID(kp, ki, kd)
        self.pid.sample_time = sampleTime
        self.pid.output_limits = (int(outputLowerLimit), int(outputUpperLimit))
