import pandas as pd
import random
from pathlib import Path
from datetime import datetime, timedelta

output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

region_structure = {
    "east": {
        "market": "Mexico",
        "market_type": "developing",
        "starting_total_day": 40,
        "base_inflow_range": (300, 430),
        "region_marketing_cost": 45000,
        "revenue_per_user_range": (120, 260),
        "paying_rate_range": (0.25, 0.50),
        "teams": {
            "Team A": ["Cathy", "Alice"],
            "Team B": ["Ben", "David"],
            "Team C": ["Emma", "Frank"],
        },
    },
    "west": {
        "market": "Brazil",
        "market_type": "developing",
        "starting_total_day": 55,
        "base_inflow_range": (380, 520),
        "region_marketing_cost": 52000,
        "revenue_per_user_range": (140, 300),
        "paying_rate_range": (0.28, 0.55),
        "teams": {
            "Team A": ["Grace", "Henry"],
            "Team B": ["Ivy", "Jack"],
            "Team C": ["Kelly", "Leo"],
            "Team D": ["Mason", "Nora"],
        },
    },
    "north": {
        "market": "Spain",
        "market_type": "developed",
        "starting_total_day": 60,
        "base_inflow_range": (430, 560),
        "region_marketing_cost": 75000,
        "revenue_per_user_range": (220, 480),
        "paying_rate_range": (0.35, 0.65),
        "teams": {
            "Team A": ["Mia", "Noah"],
            "Team B": ["Olivia", "Paul"],
            "Team C": ["Queen", "Ryan"],
            "Team D": ["Sarah", "Tony"],
            "Team E": ["Uma", "Victor"],
        },
    },
    "south": {
        "market": "France",
        "market_type": "developed",
        "starting_total_day": 70,
        "base_inflow_range": (480, 620),
        "region_marketing_cost": 88000,
        "revenue_per_user_range": (250, 550),
        "paying_rate_range": (0.38, 0.68),
        "teams": {
            "Team A": ["Wendy", "Zack"],
            "Team B": ["Aaron", "Bella"],
            "Team C": ["Chris", "Diana"],
            "Team D": ["Ethan", "Fiona"],
            "Team E": ["George", "Hannah"],
            "Team F": ["Isaac", "Julia"],
        },
    },
}

start_date = datetime(2026, 1, 1)
num_days_to_generate = 30

base_total_inflow = {}
previous_retained_users = {}

cumulative_accounts = {}
cumulative_paying_users = {}
cumulative_revenue = {}
cumulative_refund = {}

for region, structure in region_structure.items():
    min_inflow, max_inflow = structure["base_inflow_range"]

    for team, sales_reps in structure["teams"].items():
        for sales_rep in sales_reps:
            key = (region, team, sales_rep)

            base_total_inflow[key] = random.randint(min_inflow, max_inflow)
            previous_retained_users[key] = base_total_inflow[key]

            cumulative_accounts[key] = 0
            cumulative_paying_users[key] = 0
            cumulative_revenue[key] = 0.0
            cumulative_refund[key] = 0.0

for region, structure in region_structure.items():
    rows = []

    market = structure["market"]
    market_type = structure["market_type"]
    starting_total_day = structure["starting_total_day"]
    region_marketing_cost = structure["region_marketing_cost"]

    min_revenue_per_user, max_revenue_per_user = structure["revenue_per_user_range"]
    min_paying_rate, max_paying_rate = structure["paying_rate_range"]

    for day_offset in range(num_days_to_generate):
        report_date = start_date + timedelta(days=day_offset)

        operation_day = day_offset + 1
        total_day = starting_total_day + day_offset

        for team, sales_reps in structure["teams"].items():
            for sales_rep in sales_reps:
                key = (region, team, sales_rep)

                total_inflow = base_total_inflow[key]

                daily_loss = random.choice([0, 0, 1, 1, 2])
                retained_users = max(
                    previous_retained_users[key] - daily_loss,
                    int(total_inflow * 0.75)
                )
                previous_retained_users[key] = retained_users

                read_users_today = random.randint(
                    int(retained_users * 0.60),
                    int(retained_users * 0.75)
                )

                conversation_users_today = random.randint(
                    int(read_users_today * 0.70),
                    int(read_users_today * 0.90)
                )

                reply_users_today = random.randint(
                    int(conversation_users_today * 0.70),
                    int(conversation_users_today * 0.90)
                )

                deep_reply_users_today = random.randint(
                    int(reply_users_today * 0.50),
                    int(reply_users_today * 0.75)
                )

                follow_up_actions_today = random.randint(
                    int(deep_reply_users_today * 0.60),
                    max(
                        int(deep_reply_users_today * 0.90),
                        int(deep_reply_users_today * 0.60)
                    )
                )

                if total_inflow >= 600:
                    new_accounts_today = random.randint(12, 20)
                elif total_inflow >= 500:
                    new_accounts_today = random.randint(9, 16)
                elif total_inflow >= 400:
                    new_accounts_today = random.randint(6, 12)
                else:
                    new_accounts_today = random.randint(4, 9)

                new_accounts_today = min(new_accounts_today, deep_reply_users_today)

                cumulative_accounts[key] += new_accounts_today
                total_accounts = cumulative_accounts[key]

                min_paying_users = int(new_accounts_today * min_paying_rate)
                max_paying_users = int(new_accounts_today * max_paying_rate)

                if new_accounts_today > 0:
                    paying_users_today = random.randint(
                        min_paying_users,
                        max(1, max_paying_users)
                    )
                else:
                    paying_users_today = 0

                paying_users_today = min(paying_users_today, new_accounts_today)

                cumulative_paying_users[key] += paying_users_today
                total_paying_users = cumulative_paying_users[key]

                if paying_users_today > 0:
                    revenue_today = round(
                        paying_users_today
                        * random.uniform(min_revenue_per_user, max_revenue_per_user),
                        2
                    )
                else:
                    revenue_today = 0.0

                refund_today = (
                    round(revenue_today * random.uniform(0.02, 0.12), 2)
                    if revenue_today > 0
                    else 0.0
                )

                cumulative_revenue[key] += revenue_today
                cumulative_refund[key] += refund_today

                total_revenue = round(cumulative_revenue[key], 2)
                total_refund = round(cumulative_refund[key], 2)
                net_revenue = round(total_revenue - total_refund, 2)

                rows.append({
                    "report_date": report_date.strftime("%Y-%m-%d"),
                    "operation_day": operation_day,
                    "total_day": total_day,
                    "region": region,
                    "market": market,
                    "market_type": market_type,
                    "team": team,
                    "sales_rep": sales_rep,
                    "total_inflow": total_inflow,
                    "retained_users": retained_users,
                    "read_users_today": read_users_today,
                    "conversation_users_today": conversation_users_today,
                    "reply_users_today": reply_users_today,
                    "deep_reply_users_today": deep_reply_users_today,
                    "follow_up_actions_today": follow_up_actions_today,
                    "new_accounts_today": new_accounts_today,
                    "total_accounts": total_accounts,
                    "paying_users_today": paying_users_today,
                    "total_paying_users": total_paying_users,
                    "revenue_today": revenue_today,
                    "total_revenue": total_revenue,
                    "refund_today": refund_today,
                    "total_refund": total_refund,
                    "net_revenue": net_revenue,
                    "region_marketing_cost": region_marketing_cost,
                })

    df = pd.DataFrame(rows)
    file_path = output_dir / f"{region}_operations.csv"
    df.to_csv(file_path, index=False)

    print(f"Generated file: {file_path} | rows: {len(df)}")

print("All regional files generated successfully.")