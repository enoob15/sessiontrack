import os
import json
from fastapi import FastAPI, HTTPException
from typing import List, Dict

app = FastAPI()

PROJECTS_PATH = '/root/clawd/projects/sessiontrack/project_data'

@app.get("/projects", response_model=List[Dict])
async def list_projects():
    """
    Retrieve list of projects
    """
    try:
        # Ensure projects directory exists
        os.makedirs(PROJECTS_PATH, exist_ok=True)
        
        # Get all JSON files in the projects directory
        project_files = [f for f in os.listdir(PROJECTS_PATH) if f.endswith('.json')]
        
        # Load project metadata
        projects = []
        for filename in project_files:
            filepath = os.path.join(PROJECTS_PATH, filename)
            with open(filepath, 'r') as f:
                project_data = json.load(f)
                
                # Prepare project summary
                projects.append({
                    'id': project_data.get('id'),
                    'name': project_data.get('name'),
                    'description': project_data.get('description', ''),
                    'status': project_data.get('status', 'active'),
                    'total_sessions': len(project_data.get('sessions', [])),
                    'total_action_items': len(project_data.get('action_items', []))
                })
        
        return projects
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving projects: {str(e)}")

@app.get("/project/{project_id}", response_model=Dict)
async def get_project(project_id: str):
    """
    Retrieve full details of a specific project
    """
    try:
        filepath = os.path.join(PROJECTS_PATH, f"{project_id}.json")
        
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="Project not found")
        
        with open(filepath, 'r') as f:
            return json.load(f)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving project: {str(e)}")