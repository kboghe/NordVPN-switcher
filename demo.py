from nordvpn_switch import initialize_VPN,rotate_VPN,terminate_VPN

#OPTION 1: save instructions as a variable and feed it to rotate function#

settings = initialize_VPN()
rotate_VPN(settings)
rotate_VPN(settings,google_check=1) #with google and youtube captcha check
terminate_VPN(settings)

#OPTION 2: save instructions in project folder once and execute initialize and rotate function every time you run script#
#(only relevant for Linux machines who wish to execute additional settings such as enabling killswitch etc.)#

#do this once
initialize_VPN(save=1)
#open project on a later date and just use the following three lines of code:
initialize_VPN(stored_settings=1)
rotate_VPN()
#do stuff
terminate_VPN()

#OPTION 3: save instructions in project folder once and just execute the rotate function#
#(Relevant for all Windows machines or Linux machines who do not wish to execute additional settings)#

#do this once
initialize_VPN(save=1)
#open project on a later date and just use the following two lines of code:
rotate_VPN()
#do stuff
terminate_VPN()

#OPTION 4: create or obtain your own settings_nordvpn.txt file, place it in your project folder and use the rotate function#
#(For example, share particular settings with colleagues/friends who work on the same project by sending them your .txt settings file)#

rotate_VPN()
#do stuff
terminate_VPN()

#additional option:provide the initialize_VPN() function with a list of connection options beforehand#
#e.g. for rotating between 38 servers located in the Netherlands, just feed the function the names of the servers (nl800,nl801,etc.)#
range_servers = range(800,838)
server_list = ["nl"+str(number) for number in range_servers]
instructions = initialize_VPN(area_input=server_list)
rotate_VPN(instructions)
