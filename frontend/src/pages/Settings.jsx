import { Database, Save, UserPlus } from 'lucide-react'
import { useEffect, useState } from 'react'
import { api } from '../api/client'
import { Button, Card, Field, PageHeader, inputClass } from '../components/ui'

export default function Settings() {
  const [admins, setAdmins] = useState([])
  const [password, setPassword] = useState({ current_password: '', new_password: '' })
  const [newAdmin, setNewAdmin] = useState({ username: '', password: '', role: 'Administrator', status: 'Active' })
  const [message, setMessage] = useState('')
  useEffect(() => { loadAdmins() }, [])
  async function loadAdmins() { setAdmins((await api.get('/auth/admins')).data) }
  async function changePassword() { await api.post('/settings/change-password', password); setMessage('Password changed') }
  async function addAdmin() { await api.post('/auth/admins', newAdmin); setNewAdmin({ username: '', password: '', role: 'Administrator', status: 'Active' }); await loadAdmins() }
  async function backup() { setMessage((await api.post('/settings/backup')).data.message) }
  return (
    <>
      <PageHeader title="Settings" subtitle="Manage profile security, admins, database backup, and restore workflow." />
      {message && <div className="mb-4 rounded bg-blue-50 p-3 text-sm text-primary">{message}</div>}
      <div className="grid gap-4 xl:grid-cols-3">
        <Card>
          <h3 className="mb-3 font-semibold">Change Password</h3>
          <div className="grid gap-3">
            <Field label="Current Password"><input className={inputClass} type="password" value={password.current_password} onChange={(e) => setPassword({ ...password, current_password: e.target.value })} /></Field>
            <Field label="New Password"><input className={inputClass} type="password" value={password.new_password} onChange={(e) => setPassword({ ...password, new_password: e.target.value })} /></Field>
            <Button onClick={changePassword}><Save size={16} className="mr-2 inline" />Update Password</Button>
          </div>
        </Card>
        <Card>
          <h3 className="mb-3 font-semibold">Add New Admin</h3>
          <div className="grid gap-3">
            {['username', 'password', 'role', 'status'].map((field) => <Field key={field} label={field}><input className={inputClass} type={field === 'password' ? 'password' : 'text'} value={newAdmin[field]} onChange={(e) => setNewAdmin({ ...newAdmin, [field]: e.target.value })} /></Field>)}
            <Button onClick={addAdmin}><UserPlus size={16} className="mr-2 inline" />Add Admin</Button>
          </div>
        </Card>
        <Card>
          <h3 className="mb-3 font-semibold">Database</h3>
          <div className="grid gap-2">
            <Button onClick={backup} variant="secondary"><Database size={16} className="mr-2 inline" />Backup Database</Button>
            <Button onClick={() => setMessage('Restore requires a guarded production import workflow.')} variant="secondary">Restore Database</Button>
          </div>
          <h4 className="mb-2 mt-5 text-sm font-semibold">Administrators</h4>
          <ul className="space-y-2 text-sm">{admins.map((admin) => <li key={admin.id} className="rounded bg-slate-50 p-2 dark:bg-slate-800">{admin.username} | {admin.role} | {admin.status}</li>)}</ul>
        </Card>
      </div>
    </>
  )
}
