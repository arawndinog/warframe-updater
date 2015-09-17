import urllib2
import json
import threading

runtime_minute = 0
progress_record = []

def sec_to_dhms (seconds):
	min, sec = divmod(seconds,60)
	hours, min = divmod(seconds/60,60)
	days, hours = divmod(seconds/3600,24)
	return (days, hours, min, sec)

def track_synthesis(data):
	if 'EnemyType' in data['LibraryInfo']['CurrentTarget']:
		global progress_record
		current_time = data['Time']
		activation = data['LibraryInfo']['CurrentTarget']['StartTime']['sec']
		duration = current_time - activation
		duration_d, duration_h, duration_m, duration_s = sec_to_dhms(duration)
		target = data['LibraryInfo']['CurrentTarget']['EnemyType']
		progress = data['LibraryInfo']['CurrentTarget']['ProgressPercent']
		avg_speed = progress/duration
		time_left = (100-progress)/avg_speed
		time_left_d, time_left_h, time_left_m, time_left_s = sec_to_dhms(time_left)
		print target
		print "Progress: " + str(progress) + "%"
		print "Duration: %d days, %d hour(s), %d minute(s) and %d second(s)." % (duration_d, duration_h, duration_m, duration_s)
		print "Average speed: " +  str(avg_speed*60) + "% per minute."
		print "Time remaining: ~ %d day(s), %d hour(s), %d minute(s) and %d second(s)." % (time_left_d, time_left_h, time_left_m, time_left_s)
		if (len(progress_record) != 0) and (current_time != progress_record[0]):
			current_speed = (progress - progress_record[1])/(current_time - progress_record[0])
			print "Current speed: " + str(current_speed*60) + "% per minute."
		progress_record = [current_time, progress]
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
		parsed_data = parse_json('pc')
		track_synthesis(parsed_data)
		runtime_minute += 1
	except Exception:
		print "Connection error. No results saved."
	print
	print "This program refreshes every 1 minute."
	print "This bot has been run for %d without interruption." % runtime_minute
	print "------------------End Entry------------------"
	print
	threading.Timer(60, main).start()

main()
#use csv array, record time, calc speed, plot