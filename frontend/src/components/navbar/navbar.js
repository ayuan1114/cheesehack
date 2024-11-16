import React from 'react';
import { Link } from 'react-router-dom';

export default function CustomNavbar() {
  return (
    <nav className="bg-gray-800">
      <div className="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
        <div className="relative flex items-center justify-between h-16">
          {/* Logo and Site Name */}
          <div className="flex items-center">
            <img
              src="https://tailwindui.com/plus/img/logos/mark.svg?color=indigo&shade=500" // Replace with your logo URL
              alt="Site Logo"
              className="h-8 w-auto mr-2"
            />
            <span className="text-white text-lg font-bold">MySite</span>
          </div>

          {/* Navigation Links */}
          <div className="hidden sm:block">
            <div className="flex space-x-4">
              <Link
                to="/"
                className="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
              >
                Home
              </Link>
              <Link
                to="/analysis"
                className="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
              >
                Analysis
              </Link>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
