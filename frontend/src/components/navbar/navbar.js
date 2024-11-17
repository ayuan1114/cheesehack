import { Disclosure, DisclosureButton, DisclosurePanel, Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/react'
import { Bars3Icon, BellIcon, XMarkIcon } from '@heroicons/react/24/outline'
import logo from '../../assets/images/logo.svg'
import { useState } from 'react'; // Import useState for handling sign-in status
import { Link } from 'react-router-dom';

const navigation = [
  { name: 'Dashboard', href: '/', current: true },
  { name: 'Analysis', href: '/analysis', current: true },
]

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

export default function Example() {
  const [isSignedIn, setIsSignedIn] = useState(false); // State to track sign-in status

  return (
    <div className="bg-gray-50 p-16">
      <Disclosure as="nav" className="bg-[#164F37] rounded-2xl">
        <div className="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
          <div className="relative flex h-16 items-center justify-start">
            <div className="absolute inset-y-0 left-0 flex items-center sm:hidden">
              {/* Mobile menu button */}
              <DisclosureButton className="group relative inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white">
                <span className="absolute -inset-0.5" />
                <span className="sr-only">Open main menu</span>
                <Bars3Icon aria-hidden="true" className="block size-6 group-data-[open]:hidden" />
                <XMarkIcon aria-hidden="true" className="hidden size-6 group-data-[open]:block" />
              </DisclosureButton>
            </div>
            <div className="flex flex-1 items-center justify-start">
              <div className="flex items-center">
                <a href="/">
                  <img
                    alt="SwingStyle"
                    src={logo}
                    className="h-10 w-auto"
                  />
                </a>
                <a href="/" className="no-underline hover:no-underline">
                  <span className="ml-3 text-white text-lg font-bold flex items-center leading-none -mt-1">SwingStyle</span>
                </a> 
                <div className="w-px h-6 bg-gray-300 ml-6 mr-6"></div>
              </div>
              <div className="hidden sm:block">
                <div className="flex space-x-4">
                  {navigation.map((item) => (
                    <a
                      key={item.name}
                      href={item.href}
                      aria-current={item.current ? 'page' : undefined}
                      className={classNames(
                        'rounded-md px-0 py-2 text-sm font-medium no-underline',
                        item.current
                          ? 'text-white hover:bg-[#1F6F4E] hover:text-black'
                          : 'text-white hover:bg-[#1F6F4E] hover:text-black'
                      )}
                    >
                      {item.name}
                    </a>
                  ))}
                </div>
              </div>
            </div>
            <div className="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0">
              <Menu as="div" className="relative ml-3">
                <div>
                  <MenuButton className="relative flex rounded-full bg-gray-800 text-sm focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800
                                            hover:outline-none hover:ring-2 hover:ring-white hover:ring-offset-2 hover:ring-offset-gray-800">
                    <span className="absolute -inset-1.5" />
                    <span className="sr-only">Open user menu</span>
                    <img
                      alt=""
                      src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
                      className="size-8 rounded-full"
                    />
                  </MenuButton>
                </div>
                <MenuItems
                  transition
                  className="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black/5 transition focus:outline-none data-[closed]:scale-95 data-[closed]:transform data-[closed]:opacity-0 data-[enter]:duration-100 data-[leave]:duration-75 data-[enter]:ease-out data-[leave]:ease-in"
                >
                  {isSignedIn ? (
                    <MenuItem>
                      <a
                        href="#"
                        onClick={() => setIsSignedIn(false)} // Mock function to simulate sign-out
                        className="block px-4 py-2 text-sm text-gray-700 no-underline data-[focus]:bg-gray-100 data-[focus]:outline-none"
                      >
                        Sign out
                      </a>
                    </MenuItem>
                  ) : (
                    <MenuItem>
                      <Link
                        to="/signin" // Use 'to' instead of 'href' for Link component
                        onClick={() => setIsSignedIn(true)} // Mock function to simulate sign-in
                        className="block px-4 py-2 text-sm text-gray-700 no-underline data-[focus]:bg-gray-100 data-[focus]:outline-none"
                      >
                        Sign in
                      </Link>
                    </MenuItem>
                  )}
                </MenuItems>
              </Menu>
            </div>
          </div>
        </div>

        <DisclosurePanel className="sm:hidden">
          <div className="space-y-1 px-2 pb-3 pt-2">
            {navigation.map((item) => (
              <DisclosureButton
                key={item.name}
                as="a"
                href={item.href}
                aria-current={item.current ? 'page' : undefined}
                className={classNames(
                  item.current ? ' text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white',
                  'block rounded-md px-3 py-2 text-base font-medium',
                )}
              >
                {item.name}
              </DisclosureButton>
            ))}
          </div>
        </DisclosurePanel>
      </Disclosure>
    </div>
  )
}
