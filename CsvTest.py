import csv
import hashlib
from functools import partial
from os.path import walk, isfile, join, relpath
 
class FileAttributes:
    '''
    Attributes of a file to be checked and also
    temporary values for processing.
    '''
    # Persistent
    md5 = ''

    # Temporary
    visited = False

    def __init__(self):
        self.md5 =''
        self.visited = False
        
    def reset_visited (self):
        self.visited = False
    
    def to_disk (self):
        return [self.md5]

    def from_disk(self, attr_list):
        if len(attr_list) != 1:
            raise Exception('Unexpected content of file attributes')
        self.md5 = attr_list[0]
        self.visited = False

    def calc(self, filename):
        md5 = hashlib.md5()
        with open ( filename, 'rb') as f:
            for c in iter (partial (f.read, 1024), ''):
                md5.update (c)
        self.md5 = md5.hexdigest()
        self.visited = True

    def compare(self, oattributes):
        self.visited = True
        return self.md5 == oattributes.md5




class FileDb:
    '''
    Associative Storage of filename to its
    attributes/consistency check values.
    Including persistency.
    '''
    mapping = dict ()
    
    errors = []
    added = []
    basepath = ''
    
    def __init__(self, basepath = ''):
        self.basepath = basepath
        self.mapping = dict ( )
        self.reset_visited ()
        
    def relpath(self, abspath):
        return relpath(abspath, self.basepath)
        
    def reset_visited (self):
        self.errors = []
        self.added = []
        for a in self.mapping.itervalues ():
            a.reset_visited ()

    def add (self, filename, attributes):
        self.added.append (filename)
        self.mapping [self.relpath(filename)] = attributes

    def check (self, filename):
        attr = FileAttributes()
        attr.calc(filename)
        relfn = self.relpath(filename)
        if relfn in self.mapping:
            if self.mapping[relfn].compare(attr):
                return True
            else:
                self.errors.append ( filename)
                return False
        else:
            self.add (filename, attr)
            return True


    def save (self, filename):
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            for f in self.mapping:
                writer.writerow ([f] + self.mapping[f].to_disk())

    def load (self, filename):
        self.reset_visited ()
        try:
            with open ( filename, 'rb') as csvfile:
                reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
                for entry in reader:
                    self.mapping[entry[0]] = FileAttributes()
                    self.mapping[entry[0]].from_disk(entry[1:])
        except IOError:
            self.mapping = dict()
            return False
        return True
            

    def dump (self):
        print self.mapping

    def not_visited (self):
        return [ join(self.basepath, i) for i in self.mapping if not self.mapping[i].visited ]



class DirWalker:
    filedb = FileDb ()
    
    def __init__(self, basepath = ''):
        self.filedb = FileDb (basepath)

    def walk (self, dir):
        self.filedb.reset_visited ()
        walk (dir, self.visit, self)

    def visit (self, arg, dirname, names):
        for n in names:
            abspath = join (dirname,  n)
            if isfile ( abspath ):
                self.filedb.check( abspath )
                
            

if __name__ == '__main__':
    #fdb = '/sdcard/Download/filedb.csv'

    bp = 'C:\\Users\\Diana\\Desktop\\Daniel\\'
    fdb = join(bp, 'filedb.csv')
    cdir = join(bp, 'GPS alt')
    
    dw = DirWalker(bp)
    dw.filedb.load(fdb)
    dw.walk(cdir)
    # dw.filedb.dump ()
    dw.filedb.save (fdb)
    print 'Missing   files: ', dw.filedb.not_visited()
    print 'Content changed: ', dw.filedb.errors
    print 'Added     files: ', dw.filedb.added




