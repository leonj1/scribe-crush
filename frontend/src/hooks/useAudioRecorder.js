import { useState, useRef, useCallback } from 'react';
import { recordingService } from '../services/api';

export const useAudioRecorder = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [recordingId, setRecordingId] = useState(null);
  const [chunkIndex, setChunkIndex] = useState(0);
  
  const mediaRecorderRef = useRef(null);
  const streamRef = useRef(null);
  const chunksRef = useRef([]);
  
  const startRecording = useCallback(async () => {
    try {
      const recording = await recordingService.createRecording();
      setRecordingId(recording.id);
      
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm',
      });
      
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];
      
      mediaRecorder.ondataavailable = async (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
          
          const blob = new Blob([event.data], { type: 'audio/webm' });
          await recordingService.uploadChunk(recording.id, chunkIndex, blob);
          setChunkIndex((prev) => prev + 1);
        }
      };
      
      mediaRecorder.start();
      const interval = setInterval(() => {
        if (mediaRecorder.state === 'recording') {
          mediaRecorder.requestData();
        }
      }, 10000);
      
      mediaRecorder.onstop = () => {
        clearInterval(interval);
      };
      
      setIsRecording(true);
      setIsPaused(false);
    } catch (error) {
      console.error('Error starting recording:', error);
      throw error;
    }
  }, [chunkIndex]);
  
  const pauseRecording = useCallback(async () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.pause();
      setIsPaused(true);
      
      if (recordingId) {
        await recordingService.pauseRecording(recordingId);
      }
    }
  }, [recordingId]);
  
  const resumeRecording = useCallback(() => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'paused') {
      mediaRecorderRef.current.resume();
      setIsPaused(false);
    }
  }, []);
  
  const stopRecording = useCallback(async () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
      
      setIsRecording(false);
      setIsPaused(false);
      
      if (recordingId) {
        const result = await recordingService.finishRecording(recordingId);
        setRecordingId(null);
        setChunkIndex(0);
        return result;
      }
    }
  }, [recordingId]);
  
  return {
    isRecording,
    isPaused,
    recordingId,
    startRecording,
    pauseRecording,
    resumeRecording,
    stopRecording,
  };
};
