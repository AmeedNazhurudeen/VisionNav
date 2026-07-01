import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # ================= WORLD =================
    world_path = os.path.join(
        get_package_share_directory('robot_simulation'),
        'worlds',
        'warehouse.world'
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            )
        ),
        launch_arguments={'world': world_path}.items()
    )

    # ================= ROBOT DESCRIPTION =================
    robot_desc_pkg = get_package_share_directory('robot_description')

    urdf_path = os.path.join(robot_desc_pkg, 'urdf', 'visionnav_robot.urdf')

    diff_drive_config_path = os.path.join(
        get_package_share_directory('robot_simulation'),
        'config',
        'diff_drive.yaml'
    )

    with open(urdf_path, 'r') as f:
        robot_description = f.read().replace(
            'ROBOT_SIMULATION_DIFF_DRIVE_CONFIG_PATH',
            diff_drive_config_path
        )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description
        }],
        output='screen'
    )

    # ================= SPAWN ROBOT =================
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'visionnav_robot'
        ],
        output='screen'
    )

    # ================= CONTROLLER SPAWN (IMPORTANT FIX) =================
    diff_drive_spawner = TimerAction(
        period=6.0,   # WAIT until robot fully exists
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=[
                    'diff_drive_controller',
                    '--controller-manager',
                    '/controller_manager'
                ],
                output='screen'
            )
        ]
    )

    # ================= LAUNCH ORDER =================
    return LaunchDescription([

        gazebo,

        robot_state_publisher,

        # wait before spawning robot
        TimerAction(
            period=2.0,
            actions=[spawn_robot]
        ),

        # wait before spawning controller
        diff_drive_spawner

    ])