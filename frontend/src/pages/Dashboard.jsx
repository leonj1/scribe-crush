import React, { useState, useEffect } from 'react';
import { Layout, Avatar, Dropdown, List, Button, Card, Input, message } from 'antd';
import { UserOutlined, LogoutOutlined, AudioOutlined, PauseCircleOutlined, PlayCircleOutlined, StopOutlined } from '@ant-design/icons';
import { authService, recordingService } from '../services/api';
import { useAudioRecorder } from '../hooks/useAudioRecorder';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';

const { Header, Sider, Content } = Layout;
const { TextArea } = Input;

const Dashboard = () => {
  const navigate = useNavigate();
  const [recordings, setRecordings] = useState([]);
  const [selectedRecording, setSelectedRecording] = useState(null);
  const [notes, setNotes] = useState('');
  const { isRecording, isPaused, startRecording, pauseRecording, resumeRecording, stopRecording } = useAudioRecorder();

  useEffect(() => {
    loadRecordings();
  }, []);

  const loadRecordings = async () => {
    try {
      const data = await recordingService.listRecordings();
      setRecordings(data);
    } catch (error) {
      message.error('Failed to load recordings');
    }
  };

  const handleLogout = () => {
    authService.logout();
    navigate('/');
  };

  const handleStartRecording = async () => {
    try {
      await startRecording();
      message.success('Recording started');
    } catch (error) {
      message.error('Failed to start recording');
    }
  };

  const handlePauseRecording = async () => {
    try {
      await pauseRecording();
      message.info('Recording paused');
    } catch (error) {
      message.error('Failed to pause recording');
    }
  };

  const handleResumeRecording = async () => {
    try {
      await resumeRecording();
      message.success('Recording resumed');
    } catch (error) {
      message.error('Failed to resume recording');
    }
  };

  const handleStopRecording = async () => {
    try {
      const result = await stopRecording();
      message.success('Recording completed and transcription started');
      await loadRecordings();
    } catch (error) {
      message.error('Failed to stop recording');
    }
  };

  const handleSelectRecording = async (recording) => {
    setSelectedRecording(recording);
    setNotes(recording.notes || '');
  };

  const handleSaveNotes = async () => {
    if (selectedRecording) {
      try {
        await recordingService.updateNotes(selectedRecording.id, notes);
        message.success('Notes saved');
        await loadRecordings();
      } catch (error) {
        message.error('Failed to save notes');
      }
    }
  };

  const menuItems = [
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: 'Logout',
      onClick: handleLogout,
    },
  ];

  return (
    <Layout className="dashboard-layout">
      <Header className="dashboard-header">
        <div className="header-title">Audio Transcription Service</div>
        <Dropdown menu={{ items: menuItems }} placement="bottomRight">
          <Avatar icon={<UserOutlined />} className="user-avatar" />
        </Dropdown>
      </Header>
      <Layout>
        <Sider width={300} className="recordings-sider">
          <div className="sider-header">
            <h3>Recordings</h3>
          </div>
          <List
            dataSource={recordings}
            renderItem={(recording) => (
              <List.Item
                className={selectedRecording?.id === recording.id ? 'selected' : ''}
                onClick={() => handleSelectRecording(recording)}
              >
                <List.Item.Meta
                  title={new Date(recording.created_at).toLocaleString()}
                  description={`Status: ${recording.status}`}
                />
              </List.Item>
            )}
          />
        </Sider>
        <Content className="main-content">
          {!isRecording && !selectedRecording && (
            <div className="empty-state">
              <AudioOutlined className="empty-icon" />
              <Button type="primary" size="large" onClick={handleStartRecording}>
                Start Recording
              </Button>
            </div>
          )}
          
          {isRecording && (
            <div className="recording-state">
              <div className="waveform-animation">
                <div className="wave"></div>
                <div className="wave"></div>
                <div className="wave"></div>
                <div className="wave"></div>
                <div className="wave"></div>
              </div>
              <div className="recording-controls">
                {!isPaused ? (
                  <Button icon={<PauseCircleOutlined />} onClick={handlePauseRecording}>
                    Pause
                  </Button>
                ) : (
                  <Button icon={<PlayCircleOutlined />} onClick={handleResumeRecording}>
                    Resume
                  </Button>
                )}
                <Button danger icon={<StopOutlined />} onClick={handleStopRecording}>
                  End Recording
                </Button>
              </div>
            </div>
          )}
          
          {selectedRecording && !isRecording && (
            <div className="recording-details">
              <Card title="Transcription">
                <p>{selectedRecording.transcription_text || 'Transcription in progress...'}</p>
              </Card>
              <Card title="Notes" style={{ marginTop: 16 }}>
                <TextArea
                  rows={4}
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Add notes about this recording..."
                />
                <Button type="primary" onClick={handleSaveNotes} style={{ marginTop: 8 }}>
                  Save Notes
                </Button>
              </Card>
            </div>
          )}
        </Content>
      </Layout>
    </Layout>
  );
};

export default Dashboard;
