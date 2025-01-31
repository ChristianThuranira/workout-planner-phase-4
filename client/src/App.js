import React, { useEffect, useState } from 'react';
import { Route, Routes } from 'react-router-dom';
import { Box } from '@mui/material';
import axios from 'axios';

import './App.css';
import ExerciseDetail from './pages/ExerciseDetail';
import Home from './pages/Home';
import Navbar from './components/Navbar';
import Footer from './components/Footer';

const App = () => {
  const [exercises, setExercises] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchExercises = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/exercises');
        setExercises(response.data);
      } catch (err) {
        console.error("Error fetching exercises:", err);
        setError("Failed to load exercises. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchExercises();
  }, []);

  return (
    <Box width="100%" sx={{ maxWidth: '1488px', mx: 'auto', px: 2 }}>
      <Navbar />
      {loading ? (
        <p>Loading exercises...</p>
      ) : error ? (
        <p style={{ color: 'red' }}>{error}</p>
      ) : (
        <Routes>
          <Route path="/" element={<Home exercises={exercises} />} />
          <Route path="/exercise/:id" element={<ExerciseDetail />} />
        </Routes>
      )}
      <Footer />
    </Box>
  );
};

export default App;
