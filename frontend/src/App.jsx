import { Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import LandingPage from './pages/LandingPage';
import PreRegistrationPage from './pages/PreRegistrationPage';

export default function App() {
  return (
    <div>
      <Header />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/preregistro" element={<PreRegistrationPage />} />
      </Routes>
    </div>
  );
}

