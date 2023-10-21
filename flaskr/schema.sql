-- Drop the user table if it already exists
DROP TABLE IF EXISTS user;

-- Drop the post table if it already exists
DROP TABLE IF EXISTS post;

-- Create a new user table with an auto-incrementing primary key, a unique username, and a password
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incrementing primary key for the user
  username TEXT UNIQUE NOT NULL,         -- Unique username for the user
  password TEXT NOT NULL                 -- Password for the user
);

-- Create a new post table with an auto-incrementing primary key, a foreign key reference to the user table, a timestamp for when the post was created, a title, and a body
CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incrementing primary key for the post
  author_id INTEGER NOT NULL,            -- Foreign key reference to the user who authored the post
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- Timestamp for when the post was created, defaulting to the current timestamp
  title TEXT NOT NULL,                   -- Title of the post
  body TEXT NOT NULL,                    -- Body/content of the post
  FOREIGN KEY (author_id) REFERENCES user (id)  -- Establish the foreign key relationship between post and user tables
);
