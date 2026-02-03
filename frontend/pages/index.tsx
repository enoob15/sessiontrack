import React, { useState, useEffect } from 'react';
import Head from 'next/head';

interface Session {
  id: string;
  timestamp: string;
  project?: string;
  participants: string[];
  total_messages: number;
  ai_summary?: string;
}

export default function Home() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [selectedSession, setSelectedSession] = useState<Session | null>(null);

  useEffect(() => {
    // Fetch sessions from backend
    const fetchSessions = async () => {
      try {
        const response = await fetch('/api/sessions');
        const data = await response.json();
        setSessions(data);
      } catch (error) {
        console.error('Failed to fetch sessions', error);
      }
    };

    fetchSessions();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <Head>
        <title>SessionTrack - Memory Management</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="container mx-auto">
        <h1 className="text-4xl font-bold mb-8">SessionTrack Dashboard</h1>

        <div className="grid grid-cols-3 gap-8">
          {/* Sessions List */}
          <div className="col-span-1 bg-white shadow-md rounded-lg p-6">
            <h2 className="text-2xl font-semibold mb-4">Captured Sessions</h2>
            {sessions.map(session => (
              <div 
                key={session.id} 
                className="cursor-pointer hover:bg-gray-100 p-2 rounded"
                onClick={() => setSelectedSession(session)}
              >
                <p className="font-medium">{session.project || 'Untitled Session'}</p>
                <p className="text-sm text-gray-500">{new Date(session.timestamp).toLocaleString()}</p>
              </div>
            ))}
          </div>

          {/* Session Details */}
          <div className="col-span-2 bg-white shadow-md rounded-lg p-6">
            {selectedSession ? (
              <>
                <h2 className="text-2xl font-semibold mb-4">
                  {selectedSession.project || 'Session Details'}
                </h2>
                <div className="mb-4">
                  <p><strong>Timestamp:</strong> {new Date(selectedSession.timestamp).toLocaleString()}</p>
                  <p><strong>Participants:</strong> {selectedSession.participants.join(', ')}</p>
                  <p><strong>Total Messages:</strong> {selectedSession.total_messages}</p>
                </div>
                
                {selectedSession.ai_summary && (
                  <div className="bg-blue-50 p-4 rounded">
                    <h3 className="font-semibold mb-2">AI Summary</h3>
                    <p>{selectedSession.ai_summary}</p>
                  </div>
                )}
              </>
            ) : (
              <p className="text-gray-500">Select a session to view details</p>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}