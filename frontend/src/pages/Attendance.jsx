import { Save, Search, Trash2 } from 'lucide-react'
import { useEffect, useState } from 'react'
import { api } from '../api/client'
import { Button, Card, Field, PageHeader, inputClass, textareaClass } from '../components/ui'

const today = new Date().toISOString().slice(0, 10)

export default function Attendance() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [history, setHistory] = useState([])
  const [filter, setFilter] = useState('today')
  const [form, setForm] = useState({ staff_id: '', date: today, time: '09:00', status: 'Present', remarks: '' })

  useEffect(() => {
    loadHistory()
  }, [filter])

  async function searchStaff() {
    const { data } = await api.get('/attendance/search-staff', { params: { q: query || 'STF' } })
    setResults(data)
  }

  async function loadHistory() {
    const { data } = await api.get('/attendance/staff', { params: { filter } })
    setHistory(data)
  }

  async function save() {
    await api.post('/attendance/staff', { staff_id: form.staff_id, date: form.date, time: form.time, status: form.status, remarks: form.remarks })
    await loadHistory()
  }

  async function remove(id) {
    await api.delete(`/attendance/staff/${id}`)
    await loadHistory()
  }

  return (
    <>
      <PageHeader title="Staff Attendance Portal" subtitle="Search staff records, mark daily attendance, and review staff attendance history." />
      <div className="grid gap-4 xl:grid-cols-[420px_1fr]">
        <Card>
          <div className="flex gap-2">
            <input className={inputClass} placeholder="Name, staff ID, position" value={query} onChange={(event) => setQuery(event.target.value)} />
            <Button onClick={searchStaff} className="w-12 px-0" aria-label="Search"><Search size={18} /></Button>
          </div>
          <div className="mt-3 space-y-2">
            {results.map((staff) => (
              <button key={staff.staff_id} onClick={() => setForm({ ...form, staff_id: staff.staff_id })} className="flex w-full items-center justify-between rounded border border-slate-200 p-3 text-left text-sm hover:border-primary dark:border-slate-700">
                <span>
                  <strong>{staff.name}</strong>
                  <span className="block text-slate-500">{staff.staff_id} | {staff.position}</span>
                </span>
              </button>
            ))}
          </div>
          <div className="mt-4 grid gap-3">
            <Field label="Staff ID"><input className={inputClass} value={form.staff_id} onChange={(e) => setForm({ ...form, staff_id: e.target.value })} /></Field>
            <div className="grid grid-cols-2 gap-3">
              <Field label="Date"><input type="date" className={inputClass} value={form.date} onChange={(e) => setForm({ ...form, date: e.target.value })} /></Field>
              <Field label="Time"><input type="time" className={inputClass} value={form.time} onChange={(e) => setForm({ ...form, time: e.target.value })} /></Field>
            </div>
            <Field label="Status">
              <select className={inputClass} value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
                {['Present', 'Absent', 'Leave', 'Hospital'].map((item) => <option key={item}>{item}</option>)}
              </select>
            </Field>
            <Field label="Remarks"><textarea className={textareaClass} value={form.remarks} onChange={(e) => setForm({ ...form, remarks: e.target.value })} /></Field>
            <div className="flex gap-2">
              <Button onClick={save}><Save size={16} className="mr-2 inline" />Save Attendance</Button>
            </div>
          </div>
        </Card>
        <Card>
          <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
            <h3 className="font-semibold">Attendance History</h3>
            <select className={`${inputClass} w-40`} value={filter} onChange={(event) => setFilter(event.target.value)}>
              {['today', 'yesterday', 'weekly', 'monthly'].map((item) => <option key={item} value={item}>{item}</option>)}
            </select>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full min-w-[720px] text-sm">
              <thead className="bg-slate-50 text-left dark:bg-slate-800">
                <tr><th className="p-3">Date</th><th>Name</th><th>Staff ID</th><th>Status</th><th>Remarks</th><th></th></tr>
              </thead>
              <tbody>
                {history.map((row) => (
                  <tr key={row.id} className="border-t border-slate-100 dark:border-slate-800">
                    <td className="p-3">{row.date}</td><td>{row.staff?.name}</td><td>{row.staff_id}</td><td>{row.status}</td><td>{row.remarks}</td>
                    <td><button onClick={() => remove(row.id)} className="text-rose-600" aria-label="Delete attendance"><Trash2 size={17} /></button></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      </div>
    </>
  )
}
