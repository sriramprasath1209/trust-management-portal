import { Save, Trash2 } from 'lucide-react'
import { useEffect, useState } from 'react'
import { api } from '../api/client'
import { Button, Card, Field, PageHeader, inputClass, textareaClass } from '../components/ui'

const blank = { name: '', position: '', phone: '', email: '', address: '', joining_date: '', salary: '', attendance: 'Present' }

export default function Staff() {
  const [rows, setRows] = useState([])
  const [form, setForm] = useState(blank)
  const [selected, setSelected] = useState(null)
  useEffect(() => { load() }, [])
  async function load() { setRows((await api.get('/staff')).data) }
  async function save() {
    const payload = Object.fromEntries(
      Object.entries(form).map(([key, value]) => [key, value === '' || value === null ? null : key === 'salary' ? Number(value) : value])
    )
    if (selected) await api.put(`/staff/${selected}`, payload)
    else await api.post('/staff', payload)
    setForm(blank); setSelected(null); await load()
  }
  async function remove(id) { await api.delete(`/staff/${id}`); await load() }
  return (
    <>
      <PageHeader title="Staff Management" subtitle="Create staff records, salary details, and daily attendance status." />
      <div className="grid gap-4 xl:grid-cols-[420px_1fr]">
        <Card>
          <div className="grid gap-3">
            {['name', 'position', 'phone', 'email', 'joining_date', 'salary', 'attendance'].map((field) => <StaffField key={field} field={field} form={form} setForm={setForm} />)}
            <Field label="Address"><textarea className={textareaClass} value={form.address} onChange={(e) => setForm({ ...form, address: e.target.value })} /></Field>
            <Button onClick={save}><Save size={16} className="mr-2 inline" />{selected ? 'Update Staff' : 'Save Staff'}</Button>
          </div>
        </Card>
        <Card>
          <div className="overflow-x-auto">
            <table className="w-full min-w-[760px] text-sm">
              <thead className="bg-slate-50 text-left dark:bg-slate-800"><tr><th className="p-3">Staff ID</th><th>Name</th><th>Position</th><th>Mobile</th><th>Email</th><th>Salary</th><th>Attendance</th><th></th></tr></thead>
              <tbody>{rows.map((row) => <tr key={row.staff_id} className="border-t border-slate-100 dark:border-slate-800"><td className="p-3">{row.staff_id}</td><td>{row.name}</td><td>{row.position}</td><td>{row.phone}</td><td>{row.email}</td><td>{row.salary}</td><td>{row.attendance}</td><td className="flex gap-2 py-3"><button onClick={() => { setSelected(row.staff_id); setForm(row) }} className="text-primary">Edit</button><button onClick={() => remove(row.staff_id)} className="text-rose-600"><Trash2 size={16} /></button></td></tr>)}</tbody>
            </table>
          </div>
        </Card>
      </div>
    </>
  )
}

function StaffField({ field, form, setForm }) {
  return <Field label={field.replaceAll('_', ' ')}><input className={inputClass} type={field.includes('date') ? 'date' : 'text'} value={form[field] || ''} onChange={(e) => setForm({ ...form, [field]: e.target.value })} /></Field>
}
