from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    return LaunchDescription([

        Node(
            package='robot_bringup',
            executable='hello_robot',
            output='screen'
        ),

        Node(
            package='robot_bringup',
            executable='status_listener',
            output='screen'
        ),

    ])