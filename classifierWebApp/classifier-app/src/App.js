import React from 'react';
import TranscriptTextArea from './components/TranscriptTextArea';
import DecorativeBanner from './components/DecorativeBanner';
import './styles/App.css';

function App() {
  return (
    <div className="App">
      <DecorativeBanner/>
      <TranscriptTextArea/>
    </div>
  );
}

export default App;
