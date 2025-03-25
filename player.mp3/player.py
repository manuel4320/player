import pygame

class Player:
    def __init__(self, end_callback):  # callback parameter
        pygame.init()
        pygame.mixer.init()
        self.end_callback = end_callback
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)  # event when finished

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT + 1:
                self.end_callback()  # calls the function to move to the next one

    def play(self, filepath):
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()

    def pause(self): 
        pygame.mixer.music.pause()

    def resume(self):
        pygame.mixer.music.unpause()

    def stop(self):
        pygame.mixer.music.stop()
