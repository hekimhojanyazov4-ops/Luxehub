import '../css/NavBar.css'
import {  NavLink } from 'react-router-dom'

const NavBar = () => {
  return (
    <nav className='navbar'>
          <div className="navbar-brand">
              <NavLink to="/" className="navbar-brand-link">
                  Luxe 
                  <span>Hub</span>
              </NavLink>
          </div>
          <ul className="nav-links">
              <li className="nav-item"><NavLink to="/" className="nav-link">Home</NavLink></li>
              <li className="nav-item"><NavLink to="/about" className="nav-link">About</NavLink></li>
              <li className="nav-item"><NavLink to="/rooms" className="nav-link">Our rooms</NavLink></li>
              <li className="nav-item"><NavLink to="/facilities" className="nav-link">Facilities</NavLink></li>
              <li className="nav-item"><NavLink to="/blog" className="nav-link">Blog</NavLink></li>
              <li className="nav-item"><NavLink to="/contact" className="nav-link">Contact</NavLink></li>
          </ul>
          <button className="reservation-btn">
            RESERVATION
          </button>
    </nav>
  )
}

export default NavBar
