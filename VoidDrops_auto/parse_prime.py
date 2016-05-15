from html.parser import HTMLParser
from urllib import request

def main():
    response = request.urlopen('https://forums.warframe.com/forum/3-pc-update-build-notes/')
    parser = MyHTMLParser()
    parser.feed(str(response.read()))


class MyHTMLParser(HTMLParser):
    #def handle_starttag(self, tag, attrs):
    #    if tag == "p":
    #        print("attr:", attrs)
            #print("Encountered a start tag:", tag)

    #def handle_endtag(self, tag):
    #    print("Encountered an end tag :", tag)

    #def handle_data(self, data):
    #    print("Encountered some data  :", data)


if __name__ == '__main__':
    main()
