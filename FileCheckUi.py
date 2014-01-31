from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.scrollview import ScrollView

import CsvTest

class FileCheckUi(App):
    tv = None
    error = None
    missing = None


    def build(self):
        l = BoxLayout(orientation='vertical')
        b = Button(text='Run')
        b.bind(on_press=self.btn_run)
        b.size_hint = 1, 1
        sv = ScrollView()
        sv.size_hint = 1, 10
        self.tv = TreeView(root_options=dict(text='Results'))
        self.tv.size_hint = 1, None 
        self.tv.bind(minimum_height = self.tv.setter('height')) 
        self.error = self.tv.add_node(TreeViewLabel(text='Errors'))
        self.mssing = self.tv.add_node(TreeViewLabel(text='Missing'))
        sv.add_widget(self.tv)
        l.add_widget(b)
        l.add_widget(sv)
        return l

    def list2tree(self, lst, tvn):
        for t in lst:
           print t
           self.tv.add_node(TreeViewLabel(text=t), tvn)
 
    def report(self, error, missing):
        self.report_clear ()
        self.list2tree(error, self.error )
        self.list2tree(missing, self.missing)     

    def report_clear(self):
        print 'x'
        if self.error != None:
            while len (self.error.nodes) > 0:
                print ' Error',len (self.error.nodes)
                x = self.error.nodes[0]
                self.tv.remove_node(x)
                print ' Error', len (self.error.nodes)
        if self.missing != None:
            for w in self.missing.nodes:
                self.tv.remove_node(w)
        
    def btn_run(self, value):
        fdb = '/sdcard/Download/filedb.csv'
        dw = None
        dw = CsvTest.DirWalker ()
        dw.filedb.load( fdb)
        dw.walk ( '/sdcard/Download')
        dw.filedb.save (fdb)
        self.report( dw.errors, dw.filedb.not_visited())
        
        

if __name__ == '__main__':
    FileCheckUi().run()