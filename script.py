import contextlib
import tkinter as tk
from tkinter import ttk
import time, os
import customtkinter
import ctypes
import tksvg
from win32mica import MICAMODE, ApplyMica
#from BlurWindow.blurWindow import GlobalBlur
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk


PATH = os.path.dirname(os.path.realpath(__file__))
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("./assets/dark-theme.json")
default_path = os.getcwd()

class Countdown(customtkinter.CTkFrame):
    def __init__(self, parent=None, seconds=0):
        customtkinter.CTkFrame.__init__(self, parent, fg_color="#000000")
        self._start = 0.0
        self._elapsedtime = seconds
        self._running = 0
        self.timestr = tk.StringVar()
        self._savedtime = 0.0
        self.makeWidgets()

    def makeWidgets(self): 
        
        self.play_image = self.load_image("/assets/play_image.svg")
        self.pause_image = self.load_image("/assets/pause_image.svg")
        self.reset_image = self.load_image("/assets/reset_image.svg")
        self.settings_image = self.load_image("/assets/settings_image.svg")
        self.close_image = self.load_image("/assets/close_image.svg")
        self.save_image = self.load_image("/assets/save_image.svg")

        self.l = customtkinter.CTkLabel(self, textvariable=self.timestr, text_color="#DDE6E8", text_font=("Segoe UI", 45, "bold"))
        self._setTime(self._elapsedtime)
        self.l.pack(fill=tk.X, expand=tk.NO, pady=2, padx=2)

        self.f = customtkinter.CTkFrame(self, fg_color="#000000")
        self.f.pack(fill=tk.X, expand=tk.NO, pady=2, padx=2)
        
        self.start = customtkinter.CTkButton(self.f, text=None, image=self.play_image, text_color="#DDE6E8", command=self.Start, width=38, height=38)
        self.reset = customtkinter.CTkButton(self.f, text=None, image=self.reset_image, text_color="#DDE6E8", command=self.Reset, width=38, height=38)
        
        self.settings = customtkinter.CTkButton(self.f, text=None, image=self.settings_image, command=self.Settings, width=38, height=38)
        
        self.settings.pack(side=tk.RIGHT, padx=20, pady=10)
        self.start.pack(side=tk.LEFT, padx=20, pady=10)
        self.reset.pack(side=tk.BOTTOM, padx=20, pady=10)

    def _update(self):
        if round(self._elapsedtime) == 0:
            self.Pause() 
            self.start.configure(image=self.play_image)
        else:
            self._elapsedtime = self._start - time.time()
            self._setTime(self._elapsedtime)
            self._timer = self.after(50, self._update)

    def _setTime(self, elap):
        minutes, seconds = divmod(elap, 60)
        hours, minutes = divmod(minutes, 60)
        if hours <= 0:
            self.timestr.set('%02d:%02d' % (minutes, seconds))
        else:
            self.timestr.set('%02d:%02d:%02d' % (hours, minutes, seconds))

    def Start(self):
        if not self._running and self._elapsedtime != 0.0:
            self.reset.configure(image=self.reset_image)
            self._start = time.time() + self._elapsedtime
            self._update()
            self._running = 1
            self.start.configure(image=self.pause_image)
            self.start.configure(command=self.Pause)
        else:
            self.Pause()

    def Pause(self):
        if self._running:
            self.after_cancel(self._timer)
            self._elapsedtime = self._start - time.time()
            self._setTime(self._elapsedtime)
            self._running = 0
            self.start.configure(image=self.play_image)
            self.start.configure(command=self.Start)

    def Reset(self):
        self.Pause() 
        self._start = time.time()
        self._elapsedtime = self._savedtime
        self._setTime(self._elapsedtime)
        self.start.configure(image=self.play_image)
        
    
    def saveTime(self, time):
        self._savedtime = time

    def quit_window(self):
        self.icon.stop()
        root.destroy()


    def show_window(self):
        self.icon.stop()
        root.after(0,root.deiconify())


    def hide_window(self):
        global default_path
        root.withdraw()
        self.image=Image.open("./assets/icon_time11.ico")
        self.menu=(item('Show', self.show_window), item('Quit', self.quit_window))
        self.icon=pystray.Icon("name", self.image, "Time11 Hidden", self.menu)
        self.icon.run()
        
    def load_image(self, path):
        return tksvg.SvgImage(file=(PATH + path))
    
    def entrySave(self):
        entryTimer = self.settings_entry.get()
        with contextlib.suppress(ValueError):
            if int(entryTimer) > 0:
                self._elapsedtime = float(entryTimer)
                self._setTime(self._elapsedtime)
                self.saveTime(self._elapsedtime)
        self.settings_window.destroy()
        
    def Settings(self):
        self.Pause()
        self.settings_window = customtkinter.CTkToplevel(self)
        self.settings_window.title("")
        self.settings_window.geometry("250x140")
        x = root.winfo_x()
        y = root.winfo_y()
        self.settings_window.geometry("+%d+%d" % (x + 85, y))
        self.settings_window.deiconify()
        ApplyMica(HWND=ctypes.windll.user32.GetForegroundWindow(),ColorMode=MICAMODE.DARK)
        self.settings_window.update()
        self.settings_window.iconbitmap(f"{default_path}/assets/icon_time11.ico")
        self.settings_window.wm_attributes("-topmost", 1)
        self.settings_window.grab_set()
        self.settings_window.focus_set()
        self.settings_window.protocol("WM_DELETE_WINDOW", self.settings_window.destroy)


        self.settings_frame = customtkinter.CTkFrame(self.settings_window)
        self.settings_frame.pack(fill=tk.X, expand=tk.NO, pady=2, padx=2)

        self.settings_label = customtkinter.CTkLabel(self.settings_frame, text="Set time:", text_color="#DDE6E8", text_font=("Segoe UI", 12))
        self.settings_label.pack(fill=tk.X, expand=tk.NO, pady=2, padx=2)

        self.settings_entry = customtkinter.CTkEntry(self.settings_frame, textvariable=None, placeholder_text="  Time in seconds", text_color="#DDE6E8", text_font=("Segoe UI", 11))
        self.settings_entry.pack(side=tk.TOP, padx=20, pady=10)

        self.settings_save = customtkinter.CTkButton(self.settings_frame, text=None, image=self.save_image, text_color="#DDE6E8", width=38, height=38, command= lambda:self.entrySave())
        self.settings_save.pack(side=tk.LEFT, padx=30, pady=10)

        self.settings_cancel = customtkinter.CTkButton(self.settings_frame, text=None, image=self.close_image, text_color="#DDE6E8", width=38, height=38, command=self.settings_window.destroy)
        self.settings_cancel.pack(side=tk.RIGHT, padx=30, pady=10)

        
        
if __name__ == '__main__':
    root = customtkinter.CTk()
    root.title('')
    root.iconbitmap("./assets/icon_time11.ico")
    root.geometry("420x150")
    root.resizable(False, False)
    root.eval('tk::PlaceWindow . center')
    root.configure(bg="#000000")
    root.deiconify()
    ApplyMica(HWND=ctypes.windll.user32.GetForegroundWindow(),ColorMode=MICAMODE.DARK)
    root.update()
    #GlobalBlur(ctypes.windll.user32.GetForegroundWindow(),hexColor="#1f1f1f00",Acrylic = True)
    #root.protocol('WM_DELETE_WINDOW', Countdown().hide_window)
    Countdown(root,10).pack()
    root.mainloop()
    
