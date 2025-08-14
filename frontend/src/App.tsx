import React, { useEffect, useState, useRef } from 'react';
import VoxWaveform from './VoxWaveform';  // New visualizer
import Avatar from './Avatar';
import { AvatarEvent } from './types';

const App: React.FC = () => {
  const [state, setState] = useState<AvatarEvent>('idle');
  const [response, setResponse] = useState('');
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const sourceRef = useRef<MediaStreamAudioSourceNode | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    audioContextRef.current = new AudioContext();
    analyserRef.current = audioContextRef.current.createAnalyser();
    analyserRef.current.fftSize = 2048;

    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
      sourceRef.current = audioContextRef.current!.createMediaStreamSource(stream);
      sourceRef.current.connect(analyserRef.current!);
    });

    wsRef.current = new WebSocket('ws://localhost:8000');
    wsRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setState(data.state);
      if (data.data?.response) setResponse(data.data.response);
      if (data.audio_chunk) {
        // Decode and play TTS chunk, connect to analyser for viz
        const chunk = new Float32Array(data.audio_chunk);
        const buffer = audioContextRef.current!.createBuffer(1, chunk.length, 24000);
        buffer.copyToChannel(chunk, 0);
        const bufferSource = audioContextRef.current!.createBufferSource();
        bufferSource.buffer = buffer;
        bufferSource.connect(analyserRef.current!);
        bufferSource.connect(audioContextRef.current!.destination);
        bufferSource.start();
      }
    };
    wsRef.current.onopen = () => wsRef.current!.send(JSON.stringify({ action: 'start' }));
    return () => wsRef.current?.close();
  }, []);

  return (
    <div>
      <Avatar event={state} />
      <VoxWaveform analyser={analyserRef.current} state={state} />
      <p>{response}</p>
    </div>
  );
};

export default App;
