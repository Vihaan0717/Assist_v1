# tools.py
import psutil
import datetime
import os
import pywhatkit
from AppOpener import open as app_open

class SystemTools:
    def get_time(self):
        """ Returns current time """
        return datetime.datetime.now().strftime("%I:%M %p")

    def get_battery(self):
        """ Checks battery percentage """
        try:
            battery = psutil.sensors_battery()
            if battery:
                return f"{battery.percent}%"
            return "Cannot read battery info."
        except:
            return "Battery sensor not found."

    def open_app(self, app_name):
        """ Opens an app """
        try:
            print(f"🔧 Opening {app_name}...")
            app_open(app_name, match_closest=True, output=False) 
            return f"Opening {app_name}"
        except:
            return f"I could not find an app named {app_name}"

    # --- NEW HANDS BELOW ---
    
    def play_video(self, topic):
        """ Plays a video on YouTube """
        try:
            print(f"▶️ Playing {topic} on YouTube...")
            pywhatkit.playonyt(topic)
            return f"Playing {topic} on YouTube"
        except:
            return "I had trouble accessing YouTube."

    def search_google(self, query):
        """ Performs a Google search """
        try:
            print(f"🔎 Searching Google for: {query}...")
            pywhatkit.search(query)
            return f"Here is what I found for {query} on Google."
        except:
            return "I could not connect to Google."

if __name__ == "__main__":
    # Test
    tool = SystemTools()
    tool.play_video("Imagine Dragons Believer")