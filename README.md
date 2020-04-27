# Code Names
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=3GBQLRW7D77AG&item_name=Quarantine+Fun&currency_code=USD&source=url)<br><br>
Online version of the popular game from Czech Game Editions optimized for playing over Zoom, Google Hangouts, or a similar video chat program that allows for screensharing.  
<br>Only the person running the Python script needs to have access to the game.  All Spymasters (person giving the clues) need to be able to access their email on a device different than the one being used for the video call.  Because the key for the spymasters is emailed, teh spymaster does not need to be alone to give clues.

## Game Instructions
The game uses the same rules as the board game.  The full game rules can be found [here](https://czechgames.com/en/codenames/). 

1. The person running the Python script shares their screen on the video chat
1. In the command line navigate to the source directory
2. Fom the command line, Run the codeName.py script: `python codeName.py`
3. In the command line, you will be prompted for the email address of the spymaster for Team 1.  Type in the email and click enter.
4. You will then be prompted for the email address of the spymaster for Team 2.  Enter the email and hit enter.
5. Once the emails are entered, the game board should appear.  
6. Click on the words once guesses are made.  The red and blue cards will always represent Team 1 and Team 2, respectively,

## Install Instructions
1. Download the Files from GitHub
2. Install any uninstalled packages such as pygame using `pip install pygame`
3. Rename the config-sample.txt file to config.txt and update the file to have the email address and email password for the email that will be used to send the answer key

## Word List
The list of words is randomly sourced from the [words.txt](data/words.txt) file.  This file is created from several lists of common nouns.  If you do not like a word or want to add your own, you just need to update the words.txt file.

## Future Enhancements
* Ability to start new game without needing to rerun the script
* Switch the team that starts with 9 cards at the start of the  

## Donation
If you enjoyed this game with friends and family, consider buying me a beer.<br><br>
[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/donate/?token=Ykt1I3obDILkn5E6sG5zK7UqLDd9yboLYnW35c4lVtv4NVM3-7v--48XTE9TkWvk3xPGtm&country.x=US&locale.x=)
