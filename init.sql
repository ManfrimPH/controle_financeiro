CREATE SCHEMA IF NOT EXISTS financeiro;

CREATE TABLE IF NOT EXISTS financeiro.gain (
    id INT8 GENERATED ALWAYS AS IDENTITY NOT NULL,
    category VARCHAR NOT NULL,
    value NUMERIC(12,2) NOT NULL CHECK (value > 0),
    description VARCHAR NOT NULL,
    date TIMESTAMP NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS financeiro.spent (
    id INT8 GENERATED ALWAYS AS IDENTITY NOT NULL,
    category VARCHAR NOT NULL,
    payment_method VARCHAR NOT NULL,
    value NUMERIC(12,2) NOT NULL CHECK (value > 0),
    description VARCHAR NOT NULL,
    date TIMESTAMP NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (id)
);

CREATE INDEX IF NOT EXISTS idx_gain_date ON financeiro.gain(date);
CREATE INDEX IF NOT EXISTS idx_gain_category ON financeiro.gain(category);
CREATE INDEX IF NOT EXISTS idx_spent_date ON financeiro.spent(date);
CREATE INDEX IF NOT EXISTS idx_spent_category ON financeiro.spent(category);
