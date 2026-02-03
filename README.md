# SessionTrack 🚀

## Overview
SessionTrack is an intelligent conversation and project management tool designed to capture, analyze, and organize digital interactions across various platforms.

## Purpose
- Capture detailed conversation logs
- Generate AI-powered insights
- Track project-related discussions
- Provide a comprehensive memory management system

## Features

### 🔍 Session Capture
- Multi-source conversation logging
- Metadata extraction
- Timestamp and context preservation

### 🤖 AI-Powered Insights
- Automatic conversation summarization
- Semantic topic extraction
- Action item identification

### 📊 Project Tracking
- Link conversations to specific projects
- Generate progress reports
- Contextual relationship mapping

## Technical Architecture

### Core Components
- **Backend**: Python (FastAPI)
- **AI Integration**: Gemini Pro
- **Database**: PostgreSQL with TimescaleDB
- **Frontend**: Next.js
- **Containerization**: Docker

### Microservices
1. Session Capture Service
2. AI Analysis Service
3. Project Tracking Service
4. User Management Service
5. Reporting Service
6. Notification Service

## Installation

### Prerequisites
- Python 3.12+
- Docker
- Gemini API Key

### Quick Start
```bash
git clone https://github.com/enoob15/sessiontrack.git
cd sessiontrack
./setup.sh
```

## Configuration

### Environment Variables
- `GEMINI_API_KEY`: Google Gemini API Key
- `DATABASE_URL`: PostgreSQL connection string
- `SESSION_ARCHIVE_PATH`: Directory for storing session logs

## Usage Examples

### Capturing a Session
```python
from sessiontrack import SessionCapture

capture = SessionCapture()
session_file = capture.capture_session(
    session_key='manual:cli',
    source='webchat',
    messages=[...],
    project='Project Name'
)
```

### Retrieving Session Insights
```python
from sessiontrack import SessionAnalyzer

analyzer = SessionAnalyzer()
insights = analyzer.analyze_session(session_file)
```

## Roadmap
- [ ] Multi-language support
- [ ] Enhanced AI models
- [ ] More integration points
- [ ] Advanced visualization

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
MIT License

## Contact
Maintained by: Boone
Project Link: https://github.com/enoob15/sessiontrack