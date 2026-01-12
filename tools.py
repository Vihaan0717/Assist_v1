# tools.py
import datetime
import psutil
import requests
import xml.etree.ElementTree as ET # Built-in XML parser for RSS

class SystemTools:
    def get_time(self):
        return datetime.datetime.now().strftime("%I:%M %p")
    
    def get_battery(self):
        try:
            battery = psutil.sensors_battery()
            return f"{battery.percent}%"
        except:
            return "Unknown"

    def get_weather(self, city="Rajamahendravaram"):
        """ 100% Free Weather (wttr.in) with Browser Headers """
        try:
            city = city.replace(" in ", "").replace(" at ", "").strip()
            
            # format="%C+%t" -> "Mist +25C"
            url = f"https://wttr.in/{city}?format=%C+%t"
            
            # FAKE BROWSER HEADER (This fixes the connection error)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                text = response.text.strip()
                if "Unknown location" in text:
                    return f"I couldn't find the city '{city}'."
                return text
            else:
                return "Weather server is busy."
        except Exception as e:
            print(f"Weather Error: {e}") # Print error to terminal to see what's wrong
            return "Unable to connect to weather server."

    def get_news(self):
        """ 
        Fetches Google News India (RSS Feed).
        100% Free. Uses 0 Gemini Tokens.
        """
        try:
            # Direct RSS Feed for India (English)
            url = "https://news.google.com/rss/search?q=India&hl=en-IN&gl=IN&ceid=IN:en"
            response = requests.get(url, timeout=4)
            
            # Parse XML directly
            root = ET.fromstring(response.content)
            
            headlines = []
            # Find all <item> tags and get the <title>
            for item in root.findall('./channel/item')[:3]: # Top 3 only
                title = item.find('title').text
                # Clean up title (remove the news source name at the end)
                if "-" in title:
                    title = title.split("-")[0].strip()
                headlines.append(title)
            
            if not headlines:
                return "No headlines found."
                
            return ". ".join(headlines)
        except Exception as e:
            print(f"News Error: {e}")
            return "I cannot reach the news feed right now."