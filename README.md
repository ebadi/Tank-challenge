# Tank-challenge

Disaster! The evil robot overlords have built an army of attack drones to terrorize the Earth. Humanity's only hope is an ingenious new automated battle tank designed to combat the new threat. After several months of frantic work, the tank's construction has finally been completed. Now all that remains is to program it to take on the robot army. That is where you come in.

The tank and drones move on a two-dimensional grid. Movement on the grid can only be done horizontally and vertically, and only one square at a time. Your job is to program the tank to seek out and destroy as many drones and other targets as possible before its fuel runs out. The exact capabilities of the attack drones are currently not known, but reverse-engineering has shown that they do not appear to be equipped with any ranged weapons and will have to get close to attack.

The tank is equipped with state-of-the-art technology. Its caterpillar tracks allow backward and forward movement, and 90-degree turns to the left and right. It has a forward-facing cannon, ready to fire at any enemy caught in the sights of the tank's highly advanced target identification system. In addition, the tank is equipped with a high-precision lidar system, to measure the distance to objects in its surroundings.

The tank is also equipped with a shield generator, and a low-consumption fuel cell. Moving around and firing the cannon consumes fuel, and being attacked by drones or hitting walls causes the shield generator to drain even more fuel. The lidar and target identification systems are solar powered and do not consume any fuel.

http://honeypot.softwareskills.se
### api.current_fuel() : int
Returns how much fuel the tank has left.
### api.move_forward()
Moves the tank one square forward, consuming 1 fuel. If the tank hits a wall or other obstacle, the shield generator will activate, consuming 10 fuel. The tank can only move, turn, or fire its cannon once per turn.
### api.move_backward()
Moves the tank one square backward, consuming 1 fuel. If the tank hits a wall or other obstacle, the shield generator will activate, consuming 10 fuel. The tank can only move, turn, or fire its cannon once per turn.
### api.turn_left()
Turns the tank 90 degrees to the left, consuming 1 fuel. The tank can only move, turn, or fire its cannon once per turn.
### api.turn_right()
Turns the tank 90 degrees to the right, consuming 1 fuel. The tank can only move, turn, or fire its cannon once per turn.
### api.identify_target()
Returns true if the nearest object in front of the tank is an enemy. Target identification systems does not consume any fuel.
### api.fire_canon()
Fires the tank's cannon, consuming 5 fuel. The shot will hit the closest object in front of the tank on the next turn. The tank must stand still while firing, and can only move, turn, or fire its cannon once per turn.
### api.lidar_front()
Measures the distance in squares to the nearest object in front of the tank. Objects on a square directly adjacent to the tank will have a distance of 1. Lidar systems do not consume any fuel.
### api.lidar_back()
Measures the distance in squares to the nearest object behind the tank. Objects on a square directly adjacent to the tank will have a distance of 1. Lidar systems do not consume any fuel.
### api.lidar_left()
Measures the distance in squares to the nearest object to the left of the tank. Objects on a square directly adjacent to the tank will have a distance of 1. Lidar systems do not consume any fuel.
### api.lidar_right()
Measures the distance in squares to the nearest object to the right of the tank. Objects on a square directly adjacent to the tank will have a distance of 1. Lidar systems do not consume any fuel.


