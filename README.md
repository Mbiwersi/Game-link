# Game_Link
Group Members: Ben Stenberg, Ryan Gallenberg, Andrew Perrin, Michael Biwersi

## What is Game-link
GameLink solves a real problem that Xbox gamers face when playing games with their friends. Microsoft does not provide any way to compare game libraries with multiple friends simultaneously. GameLink solves this problem by providing an interface to provide a game library that you share with whatever friend(s) you select. This way, you can spend less time talking about what game to play, and more time actually playing.

## How Does it work?
Using the OpenXBL API, GameLink accesses Xbox Live data. By providing a Gamertag, it can gather your information about your game library and your friends. You then select friends that you would like to compare game libraries with, and GameLink will compare those libraries and provide a list of games that you and your selected friends all share.

## Teachnologies Used
- Python
- HTML/CSS
- Javascript
- OpenXBL API (https://xbl.io/)
- Flask

## Required Packages:
- requests
- threading
- flask
- functools

To run: Execution begins from GameLink.py. The flask server will begin, and the website should
be hosted on 127.0.0.1:5000. Provided below are some example Gamertags you can enter to try out
our program:
- BenBerg470
- Ryjay84
- Yellowacorn101

All of these Gamertags will yield the same functionality, they are just multiple examples to try out.