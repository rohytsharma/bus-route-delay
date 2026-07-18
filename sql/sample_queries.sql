

SELECT sql FROM sqlite_master WHERE type='table' AND name='route_risk_scores';

 -- Top 10 highest-risk routes
SELECT route_description, route_risk_score
FROM route_risk_scores
ORDER BY route_risk_score DESC
LIMIT 10;

--Routes below the brief's 85% Service Reliability target
SELECT route_description, service_reliability_rate
FROM route_risk_scores
WHERE service_reliability_rate < 0.85
ORDER BY service_reliability_rate ASC;

--  Routes above a risk-score threshold (parameterised in the real app:
SELECT route_description, predicted_avg_delay, route_risk_score
FROM route_risk_scores
WHERE route_risk_score > 0.5
ORDER BY route_risk_score DESC;

--  Summary statistics across all scored routes
SELECT
    COUNT(*)                       AS total_routes,
    ROUND(AVG(predicted_avg_delay), 2)   AS avg_delay_minutes,
    ROUND(AVG(service_reliability_rate), 3) AS avg_reliability,
    ROUND(MAX(route_risk_score), 3)      AS highest_risk_score
FROM route_risk_scores;
