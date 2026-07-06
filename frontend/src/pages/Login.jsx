import { useState } from 'react'
import { Navigate } from 'react-router-dom'
import { Button, Field, inputClass } from '../components/ui'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const { login, isAuthenticated } = useAuth()
  const [username, setUsername] = useState('admin')
  const [password, setPassword] = useState('admin123')
  const [error, setError] = useState('')

  if (isAuthenticated) return <Navigate to="/" replace />

  async function submit(event) {
    event.preventDefault()
    setError('')
    try {
      await login(username, password)
    } catch {
      setError('Invalid username or password')
    }
  }

  return (
    <main className="grid min-h-screen bg-[#edf5ff] px-4 py-8">
      <section className="mx-auto grid w-full max-w-5xl overflow-hidden rounded border border-blue-100 bg-white shadow-soft md:grid-cols-[1fr_420px]">
        <div className="flex min-h-[520px] flex-col justify-between bg-primary p-8 text-white">
          <div className="flex items-center gap-3">
            <div className="grid h-14 w-14 place-items-center rounded bg-white p-1.5 shadow-sm">
              <img src="/assets/suki-trust-logo.png" alt="SUKI Home Trust logo" className="h-full w-full object-contain -rotate-90" />
            </div>
            <div>
              <p className="text-sm text-blue-100">Secure Admin Portal</p>
              <h1 className="text-2xl font-bold">SUKI Home Trust</h1>
            </div>
          </div>
          <div>
            <p className="max-w-xl text-4xl font-bold leading-tight">Resident care, attendance, visitors, staff, and reports in one protected workspace.</p>
          </div>
        </div>
        <form onSubmit={submit} className="flex flex-col justify-center gap-5 p-8">
          <div>
            <h2 className="text-2xl font-bold text-slate-950">Administrator Login</h2>
            <p className="mt-1 text-sm text-slate-500">JWT protected access for active administrators.</p>
          </div>
          <Field label="Username">
            <input className={inputClass} value={username} onChange={(event) => setUsername(event.target.value)} />
          </Field>
          <Field label="Password">
            <input className={inputClass} type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
          </Field>
          {error && <p className="rounded bg-rose-50 p-3 text-sm text-rose-700">{error}</p>}
          <Button type="submit">Login</Button>
        </form>
      </section>
    </main>
  )
}
