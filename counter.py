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
    
def generate_svg(count, last_visit):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="300" height="50">
        <rect width="300" height="50" fill="#1a1a1a" rx="10" ry="10"/>
        <text x="150" y="20" font-size="16" fill="#00ff99" text-anchor="middle">
            👀 Visitors: {count}
        </text>
        <text x="150" y="40" font-size="12" fill="#ffffff" text-anchor="middle">
            Last Visit: {last_visit}
        </text>
    </svg>"""

if __name__ == "__main__":
    data = load_data()
    visitor_ip = "0.0.0.0"       # placeholder (GitHub Actions won't give real IP)
    user_agent = "GitHub Action" # placeholder
    stats = update_counter(visitor_ip, user_agent)

    # Generate SVG
    with open("counter.svg", "w") as f:
        f.write(generate_svg(stats["visits"], stats["last_visited"]))

