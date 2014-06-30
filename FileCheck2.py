import threading
import time

class Database:
    def get_dir(self, path):
        pass # ret mapping list
    
    def get_not_visited():
        pass # ret list
        
    def get_not_ok():
        pass #ret list
        
    def inset(self, path, filename, hashcode, visited, check_ok):
        pass
        
#    def update(self, path, filename, hashcode, visited):
#        pass
        
    def reset_check(self):
        pass
        
    def set_check(path, filename, visited, check_ok):
        pass
       

        

class Status:
    lock = None
    filesdone = 0
    filesleft = 0
    
    def __init__(self):
        self.lock = threading.Lock()
      
    def update(self, filedoneadd, fileleftadd = 0):
        self.lock.acquire()
        self.filesdone = self.filesdone + filedoneadd
        self.fileleft = self.fileleft + fileleftadd
        self.lock.release()
        
    def get(self):
        self.lock.acquire()
        r = (self.left, self.filesdone)
        self.lock.release()
        return r


def md5calc(status, db, files):
    status.update(0, len(files))
    for i in files:
        md5 = hashlib.md5()
        with open ( filename, 'rb') as f:
            for c in iter (partial (f.read, 1024), ''):
                md5.update (c)
        self.md5 = md5.hexdigest()
        db.set_check(i, 
        time.sleep (1)
        #print i        
        status.update(1)
        
        
def show_status(status):
    while threading.active_count() > 2:
        time.sleep(1)
        print status.get()
        


class Checker:
    def run(self, path):
        pass
    




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



