"""website-update-check in Python

This program makes it possible to track changes of a website.
It downloads the website you enter every x seconds and compares its md5
hashes to detect changes. You can even use Pushovers API to send
custom notifications to your Android phone or iPhone.

"""

from datetime import datetime
import hashlib
import os
import time

from bs4 import BeautifulSoup
from pushover import init, Client  # push notifications to your phone
import requests
import vlc  # needed for the music feature
# set the path to the music if you want to use this feature


class Md5:
    """This class holds md5 values.

    """

    original_md5sum = ""
    new_md5sum = ""


class Settings:
    """This class saves the user's settings.

    """

    url = "https://www.publix.com/covid-vaccine/florida"
    push = True
    music = True
    update_timer = 20


def check_for_update():
    """This function downloads the website and calculates hashes

    This function downloads the website using the requests module,
    then it strips HTML tags off so that raw text is left.
    Then it calculates md5 hashes of this text to detect any
    changes over time.
    """

    if os.path.isfile("website.txt"):
        request = requests.get(Settings.url)
        assert request.status_code == 200
        html = request.text
        soup = BeautifulSoup(html, "lxml")
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines
                  for phrase in line.split(" "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        with open("website_new.txt", "w") as f:
            f.write(text)
        hasher = hashlib.md5()
        with open('website_new.txt', 'rb') as f:
            buffer = f.read()
            hasher.update(buffer)
        Md5.new_md5sum = hasher.hexdigest()

    else:
        request = requests.get(Settings.url)
        assert request.status_code == 200
        html = request.text
        soup = BeautifulSoup(html, "lxml")
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines
                  for phrase in line.split(" "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        with open("website.txt", "w") as f:
            f.write(text)
        hasher = hashlib.md5()
        with open('website.txt', 'rb') as f:
            buffer = f.read()
            hasher.update(buffer)
        Md5.original_md5sum = hasher.hexdigest()
        check_for_update()


def main():
    """This function takes the user's wished settings as input

    This function not only takes input from the user but also
    cautiously handles it and checks its validity.
    """

    Settings.url = input("Paste the URL you want to check for updates: ")
    while True:
        get_notification = input("\nDo you want to get a notification \
to your phone when the website has been changed? (y/n): ")
        if get_notification != "y" and get_notification != "n":
            print("Error: Please enter y or n")
        else:
            if get_notification == "y":
                Settings.push = True
                print("Notifications to your phone have been turned ON\n")
                break
            else:
                Settings.push = False
                print("Notifications to your phone have been turned OFF\n")
                break
    while True:
        play_song = input("Do you want to play a song \
when the website has been changed? (y/n): ")
        if play_song != "y" and play_song != "n":
            print("Error: Please enter y or n")
        else:
            if play_song == "y":
                Settings.music = True
                print("The music feature has been turned ON\n")
                break
            else:
                Settings.music = False
                print("The music feature has been turned OFF\n")
                break

    while True:
        check_interval = input("How often do you want to check \
the website for updates? Enter it in seconds (min. 20): ")

        if check_interval.isdigit():
            check_interval = int(check_interval)
            if check_interval > 19:
                print("The website will be checked for \
updates every " + str(check_interval) + " seconds\n")
                Settings.update_timer = check_interval
                break
            else:
                print("Make sure to enter a value bigger than 19\n")
        else:
            print("Please enter an integer \
            (which has to be bigger than 19)\n")

    path = os.path.dirname(os.path.realpath(__file__))
    try:
        os.remove(path + "/website.txt")
    except OSError:
        pass
    try:
        os.remove(path + "/website_new.txt")
    except OSError:
        pass

    check_for_update()
    mainloop()


def mainloop():
    """This function is the clock generator of this program

    This function creates the loop which checks if any
    changes on a given website occur over time.
    """

    while True:
        check_for_update()
        '''
        print("Original: ", original_md5sum)
        print("New: ", new_md5sum)
        '''
        if Md5.original_md5sum == Md5.new_md5sum:
            print("Website hasn't been updated yet... " +
                  datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            print("Website hat been updated! " +
                  datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            if Settings.push:
                init("<email_key>")
                Client("<website_key>\
").send_message("Website has been updated!", title="Website update")

            if Settings.music:
                p = vlc.MediaPlayer("file:///home/felix/Music/\
The_next_episode.mp3")
                p.play()
                time.sleep(60)
                p.stop()
            break
        time.sleep(Settings.update_timer)

if __name__ == "__main__":
    main()
