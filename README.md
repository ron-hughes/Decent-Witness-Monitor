# Decent-~Miner~-Witness-Monitor
Monitor your missed blocks &amp; public seednode availability for the Decent Blockchain and get notifications on Telegram

This python3 script provides the monitoring of 2 core ~miner~ witness tasks and reports via a telegram bot API call the following:

**1. Monitor missing blocks**
Whenever a new block is missed you will get a notification. This part of the script can (and will) be extended towards automated switching to the backup witness signing key once a threshold is passed.

**2. Monitor the availability of your public seednode**
By utilizing the telnet library the script tries to connect to the given seednode and will report on time-out or errors.

## Dependencies
- [Python Graphenelib by @xeroc](http://python-graphenelib.readthedocs.io/en/latest/)
- A telegram bot token so you can receive notifications
- You need to have and set a websocket WSS url before this script works (I am now using the public one from Decentgo, but you should/could point it to your localhost)

*If you have any remarks/feedback or questions, please let me know! If you find this script useful, feel free to support my ~miner~ witness activities by voting for me on Decent username: `roelandp`.*

Voting via CLI: `vote_for_miner YOURACCOUNT roelandp true true`
