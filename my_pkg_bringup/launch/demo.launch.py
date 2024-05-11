#!/usr/bin/env python3
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    gui_node = Node(
        package="my_py_pkg",
        executable="py_gui_node",
    )
    control_node = Node(
        package="my_py_pkg",
        executable="py_control_node",
    )
   
    ld.add_action(control_node)
    ld.add_action(gui_node)

    return ld
