from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='leo_navigation',
            executable='object_detection_node',
            name='object_detection_node',
            output='screen'
        ),
        Node(
            package='leo_navigation',
            executable='static_tf_publisher',
            name='static_tf_publisher',
            output='screen'
        ),
        Node(
            package='rtabmap_livox',
            executable='rtabmap_livox',
            name='rtabmap_livox',
            output='screen'
        ),
        Node(
            package='leo_gz_bringup',
            executable='leo_gz',
            name='leo_gz',
            output='screen',
            parameters=[{'sim_world': '~/ros2_ws/src/leo_simulator-ros2/leo_gz_worlds/worlds/lunalab2024.sdf'}]
        )
    ])
