# SessionTrack Database Schema

## Tables

### Users
- id (UUID)
- username
- email
- password_hash
- created_at
- last_login
- role (admin, user, viewer)

### Sessions
- id (UUID)
- session_key
- start_time
- end_time
- source (webchat, cli, github)
- participants (JSON array)
- total_messages
- ai_model_used

### Conversations
- id (UUID)
- session_id (FK)
- start_time
- end_time
- summary
- ai_generated_tags (JSON)
- primary_topic
- sentiment_score

### Projects
- id (UUID)
- name
- description
- created_at
- status (active, paused, completed)
- primary_owner_id (FK to Users)

### Project_Sessions
- project_id (FK)
- session_id (FK)
- relevance_score
- tags (JSON)

### Action_Items
- id (UUID)
- session_id (FK)
- project_id (FK)
- description
- created_at
- due_date
- status (pending, in_progress, completed)
- assigned_to (FK to Users)

## Indexes
- Sessions: (start_time, source)
- Conversations: (primary_topic, start_time)
- Projects: (status, created_at)
- Action_Items: (status, due_date)

## Sample Relationships
- One Session can belong to multiple Projects
- One Project can have multiple Sessions
- Action Items can be linked to Sessions and Projects