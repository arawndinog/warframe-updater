fname = 'VoidPCAsh.txt'
output = open('lua_output.txt', 'w')

with open(fname, 'r') as origin:
	tower_type = ""
	for line in origin:
		if 'TOWER' in line:
			tower_type = line
			continue
		elif not line.isspace():
			line.partition(" PRIME ")[0]
		output.write(tower_type + line)