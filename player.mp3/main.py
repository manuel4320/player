from tkinterdnd2 import TkinterDnD
from interface import GraphicalInterface

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = GraphicalInterface(root)
    root.mainloop()
