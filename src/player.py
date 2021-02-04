"""
Player module to handle audio and video playback.
"""

import sys
import os

if os.name == 'nt': # Windows
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    # Python 3.8 things:
    with os.add_dll_directory(os.path.join(base_path, "local_vlc")):
        import vlc

else: # linux
    import vlc

class Player:
    """
    Class that creates and handles vlc player instances.
    """
    def __init__(self, window):
        self.window = window
        self.audio_player = vlc.MediaPlayer()
        vlc_options = '--no-xlib --quiet'
        inst = vlc.Instance(vlc_options)
        self.video_player = inst.media_player_new()
        self.playing = False
        self.delay = 0

    def play_audio(self, audio_file, retry=True):
        """
        Set the media of the audio player and start playing.
        """
        if self.playing: # player is busy
            if retry:
                self.window.after(500, self.play_audio, audio_file, False)
        else: # player is ready
            self.playing = True
            self.audio_player.set_media(vlc.Media(audio_file))
            self.audio_player.play()
            self.window.after(750, self.get_delay)


    def play_video(self, video_file, canvas, retry=True):
        """
        Set the media of the video player, attach it to canvas and start playing.
        """
        if self.playing: # player is busy
            if retry:
                self.window.after(500, self.play_video, video_file, canvas, False)
        else: # player is ready
            xid = canvas.winfo_id()
            self.video_player.set_media(vlc.Media(video_file))
            if os.name == 'nt': # Windows
                self.video_player.set_hwnd(xid)
            else:
                self.video_player.set_xwindow(xid)
            self.window.after(50, self.video_player.play)
            self.window.after(500, self.get_delay)

    def get_delay(self):
        """
        Get the delay and reset playing state if delay is zero.
        """
        self.delay = max([self.video_player.get_length(),
                          self.audio_player.get_length()])

        if "State.Playing" in [str(self.audio_player.get_state()),
                               str(self.video_player.get_state())]:
            self.window.after(100, self.get_delay)
        else:
            self.stop_playing()

    def stop_playing(self):
        """
        Reset the playing state after playback is over.
        """
        self.playing = False
        self.delay = 0
