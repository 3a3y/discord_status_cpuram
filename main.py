import psutil
import time
import requests
from datetime import datetime

TOKEN = "TOKEN-USER"  #TOKEN
DELAY = 10  # DELAY (S)
STATUS = "idle"  # STATUS : online, idle, dnd, invisible

def get_system_stats():
    try:
        ram_usage = psutil.virtual_memory().percent
        cpu_usage = psutil.cpu_percent(interval=1)
        return f"CPU: {cpu_usage:.1f}% RAM: {ram_usage:.1f}%"
    except Exception as e:
        print(f"Error getting system stats: {e}")
        return None

def update_discord_status(status_text):
    try:
        headers = {
            'Authorization': TOKEN,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'custom_status': {'text': status_text},
            'status': STATUS
        }
        
        response = requests.patch(
            'https://discord.com/api/v9/users/@me/settings',
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            print(f"Error updating status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Error making request: {e}")

def main():
    print("Starting Discord status updater...")
    
    while True:
        try:
            stats = get_system_stats()
            if stats:
                update_discord_status(stats)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Status updated: {stats}")
            
            time.sleep(DELAY)
            
        except KeyboardInterrupt:
            print("\nProgram stopped by user")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(DELAY)

if __name__ == "__main__":
    main()