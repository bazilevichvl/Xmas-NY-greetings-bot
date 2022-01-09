CREATE TABLE IF NOT EXISTS users (
    uid bigint PRIMARY KEY NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS greetings (
    gid serial PRIMARY KEY NOT NULL,
    content varchar(512) NOT NULL
);
