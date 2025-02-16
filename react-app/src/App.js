// App.js
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [telemetry, setTelemetry] = useState(null);

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:4000');

    socket.onopen = () => {
      console.log('WebSocket connection established');
    };

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setTelemetry(data);
      } catch (error) {
        console.error('Error parsing telemetry data:', error);
      }
    };

    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    socket.onclose = (event) => {
      console.log('WebSocket connection closed:', event);
    };

    // Clean up the connection on component unmount
    return () => socket.close();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Ground Station Dashboard</h1>
      </header>
      <main>
        <section>
          <h2>Telemetry</h2>
          {telemetry ? (
            <ul>
              <li>Altitude: {telemetry.altitude} m</li>
              <li>Speed: {telemetry.speed} km/h</li>
              <li>Heading: {telemetry.heading}°</li>
            </ul>
          ) : (
            <p>Waiting for telemetry data...</p>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
