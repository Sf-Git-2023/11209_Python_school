from tkinter import ttk
import tkinter as tk
from tkinter.simpledialog import Dialog

class YoubikeTreeView(ttk.Treeview):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent   #加'self.' -> 實體(attribute) #整個class的任何地方都可以用
        #------設定欄位名稱------#
        self.heading('site', text='城市名稱')
        self.heading('county', text='縣市名稱')
        self.heading('pm25', text='pm25')
        self.heading('datacreationdate', text='時間')

        #------設定欄位寬度------#
        self.column('site', width=80)
        self.column('county', width=80)
        self.column('pm25', width=50)
        self.column('datacreationdate', width=150)

        #------bind button1------#
        self.bind('<ButtonRelease-1>', self.selectedItem)

    def update_content(self,site_datas):
        '''
            更新內容
        '''
        #清除所有內容
        for i in self.get_children():
            self.delete(i)

        for site in site_datas:
            #'end'每插入一筆到最後
            self.insert('','end',values=site)

    def selectedItem(self,event):
        selectedItem = self.focus()
        data_dict = self.item(selectedItem)
        data_list = data_dict['values']
        title = data_list[0]
        detail = ShowDetail(self.parent, data=data_list, title=title)

   
class ShowDetail(Dialog):
    def __init__(self, parent, data, **kwargs):
        self.site = data[1]
        self.county = data[2]
        self.pm25 = data[3]
        self.datacreationdate = data[4]
        super().__init__(parent, **kwargs)
        

    def body(self, master):
        '''
        override body
        '''
        #super().body(master)
        mainFrame = tk.Frame(master)
        mainFrame.pack(padx=100, pady=100)

        #------Label------#
        tk.Label(mainFrame, text='城市名稱').grid(column=0, row=0)
        tk.Label(mainFrame, text='縣市名稱').grid(column=0, row=1)
        tk.Label(mainFrame, text='pm25').grid(column=0, row=2)
        tk.Label(mainFrame, text='時間').grid(column=0, row=3)

        #------Entry------#
        siteVar = tk.StringVar()
        siteVar.set(self.site)
        tk.Entry(mainFrame,textvariable=siteVar, state="disabled").grid(column=1, row=0)

        countyVar = tk.StringVar()
        countyVar.set(self.county)
        tk.Entry(mainFrame,textvariable=countyVar, state='disabled').grid(column=1, row=1)

        pm25Var = tk.StringVar()
        pm25Var.set(self.pm25)
        tk.Entry(mainFrame,textvariable=pm25Var, state='disabled').grid(column=1, row=2)

        datacreationdateVar = tk.StringVar()
        datacreationdateVar.set(self.datacreationdate)
        tk.Entry(mainFrame,textvariable=datacreationdateVar, state='disabled').grid(column=1, row=3)


    def buttonbox(self):
        '''
        override buttonbox
        '''
        box = tk.Frame(self)
        w = tk.Button(box, text="確認", width=10, command=self.ok, default='active')
        w.pack(padx=5, pady=(5,20))
        self.bind("<Return>", self.ok)

        box.pack()