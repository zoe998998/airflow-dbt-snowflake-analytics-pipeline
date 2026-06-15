select
    report_date,

    sum(revenue_today) as daily_revenue,
    sum(refund_today) as daily_refund,
    sum(revenue_today) - sum(refund_today) as daily_net_revenue,

    sum(new_accounts_today) as daily_new_accounts,
    sum(paying_users_today) as daily_paying_users,
    sum(follow_up_actions_today) as daily_follow_up_actions,

    sum(read_users_today) / nullif(sum(retained_users), 0) as daily_reading_rate,
    sum(reply_users_today) / nullif(sum(retained_users), 0) as daily_reply_rate,
    sum(deep_reply_users_today) / nullif(sum(retained_users), 0) as daily_deep_reply_rate

from {{ ref('int_operations_kpis') }}

group by report_date