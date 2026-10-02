import adafruit_servokit
import numpy
import time

class Murphy:
    def __init__(self):
        self._legs = {
            "frontLeft" : {
                "hip"      : {"pinNumber" : 8, "servoAngle"  : 0, "phase" : 0},
                "upperLeg" : {"pinNumber" : 9, "servoAngle"  : 0, "phase" : 0},
                "lowerLeg" : {"pinNumber" : 10, "servoAngle" : 0, "phase" : 0}
            },
            "frontRight" : {
                "hip"      : {"pinNumber" : 12, "servoAngle" : 0, "phase" : 0},
                "upperLeg" : {"pinNumber" : 13, "servoAngle" : 0, "phase" : 0},
                "lowerLeg" : {"pinNumber" : 14, "servoAngle" : 0, "phase" : 0}
            },
            "backLeft" : {
                "hip"      : {"pinNumber" : 0, "servoAngle" : 0, "phase" : 0},
                "upperLeg" : {"pinNumber" : 1, "servoAngle" : 0, "phase" : 0},
                "lowerLeg" : {"pinNumber" : 2, "servoAngle" : 0, "phase" : 0}
            },
            "backRight" : {
                "hip"      : {"pinNumber" : 4, "servoAngle" : 0, "phase" : 0},
                "upperLeg" : {"pinNumber" : 5, "servoAngle" : 0, "phase" : 0},
                "lowerLeg" : {"pinNumber" : 6, "servoAngle" : 0, "phase" : 0}
            }
        }
        self._state = None

        self._kit = adafruit_servokit.ServoKit(
            channels = 16
        )

    def _initServos(self) -> None:
        for leg in self._legs.values():
            for joint in leg.values():
                self._kit.servo[joint["pinNumber"]].actuation_range = 180
                self._kit.servo[joint["pinNumber"]].set_pulse_width_range(
                    min_pulse = 500,
                    max_pulse = 2500,
                )

