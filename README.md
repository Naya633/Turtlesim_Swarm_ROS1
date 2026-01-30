# Turtlesim Swarm (ROS1)

This ROS1 project spawns a **swarm of turtles** in the `turtlesim` simulator and makes each turtle move in **synchronized circular paths**. The number of turtles, the radius of the circles, and the spacing between turtles can be configured via ROS parameters.

---

## Project Overview

- **Goal:** Simulate a swarm of turtles moving in circular paths in a synchronized way.
- **Main Features:**
  - Spawns multiple turtles at the center of the map.
  - Each turtle moves on its own circular path with a configurable radius.
  - Synchronized motion achieved by updating positions using trigonometric calculations.
  - Uses ROS parameters to configure:
    - Number of turtles (`num_of_turtles`)
    - Base radius (`radius`)
    - Spacing between each turtle (`spacing`)
  - Default turtle (`turtle1`) is killed to avoid conflicts with new turtles.

---

## ROS Nodes

- **turtle_move.py** – The only node:
  - Spawns the turtles.
  - Subscribes to each turtle's pose (`/turtleX/pose`).
  - Publishes velocities (`/turtleX/cmd_vel`) to move turtles in circular paths.

---

## ROS Parameters (`rosparams.yaml`)

```yaml
num_of_turtles: 3   # number of turtles in the swarm
radius: 2.0         # radius of the first turtle's circular path
spacing: 1.0        # distance between each turtle's path
