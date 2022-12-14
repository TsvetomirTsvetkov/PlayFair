# External imports
from tkinter import *
from tkinter import ttk, messagebox

# Internal imports
from .playfair import PlayFair


class GUI:
    '''Class containing the GUI for the program'''

    def __init__(self):
        # Create the TK object
        self.root = Tk()

        # Set the title of the window
        self.root.title('PlayFair')

        # Prepare the window
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Create the plain text field
        self.plain_text = StringVar()
        self.plain_text_entry = ttk.Entry(self.mainframe, width=25, textvariable=self.plain_text)
        self.plain_text_entry.grid(column=2, row=1, sticky=E)

        # Create the key field
        self.key_text = StringVar()
        self.key_text_entry = ttk.Entry(self.mainframe, width=25, textvariable=self.key_text)
        self.key_text_entry.grid(column=2, row=2, sticky=(W, E))

        # Create the cipher text field
        self.cipher_message = StringVar()
        self.cipher_text_entry = ttk.Entry(self.mainframe, width=25, textvariable=self.cipher_message)
        self.cipher_text_entry.grid(column=2, row=3, sticky=(W, E))

        # Create the encrypt button
        self.encrypt_button = ttk.Button(self.mainframe, text="Encrypt", command=self.encrypt)
        self.encrypt_button.grid(column=4, row=1, sticky=E)

        # Create the decrypt button
        self.decrypt_button = ttk.Button(self.mainframe, text="Decrypt", command=self.decrypt)
        self.decrypt_button.grid(column=4, row=2, sticky=E)

        # Create the quit button
        self.quit_button = ttk.Button(self.mainframe, text="Quit", command=self.root.destroy)
        self.quit_button.grid(column=4, row=3, sticky=E)

        # Set the labels for the fields
        self.label_message = ttk.Label(self.mainframe, text="Message").grid(column=1, row=1, sticky=W)
        self.label_key = ttk.Label(self.mainframe, text="Key").grid(column=1, row=2, sticky=E)
        self.label_cipher = ttk.Label(self.mainframe, text="Cipher").grid(column=1, row=3, sticky=E)

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.plain_text_entry.focus()

        self.encrypt_button.bind('<Return>', self.encrypt)
        self.decrypt_button.bind('<Return>', self.decrypt)

    def encrypt(self):
        key = self.key_text_entry.get()
        plain_text = self.plain_text_entry.get()

        try:
            self.playfair = PlayFair(key=key, plain_text=plain_text)
            cipher = self.playfair.encrypt()
            self.cipher_message.set(cipher)
        except Exception as err:
            messagebox.showerror(title='Error', message=err)

    def decrypt(self):
        key = self.key_text_entry.get()
        cipher_text = self.cipher_text_entry.get()

        try:
            self.playfair = PlayFair(key=key, cipher_text=cipher_text)
            plain_text = self.playfair.decrypt()
            self.plain_text.set(plain_text)
        except Exception as err:
            messagebox.showerror(title='Error', message=err)

    def start_gui(self):
        # Start the mainloop
        self.root.mainloop()
