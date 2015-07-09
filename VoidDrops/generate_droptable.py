fname = 'AshVoidPC.txt'
output = open('lua_output.txt', 'w')

with open(fname, 'r') as origin:
	for line in origin:
		if not line.isspace():
			if 'TOWER' in line:
				location = line.rstrip().split(" ")
				tier = "Tower " + location[1]
				mission = ' '.join(location[2:]).title()
				rotation = ""
			elif 'DERELICT' in line:
				location = line.rstrip().split(" ")
				tier = "Derelict"
				mission =  ' '.join(location[2:]).title()
				rotation = ""
			elif 'Rotation' in line:
				rotation = " " + line.rstrip(":\n").partition(" ")[2]
			else:
				if 'PRIME' in line:
					reward = line.rstrip().partition(" PRIME ")
					item = reward[0]
					part = reward[2]
				else:
					reward = line.rstrip().split(" ")
					item = reward[0]
					part = ' '.join(reward[1:])
				output.write('	{"'+ tier + '","' + mission + rotation + '","' + item + '","' + part + '"},\n')
