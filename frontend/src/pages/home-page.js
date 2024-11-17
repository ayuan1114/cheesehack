import React from 'react';

function HomePage() {
  return (
    <div>
      <h1>Home</h1>
      <p>Welcome to MyApp. This is the home page.</p>
      <iframe 
        src="path/to/your/html-page.html" 
        title="External HTML Page" 
        style={{ width: '100%', height: '500px', border: 'none' }}
      ></iframe>
    </div>
  );
}

export default HomePage;
