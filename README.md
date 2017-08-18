# Using Load Balancing Policy to Mitigate DDoS attacks in SDN networks

"This is the source code of the Project"

# This is based on chris-mods-mooc package, I have added some fuctions like Zombie area, security alarming to mitigate and detect the attacks in SDN network
# the topology that have used in this package is a fat tree topology with zombie area and testing server.

"How to start"
#After downloading the package, start cloudnetmooc on VirtualBox
put mooc as user name and password
type startx to start GUI package

"open Two terminals and go to the following folders"
$ cd Hmza_chris_mod_mooc/cloudnetmooc
$ cd Hmza_chris_mod_mooc/cloudnetmooc/minidc/controller

"Now Firstly start building the topology by typing  the following code :"
$ Hmza_chris_mod_mooc/cloudnetmooc# sudo ./mdc --ddos

"secondaly, start Ryu controller by typing  the following code :"
$  Hmza_chris_mod_mooc/cloudnetmooc/minidc/controller# ryu-manager controller

"then the test procedure will be started by checking Static policy first with three load levels and then load balancing policy"

"at the end of test procedure, an HTML file will be created to show the differenced between both policies in terms of drpped_packets, response_time, throughput"

"Hamza"
