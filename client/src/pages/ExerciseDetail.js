import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Box } from '@mui/material';
import { fetchData } from '../utils/fetchData';
import Detail from '../components/Detail';
import ExerciseVideos from '../components/ExerciseVideos';

const ExerciseDetail = () => {
  const { id } = useParams();
  const [exerciseDetail, setExerciseDetail] = useState({});
  const [exerciseVideos, setExerciseVideos] = useState([]);

  useEffect(() => {
    const fetchExerciseData = async () => {
      const exerciseData = await fetchData(`http://localhost:5000/api/exercises/${id}`);
      setExerciseDetail(exerciseData);

      const videosData = await fetchData(`http://localhost:5000/api/exercises/${id}/videos`);
      setExerciseVideos(videosData);
    };

    fetchExerciseData();
  }, [id]);

  return (
    <Box>
      <Detail exerciseDetail={exerciseDetail} />
      <ExerciseVideos exerciseVideos={exerciseVideos} name={exerciseDetail.name} />
    </Box>
  );
};

export default ExerciseDetail;
