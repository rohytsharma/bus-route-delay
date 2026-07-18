-- Sample queries for bus_delay_project.db
-- NOTE: These are shown here with literal values for reference/documentation only.
-- In the actual application (notebook + app.py), every query is executed using
-- parameterised placeholders (?), never string concatenation, per the brief's
-- SQL-injection-prevention requirement. See app.py's Route Risk Explorer page
-- and the notebook's Step 33 for the real parameterised versions.

-- 1. Schema
SELECT sql FROM sqlite_master WHERE type='table' AND name='route_risk_scores';

-- 2. Top 10 highest-risk routes
SELECT route_description, route_risk_score
FROM route_risk_scores
ORDER BY route_risk_score DESC
LIMIT 10;

-- 3. Routes below the brief's 85% Service Reliability target
SELECT route_description, service_reliability_rate
FROM route_risk_scores
WHERE service_reliability_rate < 0.85
ORDER BY service_reliability_rate ASC;

-- 4. Routes above a risk-score threshold (parameterised in the real app:
--    cur.execute("... WHERE route_risk_score > ?", (threshold,)))
SELECT route_description, predicted_avg_delay, route_risk_score
FROM route_risk_scores
WHERE route_risk_score > 0.5
ORDER BY route_risk_score DESC;

-- 5. Summary statistics across all scored routes
SELECT
    COUNT(*)                       AS total_routes,
    ROUND(AVG(predicted_avg_delay), 2)   AS avg_delay_minutes,
    ROUND(AVG(service_reliability_rate), 3) AS avg_reliability,
    ROUND(MAX(route_risk_score), 3)      AS highest_risk_score
FROM route_risk_scores;
