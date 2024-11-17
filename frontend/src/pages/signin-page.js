import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import logo from '../assets/images/signin-logo.png';

export default function SigninPage() {
  const [username, setUsername] = useState(''); // Changed from email to username
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSignIn = (event) => {
    event.preventDefault();
    // Add your authentication logic here
    // Assuming sign-in is successful:
    navigate('/'); // Redirect to homepage after sign-in
  };

  return (
    <>
      <div className="flex h-screen flex-1 flex-col justify-center px-6 py-12 lg:px-8 bg-gradient-to-br from-[#c4e1f1] to-[#388464]">
        <div className="sm:mx-auto sm:w-full sm:max-w-sm">
          <img
            alt="Your Company"
            src={logo}
            className="mx-auto h-40 w-auto"
          />
          <h2 className="mt-3 text-center text-2xl/9 font-bold tracking-tight text-gray-900">
            Sign in to your account
          </h2>
        </div>

        <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
          <form onSubmit={handleSignIn} className="space-y-6">
            <div>
              <label htmlFor="email" className="block text-sm/6 font-medium text-gray-900">
                Username
              </label>
              <div className="mt-2">
                <input
                  id="username"
                  name="username"
                  placeholder="BuckyBadger"
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                  autoComplete="username"
                  className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600"
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between">
                <label htmlFor="password" className="block text-sm/6 font-medium text-gray-900">
                  Password
                </label>
                <div className="text-sm">
                  {/* <a href="#" className="font-semibold text-indigo-600 hover:text-indigo-500">
                    Forgot password?
                  </a> */}
                </div>
              </div>
              <div className="mt-2">
                <input
                 id="password"
                 name="password"
                 placeholder='••••••••'
                 type="password"
                 value={password}
                 onChange={(e) => setPassword(e.target.value)}
                 required
                 autoComplete="current-password"
                 className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-[#27845d]"
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                className="flex items-center justify-center w-50 mt-5 mx-auto rounded-md bg-[#164F37] px-3 py-1.5 text-sm/6 font-semibold text-white shadow-sm hover:bg-[#217854] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#27845d]"
              >
                Sign in
              </button>
            </div>
          </form>

          {/* <p className="mt-10 text-center text-sm/6 text-gray-500">
            Not a member?{' '}
            <a href="#" className="font-semibold text-indigo-600 hover:text-indigo-500">
              Start a 14 day free trial
            </a>
          </p> */}
        </div>
      </div>
    </>
  )
}
