#coding:utf-8
#author:aedoo
#github:https://github.com/aedoo/

import sys,threading,Queue,time,socket
import ipaddr

class MemCache(threading.Thread):

    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):

        while not self.queue.empty():
            ip = str(self.queue.get(timeout=5))
            port = 11211
            addr = (ip,port)
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

            try:
                s.settimeout(0.5)
                s.connect(addr)

            except Exception:
                s.close()
                continue

            try:
                s.send("stats\r\n")
                result = s.recv(1024)

                if 'STAT version' in result:
                    sys.stdout.write('%s:%d\n' % (ip,port))
            except Exception:
                s.close()
                continue
            s.close()

def main():

    thread_number = 200   #线程数
    threads = []
    queue = Queue.Queue()

    IPDuan = raw_input('Inuput CIDR IP To Scan:')
    ips = ipaddr.IPNetwork(IPDuan)
    for ip in ips:
        queue.put(str(ip))

    for i in xrange(thread_number):
        threads.append(MemCache(queue))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':

    timestart = time.time()
    main()
    timeall = time.time()-timestart
    print 'All Finish, use time:' + str(timeall)
