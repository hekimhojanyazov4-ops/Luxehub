import React from "react";
import "../css/About.css";
import image1 from "../assets/hotel/5.jpg";
import image2 from "../assets/hotel/2.jpg";

const About = () => {
    return (
        <section className="about-page" id="about">
            <div className="about-wrapper">
                {/* Left: Overlapping Architectural Collage */}
                <div className="about-images">
                    <div className="accent-backdrop"></div>
                    <img
                        className="image1"
                        src={image1}
                        alt="LuxeHub Hotel architectural lobby"
                    />
                    <img
                        className="image2"
                        src={image2}
                        alt="LuxeHub Hotel luxury suite"
                    />
                </div>

                {/* Right: Editorial Story & Highlights */}
                <div className="about-content">
                    <span className="about-subtitle">Our Story</span>
                    <h2>Where Timeless Elegance Meets Modern Comfort</h2>
                    <p className="about-lead">
                        At <strong>LuxeHub Hotel</strong>, hospitality is
                        elevated to an art form, blending timeless architectural
                        elegance with modern sophistication.
                    </p>
                    <p className="about-body">
                        Designed as an urban sanctuary for discerning travelers,
                        our property pairs bespoke, intuitive service with
                        world-class amenities—from serene, architecturally
                        curated suites and a restorative thermal spa to
                        signature fine dining crafted by acclaimed chefs. Every
                        detail is thoughtfully tailored to transform a simple
                        stay into an unforgettable experience.
                    </p>

                    {/* Luxury Metrics Strip */}
                    <div className="about-stats">
                        <div className="stat-item">
                            <span className="stat-number">48</span>
                            <span className="stat-label">Curated Suites</span>
                        </div>
                        <div className="stat-divider"></div>
                        <div className="stat-item">
                            <span className="stat-number">5★</span>
                            <span className="stat-label">Michelin Dining</span>
                        </div>
                        <div className="stat-divider"></div>
                        <div className="stat-item">
                            <span className="stat-number">24/7</span>
                            <span className="stat-label">
                                Private Concierge
                            </span>
                        </div>
                    </div>

                    <a href="#rooms" className="about-cta">
                        Discover Our Suites <span>→</span>
                    </a>
                </div>
            </div>
        </section>
    );
};

export default About;
