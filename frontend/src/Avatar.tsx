import React from 'react';
import { AvatarEvent } from './types';

interface Props {
  event: AvatarEvent;
}

const Avatar: React.FC<Props> = ({ event }) => {
  let emoji = '😊';  // Default idle
  switch (event) {
    case 'listening': emoji = '👂'; break;
    case 'thinking': emoji = '🤔'; break;
    case 'speaking': emoji = '🗣️'; break;
    case 'error': emoji = '😕'; break;
  }
  return <div style={{ fontSize: '100px' }}>{emoji}</div>;
};

export default Avatar;
