from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.scrollview import ScrollView

import CsvTest

class FileCheckUi(App):
    tv = None


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
        sv.add_widget(self.tv)
        l.add_widget(b)
        l.add_widget(sv)
        return l

    def list2tree(self, lbl, lst):
        tvn = self.tv.add_node(TreeViewLabel(text=lbl))
        for t in lst:
           self.tv.add_node(TreeViewLabel(text=t), tvn)
 
    def report(self, added, error, missing):
        self.report_clear ()
        self.list2tree ('Added', added)
        self.list2tree('Error', error)
        self.list2tree('Missing', missing)     

    def report_clear(self):
        while len (self.tv.root.nodes) > 0:
                self.tv.remove_node (self.tv.root.nodes[0])
 
    def btn_run(self, value):
        fdb = '/sdcard/Download/filedb.csv'
        self.dw = None
        self.dw = CsvTest.DirWalker ()
        self.dw.filedb.load( fdb)
        self.dw.walk ( '/sdcard/Download')
        self.dw.filedb.save (fdb)
        self.report( self.dw.filedb.added,
            self.dw.filedb.errors, 
            self.dw.filedb.not_visited())
        
        

if __name__ == '__main__':
    FileCheckUi().run()