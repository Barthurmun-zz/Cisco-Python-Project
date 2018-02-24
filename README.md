# Cisco-Python-Project
The point of it was to create automatically documentation to topology(topology.png) and gain specific information(listed below). Script was tested on Debian 7 and was written in Python 2.6.
In range.txt and password.txt are stored credential to devices which are in this specific network(loggin via SSH, telnet is blocked), only one pair of credential works for each device.

Library used:
- Sys
- Paramiko
- OS
- Time
- Paramiko
- Re

The main points are shown below:
"Minimal requirements what your manager expects:

    He wants to know all available devices in the network. For each device, he wants to know:
        hardware version,
        OS version running on the device,
        management ip address,
        password
        modules which are installed on the device - and status of each module
    He wants to know the topology
    He wants to see the interface description and interface status for each interface on each device.
    The solution should be well documented and anyone should be able to run the solution and get up to date information"
    
    
    Next part will include code based on threads and gaining information by using API.
