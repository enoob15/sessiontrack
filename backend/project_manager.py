#!/usr/bin/env python3
import os
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional

class ProjectManager:
    def __init__(self, base_path: str = '/root/clawd/projects/sessiontrack/project_data'):
        """
        Initialize ProjectManager with a base path for storing project data
        """
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    def create_project(self, name: str, description: str = "", tags: List[str] = None) -> str:
        """
        Create a new project with unique identifier
        
        Args:
            name: Project name
            description: Optional project description
            tags: Optional list of project tags
        
        Returns:
            Project unique identifier
        """
        project_id = str(uuid.uuid4())
        project_data = {
            'id': project_id,
            'name': name,
            'description': description,
            'tags': tags or [],
            'created_at': datetime.now(timezone.utc).isoformat(),
            'status': 'active',
            'sessions': [],
            'action_items': [],
            'metadata': {}
        }
        
        project_file = os.path.join(self.base_path, f"{project_id}.json")
        
        with open(project_file, 'w') as f:
            json.dump(project_data, f, indent=2)
        
        return project_id

    def update_project(self, project_id: str, updates: Dict) -> bool:
        """
        Update project details
        
        Args:
            project_id: Unique project identifier
            updates: Dictionary of fields to update
        
        Returns:
            Boolean indicating success
        """
        project_file = os.path.join(self.base_path, f"{project_id}.json")
        
        if not os.path.exists(project_file):
            return False
        
        with open(project_file, 'r') as f:
            project_data = json.load(f)
        
        # Update project data
        project_data.update(updates)
        project_data['updated_at'] = datetime.now(timezone.utc).isoformat()
        
        with open(project_file, 'w') as f:
            json.dump(project_data, f, indent=2)
        
        return True

    def add_session_to_project(self, project_id: str, session_path: str) -> bool:
        """
        Link a session to a project
        
        Args:
            project_id: Project unique identifier
            session_path: Path to the session file
        
        Returns:
            Boolean indicating success
        """
        project_file = os.path.join(self.base_path, f"{project_id}.json")
        
        if not os.path.exists(project_file):
            return False
        
        with open(project_file, 'r') as f:
            project_data = json.load(f)
        
        project_data['sessions'].append({
            'path': session_path,
            'added_at': datetime.now(timezone.utc).isoformat()
        })
        
        with open(project_file, 'w') as f:
            json.dump(project_data, f, indent=2)
        
        return True

    def add_action_item(self, project_id: str, description: str, priority: str = 'medium') -> str:
        """
        Add an action item to a project
        
        Args:
            project_id: Project unique identifier
            description: Action item description
            priority: Priority level (low/medium/high)
        
        Returns:
            Unique action item identifier
        """
        project_file = os.path.join(self.base_path, f"{project_id}.json")
        
        if not os.path.exists(project_file):
            raise ValueError(f"Project {project_id} not found")
        
        with open(project_file, 'r') as f:
            project_data = json.load(f)
        
        action_item = {
            'id': str(uuid.uuid4()),
            'description': description,
            'priority': priority,
            'status': 'pending',
            'created_at': datetime.now(timezone.utc).isoformat()
        }
        
        project_data['action_items'].append(action_item)
        
        with open(project_file, 'w') as f:
            json.dump(project_data, f, indent=2)
        
        return action_item['id']

    def get_project(self, project_id: str) -> Optional[Dict]:
        """
        Retrieve project details
        
        Args:
            project_id: Unique project identifier
        
        Returns:
            Project data or None
        """
        project_file = os.path.join(self.base_path, f"{project_id}.json")
        
        if not os.path.exists(project_file):
            return None
        
        with open(project_file, 'r') as f:
            return json.load(f)

    def list_projects(self, status: Optional[str] = None) -> List[Dict]:
        """
        List all projects, optionally filtered by status
        
        Args:
            status: Optional status filter (active/completed/paused)
        
        Returns:
            List of project summaries
        """
        projects = []
        
        for filename in os.listdir(self.base_path):
            if filename.endswith('.json'):
                project_file = os.path.join(self.base_path, filename)
                
                with open(project_file, 'r') as f:
                    project_data = json.load(f)
                
                if status is None or project_data.get('status') == status:
                    projects.append({
                        'id': project_data['id'],
                        'name': project_data['name'],
                        'status': project_data.get('status', 'unknown'),
                        'created_at': project_data.get('created_at'),
                        'total_sessions': len(project_data.get('sessions', [])),
                        'total_action_items': len(project_data.get('action_items', []))
                    })
        
        return sorted(projects, key=lambda x: x['created_at'], reverse=True)

def main():
    """
    Example usage and testing
    """
    pm = ProjectManager()
    
    # Create a project
    project_id = pm.create_project(
        name="SessionTrack Development", 
        description="Building an AI-powered session tracking tool",
        tags=['ai', 'productivity', 'startup']
    )
    
    # Add an action item
    action_item_id = pm.add_action_item(
        project_id, 
        "Resolve Gemini library installation issue",
        priority='high'
    )
    
    # List projects
    print("Current Projects:")
    for project in pm.list_projects():
        print(f"- {project['name']} (ID: {project['id']})")

if __name__ == "__main__":
    main()