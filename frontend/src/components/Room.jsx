



const Room = ({number, type, description, price_per_night, discount_price_per_night, capacity}) => {
  return (
    <article className='room-card'>
          <h1 className='room-title'>A {type} room</h1>
          <div className="content">
              <h4>Number: {number}</h4>
              <p className='description'>
                  {
                      description
                  }
              </p>
              <div className="price-box">
                  {
                      discount_price_per_night ? <h3 className='price'>{discount_price_per_night}</h3> :
                        <h3 className="price">{price_per_night}</h3>
                  }
              </div>
              <span className='capacity'>{capacity}</span>
            </div>
    </article>
  )
}

export default Room
