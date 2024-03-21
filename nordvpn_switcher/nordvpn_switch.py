#################
#import packages#
#################
#1.system and terminal/cmd
import os
from os import path
import platform
import subprocess
from subprocess import check_output,DEVNULL
#2.utilities (randomisations etc)
import psutil
import random
import re
import time
#3.scraping
import urllib
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import requests
#4.file formats
import json
#5.package dependencies
import importlib.resources as pkg_resources
from nordvpn_switcher import NordVPN_options

##################################
#retrieve useragents for scraping#
##################################
software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

##################
#helper functions#
##################
def additional_settings_linux(additional_settings):
    try:
        additional_setting_execute = str(check_output(additional_settings))
    except:
        additional_setting_execute = "error"
    else:
        pass

    if "successfully" in additional_setting_execute:
        settings_input_message = "\nDone! Anything else?\n"
    elif additional_setting_execute == "error":
        settings_input_message = "\n\x1b[93mSomething went wrong. Please consult some examples by typing 'help'\x1b[0m\n"
    elif "already" in additional_setting_execute:
        settings_input_message = "\nThis setting has already been executed! Anything else?\n"
    else:
        settings_input_message = "\n\x1b[93mNordVPN throws an unexpected message, namely:\n" + additional_setting_execute + "\nTry something different.\x1b[0m\n"
    return settings_input_message

def saved_settings_check():
    print("\33[33mTrying to load saved settings...\33[0m")
    try:
        instructions = json.load(open("settings_nordvpn.txt"))
    except FileNotFoundError:
        raise Exception("\n\nSaved settings not found.\n"
                        "Run initialize_VPN() first and save the settings on your hard drive or store it into a Python variable.")
    else:
        print("\33[33mSaved settings loaded!\n\33[0m")
    return instructions

def set_headers(user_agent_rotator):
    useragent_pick = user_agent_rotator.get_random_user_agent()
    headers = {'User-Agent': useragent_pick,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}
    return headers

def get_ip():
    headers = set_headers(user_agent_rotator)
    ip_check_websites = ['http://ip4only.me/api/',"https://api64.ipify.org/"]
    website_pick = random.choice(ip_check_websites)
    request_currentip = urllib.request.Request(url=website_pick, headers=headers)
    ip = urllib.request.urlopen(request_currentip).read().decode('utf-8')
    if website_pick == 'http://ip4only.me/api/':
        ip = re.search("IPv4,(.*?),", ip).group(1)
    return ip

def get_nordvpn_servers():
    serverlist =  BeautifulSoup(requests.get("https://api.nordvpn.com/v1/servers").content,"html.parser")
    site_json=json.loads(serverlist.text)
    filtered_servers = {'windows_names': [], 'linux_names': []}
    
    for specific_dict in site_json:
        try:
            groups = specific_dict.get('groups', [])  # Verifica se 'groups' está presente
            for group in groups:
                if group['title'] == 'Standard VPN servers':
                    filtered_servers['windows_names'].append(specific_dict['name'])
                    filtered_servers['linux_names'].append(specific_dict['domain'].split('.')[0])
                    break  # Exit the group loop if you find the desired category
        except KeyError:
            pass  # Ignore dictionaries that do not have the 'groups' or 'title' key

    return filtered_servers
#deprecated
# def get_nordvpn_servers():
#     serverlist =  BeautifulSoup(requests.get("https://nordvpn.com/api/server").content,"html.parser")
#     site_json=json.loads(serverlist.text)

#     filtered_servers = {key: [] for key in ['windows_names','linux_names']}
#     for specific_dict in site_json:
#         try:
#             if specific_dict['categories'][0]['name'] == 'Standard VPN servers':
#                 filtered_servers['windows_names'].append(specific_dict['name'])
#                 filtered_servers['linux_names'].append(specific_dict['domain'].split('.')[0])
#         except IndexError:
#             pass
#     return filtered_servers

###############
#intialize vpn#
###############
def initialize_VPN(stored_settings=0,save=0,area_input=None,skip_settings=0):

    ###load stored settings if needed and set input_needed variables to zero if settings are provided###
    windows_pause = 3
    additional_settings_needed = 1
    additional_settings_list = list()
    if stored_settings == 1:
        instructions = saved_settings_check()
        additional_settings_needed = 0
        input_needed = 0
    elif area_input is not None:
        input_needed = 2
        windows_pause = 8
    else:
        input_needed = 1

    ###performing system check###
    opsys = platform.system()

    ##windows##
    if opsys == "Windows":
        print("\33[33mYou're using Windows.\n"
              "Performing system check...\n"
              "###########################\n\33[0m")
        #seek and set windows installation path#
        option_1_path = 'C:/Program Files/NordVPN'
        option_2_path = 'C:/Program Files (x86)/NordVPN'
        custom_path = str()
        if path.exists(option_1_path) == True:
            cwd_path = option_1_path
        elif path.exists(option_2_path) == True:
            cwd_path = option_2_path
        else:
            custom_path = input("\x1b[93mIt looks like you've installed NordVPN in an uncommon folder. Would you mind telling me which folder? (e.g. D:/customfolder/nordvpn)\x1b[0m")
            while path.exists(custom_path) == False:
                custom_path = input("\x1b[93mI'm sorry, but this folder doesn't exist. Please double-check your input.\x1b[0m")
            while os.path.isfile(custom_path+"/NordVPN.exe") == False:
                custom_path = input("\x1b[93mI'm sorry, but the NordVPN application is not located in this folder. Please double-check your input.\x1b[0m")
            cwd_path = custom_path
        print("NordVPN installation check: \33[92m\N{check mark}\33[0m")

        #check if nordvpn service is already running in the background
        check_service = "nordvpn-service.exe" in (p.name() for p in psutil.process_iter())
        if check_service is False:
            raise Exception("NordVPN service hasn't been initialized, please start this service in [task manager] --> [services] and restart your script")
        print("NordVPN service check: \33[92m\N{check mark}\33[0m")

        # start NordVPN app and disconnect from VPN service if necessary#
        print("Opening NordVPN app and disconnecting if necessary...")
        open_nord_win = subprocess.Popen(["nordvpn", "-d"],shell=True,cwd=cwd_path,stdout=DEVNULL)
        while ("NordVPN.exe" in (p.name() for p in psutil.process_iter())) == False:
            time.sleep(windows_pause)
        open_nord_win.kill()
        print("NordVPN app launched: \33[92m\N{check mark}\33[0m")
        print("#####################################")

    ##linux##
    elif opsys == "Linux":
        print("\n\33[33mYou're using Linux.\n"
              "Performing system check...\n"
              "###########################\n\33[0m")

        #check if nordvpn is installed on linux#
        check_nord_linux = check_output(["nordvpn"])
        if len(check_nord_linux) > 0:
            print("NordVPN installation check: \33[92m\N{check mark}\33[0m")
        else:
            raise Exception("NordVPN is not installed on your Linux machine.\n"
                  "Follow instructions on shorturl.at/ioDQ2 to install the NordVpn app.")

        #check if user is logged in. If not, ask for credentials and log in or use credentials from stored settings if available.#
        try:
            check_output(["nordvpn", "account"])
        except:
            login_needed = 1
            while login_needed == 1:
                login_message = input("\n\033[34mYou are not logged in. Please provide your credentials in the form of LOGIN/PASSWORD\n\033[0m")
                try:
                    if instructions['credentials'] in locals():
                        credentials = stored_settings['credentials']
                    else:
                        credentials = login_message
                except:
                    credentials = login_message
                finally:
                    try:
                        login = credentials.split("/")[0]
                        password = credentials.split("/")[1]
                    except IndexError:
                        error_login = input("\n\033[34mYou have provided your credentials in the wrong format. Press enter and please try again.\n"
                              "Your input should look something like this: name@gmail.com/password\033[0m")
                    else:
                        login_needed = 0
            try:
                login_nordvpn = check_output(["nordvpn","login","-username",login,"-password",password])
            except subprocess.CalledProcessError:
                raise Exception("\nSorry,something went wrong while trying to log in\n")
            if "Welcome" in str(login_nordvpn):
                print("\n\n\033[34mLogin successful!\n\033[0m\n")
                pass
            else:
                raise Exception("\nSorry, NordVPN throws an unexpected message, namely:\n"+str(login_nordvpn))
        else:
            print("NordVPN login check: \33[92m\N{check mark}\33[0m")

        #disconnect from VPN if necessary
        terminate = subprocess.Popen(["nordvpn", "d"],stdout=DEVNULL)

        #provide opportunity to execute additional settings.#
        settings_input_message = "\n\033[34mDo you want to execute additional settings?\033[0m"
        while additional_settings_needed == 1 and skip_settings == 0:
            additional_settings = input(settings_input_message+
                                        "\n_________________________\n\n"
                                        "Press enter to continue\n"
                                        "Type 'help' for available options\n").strip()
            if additional_settings == "help":
                options_linux = pkg_resources.open_text(NordVPN_options, 'options_linux.txt').read().split('\n')
                for line in options_linux:
                    print(line)
                additional_settings = input("").strip()

            additional_settings = str(additional_settings).split(" ")
            if len(additional_settings[0]) > 0:
                settings_input_message = additional_settings_linux(additional_settings)
                if any(re.findall(r'done|already been executed', settings_input_message,re.IGNORECASE)):
                    additional_settings_list.append(additional_settings)
            else:
                additional_settings_needed = 0

        #however, if provided, just skip the additional settings option and execute the stored settings.#
        if 'instructions' in locals():
            if len(instructions['additional_settings'][0][0]) > 0:
                print("Executing stored additional settings....\n")
                for count,instruction in enumerate(instructions['additional_settings']):
                    print("Executing stored setting #"+str(count+1)+": "+str(instruction))
                    additional_settings_linux(instruction)
            else:
                pass

    else:
        raise Exception("I'm sorry, NordVPN switcher only works for Windows and Linux machines.")

    ###provide settings for VPN rotation###

    ##open available options and store these in a dict##
    areas_list = pkg_resources.open_text(NordVPN_options, 'countrylist.txt').read().split('\n')
    country_dict = {'countries':areas_list[0:60],'europe': areas_list[0:36], 'americas': areas_list[36:44],
                    'africa east india': areas_list[49:60],'asia pacific': areas_list[49:60],
                    'regions australia': areas_list[60:65],'regions canada': areas_list[65:68],
                    'regions germany': areas_list[68:70], 'regions india': areas_list[70:72],
                    'regions united states': areas_list[72:87],'special groups':areas_list[87:len(areas_list)]}

    ##provide input if needed##
    while input_needed > 0:
        if input_needed == 2:
            print("\nYou've entered a list of connection options. Checking list...\n")
            try:
                settings_servers = [area.lower() for area in area_input]
                settings_servers = ",".join(settings_servers)
            except TypeError:
                raise Exception("I expected a list here. Are you sure you've not entered a string or some other object?\n ")

        else:
            settings_servers = input("\n\033[34mI want to connect to...\n"
                                 "_________________________\n"
                                 "Type 'help' for available options\n\033[0m").strip().lower()
        #define help menu#
        if settings_servers.lower().strip() == 'help':
            #notation for specific servers differs between Windows and Linux.#
            if opsys == "Windows":
                notation_specific_server = " (e.g. Netherlands #742,Belgium #166)\n"
            else:
                notation_specific_server = " (e.g. nl742,be166)\n"

            settings_servers = input("\nOptions:\n"
                  "##########\n"
                  "* type 'quick' to choose quickconnect \n"
                  "* type 'complete rotation' to rotate between all available NordVPN servers\n"
                  "* Single country or local region (e.g.Germany)\n"
                  "* Regions within country (e.g. regions united states')\n"
                  "* World regions (europe/americas/africa east india/asia pacific)\n"
                  "* Random multiple countries and/or local regions (e.g.France,Netherlands,Chicago)\n"
                  "* Random n countries (e.g. random countries 10)\n"
                  "* Random n countries within larger region (e.g. random countries europe 5)\n"
                  "* Random n regions in country (e.g. random regions United States 6)\n"\
                  "* Specialty group name (e.g. Dedicated IP,Double VPN)\n"
                  "* Specific list of servers"+notation_specific_server).strip().lower()

        #set base command according to running os#
        if opsys == "Windows":
            nordvpn_command = ["nordvpn", "-c"]
        if opsys == "Linux":
            nordvpn_command = ["nordvpn", "c"]

        #create sample of regions from input.#
        #1. if quick connect#
        if settings_servers == "quick":
            if input_needed == 1:
                quickconnect_check = input("\nYou are choosing for the quick connect option. Are you sure? (y/n)\n")
                if 'y' in quickconnect_check:
                    sample_countries = [""]
                    input_needed = 0
                    pass
            if input_needed == 2:
                sample_countries = [""]
                input_needed = 0
            else:
                print("\nYou are choosing for the quick connect option.\n")
        #2. if completely random rotation
        elif settings_servers == 'complete rotation':
            print("\nFetching list of all current NordVPN servers...\n")
            for i in range(120):
                try:
                    filtered_servers = get_nordvpn_servers()
                    if opsys == "Windows":
                        nordvpn_command.append("-n")
                        sample_countries = filtered_servers['windows_names']
                    else:
                        sample_countries = filtered_servers['linux_names']
                except:
                    time.sleep(0.5)
                    continue
                else:
                    input_needed = 0
                    break
            else:
                raise Exception("\nI'm unable to fetch the current NordVPN serverlist. Check your internet connection.\n")
        #3. if provided specific servers. Notation differs for Windows and Linux machines, so two options are checked (first is Windows, second is Linux#
        elif "#" in settings_servers or re.compile(r'^[a-zA-Z]+[0-9]+').search(settings_servers.split(',')[0]) is not None:
            if opsys == "Windows":
                nordvpn_command.append("-n")
            sample_countries = [area.strip() for area in settings_servers.split(',')]
            input_needed = 0
        else:
            #3. If connecting to some specific group of servers#
            if opsys == "Windows":
                nordvpn_command.append("-g")
            #3.1 if asked for random sample, pull a sample.#
            if "random" in settings_servers:
                #determine sample size#
                samplesize = int(re.sub("[^0-9]", "", settings_servers).strip())
                #3.1.1 if asked for random regions within country (e.g. random regions from United States,Australia,...)#
                if "regions" in settings_servers:
                    try:
                        sample_countries = country_dict[re.sub("random", "", settings_servers).rstrip('0123456789.- ').lower().strip()]
                        input_needed = 0
                    except:
                        input("\n\nThere are no specific regions available in this country, please try again.\nPress enter to continue.\n")
                        if input_needed == 2:
                            input_needed = 1
                            continue
                    if re.compile(r'[^0-9]').search(settings_servers.strip()):
                        sample_countries = random.sample(sample_countries, samplesize)
                #3.1.2 if asked for random countries within larger region#
                elif any(re.findall(r'europe|americas|africa east india|asia pacific', settings_servers)):
                    larger_region = country_dict[re.sub("random|countries", "", settings_servers).rstrip('0123456789.- ').lower().strip()]
                    sample_countries = random.sample(larger_region,samplesize)
                    input_needed = 0
                #3.1.3 if asked for random countries globally#
                else:
                    if re.compile(r'[^0-9]').search(settings_servers.strip()):
                        sample_countries = random.sample(country_dict['countries'], samplesize)
                        input_needed = 0
                    else:
                        sample_countries = country_dict['countries']
                        input_needed = 0
            #4. If asked for specific region (e.g. europe)#
            elif settings_servers in country_dict.keys():
                sample_countries = country_dict[settings_servers]
                input_needed = 0
            #5. If asked for specific countries or regions (e.g.netherlands)#
            else:
                #check for empty input first.#
                if settings_servers == "":
                    input("\n\nYou must provide some kind of input.\nPress enter to continue and then type 'help' to view the available options.\n")
                    if input_needed == 2:
                        input_needed = 1
                        continue
                else:
                    sample_countries = [area.strip() for area in settings_servers.split(',')] #take into account possible superfluous spaces#
                    approved_regions = 0
                    for region in sample_countries:
                        if region in [area.lower() for area in areas_list]:
                            approved_regions = approved_regions + 1
                            pass
                        else:
                            input("\n\nThe region/group " + region + " is not available. Please check for spelling errors.\nPress enter to continue.\n")
                            if input_needed == 2:
                                input_needed = 1
                                continue
                    if approved_regions == len(sample_countries):
                        input_needed = 0

    ##fetch current ip to prevent ip leakage when rotating VPN##
    for i in range(59):
        try:
            og_ip = get_ip()
        except ConnectionAbortedError:
            time.sleep(1)
            continue
        else:
            break
    else:
        raise Exception("Can't fetch current ip, even after retrying... Check your internet connection.")

    ##if user does not use preloaded settings##
    if "instructions" not in locals():
        #1.add underscore if spaces are present on Linux os#
        for number,element in enumerate(sample_countries):
            if element.count(" ") > 0 and opsys == "Linux":
                    sample_countries[number] = re.sub(" ","_",element)
        else:
            pass
        #2.create instructions dict object#
        instructions = {'opsys':opsys,'command':nordvpn_command,'settings':sample_countries,'original_ip':og_ip}
        if opsys == "Windows":
            instructions['cwd_path'] = cwd_path
        if opsys == "Linux":
            instructions['additional_settings'] = additional_settings_list
            if 'credentials' in locals():
                instructions['credentials'] = credentials
        #3.save the settings if requested into .txt file in project folder#
        if save == 1:
            print("\nSaving settings in project folder...\n")
            try:
                os.remove("settings_nordvpn.txt")
            except FileNotFoundError:
                pass
            instructions_write = json.dumps(instructions)
            f = open("settings_nordvpn.txt", "w")
            f.write(instructions_write)
            f.close()

    print("\nDone!\n")
    return instructions

##########################
#rotate and terminate VPN#
##########################
#1.rotate
def rotate_VPN(instructions=None,google_check = 0):
    if instructions is None:
        instructions = saved_settings_check()

    opsys = instructions['opsys']
    command = instructions['command']
    settings = instructions['settings']
    og_ip = instructions['original_ip']

    if opsys == "Windows":
        cwd_path = instructions['cwd_path']

    for i in range(2):
        try:
            current_ip = new_ip = get_ip()
        except urllib.error.URLError:
            print("Can't fetch current ip. Retrying...")
            time.sleep(10)
            continue
        else:
            print("\nYour current ip-address is:", current_ip)
            break
    else:
        raise Exception("Can't fetch current ip, even after retrying... Check your internet connection.")

    for i in range(4):
        if len(settings) > 1:
            settings_pick = list([random.choice(settings)])
        else:
            settings_pick = settings

        input = command + settings_pick

        if settings[0] == "":
            print("\nConnecting you to the best possible server (quick connect option)...")
        else:
            print("\n\33[34mConnecting you to", settings_pick[0], "...\n\33[0m")

        try:
            if opsys == "Windows":
                new_connection = subprocess.Popen(input, shell=True, cwd=cwd_path)
                new_connection.wait(50)
            else:
                new_connection = check_output(input)
                print("Found a server! You're now on "+re.search('(?<=You are connected to )(.*)(?=\()', str(new_connection))[0].strip())
        except:
            print("\n An unknown error occurred while connecting to a different server! Retrying with a different server...\n")
            time.sleep(15)
            continue

        for i in range(12):
            try:
                new_ip = get_ip()
            except:
                time.sleep(5)
                continue
            else:
                if new_ip in [current_ip,og_ip]:
                    time.sleep(5)
                    continue
                else:
                    break
        else:
            pass

        if new_ip in [current_ip,og_ip]:
            print("ip-address hasn't changed. Retrying...\n")
            time.sleep(10)
            continue
        else:
            print("your new ip-address is:", new_ip)

        if google_check == 1:
            print("\n\33[33mPerforming captcha-check on Google search and Youtube...\n"
                  "---------------------------\33[0m")
            try:
                google_search_check = BeautifulSoup(
                    requests.get("https://www.google.be/search?q=why+is+python+so+hard").content,"html.parser")
                youtube_video_check = BeautifulSoup(
                    requests.get("https://www.youtube.com/watch?v=dQw4w9WgXcQ").content,"html.parser")

                google_captcha = google_search_check.find('div',id="recaptcha")
                youtube_captcha = youtube_video_check.find('div', id = "recaptcha")

                if None not in (google_captcha,youtube_captcha):
                    print("Google throws a captcha. I'll pick a different server...")
                    time.sleep(5)
                    continue
            except:
                print("Can't load Google page. I'll pick a different server...")
                time.sleep(5)
                continue
            else:
                print("Google and YouTube don't throw any Captcha's: \33[92m\N{check mark}\33[0m")
                break
        else:
            break

    else:
        raise Exception("Unable to connect to a new server. Please check your internet connection.\n")

    print("\nDone! Enjoy your new server.\n")
#2.terminate
def terminate_VPN(instructions=None):
    if instructions is None:
        instructions = saved_settings_check()

    opsys = instructions['opsys']
    if opsys == "Windows":
        cwd_path = instructions['cwd_path']

    print("\nDisconnecting...")
    if opsys == "Windows":
        terminate = subprocess.Popen(["nordvpn", "-d"],shell=True,cwd=cwd_path,stdout=DEVNULL)
    else:
        terminate = subprocess.Popen(["nordvpn", "d"],stdout=DEVNULL)

    terminate.wait()
    print("Done!")
