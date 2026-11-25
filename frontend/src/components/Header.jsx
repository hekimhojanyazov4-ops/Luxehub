import React from 'react'

import NavBar from './NavBar'
import { LuHotel, LuSearch, LuUser } from 'react-icons/lu'
import { Link } from 'react-router-dom'

const Header = () => {
  return (
      <header className='header'>
          <NavBar/>
    </header>
  )
}

export default Header
