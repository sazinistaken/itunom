import math
import threading
import time
import queue

DEGREE_SYMBOL = '\u00B0'

# Global queue for storing vehicle position
position_queue = queue.Queue()

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


# Send current position to the queue
    def get_position(self):
        position = self.name, self.x, self.y, self.velocity, self.direction, self.altidute
        position_queue.put(position)
    

class Quadcopter(Vehicle):
    def  __init__(self,name, x, y, velocity, direction, altitude):
        super().__init__(name, x, y, velocity, direction, altitude)

    

class Drone(Vehicle):
    def __init__(self, name, x, y, velocity, direction, altitude):
        super().__init__(name, x, y, velocity, direction, altitude)


# Thread that updates vehicle's position
class VehicleThread(threading.Thread):
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

class PositionLogThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running =  True

    def run(self):
        while self.running:
            try:
                position = position_queue.get(timeout=1.0)
                print(f"[{position[0]}] Position: ({position[1],position[2]}), Velocity: {position[3]}, Direction: {position[4]}{DEGREE_SYMBOL}, Altidute: {position[5]}")
                position_queue.task_done()
            except queue.Empty:
                continue

    def stop(self):
        self.running = False


def main():
    quadcopter = Quadcopter("Quadcopter", 0, 0, 10, 90, 100)
    quadcopter_thread = VehicleThread(quadcopter)

    drone = Drone("Drone", 0, 5, 20, 180, 100)
    drone_thread = VehicleThread(drone)

    log_thread =  PositionLogThread()

    quadcopter_thread.start()
    drone_thread.start()
    log_thread.start()

# Let threads run for 5 sec
    time.sleep(5.0)

    quadcopter_thread.stop()
    drone_thread.stop()
    log_thread.stop()

    quadcopter_thread.join()
    drone_thread.join()
    log_thread.join()

if __name__ == "__main__":
    main()