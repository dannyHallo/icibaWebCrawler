import requests
from bs4 import BeautifulSoup
import bs4
import time
import sys

sys.path.append("你的模块路径")


def load_words():
    with open('1.txt') as word_file:
        valid_words = set(word_file.read().split())

    return valid_words


def get_Colins_Soup(word):
    global startingPoint
    kv = {
        # type 'about:version' in the browser, pretending to be a real browser
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/81.0.4044.129 Safari/537.36 '
    }
    url = 'http://www.iciba.com/' + word
    try:
        r = requests.get(url, headers=kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, "html.parser")
        return soup.div.find(attrs={"class": "collins-section"})
    except:
        print("404!")
        time.sleep(2)
        # startingPoint = int(input("where to start?"))
        startingPoint = latest
        main()



def get_number_of_M(soup):
    count = 0
    for i in soup.find_all(attrs={"class": "prep-order-icon"}):
        if isinstance(i, bs4.element.Tag):
            if i.string != '':
                count += 1
    return count


def get_family_english(soup):
    global startingPoint
    list = []
    alist = []
    flist = []
    for a in range(65, 92):
        alist += chr(a)
    alist = tuple(alist)
    try:
        for i in soup.find_all(attrs={"class": 'family-english'}):
            if i is not None:
                list += i
        strrr = ''
    except:
        print("Sorry, I cannot find the meaning of this word.")
        with open('2.txt', 'a+', encoding='utf-8') as f:
            f.write("%d" % startingPoint + '\r\n')
            f.write('Sorry, I cannot find this word \r\n')
        f.close()
        print("404!")
        time.sleep(2)
        startingPoint = latest + 1
        main()

    for sen in list:
        ss = str(sen)
        if ss.endswith(alist):
            strrr += sen + ' '
    flist = strrr.split(' ')
    flist.pop()
    return flist


def get_family_english_meaning(soup):
    list = []
    for i in soup.find_all(attrs={"class": 'family-english size-english prep-en'}):
        if i != None:
            list += i
    return list


def get_family_chinese(soup):
    list = []
    alist = []
    flist = []
    for i in soup.find_all(attrs={"class": 'family-chinese size-chinese'}):
        list += i
    for j in soup.find_all(attrs={"class": 'family-chinese'}):
        alist += j
    for a in alist:
        if a not in list:
            flist.append(a)
            # avoid add the Chinese meaning of the sentences, but add the word meanings
    return flist


def main():
    global startingPoint
    global latest
    count = startingPoint - 1
    for word in words[startingPoint - 1:]:
        count = count + 1
        print(count)

        latest = count

        # time.sleep(1)

        listA = []
        listB = []
        listC = []
        soup = get_Colins_Soup(word)
        # n = get_number_of_M(soup)

        listA = get_family_english(soup)
        n = len(listA)
        listB = get_family_english_meaning(soup)
        listC = get_family_chinese(soup)
        meaning = []
        if listA != []:
            for i in range(n):
                try:
                    print(listA[i])
                    print(listB[i])
                    print(listC[i])
                    print()
                    with open('2.txt', 'a+', encoding='utf-8') as f:
                        if i == 0:
                            f.write("%d" % count + '\r\n')
                        f.write(listA[i] + '\r\n')
                        f.write(listB[i] + '\r\n')
                        f.write(listC[i] + '\r\n')
                    f.close()
                except:
                    print("Sorry, I cannot find the meaning of this word.")
                    with open('2.txt', 'a+', encoding='utf-8') as f:
                        f.write("%d" % count + '\r\n')
                        f.write('Sorry, I cannot find this word \r\n')
                    f.close()
        else:
            print("Sorry, I cannot find the meaning of this word.")
            with open('2.txt', 'a+', encoding='utf-8') as f:
                f.write("%d" % count + '\r\n')
                f.write('Sorry, I cannot find this word \r\n')
            f.close()


global startingPoint
global latest
words = []
for line in open('popular.txt', 'r'):
    rs = line.replace('\n', '')
    words.append(rs)
print(len(words))
startingPoint = int(input("where to start?"))
try:
    main()
except:
    print("404!")
    time.sleep(2)
    # startingPoint = int(input("where to start?"))
    startingPoint = latest
    main()

