# BE-PROJECT
Unmanned Terrestrial Deep Stereo ConvNet Gofer Embedded with CNN Architecture

The proposed project brings to life a robotic gofer with automatic speech recognition and obstacle avoidance mechanism using Deep Stereo ConvNet architecture. It is a cross between a chatbot and an unmanned driverless automobile. The physics, gesticulation, and motion of the designed gofer depends on the depth estimation, path planning, obstacle avoidance and navigation. The gofer chassis is designed using vehicle kinematics for the desired load. The bottom-up approach calculates the motor ratings, and develops the rotary encoder, wheel dimension and battery selection. The course of the gofer is deliberated using an orthogonally controlled differential drive. The microcontroller STM32F446 reads data from various sensors, communicates with ROS running on Raspberry Pi, and controls the two motors. The virtual environment for gofer is imported into a Gazebo world. A particle filtering algorithm is used for optimum tracking, CNN-based identification and control of the gofer. In the virtual environment, the gofer is tested on the realm of the school campus floor with Monte Carlo simulations and upgraded with neural network architecture using stereo images for object detection. The developed mobile application adds to the ease of gofer operation and control. The gofer contributes to the designed system as Merlin at the command of King Arthur.

# Simultaneous Localization And Mapping (SLAM) - Gofer Mapping the environment

![image](https://user-images.githubusercontent.com/64368871/205316344-08190728-30cd-4aad-b76a-72c0d82e48ea.png)

# Final Mapped environment 

![image](https://user-images.githubusercontent.com/64368871/205316442-3c86cf6f-8588-4c13-a453-a36acdf5423a.png)

# Path Planning Algorithm 

Here we have commanded Gofer through speech to send some message to the man (Yogesh) standing. Using Path planning algorithm and the mapped environment Gofer planned a path to reach the destination(Yogesh).

![image](https://user-images.githubusercontent.com/64368871/205316670-471325b1-3f19-4bd8-aad6-4b07183dd444.png)

Here Gofer has reached the destination and sent message to Yogesh.

![image](https://user-images.githubusercontent.com/64368871/205316822-3f8717c8-685c-4c06-bf62-ace7b95c4fc1.png)

On the bottom left we can see the camera view embeded on Gofer for Object Detection using CNN

![image](https://user-images.githubusercontent.com/64368871/205317045-2a639f37-6fbe-4b3c-ab16-c155b851efe4.png)

Below image tests the robot's obstacle avoidance algorithm in extreme conditions for the obstacles not mapped.

![image](https://user-images.githubusercontent.com/64368871/205317213-041597c7-74ed-4807-953f-81ff1366c327.png)

# Our college EXTC Department

The environment is created in Blender and imported into a Gazebo world.

![image](https://user-images.githubusercontent.com/64368871/205317603-56830110-7a3d-4277-9f1f-9e9fb896f1e9.png)


![image](https://user-images.githubusercontent.com/64368871/205317519-d72d3aab-54d2-40e4-b0fa-18f96173fdf9.png)



![image](https://user-images.githubusercontent.com/64368871/205318066-869d7e2c-4627-4f76-8db2-4f77a90fc30b.png)

# Hardware model Bolck Diagram:

![image](https://user-images.githubusercontent.com/64368871/205318727-a04b452a-5372-411e-92fe-b948055179ea.png)



![image](https://user-images.githubusercontent.com/64368871/205318987-20d6191b-74e1-4f27-9d26-591cc33a0b53.png)


