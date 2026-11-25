import heroBg from '../assets/hotel/heroBg.jpg'

const Home = () => {
  return (
      <div className='home' style={{ backgroundImage: `url(${heroBg})` }}>
          <div className="left-section">
              <h1 className='hero-title'>
                  Enjoy A Luxuary Experience
              </h1>
              <p className="hero-desc">
                  Lorem ipsum dolor sit amet consectetur adipisicing elit. Eum, unde. Nobis nostrum ex facilis veritatis incidunt repellat ducimus nemo, quasi minima odio id temporibus, porro velit optio similique. Vero, deserunt.
              </p>
              <button className="hero-btn">
                  Visit us
              </button>
          </div>
          <div className="right-section">
            <form action="/search" method="GET" className="search-form">
                  <h2 className="form-title">Book A Room</h2>
                  <div className="check-dates">
                      <div className="checkIn">
                          <label htmlFor="check-in">
                            Check in date
                          </label>
                        <input name='check-in' type="date" className="check-date" />
                      </div>
                      <div className="checkOut">
                          <label htmlFor="check-out">Check in date</label>
                        <input name='check-out' type="date" className="check-date" />
                      </div>
                  </div>
                  <div className="adults">
                      <select className="adults" id="">
                          <option value="">Adults</option>
                          <option value="">2</option>
                      </select>
                  </div>
                  <div className="child-room">
                      <select className="childs">Child</select>
                      <select className="rooms">Rooms</select>
                  </div>
            </form>
        </div>
    </div>
  )
}

export default Home
