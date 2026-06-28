with latest_sales_rep_values as (

    select *
    from {{ ref('int_operations_kpis') }}
    qualify row_number() over (
        partition by region, market_type, team, sales_rep
        order by report_date desc
    ) = 1

),

region_activity as (

    select
        region,
        market,
        market_type,

        count(distinct team) as team_count,
        count(distinct sales_rep) as sales_team_members,

        sum(total_inflow) as total_inflow,
        sum(retained_users) as retained_users

    from {{ ref('int_operations_kpis') }}

    group by
        region,
        market,
        market_type

),

region_latest_totals as (

    select
        region,
        market,
        market_type,

        sum(total_accounts) as total_accounts,
        sum(total_paying_users) as total_paying_users,
        sum(total_revenue) as total_revenue,
        sum(total_refund) as total_refund,
        sum(net_revenue) as net_revenue,
        max(team_marketing_cost) as team_marketing_cost

    from latest_sales_rep_values

    group by
        region,
        market,
        market_type

)

select
    a.region,
    a.market,
    a.market_type,

    a.team_count,
    a.sales_team_members,

    a.total_inflow,
    a.retained_users,
    l.total_accounts,
    l.total_paying_users,

    l.total_revenue,
    l.total_refund,
    l.net_revenue,
    l.team_marketing_cost,

    l.net_revenue / nullif(l.team_marketing_cost, 0) as marketing_roi,
    l.net_revenue / nullif(a.sales_team_members, 0) as net_revenue_per_team_member,

    a.retained_users / nullif(a.total_inflow, 0) as retention_rate,
    l.total_accounts / nullif(a.retained_users, 0) as account_open_rate,
    l.total_paying_users / nullif(l.total_accounts, 0) as deposit_rate

from region_activity a
join region_latest_totals l
    on a.region = l.region
    and a.market = l.market
    and a.market_type = l.market_type