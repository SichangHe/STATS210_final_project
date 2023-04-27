import sys
import os
from sortedcontainers import SortedList
import re
from queue import LifoQueue


#! take arguments and set variables {
verbose = False
if sys.argv.__len__() == 6:
    if sys.argv[5] == '-v':
        verbose = True

elif sys.argv.__len__() != 5:
    print(
        "Usage: python3 spiderRaiser.py [start url (not end with '/')] [url filter] [spider output folder (end with '/')] [spider.py location] ([-v] for verbose mode)")
    exit()

start = sys.argv[1]  # the start url
discovered = SortedList()  # list of all urls
blacklist = SortedList()  # list of urls that leads to nowhere
unchecked = LifoQueue()  # stack of unchecked urls
discovered.add(start)

header = "gtimeout -k 0.001 --signal=KILL 4.01 scrapy runspider -a \"url="
header1 = "gtimeout -k 0.001 --signal=KILL 6.01 scrapy runspider -a \"url="
middle = "\" -O \""
if verbose:
    ending = "\" -s REDIRECT_ENABLED=False -s RETRY_ENABLED=False -s DOWNLOAD_TIMEOUT=4 \"" + \
        sys.argv[4]+"\""  # with log
    ending1 = "\" -s REDIRECT_ENABLED=False -s RETRY_ENABLED=False -s DOWNLOAD_TIMEOUT=6 \"" + \
        sys.argv[4]+"\""  # with log
else:
    ending = "\" -s REDIRECT_ENABLED=False -s RETRY_ENABLED=False -s DOWNLOAD_TIMEOUT=4 --nolog \"" + \
        sys.argv[4]+"\""
    ending1 = "\" -s REDIRECT_ENABLED=False -s RETRY_ENABLED=False -s DOWNLOAD_TIMEOUT=6 --nolog \"" + \
        sys.argv[4]+"\""
nsHead = sys.argv[3]  # output folder
nsTail = ".jl"

template = re.compile(
    '{\"url\": \"('+sys.argv[2]+'.*)\"}')  # filter
#! }

#! main function to crawl a page, save to a file, and read it to add the components into list of url, add to blacklist if failed twice {


def crawl(n):       # n is a url
    #! crawl and save to file {
    ns = nsHead + \
        n.replace(':', '…').replace('/', '÷').replace('%', '∞').replace('?', '¿') + \
        nsTail      # output location

    command = header + n + middle + ns + ending
    if verbose:
        # verbose mode
        print("\nrunning command:")
        print(command)

    os.system(command)      # use scrapy to crawl n
    #! }

    #! open the file and add the components to list of url {
    crawl_failed = False
    try:
        # if readable then n is crawled successfully
        children = template.findall(open(ns).read())
        if children == []:
            if verbose:
                print("file empty")
            crawl_failed = True
        else:
            for child in children:
                if discovered.__contains__(child):  # already in the list
                    continue
                if blacklist.__contains__(child):   # already blacklisted
                    continue
                discovered.add(child)  # add to list of urls
                unchecked.put(child)  # add to stack of unchecked urls
    except:
        # if not readable then n is not crawled
        if verbose:
            print("file not found")
        crawl_failed = True

    #! try again if failed {{
    if crawl_failed:
        #! crawl and save to file {
        command = header1 + n + middle + ns + ending1
        if verbose:             # verbose mode
            print("\ncrawl failed, trying again, running command:")
            print(command)
        os.system(command)      # use scrapy to crawl n
        #! }
        #! open the file and add the components to list of url {
        try:
            # if readable then n is crawled successfully
            children = template.findall(open(ns).read())
            if children == []:  # still empty, give up
                if verbose:
                    print("file empty")
                # fix to a bug here not understood
                if not blacklist.__contains__(n):
                    blacklist.add(n)
                discovered.discard(n)
                os.remove(ns)   # delete the file if empty
            else:
                for child in children:
                    # already in the list
                    if discovered.__contains__(child):
                        continue
                    discovered.add(child)  # add to list of urls
                    unchecked.put(child)  # add to stack of unchecked urls
        except:
            # still not crawled, give up
            if verbose:
                print("file not found")
            # fix to a bug here not understood
            if not blacklist.__contains__(n):
                blacklist.add(n)
            discovered.discard(n)
        #! }}
        #! }
#! }


#! crawl from start recursively and print the crawled url and failed url {
crawl(start)
while not unchecked.empty():
    crawl(unchecked.get())

print("\ndiscovered urls:")
for dis in discovered:
    print(dis)

print("\nblacklist:")
for bla in blacklist:
    print(bla)
#! }
