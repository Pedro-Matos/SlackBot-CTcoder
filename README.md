# SlackBot-CTcoder
Repository for the SlackBot I created for a university-friends channel.


For this bot u need to have Python 2 or 3 installed. 
It's also necessary to have pip and virtualenv.
You can find a complete guide [here](https://www.fullstackpython.com/blog/build-first-slack-bot-python.html), but I will give some insights here.

You should use the command: **virtualenv CTcoder** to create a new virtualenv, and then, everytime u need to put the bot online, activate the virtualenv with this command: **source CTcoder/bin/activate**.

You will also need to get the bot's id from [Slack](https://api.slack.com).

# What does the bot do?

Right now it is possible to ask for the weather in a city. Soon will be added the possibility to see the forecast for that or any other city(5 days forecast). Right know the forecast only works for **Aveiro,PT**

## Commands
* hello weather (shows current temperature for the main Portuguese cities)
* show weather city,country (shows current temperature for the indicated city)
* show forecast city,country (shows 5 days forecast for the indicated city)

