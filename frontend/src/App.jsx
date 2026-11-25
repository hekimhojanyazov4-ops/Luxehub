import Footer from './components/Footer'
import './index.css'
import Header from './components/Header'
import Home  from './pages/Home'
import { Routes, Route, Navigate } from 'react-router-dom'



const App = () => {
  return (
    <div className='app'>
      <Header />
      <main className="main">
         <Routes>
          <Route path='/' element={<Home />}></Route>
          <Route path='/home' element={<Navigate to="/" replace />} />
          <Route path='*' element={<div style={{ padding: '4rem', textAlign: 'center', fontSize: '70px', fontFamily: 'Arial', fontWeight: 'bolder', color: 'goldenrod' }}>Page not found</div>} />
        </Routes>
       </main>
      <Footer/>
    </div>
  )
}

export default App
