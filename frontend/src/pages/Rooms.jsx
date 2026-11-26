import { getAllRooms } from '../api/client'
import { useState, useEffect } from 'react'
import Room from '../components/Room'


const Rooms = () => {

  useEffect(() => {
    getAllRooms();
  }, []);

  return (
    <div className='rooms'>
        
    </div>
  )
}

export default Rooms
