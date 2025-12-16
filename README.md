# todo-app
Full-stack Todo app with React, Flask, and CockroachDB

# Shotcuts
conn → connection
cur → cursor
db → database
req → request
res → response

# Basic SQL Commands

## SELECT - Read data
```sql
-- Get all columns from todos table
SELECT id, title, completed FROM todos;

-- Get specific todo with id=5
SELECT id, title FROM todos WHERE id = 5;

-- Get all completed todos
SELECT * FROM todos WHERE completed = true;

-- Get todos sorted by id
SELECT * FROM todos ORDER BY id;
```

## INSERT - Create new data
```sql
-- Add a new todo
INSERT INTO todos (title, completed) VALUES ('Buy milk', false);

-- Insert and get the created row back
INSERT INTO todos (title, completed) VALUES ('Study SQL', false) 
RETURNING id, title, completed;
```

## UPDATE - Modify existing data
```sql
-- Update a specific todo
UPDATE todos SET title = 'New title', completed = true WHERE id = 3;

-- Update and get the updated row back
UPDATE todos SET completed = true WHERE id = 5 
RETURNING id, title, completed;
```

## DELETE - Remove data
```sql
-- Delete a specific todo
DELETE FROM todos WHERE id = 5;

-- Delete all completed todos
DELETE FROM todos WHERE completed = true;
```

## Key SQL Clauses

- **WHERE** - Filter which rows to affect (always use with UPDATE/DELETE!)
- **VALUES** - Specifies the data to insert
- **RETURNING** - Get the affected row back after INSERT/UPDATE
- **ORDER BY** - Sort results

## Important Notes

- Always use `WHERE` with UPDATE and DELETE to avoid affecting all rows
- Use `RETURNING` to get the created/updated row in one query
- SQL commands end with semicolon (`;`) when run directly in database
- In Python with psycopg2, semicolons are optional