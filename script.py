import tkinter as tk
import time, os
import customtkinter
import ctypes
import tksvg
from BlurWindow.blurWindow import blur,Win7Blur,GlobalBlur
from BlurWindow.blurWindow import GlobalBlur
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("./assets/dark-theme.json")
default_path = os.getcwd()

class Countdown(customtkinter.CTkFrame):
    def __init__(self, parent=None, seconds=0):
        customtkinter.CTkFrame.__init__(self, parent)
        self._start = 0.0
        self._elapsedtime = seconds
        self._running = 0
        self.timestr = tk.StringVar()
        self.makeWidgets()

    def makeWidgets(self):   
        # time label
        self.l = customtkinter.CTkLabel(self, textvariable=self.timestr, text_color="#DDE6E8", text_font=("Segoe UI", 45, "bold"))
        self._setTime(self._elapsedtime)
        self.l.pack(fill=tk.X, expand=tk.NO, pady=2, padx=2)

        # start, stop, reset buttons
        self.f = customtkinter.CTkFrame(self)
        self.start = customtkinter.CTkButton(self.f, text=None, image=tksvg.SvgImage(file="./assets/play_image.svg"), text_color="#DDE6E8", command=self.Start, width=38, height=38, corner_radius=10)
        self.reset = customtkinter.CTkButton(self.f, text=None, image=tksvg.SvgImage(file="./assets/reset_image.svg"), text_color="#DDE6E8", command=self.Reset, width=38, height=38, corner_radius=10)
        
        self.settings = customtkinter.CTkButton(self.f, text=None, image=tksvg.SvgImage(file="./assets/settings_image.svg"), command=self.editTime, width=38, height=38, corner_radius=10)
        
        self.settings.pack(side=tk.RIGHT, padx=20, pady=10)
        self.start.pack(side=tk.LEFT, padx=20, pady=10)
        self.reset.pack(side=tk.BOTTOM, padx=20, pady=10)
        self.f.pack(fill=tk.X, expand=tk.NO, pady=2, padx=2)

    def _update(self):
        print(self._elapsedtime)
        if round(self._elapsedtime) == 0:
            self.Reset()
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
            self._start = time.time() + self._elapsedtime
            self._update()
            self._running = 1
            self.start.config(text='Pause')
            self.start.configure(command=self.Pause)
        else:
            self.Pause()

    def Pause(self):
        if self._running:
            self.after_cancel(self._timer)
            self._elapsedtime = self._start - time.time()
            self._setTime(self._elapsedtime)
            self._running = 0
            self.start.configure(text='Start')
            self.start.configure(command=self.Start)

    def Reset(self):
        self.Pause()
        self._start = time.time()
        self._elapsedtime = 0.0
        self._setTime(self._elapsedtime)
        self.start.configure(text='Start')   
    
    def editTime(self):
        self.dialogBox = customtkinter.CTkInputDialog(master=None, text="Set the time:", title="Timer")
        self._savedtime = int(self.dialogBox.get_input())
        self._elapsedtime = self._savedtime
        self._setTime(self._elapsedtime)

    def quit_window(self, icon, item):
        self.icon.stop()
        root.destroy()


    def show_window(self, icon, item):
        self.icon.stop()
        root.after(0,root.deiconify())


    def hide_window(self):
        global default_path
        root.withdraw()
        self.image=Image.open("./assets/icon_time11.ico")
        self.menu=(item('Show', self.show_window), item('Quit', self.quit_window))
        self.icon=pystray.Icon("name", self.image, "Time11 Hidden", self.menu)
        self.icon.run()

if __name__ == '__main__':
    root = customtkinter.CTk()
    root.title('Time11')
    root.geometry("420x150")
    root.resizable(False, False)
    root.deiconify()
    root.update()
    HWND = ctypes.windll.user32.GetForegroundWindow()
    GlobalBlur(HWND)
    blur(HWND,hexColor="#12121240")
    #root.protocol('WM_DELETE_WINDOW', Countdown().hide_window)
    Countdown(root,10).pack()
    print("ok")
    root.mainloop()
    
