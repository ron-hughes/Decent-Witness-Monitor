#!/usr/bin/env python3
import telnetlib
import time, datetime
import requests
import json
import os
import sys
from beemapi.graphenerpc import GrapheneRPC

# witness/delegate/producer account name to check
witness = "praxeaze"
backupsigningkey = ""
witnessurl = "https://twitter.com/praxeaze"

telegram_token = "1085133021:AAHJW2GZUreNsZZcujASWNUpjhiYnUybIwg"	                            # REPLACE_THIS Create your Telegram bot at @BotFather (https://telegram.me/botfather)
telegram_id    = "358913628"                                        # REPLACE_THIS Get your telegram id at @MyTelegramID_bot (https://telegram.me/mytelegramid_bot)

websocket	          	= "wss://blurtseed-se.privex.io:2015" #seednode to connect to! MUST BE DEFINED
seed_host               = ""                    # hostname/ip for the public seed to monitor
seed_port               = 2001                  # port for the public seed to monitor (decent default = 9777)
seed_timeout_check      = int(10)               # seconds before timeout is called on telnet public seed operation.
check_rate              = int(45)               # amount of time (seconds) for the script to sleep before next check! Every x seconds the script will check missed blocks.
check_rate_feeds_seed   = int(3600)             # set this to a considerably higher amount of seconds than check_rate so this script won't check your price_feed and seed availibility as much as that.
currentmisses           = int(0)                # current block misses (note this is set at -1 missed blocks so you will get 1 initial notification if you have more than 0 blocks missed currently. You could set this to your current count of misses to prevent the inital notification)
startmisses             = int(-1)               # global holder of misses at start of script
loopcounter             = int(0)                # this is an internal reference i++ counter needed for correct functioning of the script
tresholdwitnessflip     = int(7)                # after how many blocks the witness should switch to different signing key

walletpwd               = ""                    #encryption key of decent local bip32 wallet with your privkey stored inside.

check_rate_feeds_seed_ratio = round(check_rate_feeds_seed/check_rate, 0)

# Setup node instance
decent = ws = GrapheneRPC(websocket,"","")

# Telegram barebones apicall
def telegram(method, params=None):
    url = "https://api.telegram.org/bot"+telegram_token+"/"
    params = params
    r = requests.get(url+method, params = params).json()
    return r

# Telegram notifyer
def alert_witness(msg):
    # Send TELEGRAM NOTIFICATION
    payload = {"chat_id":telegram_id, "text":msg}
    m = telegram("sendMessage", payload)

# Check availability of Seednode:
def check_seednode():
  try:
    tn = telnetlib.Telnet(seed_host, seed_port,seed_timeout_check)
    print(tn.read_all())
  except Exception as e:
    tel_msg = "Your public seednode for decent is not responding!\n\nat *"+seed_host+"*.\n\n_"+str(e)+"_"
    alert_witness(tel_msg)

# Check how many blocks a witness has missed
def check_witness():
    global currentmisses
    missed = ws.get_witness_by_account(ws.get_account_by_name(witness)['id'])['total_missed']
    print(str(loopcounter)+ ": Missed blocks = " + str(missed))
    if missed > currentmisses:
    # Could create the witness_update transaction and broadcast new signing key here to switch from main to backup
    # For now this script only alerts on telegram...
        alert_witness("You are missing blocks on decent! Your current misses count = "+str(missed)+", which was "+str(currentmisses))
        currentmisses = missed
        #if (currentmisses - startmisses) == tresholdwitnessflip:
            # we have the amount of misses compared to our treshold.... lets flip witnesses to backup.
            #To Be Implemented!

# Main Loop
if __name__ == '__main__':
    alert_witness("starting running monitor for Decent node")
    while True:
        check_witness()
        sys.stdout.flush()
        loopcounter += 1
        if(loopcounter % check_rate_feeds_seed_ratio == 0 and seed_host != ""):
          check_seednode()
        time.sleep(check_rate)
