import urllib2
import json
import threading
import re
import pywikibot
from pywikibot import pagegenerators

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
		avg_speed_min = avg_speed*60
		time_left = (100-progress)/avg_speed
		time_left_d, time_left_h, time_left_m, time_left_s = sec_to_dhms(time_left)
		print "Current time: " + str(current_time)
		print "Target: " + target
		print "Personal scans required: %d" % scans
		print "Progress (percent): " + str(progress)
		print "Duration: %d days, %d hours, %d minutes, %d seconds." % (duration_d,duration_h,duration_m,duration_s)
		print "Average speed (percent per minute): " +  str(avg_speed_min)
		print "Time remaining: %d days, %d hours, %d minutes, %d seconds." % (time_left_d,time_left_h,time_left_m,time_left_s)
		print
		return (current_time,target,scans,progress,duration_d,duration_h,duration_m,duration_s,avg_speed_min,time_left_d,time_left_h,time_left_m,time_left_s)
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
	
def modify_wiki(passed_list):
	data_array = [["current_time",passed_list[0]],
	["target", passed_list[1]],
	["scans", passed_list[2]],
	["progress", passed_list[3]],
	["duration_d", passed_list[4]],
	["duration_h", passed_list[5]],
	["duration_m", passed_list[6]],
	["duration_s", passed_list[7]],
	["avg_speed_min", passed_list[8]],
	["time_left_d", passed_list[9]],
	["time_left_h", passed_list[10]],
	["time_left_m", passed_list[11]],
	["time_left_s", passed_list[12]]]
	
	site = pywikibot.Site()
	page = pywikibot.Page(site, u"User:ChickenBar/WorldStateTest")
	content = page.text
	for i in range(len(data_array)):
		p = re.compile(data_array[i][0]+',(.*?),')
		content = p.sub(data_array[i][0]+','+str(data_array[i][1])+',',content)
	page.text=content
	page.save(u"Update Synthesis status")

def main():
	print "------------------New Entry------------------"
	global runtime_minute
	parsed_dataPC, parsed_dataPS4, parsed_dataXB1 = parse_json()
	synthesis_data = track_synthesis(parsed_dataPC)
	modify_wiki(synthesis_data)
	print "------------------End Entry------------------"
	print
	threading.Timer(60, main).start()
'''
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
'''

main()
#throttle
#exceptions
#console support