import pandas as pd
import random
from pathlib import Path
from datetime import datetime, timedelta

output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

regions = ["North", "South", "East", "West"]
markets = ["Brazil", "Mexico", "Spain", "France"]
teams = ["Team A", "Team B", "Team C"]
staff = ["Alice", "Ben", "Cathy", "David", "Emma", "Frank"]

rows = []

start_date = datetime(2026, 1, 1)

for i in range(120):
    date = start_date + timedelta(days=i % 30)
    region = random.choice(regions)
    market = random.choice(markets)
    team = random.choice(teams)
    sales_rep = random.choice(staff)

    total_leads = random.randint(200, 800)
    retained_leads = random.randint(80, total_leads)
    readers = random.randint(50, retained_leads)
    conversations = random.randint(20, readers)
    replies = random.randint(10, conversations)
    deep_replies = random.randint(5, replies)
    new_accounts = random.randint(0, 20)
    total_accounts = random.randint(new_accounts, 100)
    active_customers = random.randint(0, total_accounts)
    follow_up_orders = random.randint(0, active_customers)

    rows.append({
        "report_date": date.strftime("%Y-%m-%d"),
        "operation_day": random.randint(1, 30),
        "total_day": random.randint(10, 60),
        "region": region,
        "market": market,
        "team": team,
        "sales_rep": sales_rep,
        "total_leads": total_leads,
        "retained_leads": retained_leads,
        "read_users_today": readers,
        "conversation_users_today": conversations,
        "reply_users_today": replies,
        "deep_reply_users_today": deep_replies,
        "new_accounts_today": new_accounts,
        "total_accounts": total_accounts,
        "active_customers_today": active_customers,
        "follow_up_orders_today": follow_up_orders,
        "marketing_cost": round(random.uniform(1000, 8000), 2)
    })

df = pd.DataFrame(rows)

df.to_csv(output_dir / "regional_operations_sample.csv", index=False)

print("Sample data generated: data/raw/regional_operations_sample.csv")
print(df.head())