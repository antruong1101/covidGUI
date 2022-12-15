#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 14:43:12 2020

@author: antruong
"""

import tkinter as tk

class MultiListbox(tk.Tk):
    def __init__(self, lists):
        super().__init__()
        self.lists = []
        for l in lists:
            frame = tk.Frame(self)
            frame.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
            tk.Label(frame, text=l, borderwidth=1, relief=tk.RAISED).pack(fill=tk.X)
            print(l)
            lb = tk.Listbox(frame, width=w, borderwidth=0, selectborderwidth=0,
                         relief=tk.FLAT, exportselection=tk.FALSE)
            lb.pack(expand=tk.YES, fill=tk.BOTH)
            self.lists.append(lb)
            '''
            lb.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
            lb.bind('<Button-1>', lambda e, s=self: s._select(e.y))
            lb.bind('<Leave>', lambda e: 'break')
            lb.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
            lb.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
            '''
        frame = tk.Frame(self)
        frame.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(frame, borderwidth=1, relief=tk.RAISED).pack(fill=tk.X)
        sb = tk.Scrollbar(frame, orient=tk.VERTICAL)
        #sb.config(command=.yview)
        sb.pack(expand=tk.YES, fill=tk.Y)
        self.lists[0]['yscrollcommand']=sb.set
        
        
    '''
    def _select(self, y):
        row = self.lists[0].nearest(y)
        self.selection_clear(0, tk.END)
        self.selection_set(row)
        return 'break'

    def _button2(self, x, y):
        for l in self.lists: l.scan_mark(x, y)
        return 'break'

    def _b2motion(self, x, y):
        for l in self.lists: l.scan_dragto(x, y)
        return 'break'
    
    def _scroll(self, *args):
        for l in self.lists:
            apply(l.yview, args)
    

    def curselection(self):
        return self.lists[0].curselection()
    '''

    def delete(self, first, last=None):
        for l in self.lists:
            l.delete(first, last)

    '''
    def get(self, first, last=None):
        result = []
        for l in self.lists:
            result.append(l.get(first,last))
        if last: return apply(map, [None] + result)
        return result
    '''
    
    def index(self, index):
        self.lists[0].index(index)

    def insert(self, index, *elements):
        for e in elements:
            i = 0
            for l in self.lists:
                l.insert(index, e[i])
                i = i + 1

    def size(self):
        return self.lists[0].size()
    '''
    def see(self, index):
        for l in self.lists:
            l.see(index)

    def selection_anchor(self, index):
        for l in self.lists:
            l.selection_anchor(index)

    def selection_clear(self, first, last=None):
        for l in self.lists:
            l.selection_clear(first, last)

    def selection_includes(self, index):
        return self.lists[0].selection_includes(index)

    def selection_set(self, first, last=None):
        for l in self.lists:
            l.selection_set(first, last)
    '''

if __name__ == '__main__':
    mlb = MultiListbox((('Subject', 'Sender', 'Date', 10))
    for i in range(1000):
      mlb.insert(tk.END, 
          ('Important Message: %d' % i, 'John Doe', '10/10/%04d' % (1900+i)))
    #mlb.pack(expand=tk.YES,fill=tk.BOTH)
    mlb.mainloop()