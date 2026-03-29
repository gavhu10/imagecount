-- Initialize the database.
-- Drop any existing data and create empty tables.
DROP TABLE IF EXISTS requests;

DROP TABLE IF EXISTS badges;

CREATE TABLE
    badges (
        id TEXT UNIQUE NOT NULL,
        count INTEGER NOT NULL
    );

CREATE TABLE
    requests (
        request_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        badge_id INTEGER NOT NULL,
        time_gotten TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        useragent TEXT,
        FOREIGN KEY (badge_id) REFERENCES badges (id) ON DELETE CASCADE
    );