select
    *,

    retained_users / nullif(total_inflow, 0) as retention_rate,
    read_users_today / nullif(retained_users, 0) as reading_rate,
    reply_users_today / nullif(retained_users, 0) as reply_rate,
    deep_reply_users_today / nullif(retained_users, 0) as deep_reply_rate,
    total_accounts / nullif(retained_users, 0) as account_open_rate,
    total_paying_users / nullif(total_accounts, 0) as deposit_rate,
    follow_up_actions_today / nullif(total_accounts, 0) as follow_up_rate,
    net_revenue / nullif(team_marketing_cost, 0) as marketing_roi

from {{ ref('stg_operations') }}