import { Link } from 'react-router-dom';
import logo from '../logos/indigo.png';

export default function Header() {
  return (
    <header className="header">
      <div className="container nav-row">
        <Link to="/" className="brand">
          <img src={logo} alt="Logo GDG Guadalajara" className="brand-icon-img" />
          <span className="brand-text">
            <span className="brand-main">Curso intensivo de Python</span>
            <span className="brand-sub">GDG Guadalajara</span>
          </span>
        </Link>
      </div>
    </header>
  );
}
