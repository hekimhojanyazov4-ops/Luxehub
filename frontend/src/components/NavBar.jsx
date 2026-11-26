import React, { useState } from "react";
import "../css/NavBar.css";
import { NavLink } from "react-router-dom";

const NavBar = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => setIsOpen(!isOpen);
  const closeMenu = () => setIsOpen(false);

  const navLinkClass = ({ isActive }) =>
    isActive ? "nav-link active" : "nav-link";

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <NavLink to="/" onClick={closeMenu}>
          Luxe<span>Hub</span>
        </NavLink>
      </div>

      {/* Hamburger Toggle Button (Visible only on mobile) */}
      <button
        className={`menu-toggle ${isOpen ? "open" : ""}`}
        onClick={toggleMenu}
        aria-label="Toggle navigation"
        aria-expanded={isOpen}
      >
        <span></span>
        <span></span>
        <span></span>
      </button>

      {/* Navigation Links & CTA */}
      <ul className={`nav-links ${isOpen ? "active" : ""}`}>
        <li className="nav-item">
          <NavLink to="/" end className={navLinkClass} onClick={closeMenu}>
            Home
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/rooms" className={navLinkClass} onClick={closeMenu}>
            Suites
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/contact" className={navLinkClass} onClick={closeMenu}>
            Contact
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/about" className={navLinkClass} onClick={closeMenu}>
            About
          </NavLink>
        </li>
        <li className="nav-item">
          <button className="reservation-btn" onClick={closeMenu}>
            RESERVE NOW
          </button>
        </li>
      </ul>
    </nav>
  );
};

export default NavBar;
