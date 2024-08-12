import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from tf2_ros import TransformListener, Buffer
from rclpy.qos import QoSProfile
import math

class Follower(Node):
    def __init__(self):
        super().__init__('follower')
        qos = QoSProfile(depth=10)
        self.publisher_ = self.create_publisher(Twist, 'leo2/cmd_vel', qos)
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.timer = self.create_timer(0.1, self.follow_leo1)
        self.declare_parameter('target_frame', 'base_link')

    def follow_leo1(self):
        try:
            now = rclpy.time.Time()
            trans = self.tf_buffer.lookup_transform(
                'leo2/base_footprint',  # Source frame
                self.get_parameter('target_frame').get_parameter_value().string_value,  # Target frame
                now)
            
            # Fill in the blanks here
            x = trans.transform.translation.x
            y = trans.transform.translation.y
            distance = math.sqrt(x**2 + y**2)
            
            # Proportional control for following
            msg = Twist()
            if distance > 0.5:  # Threshold to start/stop moving
                msg.linear.x = 0.5 * distance
                angle_to_goal = math.atan2(y, x)
                msg.angular.z = 2.0 * angle_to_goal

            self.publisher_.publish(msg)

        except Exception as e:
            self.get_logger().info('Could not transform: {}'.format(e))

def main(args=None):
    rclpy.init(args=args)
    node = Follower()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
