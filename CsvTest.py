import csv
import hashlib
from functools import partial
from os.path import walk, isfile, join

class FileDb:
    mapping = dict ()

    def calc_attributes (self, filename):
        md5 = hashlib.md5()
        with open ( filename, 'rb') as f:
            for c in iter (partial (f.read, 1024), ''):
                md5.update (c)
        return md5.hexdigest()

    def add (self, filename, attributes):
        self.mapping [filename] = attributes

    def check (self, filename):
        attr = self.calc_attributes (filename )
        if filename in self.mapping:
            if self.mapping [ filename ] == attr:
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
                writer.writerow ([f, self.mapping [f]])

    def load (self, filename):
        with open ( filename, 'rb') as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
            for entry in reader:
                self.mapping [entry [0]] = entry[1]

    def dump (self):
        print self.mapping



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
#dw.filedb.dump ()
dw.filedb.save (fdb)





