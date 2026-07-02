# VisionNav — Vision-Driven Autonomous Navigation in ROS 2

> A fully simulated autonomous mobile robot that **adapts its navigation decisions in real time based on what its camera sees** — built on ROS 2 Humble, Gazebo, Nav2, SLAM Toolbox, and OpenCV.

---

## What makes this different

Most ROS 2 projects treat navigation and computer vision as two separate, disconnected systems. **VisionNav bridges them.**

The robot does not just follow a planned path blindly. Its vision pipeline actively feeds into its navigation decisions:

- **Detects objects and hazard zones** from the RGB camera
- **Publishes semantic costmap layers** — detected objects inflate cost in Nav2's costmap in real time
- **Replans dynamically** when the camera sees something the LiDAR didn't catch (e.g. a person, a sign, a restricted zone)

This creates a robot that reasons about *what it sees*, not just *where walls are*.

---

## System architecture

```
[ Gazebo Simulation ]
         │
         ▼
[ Sensors: LiDAR · IMU · Depth · RGB Camera ]
         │
         ▼
[ TF2 + URDF — coordinate frames ]
         │
    ┌────┴────┐
    ▼         ▼
[ Perception ]    [ SLAM ]
  OpenCV           slam_toolbox
  object detect    occupancy map
  costmap layer    localization
    │         │
    └────┬────┘
         ▼
[ Navigation2 ]
  global planner · local planner
  costmap (+ vision layer) · BT navigator
         │
         ▼
[ ros2_control ]
  diff drive controller · cmd_vel
         │
         ▼
[ Robot moves in Gazebo ]
```

---

## Packages

| Package | Role |
|---|---|
| `robot_description` | URDF model, meshes, joint definitions |
| `robot_simulation` | Gazebo world, sensor plugins, spawn scripts |
| `robot_bringup` | Master launch files — single command to start everything |
| `robot_slam` | slam_toolbox config and launch |
| `robot_navigation` | Nav2 params, BT XML, costmap config |
| `robot_control` | ros2_control config, diff drive controller |
| `robot_perception` | OpenCV pipeline, object detection, semantic costmap publisher |
| `robot_tf` | Static transforms, frame definitions |

---

## Sensors

| Sensor | ROS 2 Topic | Purpose |
|---|---|---|
| 2D LiDAR | `/scan` | SLAM + primary obstacle detection |
| IMU | `/imu/data` | Orientation, stability |
| Depth camera | `/depth/points` | 3D perception, close-range obstacles |
| RGB camera | `/camera/image_raw` | Computer vision, object detection |

---

## Innovation: Vision-Aware Costmap

The core innovation lives in `robot_perception`. It runs an OpenCV detection pipeline on the RGB camera feed and publishes a **custom Nav2 costmap layer**:

```
/camera/image_raw  →  [ Perception Node ]  →  /vision_costmap_layer
                                            ↓
                                    Nav2 reads this as
                                    an extra cost layer
                                    and plans around it
```

This means the robot will **replan its path** around detected objects or zones that appear in the camera — even if LiDAR sees them as free space.

---

## Tech stack

- **OS:** Ubuntu 22.04
- **ROS 2:** Humble Hawksbill (LTS)
- **Simulation:** Gazebo Classic
- **Visualization:** RViz2
- **SLAM:** slam_toolbox
- **Navigation:** Nav2
- **Control:** ros2_control + diff_drive_controller
- **Vision:** OpenCV 4, cv_bridge
- **Build:** colcon
- **IDE:** VSCode + ROS extension

---

## Build status

| Phase | Status |
|---|---|
| Week 1 — ROS 2 basics | 🔲 Not started |
| Week 2 — URDF + TF2 | 🔲 Not started |
| Week 3 — Gazebo simulation | 🔲 Not started |
| Week 4 — RViz2 visualization | 🔲 Not started |
| Week 5 — SLAM | 🔲 Not started |
| Week 6 — Navigation2 | 🔲 Not started |
| Week 7 — ros2_control | 🔲 Not started |
| Week 8 — Vision-aware costmap | 🔲 Not started |

---

## Quick start (once fully built)

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/visionnav.git
cd visionnav/ros2_ws

# Install dependencies
rosdep install --from-paths src --ignore-src -r -y

# Build
colcon build --symlink-install
source install/setup.bash

# Launch everything
ros2 launch robot_bringup bringup.launch.py
```

---

## Folder structure

```
visionnav_ws/
├── ros2_ws/
│   └── src/
│       ├── robot_description/
│       ├── robot_simulation/
│       ├── robot_bringup/
│       ├── robot_slam/
│       ├── robot_navigation/
│       ├── robot_control/
│       ├── robot_perception/
│       └── robot_tf/
├── docs/
│   └── images/
├── .github/
│   └── ISSUE_TEMPLATE/
├── .gitignore
└── README.md
```

---

## Author

Built by **Ameed Nazhurudeen** - Robotics Engineer.


