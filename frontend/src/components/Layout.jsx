import {
  BarChart3,
  Bell,
  CalendarCheck,
  LayoutDashboard,
  LogOut,
  Menu,
  Moon,
  Settings,
  Sun,
  UserRound,
  Users,
  UsersRound,
  X
} from 'lucide-react'
import { useEffect, useState } from 'react'
import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const links = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/attendance', label: 'Attendance Portal', icon: CalendarCheck },
  { to: '/members', label: 'Member Details', icon: Users },
  { to: '/staff', label: 'Staff Management', icon: UserRound },
  { to: '/visitors', label: 'Visitors', icon: UsersRound },
  { to: '/reports', label: 'Reports', icon: BarChart3 },
  { to: '/settings', label: 'Settings', icon: Settings }
]

export default function Layout() {
  const [open, setOpen] = useState(false)
  const [dark, setDark] = useState(() => localStorage.getItem('theme') === 'dark')
  const { admin, logout } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark)
    localStorage.setItem('theme', dark ? 'dark' : 'light')
  }, [dark])

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <div className="app-shell min-h-screen bg-slate-50 dark:bg-slate-950">
      <aside className={`fixed inset-y-0 left-0 z-40 w-72 bg-sidebar text-white transition-transform lg:translate-x-0 ${open ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="flex h-16 items-center gap-3 border-b border-white/10 px-5">
          <div className="grid h-10 w-10 place-items-center rounded bg-white p-1 shadow-sm">
            <img src="/assets/suki-trust-logo.png" alt="SUKI Home Trust logo" className="h-full w-full object-contain -rotate-90" />
          </div>
          <div>
            <p className="text-sm text-blue-100">SUKI Home Trust</p>
            <h1 className="text-lg font-semibold leading-tight">Management Portal</h1>
          </div>
        </div>
        <nav className="space-y-1 p-4">
          {links.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              onClick={() => setOpen(false)}
              className={({ isActive }) =>
                `flex h-11 items-center gap-3 rounded px-3 text-sm font-medium transition ${
                  isActive ? 'bg-primary text-white' : 'text-blue-50 hover:bg-white/10'
                }`
              }
            >
              <Icon size={19} />
              <span>{label}</span>
            </NavLink>
          ))}
          <button onClick={handleLogout} className="flex h-11 w-full items-center gap-3 rounded px-3 text-sm font-medium text-blue-50 hover:bg-white/10">
            <LogOut size={19} />
            <span>Logout</span>
          </button>
        </nav>
      </aside>

      <div className="lg:pl-72">
        <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-slate-200 bg-white/95 px-4 backdrop-blur dark:border-slate-800 dark:bg-slate-900/95 sm:px-6">
          <div className="flex items-center gap-3">
            <button className="rounded p-2 text-slate-600 hover:bg-slate-100 lg:hidden dark:text-slate-200 dark:hover:bg-slate-800" onClick={() => setOpen(true)} aria-label="Open menu">
              <Menu size={22} />
            </button>
            <div className="hidden items-center gap-3 sm:flex">
              <div className="grid h-9 w-9 place-items-center rounded border border-blue-100 bg-white p-1 shadow-sm dark:border-slate-700">
                <img src="/assets/suki-trust-logo.png" alt="SUKI Home Trust logo" className="h-full w-full object-contain -rotate-90" />
              </div>
              <div>
                <p className="text-xs font-medium uppercase text-primary">Trust Portal</p>
                <p className="font-semibold text-slate-900 dark:text-white">SUKI Home Trust</p>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button className="relative rounded p-2 text-slate-600 hover:bg-slate-100 dark:text-slate-200 dark:hover:bg-slate-800" aria-label="Notifications">
              <Bell size={20} />
              <span className="absolute right-1 top-1 h-2 w-2 rounded-full bg-rose-500" />
            </button>
            <button className="rounded p-2 text-slate-600 hover:bg-slate-100 dark:text-slate-200 dark:hover:bg-slate-800" onClick={() => setDark((value) => !value)} aria-label="Toggle dark mode">
              {dark ? <Sun size={20} /> : <Moon size={20} />}
            </button>
            <div className="hidden items-center gap-2 rounded border border-slate-200 px-3 py-2 text-sm dark:border-slate-700 sm:flex">
              <UserRound size={17} className="text-primary" />
              <span>{admin?.username || 'Admin'}</span>
            </div>
            <button onClick={handleLogout} className="rounded bg-primary px-3 py-2 text-sm font-semibold text-white hover:bg-blue-700">
              Logout
            </button>
          </div>
        </header>
        <main className="p-4 sm:p-6">
          <Outlet />
        </main>
      </div>

      {open && (
        <button className="fixed inset-0 z-30 bg-slate-950/50 lg:hidden" onClick={() => setOpen(false)} aria-label="Close menu">
          <X className="absolute right-5 top-5 text-white" />
        </button>
      )}
    </div>
  )
}
