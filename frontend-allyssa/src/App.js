import './App.css';
import React from 'react';
import CustomNavbar from './components/navbar/navbar';
import Footer from './components/footer/footer';
import GolfSwingUpload from './components/golf-swing-upload/golf-swing-upload';
import HomePage from './pages/home-page';
import AnalysisPage from './pages/analysis-page';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="App">
        <CustomNavbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/analysis" element={<AnalysisPage />} />
        </Routes>
        <GolfSwingUpload />
        <Footer />
      </div>
    </Router>
  );
}

export default App;
