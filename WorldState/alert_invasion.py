import urllib2
import json
import yaml
import threading
#from httplib import BadStatusLine
#import socket
#import csv

runtime_minute = 0

def reward_alerts(data):
    alert_size = len(data['Alerts'])
    if alert_size != 0:
        current_time = data['Time']
        AlertsRewardsListPerMin = []
        for i in range(0,alert_size):
            if 'items' in data['Alerts'][i]['MissionInfo']['missionReward']:
                alert_reward = data['Alerts'][i]['MissionInfo']['missionReward']['items']
                print alert_reward
                AlertsRewardsListPerMin.append(alert_reward)
                expiry = data['Alerts'][i]['Expiry']['sec']
                duration_h, duration_m = divmod((expiry - current_time)/60,60)
                print "%d hours and %d minutes left for this alert." % (duration_h,duration_m)
        if AlertsRewardsListPerMin == []:
            print "There are currently no alerts with item rewards."
        print "There are currently %d ongoing alerts." % alert_size
        return AlertsRewardsListPerMin
    else:
        print "There are currently no alerts."
        pass
        
def reward_invasions(data):
    invasion_size = len(data['Invasions'])
    if invasion_size != 0:
        InvRewardsListPerMin = []
        for j in range(0,invasion_size):
            if data['Invasions'][j]['Completed'] == False:
                reward_exist = False
                if 'countedItems' in data['Invasions'][j]['AttackerReward']:
                    for k in range(len(data['Invasions'][j]['AttackerReward']['countedItems'])):
                        inv_reward = data['Invasions'][j]['AttackerReward']['countedItems'][k]['ItemType']
                        print inv_reward
                        InvRewardsListPerMin.append(inv_reward)
                        reward_exist = True
                if 'countedItems' in data['Invasions'][j]['DefenderReward']:
                    for k in range(len(data['Invasions'][j]['DefenderReward']['countedItems'])):
                        inv_reward = data['Invasions'][j]['DefenderReward']['countedItems'][k]['ItemType']
                        print inv_reward
                        InvRewardsListPerMin.append(inv_reward)
                        reward_exist = True
                if reward_exist == True:
                    inv_count = data['Invasions'][j]['Count'] + .0
                    inv_goal = data['Invasions'][j]['Goal'] + .0
                    if data['Invasions'][j]['Faction'] == 'FC_INFESTATION':
                        completion = 100+round(100*inv_count/inv_goal,2)
                        print str(completion) + "% left of Infestation."
                    else:
                        completion = 50+round(50*inv_count/inv_goal,2)
                        print str(completion) + "% of attacker progress."
        print "There are currently %d invasions." % invasion_size #invasion size includes completed, need fix
        return InvRewardsListPerMin
    else:
        print "There are currently no invasions."
        pass
        
def parse_json(platform):
    if platform == 'pc':
        worldstate = 'http://content.warframe.com/dynamic/worldState.php'
    elif platform == 'ps4':
        worldstate = 'http://content.ps4.warframe.com/dynamic/worldState.php'
    elif platform == 'xb1':
        worldstate = 'http://content.xb1.warframe.com/dynamic/worldState.php'
    response = urllib2.urlopen(worldstate, timeout = 40)
    datum = yaml.load(response)
    return datum
    

def main():
    global runtime_minute
    print "------------------New Entry------------------"
    try:
        parsed_data = parse_json('pc')
        reward_alerts(parsed_data)
        print
        reward_invasions(parsed_data)
        print
        runtime_minute += 1
#       except (urllib2.URLError, socket.timeout, BadStatusLine):
    except Exception:
        print "Connection error. No result saved."
    print "This program refreshes every 1 minute."
    print "Retrieved %d results." % runtime_minute
    print "------------------End Entry------------------"
    print
    threading.Timer(60, main).start()

main()

#last result date
#make array
#save result to csv
#keep track of counters
#if entry not exist then create new entry + start date
#auto calculate drop rate
#calculate speed change of synthesis
