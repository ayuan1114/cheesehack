import './App.css';
import React from 'react';
import Navbar from './components/navbar/navbar';
import Footer from './components/footer/footer';
import GolfSwingUpload from './components/golf-swing-upload/golf-swing-upload';
import HomePage from './pages/home-page';
import AnalysisPage from './pages/analysis-page';
import SigninPage from './pages/signin-page';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div as="App" className="bg-black">
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />}/>
          <Route path="/analysis" element={<AnalysisPage />} />
          <Route path="/signin" element={<SigninPage />} />
        </Routes>
        <GolfSwingUpload />
        <Footer />
      </div>
    </Router>
  );
}

export default App;
