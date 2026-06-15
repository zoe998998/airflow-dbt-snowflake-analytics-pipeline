select
    date_trunc('week', report_date) as week_start,
    region,
    market,
    market_type,

    sum(revenue_today) as weekly_revenue,
    sum(refund_today) as weekly_refund,
    sum(revenue_today) - sum(refund_today) as weekly_net_revenue,

    sum(new_accounts_today) as weekly_new_accounts,
    sum(paying_users_today) as weekly_paying_users,
    sum(follow_up_actions_today) as weekly_follow_up_actions,

    sum(read_users_today) / nullif(sum(retained_users), 0) as weekly_reading_rate,
    sum(reply_users_today) / nullif(sum(retained_users), 0) as weekly_reply_rate,
    sum(deep_reply_users_today) / nullif(sum(retained_users), 0) as weekly_deep_reply_rate

from {{ ref('int_operations_kpis') }}

group by
    date_trunc('week', report_date),
    region,
    market,
    market_type