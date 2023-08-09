import tkinter as tk

def button1_click():
    label1.config(text="Button 1 Clicked!")

def button2_click():
    label2.config(text="Button 2 Clicked!")

root = tk.Tk()
root.title("Complex GUI Example")

frame1 = tk.Frame(root)
frame2 = tk.Frame(root)

label1 = tk.Label(frame1, text="Label in Frame 1")
label2 = tk.Label(frame2, text="Label in Frame 2")

button1 = tk.Button(frame1, text="Button 1", command=button1_click)
button2 = tk.Button(frame2, text="Button 2", command=button2_click)

frame1.pack()
frame2.pack()

label1.pack()
button1.pack()
label2.pack()
button2.pack()

root.mainloop()
