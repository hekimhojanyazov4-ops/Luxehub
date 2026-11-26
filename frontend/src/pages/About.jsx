import '../css/About.css'
import image1 from '../assets/hotel/5.jpg'
import image2 from '../assets/hotel/2.jpg'


const About = () => {
    return (
        <section className="about-page">
            <div className="about-images">
                <img className="image1" src={image1} alt="LuxeHub Hotel interior" />
                <img className="image2" src={image2} alt="LuxeHub hotel interior" />
            </div>

            <div className="about-content">
                <span className="about-subtitle">Our Story</span>
                <h2>Where Timeless Elegance Meets Modern Comfort</h2>
                <p>
                    At <strong>LuxeHub Hotel</strong>, hospitality is elevated
                    to an art form, blending timeless architectural elegance
                    with modern sophistication. Designed as an urban sanctuary
                    for discerning travelers, our property pairs bespoke,
                    intuitive service with world-class amenities—from serene,
                    architecturally curated suites and a restorative thermal spa
                    to signature fine dining crafted by acclaimed chefs. Whether
                    you are arriving for a quiet weekend retreat or an inspiring
                    business journey, every detail at LuxeHub is thoughtfully
                    tailored to transform a simple stay into an unforgettable
                    experience.
                </p>
            </div>
        </section>
    );
};

export default About;
