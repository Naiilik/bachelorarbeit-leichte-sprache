CREATE TABLE results (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  participant_id TEXT,
  group_name TEXT,
  score INTEGER,
  answers TEXT,
  created_at TEXT
);

CREATE TABLE assignment_counter (
  group_name TEXT PRIMARY KEY,
  count INTEGER
);