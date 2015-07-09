fname = 'VoidPCAsh.txt'
output = open('lua_output.txt', 'w')

with open(fname, 'r') as origin:
	rotation = ""
	for line in origin:
		if 'TOWER' in line:
			location = line.rstrip().split(" ")
			tier = location[0] + " " + location[1]
			mission = ' '.join(location[2:])
			rotation = "" #every time it reaches tower/derelict, rotation refreshes
			continue
		elif 'DERELICT' in line:
			location =  line.rstrip().split(" ")
			tier = location[1]
			mission =  ' '.join(location[2:])
			rotation = ""
			continue
		elif 'Rotation' in line:
			rotation = line.rstrip(":\n").partition(" ")[2]
			continue
		elif not line.isspace():
			reward = line.rstrip().split(" ")
			i = 0
			item = ""
			while (i < len(reward)) and (reward[i] != "PRIME") and (reward[i] != "BLUEPRINT"):
				item += reward[i]
				i += 1
			part = reward[len(reward)-1]
		output.write(tier + "," + mission + " " + rotation + "," + item + "," + part + "\n")