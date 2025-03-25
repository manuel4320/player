import os
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from doubly_linked_list import DoublyLinkedList
from player import Player

class GraphicalInterface:
    def __init__(self, root):
        self.root = root
        self.list = DoublyLinkedList()
        self.player = Player(end_callback=self._next_song)
        self._configure_interface()
        self._load_initial_songs()
        self.root.after(100, self._check_events)
        self.root.after(100, self._update_player)  # preload 15 (or more)songs

    def _check_events(self):
        #detect pygames events
        self.player.check_events()
        self.root.after(100, self._check_events)  

    def _configure_interface(self):
        self.root.title("MP3 Player")
        self.root.geometry("500x400")

        # listbox to display songs
        self.listbox = tk.Listbox(self.root, width=60)
        self.listbox.pack(pady=10)

        # control buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        navigation_frame = tk.Frame(self.root)
        navigation_frame.pack(pady=5)

        btn_play = tk.Button(button_frame, text="Play", command=self._play)
        btn_play.pack(side=tk.LEFT, padx=5)

        btn_pause = tk.Button(button_frame, text="Pause", command=self.player.pause)
        btn_pause.pack(side=tk.LEFT, padx=5)

        btn_previous = tk.Button(navigation_frame, text="Previous", command=self._previous_song)
        btn_previous.pack(side=tk.LEFT, padx=5)

        btn_next = tk.Button(navigation_frame, text="Next", command=self._next_song)
        btn_next.pack(side=tk.LEFT, padx=5)

        btn_delete = tk.Button(button_frame, text="Delete", command=self._delete_selected_song)
        btn_delete.pack(side=tk.LEFT, padx=5)

        # configure drag and drop
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind('<<Drop>>', self._add_dragged_file)

    def _load_initial_songs(self):
        # load sample songs for "songs/"
        import os
        if os.path.exists("songs"):
            for file in os.listdir("songs"):
                if file.endswith(".mp3"):
                    self.list.add(f"songs/{file}")
            self._update_listbox()

    def _update_listbox(self):
        #updates the listbox
        self.listbox.delete(0, tk.END)
        for song in self.list.get_list():
            self.listbox.insert(tk.END, os.path.basename(song))

    def _add_dragged_file(self, event):
        files = event.data.split()
        for file in files:
            if file.endswith(".mp3"):
                file = file.strip("{}")  
            if os.path.exists(file):  # checks if the file exist
                self.list.add(os.path.abspath(file))  # use path
        self._update_listbox()

    def _play(self):
        selection = self.listbox.curselection()
        if selection:
            song = self.list.get_list()[selection[0]]
            self.player.play(song)

    def _previous_song(self):
        if self.list.current and self.list.current.prev:  
            self.list.current = self.list.current.prev
            self.player.play(self.list.current.data)
            self._highlight_current_song()
        else:
            print("No previous songs")

    def _next_song(self):
        if self.list.current and self.list.current.next:
            self.list.current = self.list.current.next
            self.player.play(self.list.current.data)
            self._highlight_current_song()  # updates the interface
        else:
            print("End of the list")

    def _highlight_current_song(self):
        songs = self.list.get_list()
        if self.list.current:
            songs = self.list.get_list()
            index = songs.index(self.list.current.data)
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(index)
            self.listbox.see(index)

    def _update_player(self):
        self.player.check_events()
        self.root.after(100, self._update_player)  # loop

    def _delete_selected_song(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            songs = self.list.get_list()
            song_to_delete = songs[index]
            
            # removes from the doubly linked list
            if self.list.delete(song_to_delete):
                self._update_listbox()
                print(f"Deleted song: {song_to_delete}")
            else:
                print("Error deleting the song")
        else:
            print("No song selected")
