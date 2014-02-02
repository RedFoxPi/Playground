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
        self.missing = self.tv.add_node(TreeViewLabel(text='Missing'))
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
        if self.error != None:
            while len (self.error.nodes) > 0:
                self.tv.remove_node (self.error.nodes[0])
        if self.missing != None:
            while len (self.missing.nodes) > 0:
                self.tv.remove_node(self.missing.nodes[0])
        
    def btn_run(self, value):
        fdb = '/sdcard/Download/filedb.csv'
        self.dw = None
        self.dw = CsvTest.DirWalker ()
        print 'xxx0', self.dw.errors
        self.dw.filedb.load( fdb)
        print 'xxx1', self.dw.errors
        self.dw.walk ( '/sdcard/Download')
        print 'xxx2', self.dw.errors
        self.dw.filedb.save (fdb)
        self.report( self.dw.errors, self.dw.filedb.not_visited())
        
        

if __name__ == '__main__':
    FileCheckUi().run()