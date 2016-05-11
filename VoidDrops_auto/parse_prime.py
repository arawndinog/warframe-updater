from urllib import request
import io

def main():
    response = request.urlopen('https://forums.warframe.com/forum/3-pc-update-build-notes/')
    parsed_topics = io.StringIO(str(response.read()))
    #link = parsed_updates.find('Prime Gear Drop Locations')
    #print(link)
    result_line = "stuff"
    while 'Prime Gear Drop Locations' not in parsed_topics:
        result_line = parsed_topics.readline()
    print(result_line)

if __name__ == '__main__':
    main()
