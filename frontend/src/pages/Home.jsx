import { useState } from "react";
import { FiCalendar, FiUsers, FiHome } from "react-icons/fi";
import heroBg from "../assets/hotel/heroBg.jpg";
import '../css/Home.css'


const Home = () => {
    const [adults, setAdults] = useState(1);
    const [children, setChildren] = useState(0);
    const [rooms, setRooms] = useState(1);

    return (
        <div className="wrapper">
            <div className="home" style={{ backgroundImage: `url(${heroBg})` }}>
                <div className="left-section">
                    <h1 className="hero-title">Enjoy A Luxury Experience</h1>
                    <p className="hero-desc">
                       Where Timeless Elegance Meets Unrivaled Comfort.Subheadline: Step into a sanctuary of refined luxury, bespoke service, and unforgettable moments. From panoramic city views to Michelin-inspired dining, every detail of your stay is crafted to perfection.CTA: Reserve Your Stay
                    </p>
                    <button className="hero-btn">Visit us</button>
                </div>

                <div className="right-section">
                    <form action="/search" method="GET" className="search-form">
                        <h2 className="form-title">Book A Room</h2>

                        <div className="check-dates">
                            <div className="date-field">
                                <label htmlFor="check-in">Check in date</label>
                                <div className="input-icon-group">
                                    <FiCalendar className="field-icon" />
                                    <input
                                        name="check-in"
                                        id="check-in"
                                        type="date"
                                        className="check-date"
                                    />
                                </div>
                            </div>

                            <div className="date-field">
                                <label htmlFor="check-out">
                                    Check out date
                                </label>
                                <div className="input-icon-group">
                                    <FiCalendar className="field-icon" />
                                    <input
                                        name="check-out"
                                        id="check-out"
                                        type="date"
                                        className="check-date"
                                    />
                                </div>
                            </div>
                        </div>

                        <div className="field-group">
                            <label htmlFor="adults-select">Adults</label>
                            <div className="input-icon-group">
                                <FiUsers className="field-icon" />
                                <select
                                    id="adults-select"
                                    className="adults"
                                    value={adults}
                                    onChange={(e) => setAdults(e.target.value)}
                                >
                                    {[1, 2, 3, 4, 5].map((n) => (
                                        <option key={n} value={n}>
                                            {n} {n === 1 ? "Adult" : "Adults"}
                                        </option>
                                    ))}
                                </select>
                            </div>
                        </div>

                        <div className="child-room">
                            <div className="field-group">
                                <label htmlFor="child-select">Children</label>
                                <div className="input-icon-group">
                                    <FiUsers className="field-icon" />
                                    <select
                                        id="child-select"
                                        className="childs"
                                        value={children}
                                        onChange={(e) =>
                                            setChildren(e.target.value)
                                        }
                                    >
                                        {[0, 1, 2, 3, 4].map((n) => (
                                            <option key={n} value={n}>
                                                {n}{" "}
                                                {n === 1 ? "Child" : "Children"}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                            </div>

                            <div className="field-group">
                                <label htmlFor="room-select">Rooms</label>
                                <div className="input-icon-group">
                                    <FiHome className="field-icon" />
                                    <select
                                        id="room-select"
                                        className="rooms"
                                        value={rooms}
                                        onChange={(e) =>
                                            setRooms(e.target.value)
                                        }
                                    >
                                        {[1, 2, 3, 4].map((n) => (
                                            <option key={n} value={n}>
                                                {n} {n === 1 ? "Room" : "Rooms"}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                            </div>
                        </div>

                        <button type="submit" className="search-submit-btn">
                            Search Rooms
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default Home;
