from View import View, tk

if __name__ == '__main__':
    root = tk.Tk()  # root object (pop up window)
    view = View(root)
    view.grid(column=0, row=1)
    root.mainloop()