import urllib2
import json
import threading
import re
import pywikibot
from pywikibot import pagegenerators

docuReplacements = {
    '&params;': pagegenerators.parameterHelp,
}

bot_minute = 0
bot_success = 0

def sec_to_dhms (seconds):
	min, sec = divmod(seconds,60)
	hours, min = divmod(seconds/60,60)
	days, hours = divmod(seconds/3600,24)
	return (days, hours, min, sec)
	
def track_synthesis(data):
	if 'EnemyType' in data['LibraryInfo']['CurrentTarget']:
		data_list = []
		current_time = data['Time']
		data_list.append(current_time)
		p = re.compile('[^/]+$')
		target = p.findall(data['LibraryInfo']['CurrentTarget']['EnemyType'])
		target = target[0]
		data_list.append(target)
		scans = data['LibraryInfo']['CurrentTarget']['PersonalScansRequired']
		data_list.append(scans)
		progress = data['LibraryInfo']['CurrentTarget']['ProgressPercent']
		data_list.append(progress)
		activation = data['LibraryInfo']['CurrentTarget']['StartTime']['sec']
		duration = current_time - activation
		duration_d, duration_h, duration_m, duration_s = sec_to_dhms(duration)
		data_list.append(duration_d)
		data_list.append(duration_h)
		data_list.append(duration_m)
		data_list.append(duration_s)
		avg_speed = progress/duration
		avg_speed_min = avg_speed*60
		data_list.append(avg_speed_min)
		time_left = int((100-progress)/avg_speed)
		remain_d, remain_h, remain_m, remain_s = sec_to_dhms(time_left)
		data_list.append(remain_d)
		data_list.append(remain_h)
		data_list.append(remain_m)
		data_list.append(remain_s)
		print "Current time: " + str(current_time)
		print "Target: " + target
		print "Personal scans required: %d" % scans
		print "Progress (percent): " + str(progress)
		print "Duration: %d days, %d hours, %d minutes, %d seconds." % (duration_d,duration_h,duration_m,duration_s)
		print "Average speed (percent per minute): " +  str(avg_speed_min)
		print "Time remaining: %d days, %d hours, %d minutes, %d seconds." % (remain_d,remain_h,remain_m,remain_s)
		print
		return data_list
	else:
		print "Cephalon Simaris is picking a new target."
		target = "Awaiting New Target"
		data_list = [0,target,0,0,0,0,0,0,0,0,0,0,0]
		return data_list

def parse_json(platform):
	if platform == "PC":
		response = urllib2.urlopen('http://content.warframe.com/dynamic/worldState.php', timeout = 40)
	elif platform == "PS4":
		response = urllib2.urlopen('http://content.ps4.warframe.com/dynamic/worldState.php', timeout = 40)
	elif platform == "XB1":
		response = urllib2.urlopen('http://content.xb1.warframe.com/dynamic/worldState.php', timeout = 40)
	datum = json.load(response)
	return datum
	
def modify_wiki(passed_list, platform):

	data_array = [["current_time",passed_list[0]],
	["target", passed_list[1]],
	["scans", passed_list[2]],
	["progress", passed_list[3]],
	["duration_d", passed_list[4]],
	["duration_h", passed_list[5]],
	["duration_m", passed_list[6]],
	["duration_s", passed_list[7]],
	["speed",	 passed_list[8]],
	["remain_d", passed_list[9]],
	["remain_h", passed_list[10]],
	["remain_m", passed_list[11]],
	["remain_s", passed_list[12]]]
	
	site = pywikibot.Site()
	
	if platform == "PC":
		page = pywikibot.Page(site, u"Template:WorldState/Synthesis/PC")
	elif platform == "PS4":
		page = pywikibot.Page(site, u"Template:WorldState/Synthesis/PS4")
	elif platform == "XB1":
		page = pywikibot.Page(site, u"Template:WorldState/Synthesis/XB1")
	content = page.text
	for i in range(len(data_array)):
		p = re.compile(data_array[i][0]+',(.*?),')
		content = p.sub(data_array[i][0]+','+str(data_array[i][1])+',',content)
	page.text=content
	page.save(u"Update " + platform + " Synthesis status")

def main(*args):
	local_args = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()
	for arg in local_args:
		genFactory.handleArg(arg)
	global bot_minute
	global bot_success
	print "------------------New Entry------------------"
	try:
		
		parsed_data = parse_json("PC")
		synthesis_data = track_synthesis(parsed_data)
		modify_wiki(synthesis_data, "PC")
		print
		
		parsed_data = parse_json("PS4")
		synthesis_data = track_synthesis(parsed_data)
		modify_wiki(synthesis_data, "PS4")
		print
		
		parsed_data = parse_json("XB1")
		synthesis_data = track_synthesis(parsed_data)
		modify_wiki(synthesis_data, "XB1")
		bot_success += 1
	except Exception:
		print "Connection error."
	bot_minute += 1
	print
	print "Runtime: %d minutes." % bot_minute
	print "Success: %d saves." % bot_success
	print "------------------End Entry------------------"
	print
	threading.Timer(60, main).start()

main()