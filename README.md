# website_update_check - programmed by felix

website_update_check is a Python tool that checks simple websites for updates:

Features:

- Get custom notifications on your smartphone when the website you want to watch has changed (you need the Pushover App for this feature)

- Play a locally saved song when the website you want to watch has changed (uses VLC)

- You can choose how often you want to check the website for changes

How does it work?

In short, this tool downloads the website you enter every x seconds and compares its md5 hashes to detect changes of the website.
Then you optionally can use the Pushover API to send a custom notification to your Android phone or iPhone.
I am in no way associated or affiliated with Pushover, I just think it's a cool app that does what I want it to do for $4 (one week free trial).

Motivation:

Whenever we write exams in university the results will be posted online. We never know when exactly the results get posted which is why I was bored after checking it myself. With this tool I just get a notfication to my iPhone when the exam results have been uploaded.
I know that you can use "javascript:alert(document.lastModified)" in the URL bar to get the last modified date of a website, but most of the time websites will just give you the current time which wouldn't work for my purposes. 

Planned features / What to expect in the future:

- Support for websites where you have to log-in first 

- Support for every website: Right now there can be issues when there is dynamic content like changing dates on a website (because it messes up the md5 hash and the tool thinks the whole website has changed)
