import rospy
from turtlesim.srv import *
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math

rospy.init_node('Swarm_turtles')


class TurtleBot:
	def __init__(self, name ,radius, initial_x=5.544445, initial_y=5.544445,  initial_theta=0.0):
		
		self.name=name
		self.radius=radius
		self.cx=initial_x
		self.cy=initial_y
		self.spawnTurtle(name , initial_x, initial_y,  initial_theta)
		
		self.position=Pose()
		
	
		self.target_x = self.cx + self.radius
		self.target_y = self.cy
		self.start_theta = math.atan2(self.cy - self.target_y, self.cx - self.target_x) + math.pi / 2

		
		self.pose_subscriber = rospy.Subscriber(f'{name}/pose' , Pose,  self.update_pose)

		self.velocity_publisher=rospy.Publisher(f'{name}/cmd_vel', Twist, queue_size=10)	
		self.rate = rospy.Rate(10)
		
		
	def spawnTurtle(self, name , x , y, theta):
		rospy.wait_for_service('spawn')
		server=rospy.ServiceProxy('spawn', Spawn)
		request=server(x, y, theta , name)
	
		
		

	def update_pose(self,data):
		
		self.position= data
		
		
	def steering_angle(self, goal_pose):
		return math.atan2(goal_pose.y - self.position.y, goal_pose.x - self.position.x)
		
		
	def angular_velocity(self, goal_pose, constant=0.6):
		return constant * (self.steering_angle(goal_pose)-self.position.theta)
		

	def linear_velocity(self, goal_pose, constant=0.5):
		return constant * self.euclidean_distance(goal_pose)
		
	def euclidean_distance(self, goal_pose):
		return math.sqrt((goal_pose.x - self.position.x)**2 + (goal_pose.y - self.position.y)**2)
	

	def move_to_goal(self, x, y):
		goal_pose = Pose()
		goal_pose.x = x
		goal_pose.y = y
		tolerance = 0.5
		tolerance_pos=0.01
		tolerance_theta=0.01
		vel = Twist()
		
		K_linear =1.7
		K_angular = 6.2
		dx=x-self.position.x
		dy=y-self.position.y
		
		distance = math.sqrt(dx**2 + dy**2)
		thg = math.atan2(dy, dx)
		dth = thg - self.position.theta
		dth = math.atan2(math.sin(dth), math.cos(dth))  
		
		vel.angular.z = K_angular * dth
		vel.linear.x = K_linear* distance
		
		self.velocity_publisher.publish(vel)
	
	
if __name__ == '__main__' :



	rospy.wait_for_service('kill')
	killer = rospy.ServiceProxy('kill', Kill)
	killer('turtle1')
	rospy.loginfo("Killed default turtle1")
	
	num_of_t=rospy.get_param('~num_of_turtles', 3)

	base_radius = rospy.get_param('~radius', 1.0)
	spacing = rospy.get_param('~spacing', 1.0)
	
	
	
	base_radius=2
	turtles=[]
	R=[]
	
	
	for i  in range(num_of_t+1):
		print (i)
		
		name=f"t{i+1}"
		print (name)
		radius = base_radius + i * spacing
		R.append(radius)
		turtle = TurtleBot(name, radius)
		turtles.append(turtle)
	
	theta=0.0
	dtheta=0.1


	
	rate = rospy.Rate(10)	
	while not rospy.is_shutdown():
		for i, turtle in enumerate(turtles):
			x = turtle.cx + R[i] * math.cos(theta)
			y = turtle.cy + R[i] * math.sin(theta)
			
			turtle.move_to_goal(x, y)
			
		theta += dtheta
		if theta > 2 * math.pi:
			theta -= 2 * math.pi
		rate.sleep()






		
	

