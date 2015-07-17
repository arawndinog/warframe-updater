import argparse
import time

def rw_lua(fname,platform,output):
	with open(fname, 'r') as origin:
		output.write('["' + platform + '"] = {\n')
		for line in origin:
			if not line.isspace():
				if 'TOWER' in line:
					location = line.strip().split(" ")
					tier = "Tower " + location[1]
					mission = ' '.join(location[2:]).title()
					rotation = ""
				elif 'DERELICT' in line:
					location = line.strip().split(" ")
					tier = "Derelict"
					mission =  ' '.join(location[2:]).title()
					rotation = ""
				elif 'Rotation' in line:
					rotation = " " + line.rstrip(":\n").partition(" ")[2]
				else:
					if 'PRIME' in line:
						reward = line.strip().partition(" PRIME ")
						item = reward[0].strip()
						part = reward[2].strip()
					else:
						reward = line.strip().split(" ")
						item = reward[0].strip()
						part = ' '.join(reward[1:]).strip()
					output.write('	{"'+ tier + '","' + mission + rotation + '","' + item + '","' + part + '"},\n')
		output.write("},\n")
		
def parseArgs():
	parser = argparse.ArgumentParser(description='Generate Lua format table from forum Void drop tables. You will need three files for input: PC, PS and XB. Format being: AshVoidPC.txt')
	parser.add_argument('prime_access', help='Prime Access Warframe name.')
	args = parser.parse_args()
	return args
	
def main():
	wf_name = parseArgs()
	lua_dest = open(wf_name.prime_access + '_lua_output.txt', 'w')
	lua_dest.write("--Last update: " + time.strftime("%m/%d/%Y") + "\n\nlocal VoidData = {\n")
	rw_lua(wf_name.prime_access + 'VoidPC.txt', "PC",lua_dest)
	rw_lua(wf_name.prime_access + 'VoidPS4.txt', "PS4",lua_dest)
	rw_lua(wf_name.prime_access + 'VoidXB1.txt', "XB1",lua_dest)
	lua_dest.write("}")

main()