from View import View, CTk

# point of execution for the GUI package. The file creates a View and CustomTkinter object to run the GUI
if __name__ == '__main__':
    root = CTk.CTk()  # root object (pop up window)
    root.resizable(0,0)
    root.title("Ground Control Station")
    view = View(root, master=root)
    view.update_label()
    root.mainloop()
