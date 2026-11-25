import React from 'react'
import NavBar from './components/NavBar'
import './App.css'
import Header from './components/Header'
import Home  from './pages/Home'
import {Routes, Route} from 'react-router-dom'


const App = () => {
  return (
    <div className='app'>
      <Header />
      <Routes>
        <Route path='/' element={<Home />}></Route>
      </Routes>
      <Home/>
    </div>
  )
}

export default App
