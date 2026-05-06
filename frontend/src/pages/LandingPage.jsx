import { Link } from 'react-router-dom';
import HeroSection from '../components/HeroSection';
import CurriculumSection from '../components/CurriculumSection';
import BenefitsSection from '../components/BenefitsSection';
import RequirementsSection from '../components/RequirementsSection';

export default function LandingPage() {
  return (
    <main className="landing-page">
      <HeroSection />
      <BenefitsSection />
      <RequirementsSection />
      <CurriculumSection />
      <CTABanner />
      <footer className="footer">
        <div className="container">
          <p>© 2025 GDG Guadalajara × CUGDL. Todos los derechos reservados.</p>
        </div>
      </footer>
    </main>
  );
}

function CTABanner() {
  return (
    <section className="cta-banner">
      <div className="container">
        <div className="cta-content">
          <h2>¿Listo para tu transformación?</h2>
          <p>Únete a la próxima generación de desarrolladores Python. Plazas limitadas.</p>
          <Link to="/preregistro" className="btn btn-primary btn-large">
            Iniciar Pre-Registro
          </Link>
        </div>
      </div>
    </section>
  );
}

