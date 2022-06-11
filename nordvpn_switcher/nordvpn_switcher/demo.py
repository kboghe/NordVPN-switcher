from nordvpn_switcher import initialize_VPN,rotate_VPN
import time

##############
## WINDOWS ###
##############

# [1] save settings file as a variable

instructions = initialize_VPN() #this will guide you through a step-by-step guide, including a help-menu with connection options

for i in range(3):
    rotate_VPN(instructions) #refer to the instructions variable here
    print('\nDo whatever you want here (e.g.scraping). Pausing for 10 seconds...\n')
    time.sleep(10)

# [2] if you'd like to skip the step-by-step menu (because you want to automate your script fully without any required human intervention, use the area_input parameter

instructions = initialize_VPN(area_input=['Belgium,France,Netherlands']) # <-- Be aware: the area_input parameter expects a list, not a string

for i in range(3):
    rotate_VPN(instructions) #refer to the instructions variable here
    print('\nDo whatever you want here (e.g.scraping). Pausing for 10 seconds...\n')
    time.sleep(10)

# [3] of course, you can try one of the built-in randomizers if you can't be bothered with selecting specific regions

#The following options are avilable:
#random countries X
#random countries europe X
#random countries americas X
#random countries africa east india X
#random countries asia pacific X
#random regions australia X
#random regions canada X
#random regions germany X
#random regions india X
#random regions united states X

instructions = initialize_VPN(area_input=['random countries europe 8'])

for i in range(3):
    rotate_VPN(instructions) #refer to the instructions variable here
    print('\nDo whatever you want here (e.g.scraping). Pausing for 10 seconds...\n')
    time.sleep(10)

# [4] instead of saving the instructions as a variable, you could save your settings in your work directory. Just set the save parameter to 1

initialize_VPN(save=1)

for i in range(3):
    rotate_VPN() #Call the rotate_VPN without any parameter. It will look for a settings file in your work directory
    print('\nDo whatever you want here (e.g.scraping). Pausing for 10 seconds...\n')
    time.sleep(10)

# [5] If you'd like to use an already saved settings file in your work directory (for example: a colleague/friend has sent you his/her settings file),
# use the stored settings parameter

initialize_VPN(save=1,area_input = ['random countries 20']) #save settings file to work directory
print('Imagine you close your python environment and run your script on a later date. Just load your saved settings by running the following line of code:\n')
time.sleep(7)
initialize_VPN(stored_settings=1) #the function will look for a settingsfile in your work directory, launch NordVPN, disconnect if necessary and validate the stored settings file.

for i in range(3):
    rotate_VPN()
    print('\nDo whatever you want here (e.g.scraping). Pausing for 10 seconds...\n')
    time.sleep(10)


# [6] save settings file to work directory and perform a 'complete rotation'

# --> a complete rotation will fetch a list of the currently 4000+ active available servers of NordVPN.
# The rotation will rotate between all the available servers completely by random.
# The difference with picking particular regions is that NordVPN will NOT pick the 'most appropriate' (fastest) server within a particular region when rotating.
# Instead, complete rotation will pick a specific server at random, which mens you're unlikely to revisit the same server twice in a row.
# Because of this, the 'complete rotation' option is ideal for webscraping purposes

initialize_VPN(save=1,area_input=['complete rotation'])

for i in range(3):
    rotate_VPN()
    print('\nDo whatever you want here (e.g.scraping). Pausing for 10 seconds...\n')
    time.sleep(10)

# [7] You can be as creative as you like. For example, the following code will perform an infinite loop of picking a random server every hour

instructions = initialize_VPN(area_input=['complete rotation'])

while True:
    rotate_VPN(instructions)
    time.sleep(3600)

# [8] To implement the google and youtube captcha-check, use the google_check parameter

instructions = initialize_VPN(area_input=['random regions united states 8'])

for i in range(3):
    rotate_VPN(google_check = 1)
    print('\nDo whatever you want here (e.g.scraping). Pausing for 10 seconds...\n')
    time.sleep(10)

##############
## LINUX #####
##############

# [1] Perform a complete rotation and skip the settings menu for complete automation
# the 'skip settings' parameter is only available for Linux users (since setting additional settings such as whitelisting ports is only available on Linux)

instr = initialize_VPN(area_input=['complete rotation'],skip_settings=1)

for i in range(3):
    rotate_VPN(instr)
    print('\nDo whatever you want here (e.g. scraping). Pausing for 10 seconds...\n')
    time.sleep(10)