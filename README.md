# Story
You suspect your boss is embezzling money, and you would really like to obtain your boss's password to gather evidence.
What you do with it is up to you...
Luckily, the sysadmin (who has a sudo account) at your company set the DAC permissions incorrectly on the default Linux password management files.
After learning this, you made friends with a temp worker (to frame him in the event of being found out), and came to an arrangement: if the temp will help you get the bosses password, you will write a program that does his job for him, so he can just surf Facebook and Tinder at work all day.
The temp worker does not know how to work "the PuTTY", and he cannot type very fast either, so you can't expect him to type out your commands at the bash terminal.
You can teach him enough to execute a singe script via the terminal however.
You job is to write this script, which you can give to your "friend" the temp worker, that he can execute for you, that does the following: processes the password files, cracks the password for the account "yourboss", outputs the password (and only the password) to the screen, then fixes the permissions of the shadow and password files to match the Debian defaults, clears the bash history, deletes any log or "dot" / config files created in the process of cracking the password, and finally, add the temp worker to the sudo'ers group (for future mischief).
The user tempworker gave you his password so you can include it in the script: "correctbatteryhorsestaple99" (why he has a reasonably good password is a mystery to you...).
You can't just use the password at any terminal though, since someone might notice you at the temp's computer, and you don't want evidence that you logged onto his account with your computer.
You may also discover that the system administrator's (sysadmin) password is also ironically weak.
Your internet research has discovered the following links about how to perform your task (not all of these will be critical, depending on which tools and methods you choose):

# Your internet research
Sudo and passwords
* http://www.yourownlinux.com/2015/08/etc-shadow-file-format-in-linux-explained.html
* https://www.debian.org/doc/manuals/debian-handbook/sect.user-group-databases.en.html
* https://wiki.debian.org/sudo
* https://unix.stackexchange.com/questions/86748/how-to-properly-configure-sudoers-file-on-debian-wheezy
* https://www.debian.org/doc/manuals/debian-reference/ch04.en.html#_managing_account_and_password_information
* https://www.linuxquestions.org/questions/linux-general-1/execute-command-as-different-user-63197/

Bash and sudo
* https://stackoverflow.com/questions/11955298/use-sudo-with-password-as-parameter
* https://superuser.com/questions/67765/sudo-with-password-in-one-command-line

Bash and executing system bash commands in python:
* https://docs.python.org/3.5/library/subprocess.html#subprocess.run
* http://www.linuxcommand.org/lc3_learning_the_shell.php
* http://www.linuxcommand.org/lc3_writing_shell_scripts.php

John and Hashcat
* https://www.samsclass.info/123/proj10/p12-hashcat.htm
* https://www.blackmoreops.com/2015/11/10/cracking-password-in-kali-linux-using-john-the-ripper/

# Overview
1. Get password of yourboss using a python script and nothing other than basic crypto tools (65 pts)
2. After getting password, then fix permissions on the shadow file (debian secure defaults) (10 pts)
3. Get yourbuddy's password by using John or Hashcat (already installed in Kali). Hint: this will require brute force, but the password is short (10 pts)
4. Get password of sysadmin (using any method) (5 pts)
5. Clear your tracks, if you left any (10 pts)

# Setup
In a fresh install of your Kali VM (updated to latest software via apt-get), run this to setup the assignment:

```bash
#!/usr/bin/env bash

# This should be executed as root or sudo on your Kali VM.

# Creates sysadmin's account and password
sudo useradd sysadmin -m -p '$6$g0oUQt7l$Su1Nzm5XgOSnZqvECAqOhnxdHrGiuhqTRRaTEdAOw2jIQzLMx32Tluv3d5lfG7O5UAPM79LKnm4voFa2GJ36O0'
sudo usermod -a -G sudo sysadmin

# Creates yourboss's account and password
sudo useradd yourboss -m -p '$6$dbkKuKGS$XsniIqjOF39Kar2w3vZ8DuImkBihLJ0wR6skCAzwIFTDfbDdgQLYCyzRrcQeouT83didVrrOiXVYVARDpX88L/'
sudo usermod -a -G sudo yourboss

# Creates tempworker's account and password
sudo useradd tempworker -m -p '$6$g1VamdqE$RiEKGpb7gemh1Zt2JyVPq4Gzp/a2wTE5CPxNu97YaFfjS4wqbL2Nj1ousP2NWrUtjoVWw2nm8KdIcHzgzkw7R.'

# Your friend
sudo useradd yourbuddy -m -p '$6$tvsAYmsV$a5dekP.yLet1VJa51LlYc6Gt/z0Kopq8yNldXPMmnjwiPr9stkJ2tP5V.RIjLvktcM3UGV6JXB662.XZl3Mix0'

# break permissions on shadow file
sudo chmod a+rwx /etc/shadow
```

# Hints
* You will need to make bash/system calls in python3; the best way to do this is subprocess.run
* You will want to take and refresh VM snaphshots for testing your code repeatedly
* The sudo password for the tempworker must be typed automatically for your script.
We will NOT provide any keyboard input during grading running.

# What to submit
* funandgames.py
* screenshot of how you ran your script
* screenshot of the results produced by your script

# Running
We will run your script as follows (in the home directory of a random new user we have created without sudo permissions:

`$ python3 funandgames.py`

Note: Putting a space before a command means it does not get entered into bash history, if the environmental variable, $HISTCONTROL=ignoreboth, as it is in Debian.

# Password output:
* You can check your program output by doing this (which is how we will run it)

    `$ ./fundandgames.py >myout.txt  # Put space before command`

    `$ diff myout.txt example-output.txt`

* Make sure you don't have newline differences with this file. 
* To make sure there are no differences (other than the passwords)
* No output other than the system changes themselves should be produced for the other assignment components (like the permissions changes).

