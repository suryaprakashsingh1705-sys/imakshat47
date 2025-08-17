import json
import datetime
import os

COUNTER_FILE = "counter.json"

def load_data():
    if not os.path.exists(COUNTER_FILE):
        return {"visits": 0, "last_visited": None, "details": []}
    with open(COUNTER_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(COUNTER_FILE, "w") as f:
        json.dump(data, f, indent=4)

def update_counter(visitor_ip, user_agent):
    data = load_data()

    # Increment visitor count
    data["visits"] += 1
    
    # Store timestamp
    now = datetime.datetime.utcnow().isoformat()
    data["last_visited"] = now
    
    # Store detailed log
    data["details"].append({
        "ip": visitor_ip,
        "user_agent": user_agent,
        "time": now
    })
    
    # Limit stored logs to last 100
    data["details"] = data["details"][-100:]
    
    save_data(data)
    return data

# Example usage
if __name__ == "__main__":
    # Simulate a visitor
    visitor_ip = "192.168.1.100"
    user_agent = "Mozilla/5.0"
    stats = update_counter(visitor_ip, user_agent)
    print(stats)
