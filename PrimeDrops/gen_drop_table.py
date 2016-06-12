from html.parser import HTMLParser
from urllib import request
from datetime import datetime
from time import time

def main():
    start_time = time()
    now_date = datetime.now()
    pc_url = "https://forums.warframe.com/forum/3-pc-update-build-notes/"
    ps_url = "https://forums.warframe.com/forum/152-ps4-update-build-notes/"
    xb_url = "https://forums.warframe.com/forum/253-xb1-update-build-notes/"
    pc_drop_list = gen_drop_list(pc_url)
    print("Parsed PC drop list.")
    ps_drop_list = gen_drop_list(ps_url)
    print("Parsed PS4 drop list.")
    xb_drop_list = gen_drop_list(xb_url)
    print("Parsed XB1 drop list.")
    result_str = "--Last update: " + str(now_date.month) + "/" + str(now_date.day) + "/" + str(now_date.year) + "\n\nlocal VoidData = {\n"
    result_str += gen_drop_str(pc_drop_list, 'PC')
    result_str += gen_drop_str(ps_drop_list, 'PS4')
    result_str += gen_drop_str(xb_drop_list, 'XB1')
    result_str += "}"
    lua_output = open('lua_output.lua', 'w')
    lua_output.write(result_str)
    lua_output.close()
    print("Lua table generated.")
    elapsed_time = time() - start_time
    print("Time elapsed: %.3f seconds." % elapsed_time)
    return

def gen_drop_str(drop_list,platform):
    drop_str = '["' + platform + '"] = {\n'
    for i in range(len(drop_list)):
        if 'TOWER' in drop_list[i]:
            location = drop_list[i].split(" ")
            tier = "Tower " + location[1]
            mission = ' '.join(location[2:]).title()
            rotation = ""
        elif 'DERELICT' in drop_list[i]:
            location = drop_list[i].split(" ")
            tier = "Derelict"
            mission =  ' '.join(location[2:]).title()
            rotation = ""
        elif 'Rotation' in drop_list[i]:
            rotation = " " + drop_list[i].rstrip(":").partition(" ")[2]
        else:
            if 'PRIME' in drop_list[i]:
                reward = drop_list[i].partition(" PRIME ")
                item = reward[0]
                part = reward[2]
            else:
                reward = drop_list[i].split(" ")
                item = reward[0]
                part = ' '.join(reward[1:])
            drop_str += '    {"'+ tier + '","' + mission + rotation + '","' + item + '","' + part + '"},\n'
    drop_str += "},\n"
    return drop_str
    

def gen_drop_list(url):
    source = get_source(url)

    link_finder = PrimeLinkFinder()
    link_finder.feed(source)
    drop_link = link_finder.get_links()[0]

    drop_source = get_source(drop_link)

    drop_parser = DropListParser()
    drop_parser.feed(drop_source)
    drop_list = drop_parser.filter_content()

    return drop_list

def get_source(url):
    req = request.Request(url)
    page_source = request.urlopen(req).read().decode('utf-8')
    return page_source

class PrimeLinkFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.target_links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if (attribute == 'href') and ('prime-gear-drop' in value):
                    self.target_links.append(value)

    def get_links(self):
        return self.target_links
        
class DropListParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parsed_content = []

    def handle_starttag(self, tag, attrs):
        if tag == 'article':
            for (attribute, value) in attrs:
                if (attribute == 'class') and ('ipsBox ipsPad' in value):
                    self.parsed_content.append('drop_table_start')

    def handle_endtag(self,tag):
        if tag == 'article':
            self.parsed_content.append('article_ends')

    def handle_data(self, data):
        self.parsed_content.append(data)

    def filter_content(self):
        parsed_list = self.parsed_content
        essence_start = 0
        essence_end = 0
        found_essence = False
        i = 0
        while (found_essence == False) or (parsed_list[i] != 'article_ends'):
            if parsed_list[i].isspace() or not parsed_list[i]:
                del parsed_list[i]
                continue
            elif parsed_list[i] == 'drop_table_start':
                essence_start = i+1
                found_essence = True
            else:
                parsed_list[i] = parsed_list[i].strip()
            i += 1
        essence_end = i
        parsed_list = parsed_list[essence_start:essence_end]
        return parsed_list

if __name__ == '__main__':
    main()
