First, install Python3.9.2 by running the included installer. Make sure to tick the box that says add Python to PATH. Follow instructions to finish install. 

Next, open Command Prompt. You can find it by typing "Command Prompt" in the windows search bar. 
Then, type in "python -v" to check if it's been installed correctly. It should output "Python 3.9.2". 
Then, type in "pip --version" to check pip install. If both output their version then you're good to go

Next, while still in command prompt, type in "pip install beautifulsoup4" press 'Enter'
It should start installing automatically with a lot of lines popping up. It shouldn't take very long.
When it's done do the same with "pip install requests" and "pip install playsound"

After that, open up config.txt and put the direct product links from best buy and newegg in there. 
All you have to do is copy the exact url to the product page from your browser and paste it into the config file.
Once it's pasted in just press enter and repeat with another link from either site. You can have up to 8 links at a time.
I've put a few in there as an example to show you how it should look. You can delete and replace them.

Once all that is completed then you should be ready to go. Run the 'StockChecker.py' file with your newly installed python module and it should begin running.

If you have an issue or need help lemme know and I'll help you out.

---------General Advice---------

- The refresh time on the script is in seconds. Put in whole numbers no decimals.
- Run the script at your own discretion. Newegg does have protections in place to catch bots.
  I haven't been caught using around 45-60 seconds for them. Generally speaking, the shorter the
  refresh time, the higher the likelihood of being caught. Best buy doesn't seem to care about bots. 
- Newegg seems to drop Mon-Fri from 1pm-6pm the most, however it can be at any time. 
  Best Buy drops on Tues, Thurs, Fri at 7am-9am usually. 
  For best results, run the script during these windows. It is more likely to be caught the longer it runs.
- Recommended run times: Newegg - 60 seconds | Best Buy - 20-30 seconds. Use whatever times you're comfortable with though.
