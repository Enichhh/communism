from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
from database import Databaase
import threading
import subprocess

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Enoch Gabriel Astor\Desktop\Arisuu-main\ASSETS\Login_assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def opencashier():
    # Use Popen to open the cashier window without blocking
    subprocess.Popen(["python", "cashier.py"])

def handle_login():
    username = entry_1.get()
    password = entry_2.get()
    
    db = Databaase()  # Create a database instance
    if db.login(username, password):
        print("Login successful, opening cashier...")  # Debugging output
        threading.Thread(target=opencashier).start()  # Correctly call the function
        window.after(3000, window.withdraw) # Then close the login window
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")
        
window = Tk()
window.title("Login")
window.geometry("1280x800")
window.configure(bg="#FFFFFF")

canvas = Canvas(window, bg="#FFFFFF", height=800, width=1280, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0) 
canvas.create_rectangle(0.0, 0.0, 1280.0, 800.0, fill="#97BCC7", outline="")
canvas.create_rectangle(136.0, 98.0, 1145.0, 702.0, fill="#FFFFFF", outline="")

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=button_image_1, borderwidth=0, highlightthickness=0, command=handle_login, relief="flat")

button_1.place(x=874.0, y=476.0, width=215.0, height=71.0)

canvas.create_text(257.0, 143.0, anchor="nw", text="Log In", fill="#01174A", font=("ShareTechMono Regular", 36 * -1))

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(331.0, 452.0, image=image_image_1)

canvas.create_text(597.0, 316.0, anchor="nw", text="Password", fill="#01174A", font=("ShareTechMono Regular", 36 * -1))

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(829.0, 392.0, image=image_image_2)

canvas.create_text(606.0, 189.0, anchor="nw", text="User  ", fill="#01174A", font=("ShareTechMono Regular", 36 * -1))

image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(829.0, 270.0, image=image_image_3)

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(862.5, 270.0, image=entry_image_1)

entry_1 = Entry(bd=0, bg="#97BCC7", fg="#000716", highlightthickness=0)
entry_1.place(x=622.0, y=245.0, width=481.0, height=48.0)

entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(862.5, 392.0, image=entry_image_2)
entry_2 = Entry(bd=0, bg="#97BCC7", fg="#000716", highlightthickness=0)
entry_2.place(x=622.0, y=367.0, width=481.0, height=48.0)

window.resizable(False, False)
window.mainloop()