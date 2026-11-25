// import heroBg from '../assets/hotel/heroBg.jpg'

// const Home = () => {
//   return (
//       <div className='home' style={{ backgroundImage: `url(${heroBg})` }}>
//           <div className="left-section">
//               <h1 className='hero-title'>
//                   Enjoy A Luxuary Experience
//               </h1>
//               <p className="hero-desc">
//                   Lorem ipsum dolor sit amet consectetur adipisicing elit. Eum, unde. Nobis nostrum ex facilis veritatis incidunt repellat ducimus nemo, quasi minima odio id temporibus, porro velit optio similique. Vero, deserunt.
//               </p>
//               <button className="hero-btn">
//                   Visit us
//               </button>
//           </div>
//           <div className="right-section">
//             <form action="/search" method="GET" className="search-form">
//                   <h2 className="form-title">Book A Room</h2>
//                   <div className="check-dates">
//                       <div className="checkIn">
//                           <label htmlFor="check-in">
                              
//                             Check in date
//                           </label>
//                         <input name='check-in' type="date" className="check-date" />
//                       </div>
//                       <div className="checkOut">
//                           <label htmlFor="check-out">Check in date</label>
//                         <input name='check-out' type="date" className="check-date" />
//                       </div>
//                   </div>
//                   <div className="adults">
//                       <select className="adults" id="">
//                           <option value="">Adults</option>
//                           <option value="">2</option>
//                       </select>
//                   </div>
//                   <div className="child-room">
//                       <select className="childs">Child</select>
//                       <select className="rooms">Rooms</select>
//                   </div>
//             </form>
//         </div>
//     </div>
//   )
// }

// export default Home



import { useState } from "react";
import { FiCalendar, FiUsers, FiHome } from "react-icons/fi";
import heroBg from "../assets/hotel/heroBg.jpg";

const Home = () => {
    const [adults, setAdults] = useState(1);
    const [children, setChildren] = useState(0);
    const [rooms, setRooms] = useState(1);

    return (
        <div className="home" style={{ backgroundImage: `url(${heroBg})` }}>
            <div className="left-section">
                <h1 className="hero-title">Enjoy A Luxury Experience</h1>
                <p className="hero-desc">
                    Lorem ipsum dolor sit amet consectetur adipisicing elit.
                    Eum, unde. Nobis nostrum ex facilis veritatis incidunt
                    repellat ducimus nemo, quasi minima odio id temporibus,
                    porro velit optio similique. Vero, deserunt.
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
                            <label htmlFor="check-out">Check out date</label>
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
                                            {n} {n === 1 ? "Child" : "Children"}
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
                                    onChange={(e) => setRooms(e.target.value)}
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
    );
};

export default Home;
