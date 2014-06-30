import threading
import time

class Status:
    lock = None
    statusno =0
    
    def __init__(self):
        self.lock = threading.Lock()
      
    def update(self, add):
        self.lock.acquire()
        self.statusno = self.statusno + add
        self.lock.release()
        
    def get(self):
        self.lock.acquire()
        n = self.statusno
        self.lock.release()
        return n


def md5calc(status, args):
    for i in args:
        time.sleep (1)
        #print i        
        status.update(1)
        
        
def show_status(status):
    while threading.active_count() > 2:
        time.sleep(0.5)
        print status.get()
        

status = Status()


slaves = []
for i in range(5):
    t = threading.Thread(target=md5calc, args=(status, [1,2,5]))
    t.start()
    slaves.append(t)


m = threading.Thread(target=show_status, args=(status,))
m.start()
m.join()

for t in slaves:
    t.join()