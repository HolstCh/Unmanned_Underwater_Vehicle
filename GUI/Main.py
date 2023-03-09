from View import View, CTk

if __name__ == '__main__':
    root = CTk.CTk()  # root object (pop up window)
    root.title("ChadGPT")
    view = View(root, master=root)
    root.mainloop()
