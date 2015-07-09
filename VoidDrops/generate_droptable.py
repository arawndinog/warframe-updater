import argparse
import time

prime_access = 'Ash'

def rw_lua(fname,output):
	output = open(output, 'w')
	with open(fname, 'r') as origin:
		output.write("--Last update: " + time.strftime("%d/%m/%Y") + "\n")
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
					
					
def parseArgs():
	parser = argparse.ArgumentParser(description='Generate Lua format table from forum Void drop tables.\nYou will need three files for input: PC, PS and XB. Format being AshVoidPC.txt.')
	parser.add_argument('prime_access', help='Prime Access Warframe name.')
	args = parser.parse_args()
	return args
	
def main():
	wf_name = parseArgs()
	rw_lua(wf_name.prime_access + 'VoidPC.txt', wf_name.prime_access + '_lua_output_PC.txt')
	rw_lua(wf_name.prime_access + 'VoidPS.txt', wf_name.prime_access + '_lua_output_PS.txt')
	rw_lua(wf_name.prime_access + 'VoidXB.txt', wf_name.prime_access + '_lua_output_XB.txt')

main()