import React, { useState, useEffect } from 'react';
import Head from 'next/head';

interface Session {
  id: string;
  timestamp: string;
  project?: string;
  participants: string[];
  total_messages: number;
  ai_insights?: {
    summary?: string;
    topics?: string[];
    action_items?: string[];
  };
}

interface Project {
  id: string;
  name: string;
  description?: string;
  status: string;
  total_sessions: number;
  total_action_items: number;
}

export default function Dashboard() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedSession, setSelectedSession] = useState<Session | null>(null);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);

  useEffect(() => {
    // Fetch sessions and projects
    const fetchData = async () => {
      try {
        // Mock API calls - will replace with actual backend later
        const sessionsResponse = await fetch('/api/sessions');
        const projectsResponse = await fetch('/api/projects');
        
        const sessionsData = await sessionsResponse.json();
        const projectsData = await projectsResponse.json();
        
        setSessions(sessionsData);
        setProjects(projectsData);
      } catch (error) {
        console.error('Failed to fetch data', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <Head>
        <title>SessionTrack Dashboard</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="container mx-auto">
        <h1 className="text-4xl font-bold mb-8">SessionTrack Dashboard</h1>

        <div className="grid grid-cols-3 gap-8">
          {/* Projects List */}
          <div className="col-span-1 bg-white shadow-md rounded-lg p-6">
            <h2 className="text-2xl font-semibold mb-4">Projects</h2>
            {projects.map(project => (
              <div 
                key={project.id} 
                className="cursor-pointer hover:bg-gray-100 p-2 rounded"
                onClick={() => setSelectedProject(project)}
              >
                <p className="font-medium">{project.name}</p>
                <p className="text-sm text-gray-500">
                  {project.total_sessions} sessions | {project.total_action_items} action items
                </p>
              </div>
            ))}
          </div>

          {/* Sessions List */}
          <div className="col-span-1 bg-white shadow-md rounded-lg p-6">
            <h2 className="text-2xl font-semibold mb-4">Recent Sessions</h2>
            {sessions.map(session => (
              <div 
                key={session.id} 
                className="cursor-pointer hover:bg-gray-100 p-2 rounded"
                onClick={() => setSelectedSession(session)}
              >
                <p className="font-medium">{session.project || 'Untitled Session'}</p>
                <p className="text-sm text-gray-500">
                  {new Date(session.timestamp).toLocaleString()}
                </p>
              </div>
            ))}
          </div>

          {/* Details Panel */}
          <div className="col-span-1 bg-white shadow-md rounded-lg p-6">
            <h2 className="text-2xl font-semibold mb-4">Details</h2>
            
            {selectedSession && (
              <div>
                <h3 className="font-bold text-xl mb-2">Session Details</h3>
                <p><strong>Project:</strong> {selectedSession.project || 'N/A'}</p>
                <p><strong>Timestamp:</strong> {new Date(selectedSession.timestamp).toLocaleString()}</p>
                <p><strong>Participants:</strong> {selectedSession.participants.join(', ')}</p>
                <p><strong>Total Messages:</strong> {selectedSession.total_messages}</p>
                
                {selectedSession.ai_insights && (
                  <div className="mt-4">
                    <h4 className="font-semibold">AI Insights</h4>
                    {selectedSession.ai_insights.summary && (
                      <div>
                        <p className="font-medium">Summary:</p>
                        <p className="text-sm">{selectedSession.ai_insights.summary}</p>
                      </div>
                    )}
                    
                    {selectedSession.ai_insights.topics && (
                      <div className="mt-2">
                        <p className="font-medium">Topics:</p>
                        <ul className="list-disc list-inside text-sm">
                          {selectedSession.ai_insights.topics.map((topic, index) => (
                            <li key={index}>{topic}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    
                    {selectedSession.ai_insights.action_items && (
                      <div className="mt-2">
                        <p className="font-medium">Action Items:</p>
                        <ul className="list-disc list-inside text-sm">
                          {selectedSession.ai_insights.action_items.map((item, index) => (
                            <li key={index}>{item}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
            
            {selectedProject && (
              <div>
                <h3 className="font-bold text-xl mb-2">Project Details</h3>
                <p><strong>Name:</strong> {selectedProject.name}</p>
                <p><strong>Status:</strong> {selectedProject.status}</p>
                <p><strong>Total Sessions:</strong> {selectedProject.total_sessions}</p>
                <p><strong>Total Action Items:</strong> {selectedProject.total_action_items}</p>
              </div>
            )}
            
            {!selectedSession && !selectedProject && (
              <p className="text-gray-500">Select a session or project to view details</p>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}