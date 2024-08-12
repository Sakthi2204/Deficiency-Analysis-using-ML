import React, { useState } from 'react';
import './App.css';
import axios from 'axios';

function App() {
  const [activeContent, setActiveContent] = useState('home');
  const [symptoms, setSymptoms] = useState('');
  const [deficiencies, setDeficiencies] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/predict', { symptoms });
      setDeficiencies(response.data.deficiencies);
      setActiveContent('predictions');
    } catch (error) {
      console.error('Prediction request failed:', error);
    }
  };

  const handleMenuClick = (contentId) => {
    setActiveContent(contentId);
  };

  return (
    <div className="container">
      <div className="menu">
        <ul>
          <li><button onClick={() => handleMenuClick('home')}>Home</button></li>
          <li><button onClick={() => handleMenuClick('about')}>About Us</button></li>
          <li><button onClick={() => handleMenuClick('contact')}>Contact Us</button></li>
          <li><button onClick={() => handleMenuClick('queries')}>Queries</button></li>
          <li><button onClick={() => handleMenuClick('predictions')}>Analyze</button></li>
        </ul>
      </div>
      <div className="content">
        <div className={`homeContent ${activeContent === 'home' ? 'active' : ''}`}>
          <h2>Welcome to Deficiency Advisor for Human Health</h2>
          <p>Our website aims to provide valuable insights into nutritional deficiencies and their impact on human health.</p>
          <p>Here's what you can expect from our platform:</p>
          <ul>
            <li><strong>Information:</strong> Access comprehensive information about various nutritional deficiencies, their symptoms, and potential health consequences.</li>
            <li><strong>Analysis:</strong> Input your symptoms, and our advanced machine learning algorithms will analyze them to provide personalized recommendations and insights.</li>
            <li><strong>Expertise:</strong> Our team of healthcare professionals ensures that the information and recommendations provided are accurate, reliable, and up-to-date.</li>
            <li><strong>Community:</strong> Connect with others who are experiencing similar health concerns, share experiences, and support one another in managing nutritional deficiencies.</li>
          </ul>
          <p>Whether you're looking to learn more about nutritional deficiencies, seek guidance on managing your symptoms, or connect with a supportive community, Deficiency Advisor for Human Health is here to help you on your journey to better health and well-being.</p>
        </div>
        <div className={`aboutContent ${activeContent === 'about' ? 'active' : ''}`}>
          <h2>About Us</h2>
          <p>Our mission is to promote awareness and understanding of nutritional deficiencies and their impact on human health.</p>
          <p>We believe that education is key to prevention and early intervention. By providing accessible and reliable information, we empower individuals to take control of their health and make informed decisions.</p>
          <p>At Deficiency Advisor for Human Health, we are committed to delivering accurate and up-to-date information, supported by evidence-based research and expertise from healthcare professionals.</p>
        </div>
        <div className={`contactContent ${activeContent === 'contact' ? 'active' : ''}`}>
          <h2>Contact Us</h2>
          <p>If you have any questions or concerns, please feel free to reach out to us:</p>
          <ul>
            <li>Email: contact@example.com</li>
            <li>Phone: +1234567890</li>
            <li>Address: RMK Engineering College, Kavaraipettai, Gummidipoondi.</li>
          </ul>
        </div>
        <div className={`queriesContent ${activeContent === 'queries' ? 'active' : ''}`}>
          <h2>Queries</h2>
          <p>Here are some common queries related to our website:</p>
          <ul>
            <li>How can I register for an account?</li>
            <p>There is no registration for an account.</p>
            <li>What symptoms should I provide for analysis?</li>
            <p>You can provide the symptoms that are unusual from the regular behavior.</p>
            <li>How accurate are the predictions for nutritional deficiencies?</li>
            <p>We can provide you the most accurate predictions based on your symptoms.</p>
            <li>Can I get personalized recommendations based on my symptoms?</li>
            <p>Yes, you can get personalized recommendations based on your concerns with consultation from your nearby hospital.</p>
            <li>Is my personal information secure on this website?</li>
            <p>Yes, your personal information is secure, and we mostly do not need your personal information.</p>
          </ul>
          <p>For any further queries, please feel free to contact us via email or phone.</p>
        </div>
        <div className={`predictionsContent ${activeContent === 'predictions' ? 'active' : ''}`}>
          <h2>Enter your Symptoms</h2>
          <form onSubmit={handleSubmit}>
            <input type="text" value={symptoms} onChange={(e) => setSymptoms(e.target.value)} placeholder="Enter your symptoms..." />
            <button type="submit">Predict</button>
          </form>
          {deficiencies.length > 0 && (
            <div>
              <h3>Predicted Deficiencies:</h3>
              <ul>
                {deficiencies.map((deficiency, index) => (
                  <li key={index}>{deficiency.join(', ')}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;



