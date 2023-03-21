from View import View, CTk

if __name__ == '__main__':
    root = CTk.CTk()  # root object (pop up window)
    root.title("Ground Control Station")
    view = View(root, master=root)
    root.mainloop()
