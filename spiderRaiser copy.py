import sys
import os
from sortedcontainers import SortedList
import re
from queue import LifoQueue

# print(sys.argv.__len__())
verbose = False
if sys.argv.__len__() == 5:
    if sys.argv[4] == '-v':
        verbose = True

elif sys.argv.__len__() != 4:
    print(
        "Usage: python3 spiderRaiser.py [start url (not end with '/')] [url filter] [spider output folder (end with '/)] ([-v] for verbose mode)")
    exit()

start = sys.argv[1]  # the start url
discovered = SortedList()  # list of all urls
blacklist = SortedList()  # list of urls that leads to nowhere
unchecked = LifoQueue()  # stack of unchecked urls
discovered.add(start)

header = "gtimeout --signal=KILL 5 scrapy runspider -a \"url="
middle = "\" -O \""
if verbose:
    ending = "\" \"/Users/sichanghe/Desktop/STATS 210/presentation/spider.py\""  # with log
else:
    ending = "\" \"/Users/sichanghe/Desktop/STATS 210/presentation/spider.py\" --nolog"
nsHead = sys.argv[3]  # output folder
nsTail = ".jl"

template = re.compile(
    '{\"url\": \"('+sys.argv[2]+'.*)\"}')  # filter


def crawl(n):       # n is a url

    ns = nsHead + \
        n.replace(':', '…').replace('/', '÷').replace('%', '∞') + \
        nsTail      # output location

    command = header + n + middle + ns + ending
    if verbose:
        # verbose mode
        print("\nrunning command:")
        print(command)

    os.system(command)      # use scrapy to crawl n
#     searchGened(ns)
# def searchGened(ns):

    # read all urls in the file generated
    try:
        # if readable then n is crawled successfully
        children = template.findall(open(ns).read())
        if children == '':
            discovered.discard(n)
            blacklist.add(n)
            os.remove(ns)
            return

        for child in children:
            if discovered.__contains__(child):  # already in the list
                continue
            if blacklist.__contains__(child):   # already blacklisted
                continue
            discovered.add(child)  # add to list of urls
            unchecked.put(child)  # add to stack of unchecked urls

            # # crawl this new url
            # crawl(child)
    except:
        # if not readable then n is not crawled
        # remove it from the url list
        discovered.discard(n)
        blacklist.add(n)
    finally:
        return


crawl(start)
while not unchecked.empty():
    crawl(unchecked.get())

print("\ndiscovered urls:")
for dis in discovered:
    print(dis)

print("\nblacklist:")
for bla in blacklist:
    print(bla)
