# Pillowbot Readme
## Concept by Punk
## Written by iso
## debugging and generally being a great person: alien


__use this branch for reference, the other one is old__


Pillow bot is a listener assistant bot written for Discord. 

##Requirements: 
Python3.5 (sudo apt-get python3.5 python3.5-dev) 

It can be downloaded here [python3.5.0 tarball] (https://www.python.org/ftp/python/3.5.0/Python-3.5.0.tgz)  << if you dont wanna mess with ppa

Discord.py by Rapptz can be downloaded [here] (https://github.com/Rapptz/discord.py)

**NOTE: To effectively install discord.py I had to use pip3.5 install instead of pip install**


rename config.txt to config.ini before running first time. 


Im still learning github. So there may be a clusterfuck of pulls and stuff. Please bear with me. 









##For those of you that want to play with this on a raspberry pi: 
###I have a 2B+ at no overclock, 3 radios and this bot runs just fine on it 

[Raspberry pi 2 python3.5 instructions](http://bohdan-danishevsky.blogspot.com/2015/10/building-python-35-on-raspberry-pi-2.html) 

**IMPORTANT NOTES** 

1. Do not skip the dependency step. I had to reformat my Pi to get python to work again. 

2. It is not reccomended to use make -j4 to multithread the make process, just let it run

3. After installing pip using `get-pip.py` from [pypa.io](https://bootstrap.pypa.io/get-pip.py) use pip3.5 for python3.5 operations.     
    It installs libraries under python3.5 instead of default 2.7 or 3.4.2 (current version as i'm writing this) 

###--How to install discord.py@async---

1. After installing python3.5 make sure you do these 3 steps: 

   ```
   $ sudo reboot now
   $ sudo apt-get update && sudo apt-get upgrade -y
   $ python3.5.0 -- version
   ```

   python3.5.0 should ouput something like `Python3.5.0` 

   if you get a "not found" error, check your installation and make sure you did everything right



2. sit in your home directory (`~`) and do `pip3.5 install git+https://github.com/Rapptz/discord.py@async` 
3. then do `pip3.5 install --upgrade discord.py`

   *and now for the fun bits* 

4. Follow these instructions to install pillowbot 
   ```
   $ sudo mkdir /pillow (you can name this whatever you like) 
   $ sudo git clone https://github.com/hdmifish/pillowbot.git /pillow
   $ cd /pillow
   $ checkout rebuild
   ~~<fill out and rename your config file to config.ini, do not use ' or " when changing the fields>~~ 
   ~~if you dont know how to rename do $ sudo mv config.txt config.ini~~
   $ python3.5 pillow.py 
   ```

5. If you get any errors, put them in issues. This is still under development. Currently as I'm writing this pillowbot is `pillowbot 1.0` 
