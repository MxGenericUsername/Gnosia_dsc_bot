# Gnosia_dsc_bot
A discord bot for live gnosia games
RUNNING THE BOT:
Linux:
    1.Replace the "#" in the config with your discord bot's token and your discord   
    account's id (or the id of anyone else who'll start the game)
    2.Make a virtual python enviorment (preferrably in a child folder of the bot's 
    folder) with the following packages:
        -enum
        -random
        -discord
        -time
        (and any other packages that the interpreter will complain about being    
        missing if I forgot to mention them here)
    3.Run "sudo PATH/TO/YOUR/VENV/bin/python3 PATH/TO/THE/GNOSIA/BOT/gnosia_bot.py
Windows:
	1.Replace the "#" in the config with your discord bot's token and your discord   
    account's id (or the id of anyone else who'll start the game)
    2.Make a virtual python enviorment (preferrably in a child folder of the bot's 
    folder) with the following packages:
        -enum
        -random
        -discord
        -time
        (and any other packages that the interpreter will complain about being    
        missing if I forgot to mention them here)
	3.Run PATH\TO\YOUR\VENV\Scripts\activate.bat
	4.Run python3 PATH/TO/THE/GNOSIA/BOT/gnosia_bot.py
Windows:
TO START THE GAME: just call !start [a] [b]     where [a] is the number that determines what roles are turned on, and [b] is the amount of gnosia you want in your game. 
To turn on any of the following roles, just add their numbers together and you get [a]
Engineer: 2
Guard Duty: 4
Guardian Angel: 8
AC Follower: 32
Bug: 64
Doctor: 128
