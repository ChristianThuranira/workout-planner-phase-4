import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Box, Typography, Stack } from '@mui/material';
import { fetchData } from '../utils/fetchData';

const Day = () => {
  const { id } = useParams();
  const [workoutPlans, setWorkoutPlans] = useState([]);

  useEffect(() => {
    const fetchWorkoutPlans = async () => {
      const data = await fetchData(`http://localhost:5000/api/days/${id}/workouts`);
      setWorkoutPlans(data);
    };

    fetchWorkoutPlans();
  }, [id]);

  return (
    <Box>
      <Typography variant="h3" textAlign="center">Workouts for This Day</Typography>
      <Stack direction="column" alignItems="center">
        {workoutPlans.map((workout) => (
          <Typography key={workout.id}>{workout.title} - {workout.description}</Typography>
        ))}
      </Stack>
    </Box>
  );
};

export default Day;
