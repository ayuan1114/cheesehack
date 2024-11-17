import React from 'react';

function HomePage() {
  return (
    <div>
      <iframe 
        src="home-page.html" 
        title="External HTML Page" 
        style={{ width: '100%', height: '500px', border: 'none' }}
      ></iframe>
    </div>
  );
}

export default HomePage;
