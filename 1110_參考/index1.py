import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datasource1
from threading import Timer
from youbikeTreeView import YoubikeTreeView


class Window(tk.Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #------interface-----#
        topFrame = tk.Frame(self, relief=tk.GROOVE, borderwidth=1)
        tk.Label(
            topFrame,
            text="pm2.5",
            font=("arial", 20),
            bg="#333333",
            fg="#ffffff",
            padx=10,
            pady=10,
        ).pack(padx=20, pady=20)
        topFrame.pack(pady=30)

        #------create search frame-----#
        middleFrame = ttk.Labelframe(self, text="搜尋")
        tk.Label(middleFrame, text="城市名稱搜尋").pack(
            side="left", pady=5
        )
        search_entry = tk.Entry(
            middleFrame
        )
        search_entry.bind("<KeyRelease>", self.onEntryClick)
        search_entry.pack(side="left")

        middleFrame.pack(fill="x", padx=20)

        #-------treeview-----#
        bottomFrame = tk.Frame(self)
        self.youbikeTreeView = YoubikeTreeView(
            bottomFrame,
            columns=("site", "county", "pm25", "datacreationdate"),
            show="headings",
            height=20,
        )
        self.youbikeTreeView.pack(side="left")

        #------scrollbar-----#
        self.scrollbar = ttk.Scrollbar(
            bottomFrame, orient="vertical", command=self.youbikeTreeView.yview
        )
        self.scrollbar.pack(side="left", fill="y")
        self.youbikeTreeView.configure(yscrollcommand=self.scrollbar.set)

        bottomFrame.pack(pady=(15, 30), padx=20)

    #------抓出使用者輸入的值-----#
    def onEntryClick(self, event):
        searchEntry = event.widget
        input_value = searchEntry.get()
        if input_value == "":
            lastest_data = datasource1.lastest_datetime_data()
            self.youbikeTreeView.update_content(site_datas=lastest_data)
        else:
            search_data = datasource1.search_sitename(word=input_value)
            self.youbikeTreeView.update_content(site_datas=search_data)


def main():
    def update_data(w: Window) -> None:
        try:
            datasource1.update_render_data()

        except Exception:
            messagebox.showerror("錯誤", "將關閉應用程式\n請稍後再試")

        lastest_data = datasource1.lastest_datetime_data()
        w.youbikeTreeView.update_content(lastest_data)
        
        t = Timer(6, update_data, args=(window,))
        t.start()

    window = Window()
    window.title("台北市youbike2.0")
    window.resizable(width=False, height=False)

    #------update treeview data-----#
    lastest_data = datasource1.lastest_datetime_data()
    window.youbikeTreeView.update_content(lastest_data)
    t = Timer(1, update_data, args=(window,))
    t.start()
    window.mainloop()


if __name__ == "__main__":
    main()