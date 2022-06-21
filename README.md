# Gecko Tasks

Gecko Tasks is a simple-to-use program designed to make it significantly easier to get started making programs to crawl or debug websites. It uses Selenium with geckodriver to simulate user behavior, with the optional ability to use a list of proxies for Requesters to use. You can scale it up to as many Requesters as you want using the Tasks.json file which includes all of Gecko Tasks’ configuration options.

Gecko Tasks is **not** a lightweight program by nature. It runs actual browser instances (Completely separate from your own, using a standalone executable of Firefox's geckodriver), not *just* web requests. This means that per requester, you could be looking at about 300mb of RAM usage, which you’ll need to consider as you scale up.


## Installation

For installing/setting up Gecko Tasks, you'll need to install [Python **3.10**+](https://www.python.org/downloads/), run `pip install selenium`, and download [geckodriver](https://github.com/mozilla/geckodriver/releases) from Mozilla's GitHub, then drag the executable into Gecko Tasks' folder. You may need to install Mozilla Firefox if you don't have it already installed.

After doing all of that, you'll likely want to check out `Tasks.json` and change the options there to your liking. Run `python RequestHandler.py` to run Gecko Tasks after creating your own Task Flow, or to run the example that Gecko Tasks comes shipped with to make sure everything is working as intended.
