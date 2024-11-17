import './App.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import Navbar from './components/navbar/navbar';
import Footer from './components/footer/footer';
import GolfSwingUpload from './components/golf-swing-upload/golf-swing-upload';
import HomePage from './pages/home-page';
import AnalysisPage from './pages/analysis-page';
import SigninPage from './pages/signin-page';

function AppContent() {
  const location = useLocation();
  
  // Conditionally render Navbar based on current route
  const showNavbar = location.pathname !== '/signin';

  return (
    <div className="App">
      {showNavbar && <Navbar />}
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/analysis" element={<AnalysisPage />} />
        <Route path="/signin" element={<SigninPage />} />
      </Routes>
      {showNavbar && <Footer />}
      {showNavbar && <GolfSwingUpload />}
    </div>
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
