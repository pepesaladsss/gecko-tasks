# Gecko Tasks

Gecko Tasks is a simple-to-use program designed to make it significantly easier to get started making programs to crawl or debug websites. It uses Selenium with geckodriver to simulate user behavior, with the optional ability to use a list of proxies for Requesters to use. You can scale it up to as many Requesters as you want using the Tasks.json file which includes all of Gecko Tasks’ configuration options.

Gecko Tasks is **not** a lightweight program by nature. It runs actual browser instances, not *just* web requests. This means that per requester, you could be looking at about 300mb of RAM usage, which you’ll need to consider as you scale up.

## Installation

For installation instructions on Windows and Linux machines, visit the [Gecko Tasks Wiki](https://github.com/pepesaladsss/gecko-tasks/wiki)

Complete list of requirements:
- Python 3.10+ (Earlier will not work)
- Selenium installed via pip
- Firefox installed and its binary on PATH
- Geckodriver v0.30.0+ in PATH or Gecko Tasks' install directory
