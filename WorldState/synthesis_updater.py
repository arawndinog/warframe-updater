import urllib2
import json
import threading
import re

runtime_minute = 0

def sec_to_dhms (seconds):
    min, sec = divmod(seconds,60)
    hours, min = divmod(seconds/60,60)
    days, hours = divmod(seconds/3600,24)
    return (days, hours, min, sec)

def track_synthesis(data):
    if 'EnemyType' in data['LibraryInfo']['CurrentTarget']:
        current_time = data['Time']
        activation = data['LibraryInfo']['CurrentTarget']['StartTime']['sec']
        duration = current_time - activation
        duration_d, duration_h, duration_m, duration_s = sec_to_dhms(duration)
        p = re.compile('[^/]+$')
        target = p.findall(data['LibraryInfo']['CurrentTarget']['EnemyType'])
        target = target[0]
        scans = data['LibraryInfo']['CurrentTarget']['PersonalScansRequired']
        progress = data['LibraryInfo']['CurrentTarget']['ProgressPercent']
        avg_speed = progress/duration
        time_left = (100-progress)/avg_speed
        time_left_d, time_left_h, time_left_m, time_left_s = sec_to_dhms(time_left)
        print "Current time: " + str(current_time)
        print "Target: " + target
        print "Personal scans required: %d" % scans
        print "Progress (percent): " + str(progress)
        print "Duration (day): %d" % duration_d
        print "Duration (hours): %d" % duration_h
        print "Duration (minutes): %d" % duration_m
        print "Duration (seconds): %d" % duration_s
        print "Average speed (percent per minute): " +  str(avg_speed*60)
        print "Time remaining (days): %d" % time_left_d
        print "Time remaining (hours): %d" % time_left_h
        print "Time remaining (minutes): %d" % time_left_m
        print "Time remaining (seconds): %d" % time_left_s
    else:
        print "Cephalon Simaris is picking a new target."
        pass
            
def parse_json():
    responsePC = urllib2.urlopen('http://content.warframe.com/dynamic/worldState.php', timeout = 40)
    responsePS4 = urllib2.urlopen('http://content.ps4.warframe.com/dynamic/worldState.php', timeout = 40)
    responseXB1 = urllib2.urlopen('http://content.xb1.warframe.com/dynamic/worldState.php', timeout = 40)
    datumPC = json.load(responsePC)
    datumPS4 = json.load(responsePS4)
    datumXB1 = json.load(responseXB1)
    return (datumPC, datumPS4, datumXB1)

def main():
    global runtime_minute
    print "------------------New Entry------------------"
    try:
        parsed_dataPC, parsed_dataPS4, parsed_dataXB1 = parse_json()
        print "--------------PC---------------"
        track_synthesis(parsed_dataPC)
        print "--------------PS4--------------"
        track_synthesis(parsed_dataPS4)
        print "--------------XB1--------------"
        track_synthesis(parsed_dataXB1)
        runtime_minute += 1
    except Exception:
        print "Connection error. No results parsed."
    print
    print "This bot has been run for %d minutes without interruption." % runtime_minute
    print "------------------End Entry------------------"
    print
    threading.Timer(60, main).start()

main()
