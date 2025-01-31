import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Stack } from '@mui/material';
import { fetchData } from '../utils/fetchData';

const Navbar = () => {
  const [days, setDays] = useState([]);

  useEffect(() => {
    const getDays = async () => {
      const daysData = await fetchData('http://localhost:5000/api/days');
      setDays(daysData);
    };

    getDays();
  }, []);

  return (
    <Stack direction="row" justifyContent="space-around" px="20px">
      <Link to="/">Home</Link>
      <a href="#exercises">Exercises</a>
      {days.map((day) => (
        <Link key={day.id} to={`/day/${day.id}`}>{day.name}</Link>
      ))}
    </Stack>
  );
};

export default Navbar;
