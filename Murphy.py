import adafruit_servokit
import sys

class Murphy:
    def __init__(self):
        self._legs  = {
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
        self._kit   = adafruit_servokit.ServoKit(
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

    def _validateInstructions(self, instructions) -> None:
        for legName, joints in instructions.items():
            if legName not in self._legs:
                raise ValueError(
                    f"! ERROR: instruction contains invalid leg: {legName}"
                )
            for jointName, angle in joints.items():
                if jointName not in self._legs[legName]:
                    raise ValueError(
                        f"! ERROR: instruction contains invalid joint: ({legName}, {jointName})"
                    )
                if not 0 <= angle <= 180:
                    raise ValueError(
                        f"! ERROR: an attempt was made to instruct ({legName}, {jointName}) to an invalid angle {angle}"
                    )

    def actuate(self, instructions) -> None:
        try:
            self._validateInstructions(instructions)
        except ValueError as error:
            self.shutdown(exitCode = 1)
            # maybe make a logger class in Auxiliaries.py and save it to a log.txt

        for legName, joints in instructions.items():
            for jointName, angle in joints.items():
                self._kit.servo[legName][jointName]["servoAngle"] = angle
                self._kit.servo[self._legs[legName][jointName]["pinNumber"]].angle = angle

    def shutdown(self, exitCode = 0) -> None:
        self.lay()
        sys.exit(exitCode)

    def stand(self) -> None:
        self._state = "NOT_TELEOPERATED"
        self.actuate(
            instructions = {
                "frontLeft"  : {"hip" : 90, "upperLeg" : 90, "lowerLeg" : 90},
                "frontRight" : {"hip" : 90, "upperLeg" : 90, "lowerLeg" : 90},
                "backLeft"   : {"hip" : 0, "upperLeg"  : 0, "lowerLeg"  : 0},
                "backRight"  : {"hip" : 0, "upperLeg"  : 0, "lowerLeg"  : 0}
            }
        )

    def sit(self) -> None:
        self._state = "NOT_TELEOPERATED"
        self.actuate(
            instructions = {
                "frontLeft"  : {"hip" : 0, "upperLeg" : 0, "lowerLeg" : 90},
                "frontRight" : {"hip" : 0, "upperLeg" : 0, "lowerLeg" : 90},
                "backLeft"   : {"hip" : 0, "upperLeg" : 0, "lowerLeg" : 90},
                "backRight"  : {"hip" : 0, "upperLeg" : 0, "lowerLeg" : 90}
            }
        )

    def lay(self) -> None:
        self._state = "NOT_TELEOPERATED"
        self.actuate(
            instructions = {
                "frontLeft"  : {"hip" : 90, "upperLeg" : 90, "lowerLeg" : 90},
                "frontRight" : {"hip" : 90, "upperLeg" : 90, "lowerLeg" : 90},
                "backLeft"   : {"hip" : 90, "upperLeg" : 90, "lowerLeg" : 90},
                "backRight"  : {"hip" : 0, "upperLeg"  : 0, "lowerLeg" : 0}
            }
        )

