import argparse
import time

def main():
    #wf_name = parseArgs()
    source_dir = "Drop Lists/"
    # output_dir = "Lua Outputs/"
    lua_dest = open('lua_output.txt', 'w')
    lua_dest.write("--Last update: " + time.strftime("%m/%d/%Y") + "\n\nlocal VoidData = {\n")
    rw_lua(source_dir + 'AshVoidPC.txt', "PC", lua_dest)
    rw_lua(source_dir + 'AshVoidPS4.txt', "PS4", lua_dest)
    rw_lua(source_dir + 'AshVoidXB1.txt', "XB1", lua_dest)
    # rw_lua('PC_output.txt', "PC", lua_dest)
    # rw_lua('PS4_output.txt', "PS4", lua_dest)
    # rw_lua('XB1_output.txt', "XB1", lua_dest)
    lua_dest.write("}")
    return
    
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
                        output.write('  {"'+ tier + '","' + mission + rotation + '","' + item + '","' + part + '"},\n')
            output.write("},\n")
    return
            
# def parseArgs():
#     parser = argparse.ArgumentParser(description='Generate Lua format table from forum Void drop tables.')
#     parser.add_argument('prime_access', help='Prime Access Warframe name.')
#     args = parser.parse_args()
#     return args
    
if __name__ == '__main__':
    main()
