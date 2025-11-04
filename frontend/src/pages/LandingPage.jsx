import React from 'react';
import { Button } from 'antd';
import { GoogleOutlined } from '@ant-design/icons';
import { authService } from '../services/api';
import './LandingPage.css';

const LandingPage = () => {
  const handleLogin = () => {
    window.location.href = authService.getLoginUrl();
  };

  return (
    <div className="landing-page">
      <div className="hero-section">
        <div className="hero-content">
          <h1>Audio Transcription Service</h1>
          <p>Secure and efficient transcription for healthcare professionals</p>
          <Button
            type="primary"
            size="large"
            icon={<GoogleOutlined />}
            onClick={handleLogin}
            className="login-button"
          >
            Login with Google
          </Button>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
