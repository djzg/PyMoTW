#!/usr/bin/env/python3

""" queue - Thread-safe FIFO implementation """

# The queue module provides a first-in, first-out data structure suitable for multi-threaded programming. It can be
# used to pass messages or other data between producer and consumer threads safely. Locking is handled for the caller,
# so many threads can works with the same Queue instance safely and easily. The size of a Queue may be restricted to
# throttle memory usage or processing.

""" Basic FIFO queue """

# Elements are added to one "end" of sequence using put(), and removed from the other end using get().

import queue

q = queue.Queue()

for i in range(5):
    q.put(i)

while not q.empty():
    print(q.get(), end=" ")
print()

# This example uses a single thread to illustrate that elements are removed from the queue in the same order in which
# they are inserted.

""" LIFO queue """

# LIFO queue uses last-in, first-out ordering (normally associated with a stack data structure)

q = queue.LifoQueue()

for i in range(5):
    q.put(i)

while not q.empty():
    print(q.get(), end=" ")
print()

# The item most recently put into the queue is removed by get


""" Priority queue """

# Sometimes the processing order of the items in a queue needs to be based on characteristics of those items, rather
# than just the order they are created or added to the queue. For example, print jobs from the payroll department
# may take precedence over a code listing that a developer wants to print.
# PriorityQueue uses the sort oder of the contents of the queue to decide which item to retrieve.

import functools
import threading

@functools.total_ordering
class Job:
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description
        print("New job:", description)
        return

    def __eq__(self, other):
        try:
            return self.priority == other.priority
        except AttributeError:
            return NotImplemented

    def __lt__(self, other):
        try:
            return self.priority < other.priority
        except AttributeError:
            return NotImplemented

q = queue.PriorityQueue()

q.put(Job(3, "Mid-level job"))
q.put(Job(10, "Low-level job"))
q.put(Job(1, "Important job"))

def process_job(q):
    while True:
        next_job = q.get()
        print("Processing job:", next_job.description)
        q.task_done()

workers = [
    threading.Thread(target=process_job, args=(q,)),
    threading.Thread(target=process_job, args=(q,)),
]

for w in workers:
    w.setDaemon(True)
    w.start()

q.join()

# This example has multiple threads consuming the jobs, which are processed based on the priority of items in the queue
# at the time get() was called. The order of processing for items added to the queue while the consumer threads are
# running depends on thread context switching.


""" Building a threaded podcast client """

# The source code for the podcasting client in this section demonstrates how to use the Queue class with multiple threads.
# The program reads one or more RSS feeds, queues up the enclosures for the five most recent episodes from each feed to
# be downloaded, and processes several downloads in parallel using threads. It does not have enough error handling for
# production use, but the skeleton implementation illustrates the use of the queue module.

# First, some operating parameters are established. Usually, these would come from user inputs (e.g., preferences or a
# database). The example uses hard-coded values for the number of threads and list of URLs to fetch.

from queue import Queue
import time
import urllib
from urllib.parse import urlparse

import feedparser

# set up some global variables
num_fetch_threads = 2
enclosure_queue = Queue()

feed_urls = ["http://talkpython.fm/episodes/rss"]

def message(s):
    print("{}: {}".format(threading.current_thread().name, s))

# the function download_enclosures() runs in the worker thread and processes the downloads using urllib

def download_enclosures(q):
    """This is the worker thread function.
        It processes items in the queue one after
        another.  These daemon threads go into an
        infinite loop, and exit only when
        the main thread ends.
    """
    while True:
        message("looking for the next enclosure")
        url = q.get()
        filename = url.rpartition("/")[-1]
        message("downloading {}".format(filename))
        response = urllib.request.urlopen(url)
        data = response.read()

        # save the downloaded file to the current directory
        message("writing to {}".format(filename))
        with open(filename, "wb") as outfile:
            outfile.write(data)

        q.task_done()

# Once the target function for the threads is defined, the worker threads can be started. When download_enclosures()
# processes the statement url = q.get(), it blocks and waits until the queue has something to return. That means it is
# safe to start th threads before there is anything in the queue.

# set up some threads to fetch the enclosurse
for i in range(num_fetch_threads):
    worker = threading.Thread(
        target=download_enclosures,
        args=(enclosure_queue,),
        name="worker-{}".format(i),
    )
    worker.setDaemon(True)
    worker.start()

# The next step is to retrieve the feed contents using the feedparser module and enqueue the URLs of the enclosures.
# As soon as the first URL is added to the queue, one of the worker threads picks it up and starts downloading it.
# The loop continues to add items until the feed is exhausted, and the worker threads take turns dequeuing URLs
# to download them.

for url in feed_urls:
    response = feedparser.parse(url, agent="fetch_podcasts.py")
    for entry in response["entries"][:5]:
        for enclosure in entry.get("enclosures", []):
            parsed_url = urlparse(enclosure["url"])
            message("queuing {}".format(
                parsed_url.path.rpartition("/")[-1]
            ))
            enclosure_queue.put(enclosure["url"])

# The only thing left to do is wait for the queue to empty out again, using join()

message("*** main thread waiting")
enclosure_queue.join()
message("*** done")

