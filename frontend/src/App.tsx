import React, { useEffect, useState } from 'react';
import FFTWave from './FFTWave';
import useAudioPipe from './useAudioPipe';
import Avatar from './Avatar';
import { AvatarEvent } from './types';

const App: React.FC = () => {
  const [state, setState] = useState<AvatarEvent>('idle');
  const [response, setResponse] = useState('');
  const { rms } = useAudioPipe();  // For audio visualization

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000');
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setState(data.state);
      if (data.data?.response) setResponse(data.data.response);
    };
    ws.onopen = () => ws.send(JSON.stringify({ action: 'start' }));
    return () => ws.close();
  }, []);

  return (
    <div>
      <Avatar event={state} />
      <FFTWave rms={rms} />
      <p>{response}</p>
    </div>
  );
};

export default App;
