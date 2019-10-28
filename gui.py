import tkinter as tk
from main import Instance


class MainWindow(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        self.place(relwidth=1, relheight=1)
        self.parent = parent
        parent.title("Run Simulation From File")

        self.execute = tk.Button(self, text="Run", width=100, command=self.run)
        self.execute.pack()
    def run(self):
        inst = Instance()
        inst.readFile(filename)
        inst.run()
        
if __name__ == "__main__":
    filename = "samplefile.txt"
    

    root = tk.Tk()
    MainWindow(root)
    root.mainloop()