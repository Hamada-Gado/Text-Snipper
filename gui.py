import tkinter as tk

from text_snipper import TextSnipper

from ctypes import windll
try:
    windll.shcore.SetProcessDpiAwareness(2) # if your windows version >= 8.1
except:
    windll.user32.SetProcessDPIAware() # win 8.0 or less 

class App:
    
    BACKGROUND_COLOR: str = "gray10"
    
    def __init__(self, args: list[str]) -> None:
        self.master = tk.Tk() 
        self.master.title("Text Snipper")
        
        self.master.attributes("-fullscreen", True)
        self.master.configure(background= App.BACKGROUND_COLOR)
        self.master.resizable(False, False)
        self.master.attributes("-alpha", 0.3)
         
        self.master.bind("<Escape>", lambda _: self.master.destroy())

        self.canvas = tk.Canvas(self.master, bg= App.BACKGROUND_COLOR)
        self.canvas.pack(fill= tk.BOTH, expand= True)
        
        self.master.bind("<Button-1>", self.on_mouse_press)
        self.master.bind("<B1-Motion>", self.on_mouse_motion)
        self.master.bind("<ButtonRelease-1>", self.on_mouse_release)
        
        self.startX: int = -1
        self.startY: int = -1
        self.endX: int = -1
        self.endY: int = -1
        self.text_snipper: TextSnipper = TextSnipper(args[1], args[2:])
        
    def run(self) -> None:
        self.master.mainloop()
        
    @property
    def box(self) -> tuple[int, int, int, int]:
        return (self.startX, self.startY, self.endX, self.endY)
    
    def order_box(self) -> None:
        if self.startX > self.endX:
            self.startX, self.endX = self.endX, self.startX
        if self.startY > self.endY:
            self.startY, self.endY = self.endY, self.startY
        
    def on_mouse_press(self, event: tk.Event) -> None:
        self.startX = event.x
        self.startY = event.y
        
    def on_mouse_motion(self, event: tk.Event) -> None:
        self.endX = event.x
        self.endY = event.y
        
        self.draw_rect()
        
    def on_mouse_release(self, event: tk.Event) -> None:
        self.endX = event.x
        self.endY = event.y
         
        self.master.destroy()
        
        self.order_box()
        
        if self.startX == self.endX or self.startY == self.endY:
            self.text_snipper.getTextFromImage(None)
        else:
            self.text_snipper.getTextFromImage(self.box)    
        
    def draw_rect(self) -> None:
        self.canvas.delete("all")
        self.canvas.create_rectangle(self.box, fill= "gray90", outline= "white")