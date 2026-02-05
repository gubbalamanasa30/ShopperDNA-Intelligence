-- ShopperDNA Analytics Engine: RFM Segmentation Logic
-- Updated with Industry Standard Segmentation

WITH MaxDate AS (
    SELECT MAX(order_date) as max_date FROM orders
),

RFM_Base AS (
    SELECT 
        customer_id,
        customer_name,
        -- Recency: Days since last order
        CAST(julianday((SELECT max_date FROM MaxDate)) - julianday(MAX(order_date)) AS INTEGER) as recency_days,
        -- Frequency: Count of distinct orders
        COUNT(DISTINCT order_id) as frequency,
        -- Monetary: Total sales
        ROUND(SUM(sales), 2) as monetary_value
    FROM orders
    GROUP BY customer_id, customer_name
),

RFM_Scores AS (
    SELECT 
        customer_id,
        customer_name,
        recency_days,
        frequency,
        monetary_value,
        -- NTILE(5) creates quintiles (1-5)
        -- Recency: 5 = Newest (Best), 1 = Oldest (Worst)
        NTILE(5) OVER (ORDER BY recency_days DESC) as r_score,
        -- Frequency: 5 = Highest (Best), 1 = Lowest (Worst)
        NTILE(5) OVER (ORDER BY frequency ASC) as f_score,
        -- Monetary: 5 = Highest (Best), 1 = Lowest (Worst)
        NTILE(5) OVER (ORDER BY monetary_value ASC) as m_score
    FROM RFM_Base
)

SELECT 
    customer_id,
    customer_name,
    recency_days,
    frequency,
    monetary_value,
    r_score,
    f_score,
    m_score,
    -- Concatenated Score for reference (e.g. 555)
    (r_score || f_score || m_score) as rfm_score_str,
    -- Complex Logic for Segmentation
    CASE 
        -- Champions: Best of the best
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
        
        -- Loyal Customers: Buy often and spend big, but maybe valid recency is dropping a bit? 
        -- Or just High F/M in general. catch-all for high performers who missed Champion
        WHEN f_score >= 4 AND m_score >= 4 THEN 'Loyal Customers'
        
        -- Potential Loyalists: Above average
        WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Potential Loyalists'
        
        -- At Risk: Haven't bought in a while (Low R), but were good customers (Med/High F/M)
        WHEN r_score <= 2 AND (f_score >= 3 OR m_score >= 3) THEN 'At Risk'
        
        -- Can't forget "Recent Customers": High R, but Low F/M (New users)
        WHEN r_score >= 4 AND f_score <= 2 THEN 'Recent Customers'
        
        -- Lost: Low scores across board
        WHEN r_score <= 2 AND f_score <= 2 AND m_score <= 2 THEN 'Lost Customers'
        
        -- Everyone else
        ELSE 'Needs Attention'
    END as customer_segment
FROM RFM_Scores
ORDER BY 
    r_score DESC, f_score DESC, m_score DESC;
