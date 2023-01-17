from View import View, tk

if __name__ == '__main__':
    root = tk.Tk()  # root object (pop up window)
    view = View(root)
    view.pack(side="top", fill="both", expand=True)
    root.mainloop()