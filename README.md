# NordVPN-switcher
Rotate between different NordVPN servers with ease. Works both on Linux and Windows without any required changes to your code.

`pip install nordvpn-switcher` and you're all set!

Created by Kristof Boghe

# But...why?

I realize there are multiple NordVPN-related packages available, but they only work for Linux and/or are not exactly user-friendly. 

**NordVPN-switcher is:** 

**1. Able to run both on Windows and Linux**

* You don't need to perform any changes to your script. NordVPN-switcher automatically detects your OS and executes the appropriate code automatically. 
This means you're able to share your code with your colleagues without having to worry about the OS they use.

**2. User-friendly**

* NordVPN-switcher includes a step-by-step menu that takes you through the entire setup. You don't need to construct some chaotic .txt files; you don't even need to know how to run a terminal/cmd command at all! 
* Before attempting any VPN connection, it performs a system-checkup and checks whether the NordVPN app is installed, running and whether you are logged in. 
* If you're not logged in and you're on Linux, you can log in through the Python terminal with ease
* If you're on Linux, it's possible to run whatever additional setting through the NordVPN app (such as setting the killswitch value, whitelisting ports, etc.). You can replicate these settings every time you run your script with ease by saving these commands into a JSON-file (simply by setting the `save` parameter to 1). 
* On Windows, it checks multiple installation directories for the NordVPN app. When the script is unable to locate the installation folder, the menu will ask you for the folder location. The script is able to save this installation folder so you'll never have to worry about it again.
* It even includes a spelling checker (So any attempt to connect to - let's say - "Flance" won't cause any trouble) 
* A dictionary of world regions (e.g. Europe) and local regions (e.g. Cities in the US) is included as well. Especially on windows, taking a random pick within a wider region (e.g. asia pacific) is a real drag. NordVPN-switcher handles these kind of random-pick use-cases with ease.

**3. Forgiving**

* We all like to run our script and ignore it for the next couple of days without worrying about random connectivity hiccups. NordVPN-switcher retries and connects to a different server when it is unable to fetch your new ip. 
* If requested, it also switches servers when Google and/or Youtube throws a captcha (see further).

**4. Able to check for captcha's on Google and/or YouTube**

* Especially on busy servers, captcha checks can disrupt your webscraper (e.g. when scraping Google) or overall browsing experience. If requested (by setting the `google_check` parameter to 1), captcha-checks are performed after each server rotation. If a captcha pops up, the script will automatically try a new server. 

**5. Flexible** 
* You can ask NordVPN-switcher to hold your hand or go rogue and feed it your own settings-file in JSON-format. if a collaborator wants to share his or her unique settings, he or she can simply send you its settings-file and that's about it!

# Install

1. Make sure NordVPN is installed.

* On Linux, run:
```
wget -qnc https://repo.nordvpn.com/deb/nordvpn/debian/pool/main/nordvpn-release_1.0.0_all.deb
sudo dpkg -i /pathToFile/nordvpn-release_1.0.0_all.deb #replace pathToFile to location download folder
sudo apt update 
sudo apt install nordvpn
```
(From the NordVPN FAQ)

* On Windows

Download the app here --> https://bit.ly/3ig2lU5

2. Install the package 

* Execute in terminal:
```
pip install nordvpn-switcher
```

OR, for the ones who don't use pip for some reason:
* Download/clone this repository
* Run `pip install -r requirements.txt` to install dependencies

3. Import functions`from nordvpn_switch import initialize_VPN,rotate_VPN,terminate_VPN

That's it!

# The building blocks

* In essence, you'll just use the following three functions:

**1. Setting up your NordVPN settings**
- save: if you want to save these settings for later
- stored_settings: if you want to execute particular settings already saved in your project folder
- area_input: if you want to feed a list of connection options. Useful when you want to automate the formulation of a server list (see option 5 in the 'some features and options' section).

`initialize_VPN(stored_settings=0,save=0,area_input=None)`

**2. Rotating between servers.** 
- instructions: the instructions saved from the initialize_VPN function. If none is provided, the script looks for a nordvpn_settings.txt file in your project folder (which you can create by setting the `save` parameter in the first function to 1).
- google_check: if you want to perform a google and Youtube captcha-check

`rotate_VPN(instructions=None,google_check = 0)`

**3. Disconnecting from the VPN service**
- Execute this function at the end of your script (not (!) while you're hopping from server to server in a loop)

`terminate_VPN(instructions=None)`

# How to use

**Option 1: save settings in environment**
The easiest and most user-friendly (although least automated) way of using NordVPN switcher is by saving the instructions into a new variable and feeding it to the rotate_VPN() function. 

```
from nordvpn_switcher import initialize_VPN,rotate_VPN,terminate_VPN

settings = initialize_VPN() 
rotate_VPN(settings) 
rotate_VPN(settings,google_check=1) 
terminate_VPN(settings)
```
![resulting output option 1](https://static.wixstatic.com/media/707176_04d56aed046e4c1abe960f98a39d6fba~mv2.gif)

**Option 2: save settings and execute on each run**

If you want to make sure that certain NordVPN setting commands are executed (e.g. killswitch, whitelisting ports, etc.) on each run, save the instructions into your project folder once by setting the `save` parameter to 1 and execute the `initialize_VPN` and `rotate_VPN` function every time you run the script. NordVPN-switcher will alert you what kind of additional settings are pulled from the settings-file.

```
#do this once
initialize_VPN(save=1)
```

If `save=1`, the script will write a .txt file in JSON format to your project folder. It contains all the necessary information needed to execute the `rotate_VPN` function. Again, when the instructions parameter is missing in `rotate_VPN`, it will automatically look for the settings file in your project folder.

--On Windows, the contents of the nordvpn_settings.txt file look something like this (random example): 

`{'opsys': 'Windows', 'command': ['nordvpn', '-c', '-g'], 'settings': ['belgium', 'netherlands', 'germany', 'spain', 'france'], 'cwd_path': 'C:/Program Files/NordVPN'}`

-- On Linux, the file looks slightly different (different random example): 

`{'opsys': 'Linux', 'command': ['nordvpn', 'c'], 'settings': ['United_States', 'Canada', 'Brazil', 'Argentina', 'Mexico', 'Chile', 'Costa_Rica', 'Australia'], 'additional_settings': [['nordvpn', 'set', 'killswitch', 'disable'], ['nordvpn', 'whitelist', 'add', 'port', '23']],'credentials':[['name@gmail.com'],['coolpassword]]}`

Thanks to the saved .txt file, you never need to go through the menu options of `initialize_VPN()` again. So, some time later, you simply perform:

```
initialize_VPN(stored_settings=1)
rotate_VPN()
#do stuff
terminate_VPN()
```
![resulting output option 2](https://static.wixstatic.com/media/707176_006e832eae5f48c7bb3fabdefd18b61c~mv2.gif)

This option is only relevant for Linux users who wish to execute additional settings such as enabling killswitch etc. Executing these settings is not an available option on Windows machines. 

**Option 3: save settings and just use rotate on each run**

This is similar to option 2, but without executing the `initialize_VPN` function on each run. 
This is relevant for all Windows machines or Linux machines who do not wish to execute additional settings.

```
#do this once
initialize_VPN(save=1)

#open project on a later date and just use the following two lines of code:
rotate_VPN()
#do stuff
terminate_VPN()
```
![resulting output option 3](https://static.wixstatic.com/media/707176_996821904d1a4f8cac71d943dca58d83~mv2.gif)

**Option 4: manual option**

Create or obtain your own settings_nordvpn.txt file, place it in your project folder and use the rotate function#
For example, share particular settings with colleagues/friends who work on the same project by sending them your .txt settings file. Place it in your project folder and just use the `rotate_VPN` function.

```
rotate_VPN()
#do stuff
terminate_VPN()
```

**> See the demo.py file for a summary**

# Some features and options

**1. Provide additional settings and save these for later use, if so desired (only on Linux)**

![additional settings gif](https://static.wixstatic.com/media/707176_f419292769834df5bb1e3e4883353ef6~mv2.gif)

**2. Login to NordVPN if logged out (only on Linux)**

![login nordvpn](https://static.wixstatic.com/media/707176_594ed7b6b8044dbfbf260d969a5b50a6~mv2.gif)

**3. Take a random sample from a larger region**

![random sample gif](https://static.wixstatic.com/media/707176_9dcaa96814c44a99a33a9732e13fe490~mv2.gif)

**4.Spellchecker**

![spellchecker gif](https://static.wixstatic.com/media/707176_2e40511ea0b0493f8f95889613b22f1a~mv2.gif)

**5. Provide a list of connection options, which will be automatically incorporated into the nordvpn_settings.txt file**

```
range_servers = range(800,837)
server_list = ["nl"+str(number) for number in range_servers]
instructions = initialize_VPN(area_input = server_list)
rotate_VPN(instructions)
```

![server list gif](https://static.wixstatic.com/media/707176_8ea7e75a73024faca7a739a8e732cc7a~mv2.gif)


**6. NordVPN app starts automatically (if closed) on Windows. Connection process can also be monitored by checking the NordVPN app**

![windows app gif](https://static.wixstatic.com/media/707176_e79bcbe217e44d519a245abae28c360b~mv2.gif)

# Windows vs Linux

* The script runs slower on Windows. This can be explained by the fact that the script communicates directly with NordVPN.exe, which means it inherits the poor speed performance of the Windows app by definition. Compare the speed of the previous gifs (all executed on a Linux machine) with the following gif, executed on Windows:

![windows slowness gif](https://static.wixstatic.com/media/707176_9fc88bae04ad4bf7ab98c1f20ac5bd85~mv2.gif)

* Linux users have a couple of additional options at their disposal, namely:

1.Being able to log in through the Python interface. Windows users need to make sure they're already logged into the NordVPN app. The Windows app remembers your log in by default though, so this shouldn't cause too much trouble. So even when the app is closed, NordVPN-switcher should work.

2.Executing additional settings (e.g. killswitch etc.)

* Settings files can't be directly shared between Windows and Linux machines (see option 4 - how to use). Of course, with a little tweaking, separate Windows and Linux settings-files can easily be constructed for your specific project.

# Possible applications

* To circumvent ip-blocks from certain websites (e.g. while scraping particular platforms)

In this case, the VPN switcher basically serves the same function as the often-used proxy lists while scraping the web (e.g. with BeauitfulSoup), but without the common disadvantages associated with the latter. 

* To automate a particular task that benefits from being performed by many ip-addresses

* For security reasons 

I'm pretty sure there are plenty of other viable applications out there. NordVPN-switcher is extremely easy to implement, no matter the particular problem/project at hand.

# Questions, problems, nasty bugs to report? 

kboghe@gmail.com 

Have fun!
