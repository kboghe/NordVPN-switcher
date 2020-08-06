# NordVPN-switcher
Rotate between different NordVPN servers with ease. Works both on Linux and Windows without any required changes to your code.

# But...why?

I realize there are multiple NordVPN-related packages available to rotate between different servers, but they only work for Linux and/or are not exactly user-friendly. 
NordVPN-switcher is: 

**1. Able to run both on Windows and Linux**

* You don't need to perform any changes to your script. NordVPN-switcher automatically detects your OS and executes the appropriate code automatically. 
This means you're able to share your code with your colleagues without having to worry about the OS they use.

**2. Extremely user-friendly**

* NordVPN-switcher includes a step-by-step menu that takes you through the entire setup. You don't need to construct some chaotic .txt files yourselves; you don't even need to know how to run a terminal/cmd command at all! 
* Before attempting any VPN connection, it performs a system-checkup and checks whether the NordVPN app is installed, running and whether you are logged in. 
* If you're not logged in and you're on Linux, you can log in through the Python terminal with ease
* If you're on Linux, it's possible to run whatever additional setting through the NordVPN app (such as setting the killswitch value, whitelisting ports, etc.). You can replicate these settings every time you run your script with ease by saving these commands into a JSON-file (simply by setting the `save` parameter to 1). 
* On Windows, it checks multiple installation directories for the NordVPN app. When the script is unable to locate the installation folder, the menu will ask you for the folder location. The script is able to save this installation folder so you'll never have to worry about it again.
* It even includes a spelling checker (So any attempt to connect to - let's say - "Flance" won't cause any trouble) 
* A dictionary to world regions (e.g. Europe) and local regions (e.g. Cities in the US) is included as well. Especially on windows, taking a random pick within a wider region (e.g. asia pacific) is a real drag. NordVPN-switcher handles these kind of random-pick use-cases with ease.

**3. Forgiving**

* We all like to run our script and ignore it for the next couple of days without worrying about random connectivity hiccups. NordVPN-switcher retries and connects to a different server when it is unable to fetch your new ip. 
* If requested, it also switches servers when Google and/or Youtube throws a captcha (see further).

**4. Able to check for captcha's on Google and/or YouTube**

* Especially on busy servers, captcha checks can disrupt your webscraper (e.g. when scraping Google) or overall browsing experience. If requested (by setting the `google_check` parameter to 1), captcha-checks are performed after each server rotation. If a captcha pops up, the script will automatically try a new server. 

**5. Flexible** 
* You can ask NordVPN-switcher to hold your hand or go rogue and feed it your own settings-file in JSON-format. if a collaborator wants to share his or her unique settings, he or she can simply send you its settings-file and that's about it!

# Install and use

1. Make sure NordVPN is installed.
2. Download/clone this repository
3. Run `pip install -r requirements.txt` to install dependencies
4. Using NordVPN-switcher:

**Option 1: set settings in project**
The easiest and most user-friendly (although least automated) way of using NordVPN switcher is by saving the instructions into a new variable and feeding it to the rotate_VPN() function. 

```
from nordvpn_switch import initialize_VPN,rotate_VPN,terminate_VPN

settings = initialize_VPN() 
rotate_VPN(settings) 
rotate_VPN(settings,google_check=1) 
terminate_VPN(settings)
```
![resulting output option 1](https://media.giphy.com/media/Y3NIgq6cPzBPQONE49/giphy.gif)

**Option 2: save settings and execute on each run**

If you want to make sure that certain NordVPN setting commands are executed (e.g. killswitch, whitelisting ports, etc.) on each run, save the instructions into your project folder once by setting the `save` parameter to 1 and execute the `initialize_VPN` and `rotate_VPN` function every time you run the script.
This option is only relevant for Linux machines who wish to execute additional settings such as enabling killswitch etc. Executing these settings is not an available option on Windows machines. 

```
#do this once
initialize_VPN(save=1)

#open project on a later date and just use the following three lines of code:
initialize_VPN(stored_settings=1)
rotate_VPN()
#do stuff
terminate_VPN()
```
![resulting output option 2](http://digitalmethods.be/wp-content/uploads/2020/08/option2_linux.gif)

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
**Option 4: manual option**

Create or obtain your own settings_nordvpn.txt file, place it in your project folder and use the rotate function#
For example, share particular settings with colleagues/friends who work on the same project by sending them your .txt settings file. Place it in your project folder and just use the `rotate_VPN` function.

```
rotate_VPN()
#do stuff
terminate_VPN()
```

# Some features and options

**1. Provide additional settings and save these for later use, if so desired (only on Linux)**

**2. Login to NordVPN if logged out (only on Linux)**

**3. Take a random sample from a larger region**

**4.Spellchecker**

**5. NordVPN app starts automatically (if closed) on Windows. Connection process can also be monitored by checking the NordVPN app**

**6. NordVPN-switcher automatically picks a new server if Google and/or YouTube throw a captcha, if so desired**

# Windows vs Linux

* The script runs slower on Windows. This is because the script communicates directly with the NordVPN.exe
* 
