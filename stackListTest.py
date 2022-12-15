#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 18:15:33 2020

@author: antruong
"""

import tkinter as tk

root = tk.Tk()

def yview(*args):
    """ scroll both listboxes together """
    listbox1.yview(*args)
    listbox2.yview(*args)

listbox1 = tk.Listbox(root)
listbox1.grid(row=1, column=2)
listbox2 = tk.Listbox(root)
listbox2.grid(row=1, column=3)
scrollbary = tk.Scrollbar(root, command=yview)
listbox1.config(yscrollcommand=scrollbary.set)
listbox2.config(yscrollcommand=scrollbary.set)
scrollbary.grid(row=1, column=1, sticky="ns")

for i in range(100):
    listbox1.insert("end","item %s" % i)
    listbox2.insert("end","item %s" % i)

root.mainloop()