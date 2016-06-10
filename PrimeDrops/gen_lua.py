from datetime import datetime

def main():
    drop_files = ['PC_output.txt','PS4_output.txt','XB1_output.txt']
    lua_output_path = 'lua_output.txt'
    now_date = datetime.now()
    result_str = "--Last update: " + str(now_date.month) + "/" + str(now_date.day) + "/" + str(now_date.year) + "\n\nlocal VoidData = {\n"
    for i in range(len(drop_files)):
        result_str += write_lua(drop_files[i])
    result_str += "}"
    lua_output = open('lua_output.txt', 'w')
    lua_output.write(result_str)
    lua_output.close()
    return

def write_lua(source_path):
    platform = source_path.partition("_")[0]
    drop_str = '["' + platform + '"] = {\n'
    with open(source_path,'r') as source_f:
        for line in source_f:
            if not line.isspace():
                if 'TOWER' in line:
                    location = line.strip().split(" ")
                    tier = "Tower " + location[1]
                    mission = ' '.join(location[2:]).title()
                elif 'DERELICT' in line:
                    location = line.strip().split(" ")
                    tier = "Derelict"
                    mission =  ' '.join(location[2:]).title()
                elif 'Rotation' in line:
                    mission = " " + line.rstrip(":\n").partition(" ")[2]
                else:
                    if 'PRIME' in line:
                        reward = line.strip().partition(" PRIME ")
                        item = reward[0].strip()
                        part = reward[2].strip()
                    else:
                        reward = line.strip().split(" ")
                        item = reward[0].strip()
                        part = ' '.join(reward[1:]).strip()
                    drop_str += '  {"'+ tier + '","' + mission + '","' + item + '","' + part + '"},\n'
        drop_str += "},\n"
    return drop_str
    
if __name__ == '__main__':
    main()