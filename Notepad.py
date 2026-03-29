import tkinter as Tk
from tkinter import messagebox
import sqlite3


class Notepad:
    def __init__(self,root):
      self.root=root
      self.root.title("Notepad")
      self.connection=sqlite3.connect('NotesDatabase.db')
      self.custom=self.connection.cursor()
      self.create_table()
      self.setup_gui()
      
    def create_table(self):
        self.custom.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY,title text ,content text)")
        self.connection.commit()
        
    def setup_gui(self):
        #Title
        Tk.Label(self.root,text="Title").pack()
        self.enter_title=Tk.Entry(self.root)
        self.enter_title.pack()
        
        #Text_Area
        self.Text_Area=Tk.Text(self.root)
        self.Text_Area.pack(fill=Tk.BOTH,expand=True)
        
        #Buttons
        buttons_frame = Tk.Frame(self.root)
        buttons_frame.pack()
        Tk.Button(buttons_frame,text="Save",command=self.save_note).pack(side=Tk.LEFT)
        Tk.Button(buttons_frame,text="Open", command=self.open_note).pack(side=Tk.LEFT)
        Tk.Button(buttons_frame,text="Delete",command=self.delete_note).pack(side=Tk.LEFT)
        Tk.Button(buttons_frame,text="Clear", command=lambda:self.enter_title.delete(len(self.enter_title.get())-1,Tk.END)).pack(side=Tk.LEFT)
        Tk.Button(buttons_frame,text="New",command=self.new_note).pack(side=Tk.LEFT)
        
        #Listbox for Notes List
        self.Listbox = Tk.Listbox(self.root)
        self.Listbox.pack(fill=Tk.BOTH,expand=True)
        self.update_listbox()
        self.Listbox.bind("<Double-1>",self.load_selected_note)
        
    def save_note(self):
        title= self.enter_title.get()
        content = self.Text_Area.get('1.0',Tk.END)
        self.custom.execute("SELECT id FROM notes WHERE title=?",(title,))
        existing_note = self.custom.fetchone()
        if existing_note:
            note_id = existing_note[0]
            self.custom.execute("UPDATE notes SET title=?,content=? WHERE id=?",(title,content,note_id))
        else:
            self.custom.execute("INSERT INTO notes (title,content) VALUES (?,?)",(title,content))  
        self.connection.commit()
        self.update_listbox()
        messagebox.showinfo("Note Saved")
        
    #Open Notes (update listbox):
    def open_note(self):
        self.update_listbox()
    def load_selected_note(self,event=None):
        try:
            selected_index= self.Listbox.curselection()[0]
            note_id = self.Listbox.get(selected_index).split(':')[0]
            self.custom.execute("SELECT title,content FROM notes WHERE id=?",(note_id))
            note=self.custom.fetchone()
            self.enter_title.delete(0,Tk.END)
            self.enter_title.insert(0,note[0])
            self.Text_Area.delete('1.0',Tk.END)
            self.Text_Area.insert('1.0',note[1])
        except IndexError:
            messagebox.showerror("Notes Not Selected")
    
    
    #Deleting selected Notes        
    def delete_note(self):
           try:
               selected_index=self.Listbox.curselection()[0] 
               note_id= self.Listbox.get(selected_index).split(':')[0]
               self.custom.execute("DELETE FROM notes WHERE id=?",(note_id,))
               self.connection.commit()
               self.update_listbox()
               messagebox.showinfo("Notes Deleted")
           except IndexError:
               messagebox.showerror("Error","Select Note")
               
    #Clear Title & Text
    def clear_note(self):
        self.enter_title.delete(0,Tk.END)
        self.Text_Area.delete('1.0',Tk.END)
        
    #Update list wit Notes from Notepad Database
    def update_listbox(self):
        self.Listbox.delete(0,Tk.END)
        self.custom.execute("SELECT id, title FROM notes")
        notes = self.custom.fetchall()
        
        for note in notes:
            self.Listbox.insert(Tk.END, f"{note[0]}:{note[1]}")
            
    def new_note(self):
        self.enter_title.delete(0,Tk.END)
        self.Text_Area.delete('1.0',Tk.END)
            
   #Run Application
    def run(self):
        self.root.mainloop()
        self.connection.close()
        
 #Main Execution
if __name__=="__main__":
    root = Tk.Tk()
    App=Notepad(root)
    App.run()
        
