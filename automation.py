# automation.py
from AppOpener import open as app_open, close as app_close
import pyautogui
import time

class SystemController:
    def open_app(self, app_name):
        """ Opens an application by name """
        print(f"📂 Opening {app_name}...")
        try:
            # match_closest=True means if you say "code", it opens "VS Code"
            app_open(app_name, match_closest=True, output=False) 
            return True
        except:
            return False

    def close_app(self, app_name):
        """ Closes an application """
        print(f"❌ Closing {app_name}...")
        try:
            app_close(app_name, match_closest=True, output=False)
            return True
        except:
            return False

    def type_text(self, text):
        """ Types text like a ghost keyboard """
        time.sleep(1) # Wait a sec for you to click the text box
        pyautogui.write(text, interval=0.1) # interval makes it look like natural typing

    def press_key(self, key):
        """ Presses a specific key (enter, space, esc) """
        pyautogui.press(key)

    def take_screenshot(self):
        """ Saves a screenshot """
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        pyautogui.screenshot(filename)
        return filename
# ... inside automation.py ...

    def media_control(self, action):
        """ Controls Media Player (Spotify, YouTube, VLC) """
        print(f"🎵 Media Command: {action}")
        
        if action == "play" or action == "pause" or action == "stop":
            pyautogui.press("playpause") # Toggles Play/Pause
        elif action == "next":
            pyautogui.press("nexttrack")
        elif action == "previous" or action == "back":
            pyautogui.press("prevtrack")
        elif action == "volume up" or action == "louder":
            pyautogui.press("volumeup")
            pyautogui.press("volumeup") # Press twice for noticeable change
        elif action == "volume down" or action == "quieter":
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
        elif action == "mute":
            pyautogui.press("volumemute")