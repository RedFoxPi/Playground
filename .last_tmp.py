import csv
import hashlib
from functools import partial
from os.path import walk, isfile, join

class FileAttributes:
    '''
    Attributes of a file to be checked and also
    temporary values for processing.
    '''
    # Persistent
    md5 = ''

    # Temporary
    visited = False

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

    def add (self, filename, attributes):
        self.mapping [filename] = attributes

    def check (self, filename):
        attr = FileAttributes()
        attr.calc(filename)
        if filename in self.mapping:
            if self.mapping[filename].compare(attr):
                return True
            else:
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
        with open ( filename, 'rb') as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
            for entry in reader:
                self.mapping[entry[0]] = FileAttributes()
                self.mapping[entry[0]].from_disk(entry[1:])

    def dump (self):
        print self.mapping

    def not_visited (self):
        return [ i for i in self.mapping if not self.mapping[i].visited ]



class DirWalker:
    filedb = FileDb ()


    def walk (self, dir):
        walk (dir, self.visit, self)

    def visit (self, arg, dirname, names):
        for n in names:
            abspath = join (dirname,  n)
            #print abspath
            if isfile ( abspath ):
                if not self.filedb.check( abspath ):
                    print 'Error: Mismatch ', abspath
                
            

fdb = '/sdcard/Download/filedb.csv'

dw = DirWalker ()
dw.filedb.load( fdb)
dw.walk ( '/sdcard/Download')
# dw.filedb.dump ()
print dw.filedb.not_visited()
dw.filedb.save (fdb)





