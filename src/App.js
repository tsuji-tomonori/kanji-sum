import React, { useState } from 'react';
import axios from 'axios';
import './styles/App.css';

// KanjiCard component
function KanjiCard({ kanji }) {
  return (
    <div className="kanji-card">
      <h2>{kanji.font}</h2>
      <p>Total strokes (reference): {kanji["総画数(参考)"]}</p>
      <p>Reading (reference): {kanji["読み(参考)"]}</p>
    </div>
  );
}

// App component
function App() {
  const [input, setInput] = useState('');
  const [kanjiList, setKanjiList] = useState([]);
  const [kanjiSum, setKanjiSum] = useState(null);

  const calculateStrokeCount = () => {
    if (input) {
      axios.get(`https://kkmmccgnfi.execute-api.ap-northeast-1.amazonaws.com/v1/kanji?tokens=${encodeURIComponent(input)}`)
        .then(response => {
          setKanjiList(response.data.kanji_list);
          setKanjiSum(response.data.kanji_sum);
        })
        .catch(error => {
          console.error('Error fetching data: ', error);
          setKanjiList([]);
          setKanjiSum(null);
        });
    } else {
      setKanjiList([]);
      setKanjiSum(null);
    }
  };

  return (
    <div className="container bg-gray-900 text-white">
      <h1 className="title">Kanji Stroke Count</h1>
      <div className="card">
        <input 
          type="text" 
          value={input} 
          onChange={e => setInput(e.target.value)} 
          className="input text-lg px-3 py-2 w-full"
          placeholder="Enter Kanji"
        />
        <button 
          onClick={calculateStrokeCount} 
          className="button mt-4 w-full"
        >
          Calculate
        </button>
        {kanjiSum !== null && <p className="mt-4">Stroke count: {kanjiSum}</p>}
      </div>
      <div className="kanji-list">
        {kanjiList.map((kanji, index) => (
          <KanjiCard key={index} kanji={kanji} />
        ))}
      </div>
    </div>
  );
};

export default App;
