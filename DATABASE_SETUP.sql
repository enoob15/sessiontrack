-- SessionTrack Database Schema

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE,
    role VARCHAR(20) CHECK (role IN ('admin', 'user', 'viewer'))
);

-- Sessions Table
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_key TEXT NOT NULL UNIQUE,
    start_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP WITH TIME ZONE,
    source VARCHAR(50),
    participants JSONB,
    total_messages INTEGER DEFAULT 0,
    ai_model_used TEXT,
    context_summary TEXT,
    total_tokens INTEGER
);

-- Conversations Table
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES sessions(id),
    start_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP WITH TIME ZONE,
    summary TEXT,
    ai_generated_tags JSONB,
    primary_topic TEXT,
    sentiment_score NUMERIC(5,2)
);

-- Messages Table (for full conversation reconstruction)
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID REFERENCES conversations(id),
    session_id UUID REFERENCES sessions(id),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    sender TEXT NOT NULL,
    content TEXT,
    embeddings VECTOR(768), -- Adjust dimension based on embedding model
    metadata JSONB
);

-- Projects Table
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) CHECK (status IN ('active', 'paused', 'completed')),
    primary_owner_id UUID REFERENCES users(id)
);

-- Project Sessions Mapping
CREATE TABLE project_sessions (
    project_id UUID REFERENCES projects(id),
    session_id UUID REFERENCES sessions(id),
    relevance_score NUMERIC(5,2),
    tags JSONB,
    PRIMARY KEY (project_id, session_id)
);

-- Action Items Table
CREATE TABLE action_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES sessions(id),
    project_id UUID REFERENCES projects(id),
    description TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) CHECK (status IN ('pending', 'in_progress', 'completed')),
    assigned_to UUID REFERENCES users(id)
);

-- Indexes for Performance
CREATE INDEX idx_sessions_start_time ON sessions(start_time);
CREATE INDEX idx_sessions_source ON sessions(source);
CREATE INDEX idx_conversations_topic ON conversations(primary_topic);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_action_items_status ON action_items(status);