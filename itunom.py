import math
import threading
import time

DEGREE_SYMBOL = '\u00B0'

class Vehicle():
    def __init__(self, name: str, x, y, velocity, direction, altidute=0):
        self.name = name
        self.x = x
        self.y = y
        self.velocity = velocity
        self.direction = direction
        self.altidute = altidute


    def update_position(self, t):

        radian_direciton = math.radians(self.direction)

        self.x = self.x + self.velocity * math.cos(radian_direciton) * t
        self.y = self.y + self.velocity * math.sin(radian_direciton) * t


    def  update_altidute(self, delta_altidute):
        self.altidute += delta_altidute


    def get_position(self):
        print(f"[{self.name}] Position: ({self.x}, {self.y}), Velocity: {self.velocity}, Direction: {self.direction}{DEGREE_SYMBOL}, Altitude: {self.altidute}")
    


class Quadcopter (Vehicle):
    def  __init__(self,name, x, y, velocity, direction, altitude):
        super().__init__(name, x, y, velocity, direction, altitude)

    

class Drone (Vehicle):
    def __init__(self, name, x, y, velocity, direction, altitude):
        super().__init__(name, x, y, velocity, direction, altitude)


class VehicleThread (threading.Thread):
    def __init__(self, vehicle, frequency=1.0):
        super().__init__()
        self.vehicle = vehicle
        self.frequency = frequency
        self.running = True
    
    def run(self):
        while self.running:
            self.vehicle.update_position(self.frequency)
            self.vehicle.get_position()
            time.sleep(self.frequency)

    def stop(self):
        self.running = False


def main():
    quadcopter = Quadcopter("Quadcopter", 0, 0, 10, 90, 100)
    quadcopter_thread = VehicleThread(quadcopter)
    quadcopter_thread.start()

    drone = Drone("Drone", 0, 5, 20, 180, 100)
    drone_thread = VehicleThread(drone)
    drone_thread.start()

    time.sleep(5.0)

    quadcopter_thread.stop()
    drone_thread.stop()
    #quadcopter_thread.join()
    #drone_thread.join()


if __name__ == "__main__":
    main()