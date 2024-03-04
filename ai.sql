CREATE TABLE users (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "username" TEXT NOT NULL,
    "email" TEXT NOT NULL UNIQUE
);


CREATE TABLE stories (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "title" TEXT NOT NULL,
  "content" TEXT NOT NULL
);

CREATE TABLE conversation_histories (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "story_id" INTEGER,
  "conversaion" TEXT,
  FOREIGN KEY(user_id) REFERENCES "users"("id"),
  FOREIGN KEY(story_id) REFERENCES "stories"("id")
);