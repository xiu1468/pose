#include "ros/ros.h"
#include "geometry_msgs/PoseStamped.h"

void chatterCallback(const geometry_msgs::PoseStamped::ConstPtr& msg) 
{
    

    double x = msg->pose.position.x;
    double y = msg->pose.position.y;
    double z = msg->pose.position.z;

    
    if (x > 10)
    {
        ROS_INFO("turn left");
    }
    else if (x < -10)
    {
        ROS_INFO("turn right");      //目的地是(0,50),靠近範圍是10
    }
    else if (y > 60)
    {
        ROS_INFO("move backward");
    }
    else if (y < 40)
    {
        ROS_INFO("move forward");
    }
    else 
    {
        ROS_INFO("stop");
    }
    std::cout<<"\n \n"<<std::endl; 
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "listener");

    ros::NodeHandle n;

    ros::Subscriber sub = n.subscribe("chatter", 10, chatterCallback);

    ros::spin();

    return 0;
}
