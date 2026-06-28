USE DATABASE RETAIL_ANALYTICS;
USE SCHEMA RAW;

CREATE OR REPLACE TABLE OPERATIONS_RAW (
    report_date DATE,
    operation_day NUMBER,
    total_day NUMBER,
    region STRING,
    market STRING,
    market_type STRING,
    team STRING,
    sales_rep STRING,
    total_inflow NUMBER,
    retained_users NUMBER,
    read_users_today NUMBER,
    conversation_users_today NUMBER,
    reply_users_today NUMBER,
    deep_reply_users_today NUMBER,
    follow_up_actions_today NUMBER,
    new_accounts_today NUMBER,
    total_accounts NUMBER,
    paying_users_today NUMBER,
    total_paying_users NUMBER,
    revenue_today FLOAT,
    total_revenue FLOAT,
    refund_today FLOAT,
    total_refund FLOAT,
    net_revenue FLOAT,
    team_marketing_cost NUMBER
);