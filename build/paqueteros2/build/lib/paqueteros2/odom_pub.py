import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from math import sin, cos, sqrt, atan2, pi

class SquarePath(Node):

    def __init__(self):
        super().__init__('square_path')
        
        # Publisher for /cmd_vel
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Subscriber for /odom
        self.subscription = self.create_subscription(
            Odometry, 
            '/odom', 
            self.listener_callback, 
            10)
        
        # State variables
        self.current_position = None
        self.current_orientation = None
        self.start_position = None
        self.start_orientation = None
        self.stage = 0
        self.delta = 0.001  # 0.1% difference as error margin
        
        # Timer for controlling the movement
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info('Square path node has been initialized')

    def listener_callback(self, msg):
        self.current_position = msg.pose.pose.position
        self.current_orientation = msg.pose.pose.orientation

        if self.start_position is None:
            self.start_position = self.current_position
            self.start_orientation = self.current_orientation

    def timer_callback(self):
        if self.current_position is None or self.current_orientation is None:
            return

        move_cmd = Twist()
        
        # Movement logic
        if self.stage % 2 == 0:
            # Move forward
            if self.has_reached_distance(1.0):
                self.start_position = self.current_position
                self.stage += 1
                move_cmd.linear.x = 0.0
            else:
                move_cmd.linear.x = 0.2
        else:
            # Rotate 90 degrees
            if self.has_reached_orientation(90.0):
                self.start_orientation = self.current_orientation
                self.stage += 1
                move_cmd.angular.z = 0.0
            else:
                move_cmd.angular.z = 0.2

        self.publisher_.publish(move_cmd)

    def has_reached_distance(self, distance):
        if self.current_position is None or self.start_position is None:
            return False
        
        dx = self.current_position.x - self.start_position.x
        dy = self.current_position.y - self.start_position.y
        distance_moved = sqrt(dx**2 + dy**2)
        
        return distance_moved >= distance - (distance * self.delta)

    def has_reached_orientation(self, angle):
        if self.current_orientation is None or self.start_orientation is None:
            return False
        
        start_yaw = self.euler_from_quaternion(self.start_orientation)
        current_yaw = self.euler_from_quaternion(self.current_orientation)
        angle_moved = abs(current_yaw - start_yaw) * (180.0 / pi)
        
        return angle_moved >= angle - (angle * self.delta)

    def euler_from_quaternion(self, orientation):
        """
        Convert a quaternion into euler angles (yaw only)
        """
        x = orientation.x
        y = orientation.y
        z = orientation.z
        w = orientation.w

        sin_yaw = 2.0 * (w * z + x * y)
        cos_yaw = 1.0 - 2.0 * (y * y + z * z)
        yaw = atan2(sin_yaw, cos_yaw)

        return yaw

def main(args=None):
    rclpy.init(args=args)
    node = SquarePath()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
