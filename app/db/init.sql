CREATE TABLE IF NOT EXISTS Users(
    user_id BIGSERIAL PRIMARY KEY,
    lang VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS Orders(
    user_id BIGSERIAL REFERENCES Users (user_id),
    order_id SERIAL,
    date_time DATE DEFAULT CURRENT_DATE,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    short_description TEXT NOT NULL,
    price TEXT NOT NULL,
    address TEXT NOT NULL
);
