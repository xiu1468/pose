#include "ros/ros.h"
#include "geometry_msgs/PoseStamped.h" 

#include <cmath>

int main(int argc, char **argv)
{
    ros::init(argc, argv, "talker");

    ros::NodeHandle n;

    ros::Publisher chatter_pub = n.advertise<geometry_msgs::PoseStamped>("chatter", 10); 

    ros::Rate loop_rate(5);

    double count;

    ros::param::get("co",count);

    double positionX, positionY, positionZ;
    double orientationX, orientationY, orientationZ, orientationW;

    
    
    orientationX = 0;
    orientationY = 0;
    orientationZ = 0;
    orientationW = 1;

    
    while (ros::ok())
    {
        if (count < 0) {
            positionX = count;
            positionY = count;
            positionZ = 0;

            geometry_msgs::PoseStamped msg;

        
            ros::Time currentTime = ros::Time::now();
            msg.header.stamp = currentTime;

            
            msg.pose.position.x = positionX;
            msg.pose.position.y = positionY;
            msg.pose.position.z = positionY;

            msg.pose.orientation.x = orientationX;
            msg.pose.orientation.y = orientationY;
            msg.pose.orientation.z = orientationZ;
            msg.pose.orientation.w = orientationW;

            
            ROS_INFO("the position(x,y,z) is %f , %f, %f", msg.pose.position.x, msg.pose.position.y, msg.pose.position.z);
            ROS_INFO("the orientation(x,y,z,w) is %f , %f, %f, %f", msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w);
            ROS_INFO("the time we get the pose is %f",  msg.header.stamp.sec + 1e-9*msg.header.stamp.nsec);

            std::cout<<"\n \n"<<std::endl; 

            chatter_pub.publish(msg);

            ros::spinOnce();

            loop_rate.sleep();

            ++count;
        } else{
            positionX = 0;
            positionY = count;
            positionZ = 0;

            geometry_msgs::PoseStamped msg;

        
            ros::Time currentTime = ros::Time::now();
            msg.header.stamp = currentTime;

            
            msg.pose.position.x = positionX;
            msg.pose.position.y = positionY;
            msg.pose.position.z = positionY;

            msg.pose.orientation.x = orientationX;
            msg.pose.orientation.y = orientationY;
            msg.pose.orientation.z = orientationZ;
            msg.pose.orientation.w = orientationW;

            
            ROS_INFO("the position(x,y,z) is %f , %f, %f", msg.pose.position.x, msg.pose.position.y, msg.pose.position.z);
            ROS_INFO("the orientation(x,y,z,w) is %f , %f, %f, %f", msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w);
            ROS_INFO("the time we get the pose is %f",  msg.header.stamp.sec + 1e-9*msg.header.stamp.nsec);

            std::cout<<"\n \n"<<std::endl; 

            chatter_pub.publish(msg);

            ros::spinOnce();

            loop_rate.sleep();

            ++count;
        }
        
    }


  return 0;
}