import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import positiveBg from './positive.png';
import neutralBg from './neutral.png';
import negativeBg from './youtube.png';
const VideoAnalyzer = () => {
  const [videoLink, setVideoLink] = useState('');
  const [sentimentData, setSentimentData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [backgroundImg, setBackgroundImg] = useState('./youtube.png');

  const extractVideoId = (link) => {
    const videoIdMatch = link.match(/(?:\?v=|&v=|youtu\.be\/)(.*?)(?:\?|$)/);
    return videoIdMatch ? videoIdMatch[1] : null;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const videoId = extractVideoId(videoLink);
    if (videoId) {
      try {
        const response = await axios.post('http://localhost:5000/', { video_id: videoId });
        const { report, positive_percentage, neutral_percentage, negative_percentage } = response.data;
        setSentimentData({
          report,
          positive: positive_percentage,
          neutral: neutral_percentage,
          negative: negative_percentage,
        });

        // Determine the class with the highest percentage
        if (positive_percentage > neutral_percentage && positive_percentage > negative_percentage) {
          setBackgroundImg(positiveBg);
        } else if (neutral_percentage > positive_percentage && neutral_percentage > negative_percentage) {
          setBackgroundImg(neutralBg);
        } else {
          setBackgroundImg(negativeBg);
        }
      } catch (error) {
        console.error('Error:', error);
      }
    } else {
      console.error('Invalid YouTube video link');
    }
    setLoading(false);
  };

  return (
    <div className="main-container" style={{ backgroundImage: `url(${backgroundImg})` }}>
      <div className="container">
        <h1 className="heading"> YouTube Comment Sentiment Analyzer </h1>
        <form onSubmit={handleSubmit}>
          <label htmlFor="videoLink">Enter the YouTube link:</label>
          <input
            type="text"
            id="videoLink"
            value={videoLink}
            onChange={(e) => setVideoLink(e.target.value)}
            placeholder="video link"
            required
          />
          <button type="submit" disabled={loading} className="analyze-button">
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </form>
        {sentimentData && (
          <div>
            <h2>Sentiment Analysis Results</h2>
            <div>
              <p>Positive 😊:</p>
              <div style={{ display: 'flex', alignItems: 'center' }}>
                <div
                  style={{
                    width: `${sentimentData.positive}%`,
                    backgroundColor: 'green',
                    height: '20px',
                    marginRight: '5px',
                  }}
                />
                <p>{`${sentimentData.positive.toFixed(2)}%`}</p>
              </div>
            </div>
            <div>
              <p>Neutral 😐:</p>
              <div style={{ display: 'flex', alignItems: 'center' }}>
                <div
                  style={{
                    width: `${sentimentData.neutral}%`,
                    backgroundColor: 'grey',
                    height: '20px',
                    marginRight: '5px',
                  }}
                />
                <p>{`${sentimentData.neutral.toFixed(2)}%`}</p>
              </div>
            </div>
            <div>
              <p>Negative 😠:</p>
              <div style={{ display: 'flex', alignItems: 'center' }}>
                <div
                  style={{
                    width: `${sentimentData.negative}%`,
                    backgroundColor: 'red',
                    height: '20px',
                    marginRight: '5px',
                  }}
                />
                <p>{`${sentimentData.negative.toFixed(2)}%`}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default VideoAnalyzer;

