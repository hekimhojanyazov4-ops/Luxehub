import { Link } from "react-router-dom";
import {
    FiFacebook,
    FiInstagram,
    FiMail,
    FiMapPin,
    FiPhone,
    FiTwitter,
} from "react-icons/fi";

const EXPLORE_LINKS = [
    { label: "Rooms & Suites", to: "/rooms" },
    { label: "Book A Stay", to: "/booking" },
    { label: "Gallery", to: "/gallery" },
    { label: "Offers", to: "/offers" },
];

const COMPANY_LINKS = [
    { label: "About Us", to: "/about" },
    { label: "Careers", to: "/careers" },
    { label: "Reviews", to: "/reviews" },
    { label: "Contact", to: "/contact" },
];

const SUPPORT_LINKS = [
    { label: "FAQ", to: "/faq" },
    { label: "Privacy Policy", to: "/privacy" },
    { label: "Terms of Service", to: "/terms" },
    { label: "Cancellation Policy", to: "/cancellation" },
];

const SOCIALS = [
    { label: "Facebook", Icon: FiFacebook, href: "https://facebook.com" },
    { label: "Instagram", Icon: FiInstagram, href: "https://instagram.com" },
    { label: "Twitter", Icon: FiTwitter, href: "https://twitter.com" },
];

const Footer = () => {
    const year = new Date().getFullYear();

    return (
        <footer className="site-footer">
            <div className="footer-top">
                <div className="footer-brand">
                    <p className="footer-logo">
                        Luxe<span>Hub</span>
                    </p>
                    <p className="footer-tagline">
                        Timeless comfort, modern hospitality. Book your stay with us and
                        experience a home away from home.
                    </p>

                    <ul className="footer-contact">
                        <li>
                            <FiMapPin aria-hidden="true" />
                            <span>123 Garden Street, Ashgabat, Turkmenistan</span>
                        </li>
                        <li>
                            <FiPhone aria-hidden="true" />
                            <a href="tel:+99312345678">+993 12 345 678</a>
                        </li>
                        <li>
                            <FiMail aria-hidden="true" />
                            <a href="mailto:hello@luxehub.com">hello@luxehub.com</a>
                        </li>
                    </ul>
                </div>

                <div className="footer-links">
                    <div className="footer-column">
                        <h3>Explore</h3>
                        <ul>
                            {EXPLORE_LINKS.map((link) => (
                                <li key={link.label}>
                                    <Link to={link.to}>{link.label}</Link>
                                </li>
                            ))}
                        </ul>
                    </div>

                    <div className="footer-column">
                        <h3>Company</h3>
                        <ul>
                            {COMPANY_LINKS.map((link) => (
                                <li key={link.label}>
                                    <Link to={link.to}>{link.label}</Link>
                                </li>
                            ))}
                        </ul>
                    </div>

                    <div className="footer-column">
                        <h3>Support</h3>
                        <ul>
                            {SUPPORT_LINKS.map((link) => (
                                <li key={link.label}>
                                    <Link to={link.to}>{link.label}</Link>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>

            <div className="footer-bottom">
                <p className="footer-copyright">
                    &copy; {year} LuxeHub. All rights reserved.
                </p>

                <ul className="footer-socials">
                    {SOCIALS.map(({ label, Icon, href }) => (
                        <li key={label}>
                            <a
                                href={href}
                                target="_blank"
                                rel="noopener noreferrer"
                                aria-label={label}
                            >
                                <Icon aria-hidden="true" />
                            </a>
                        </li>
                    ))}
                </ul>
            </div>
        </footer>
    );
};

export default Footer;