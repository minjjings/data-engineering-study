
CREATE TABLE IF NOT EXISTS raw_market_prices (
    id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR(20),
    trade_date DATE,
    close_price VARCHAR(50),
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO raw_market_prices
    (symbol, trade_date, close_price)
VALUES
    ('QQQ', '2026-10-26', '620.50'),
    ('SPY', '2026-10-26', '680.20'),
    ('QQQ', '2026-10-26', '620.50'),
    ('SPY', '2026-10-27', NULL),
    ('QQQ', '2026-10-27', 'N/A');
