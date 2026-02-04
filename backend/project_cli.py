#!/usr/bin/env python3
import argparse
import sys
from project_manager import ProjectManager

def main():
    parser = argparse.ArgumentParser(description='SessionTrack Project Management CLI')
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Project management commands')
    
    # Create Project
    create_parser = subparsers.add_parser('create', help='Create a new project')
    create_parser.add_argument('name', help='Project name')
    create_parser.add_argument('-d', '--description', help='Project description', default='')
    create_parser.add_argument('-t', '--tags', nargs='+', help='Project tags', default=None)
    
    # List Projects
    list_parser = subparsers.add_parser('list', help='List projects')
    list_parser.add_argument('-s', '--status', help='Filter by project status', 
                             choices=['active', 'completed', 'paused'], default=None)
    
    # View Project
    view_parser = subparsers.add_parser('view', help='View project details')
    view_parser.add_argument('project_id', help='Project ID to view')
    
    # Add Action Item
    action_parser = subparsers.add_parser('action', help='Add action item to a project')
    action_parser.add_argument('project_id', help='Project ID')
    action_parser.add_argument('description', help='Action item description')
    action_parser.add_argument('-p', '--priority', 
                               choices=['low', 'medium', 'high'], 
                               default='medium', 
                               help='Priority of action item')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize ProjectManager
    pm = ProjectManager()
    
    # Command handling
    if args.command == 'create':
        project_id = pm.create_project(args.name, args.description, args.tags)
        print(f"Project created successfully. Project ID: {project_id}")
    
    elif args.command == 'list':
        projects = pm.list_projects(args.status)
        if not projects:
            print("No projects found.")
        else:
            print("Projects:")
            for project in projects:
                print(f"- {project['name']} (ID: {project['id']}, Status: {project['status']})")
    
    elif args.command == 'view':
        project = pm.get_project(args.project_id)
        if project:
            print(f"Project: {project['name']}")
            print(f"Description: {project.get('description', 'No description')}")
            print(f"Status: {project.get('status', 'Unknown')}")
            print(f"Created At: {project.get('created_at', 'N/A')}")
            
            print("\nAction Items:")
            for item in project.get('action_items', []):
                print(f"- {item['description']} (Priority: {item['priority']}, Status: {item['status']})")
        else:
            print(f"Project {args.project_id} not found.")
    
    elif args.command == 'action':
        try:
            action_id = pm.add_action_item(args.project_id, args.description, args.priority)
            print(f"Action item added successfully. Action ID: {action_id}")
        except ValueError as e:
            print(f"Error: {e}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()