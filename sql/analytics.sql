-- 行为事件分析 SQL（生产可对接 PostgreSQL / ClickHouse）

-- 漏斗分析
SELECT
    event_type,
    COUNT(DISTINCT user_id) AS user_count
FROM events_clean
WHERE timestamp >= '2024-01-01'
GROUP BY event_type
ORDER BY user_count DESC;

-- 每日活跃用户 (DAU)
SELECT
    DATE(timestamp)         AS day,
    COUNT(DISTINCT user_id) AS dau,
    COUNT(*)                AS event_count,
    SUM(value)              AS total_value
FROM events_clean
GROUP BY DATE(timestamp)
ORDER BY day DESC
LIMIT 30;

-- Top 10 用户贡献
SELECT
    user_id,
    COUNT(*)                AS event_count,
    SUM(value)              AS total_value
FROM events_clean
GROUP BY user_id
ORDER BY total_value DESC
LIMIT 10;

-- 各操作系统占比
SELECT
    device_os,
    COUNT(*)                AS event_count,
    COUNT(DISTINCT user_id) AS unique_users
FROM events_clean
GROUP BY device_os
ORDER BY event_count DESC;