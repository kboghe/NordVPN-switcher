from nordvpn_switch import initialize_VPN,rotate_VPN,terminate_VPN


###########
instructions = initialize_VPN()

for i in range(2):
    print("\n\nBasic rotation #"+str(i+1)+
          "\n__________________________")
    rotate_VPN(instructions)
terminate_VPN()

for i in range(2):
    print("\n\nRotation with captcha-check #" + str(i + 1) +
          "\n__________________________")
    rotate_VPN(instructions,google_check=1)
terminate_VPN()

# Option 2:
#(only relevant for Linux machines who wish to execute additional settings#

initialize_VPN(save=1)
initialize_VPN(stored_settings=1)
rotate_VPN()

############
initialize_VPN(save=1)
rotate_VPN()
terminate_VPN()

############
rotate_VPN()
terminate_VPN()
