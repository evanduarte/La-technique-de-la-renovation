DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS pics;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    /*created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,*/
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    filename VARCHAR(100) NOT NULL UNIQUE
);
