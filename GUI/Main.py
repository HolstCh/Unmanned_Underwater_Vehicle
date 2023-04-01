from View import View, CTk

if __name__ == '__main__':
    root = CTk.CTk()  # root object (pop up window)
    root.geometry("850x700")
    root.resizable(0,0)
    root.title("Ground Control Station")
    view = View(root, master=root)
    root.mainloop()
