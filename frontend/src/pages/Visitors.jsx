import { Save, Trash2 } from 'lucide-react'
import { useEffect, useState } from 'react'
import { api } from '../api/client'
import { Button, Card, Field, PageHeader, inputClass, textareaClass } from '../components/ui'

const blank = { visitor_name: '', phone: '', purpose: '', member_id: '', entry_time: '', exit_time: '', remarks: '' }

export default function Visitors() {
  const [rows, setRows] = useState([])
  const [form, setForm] = useState(blank)
  useEffect(() => { load() }, [])
  async function load() { setRows((await api.get('/visitors')).data) }
  async function save() {
    const payload = Object.fromEntries(Object.entries(form).map(([key, value]) => [key, value === '' ? null : value]))
    await api.post('/visitors', payload)
    setForm(blank)
    await load()
  }
  async function remove(id) { await api.delete(`/visitors/${id}`); await load() }
  return (
    <>
      <PageHeader title="Visitors" subtitle="Maintain entry, exit, purpose, member visit, and remarks." />
      <div className="grid gap-4 xl:grid-cols-[420px_1fr]">
        <Card>
          <div className="grid gap-3">
            {['visitor_name', 'phone', 'purpose', 'member_id', 'entry_time', 'exit_time'].map((field) => (
              <Field key={field} label={field.replaceAll('_', ' ')}>
                <input className={inputClass} type={field.includes('time') ? 'datetime-local' : 'text'} value={form[field] || ''} onChange={(e) => setForm({ ...form, [field]: e.target.value })} />
              </Field>
            ))}
            <Field label="Remarks"><textarea className={textareaClass} value={form.remarks} onChange={(e) => setForm({ ...form, remarks: e.target.value })} /></Field>
            <Button onClick={save}><Save size={16} className="mr-2 inline" />Save Visitor</Button>
          </div>
        </Card>
        <Card>
          <div className="overflow-x-auto">
            <table className="w-full min-w-[820px] text-sm">
              <thead className="bg-slate-50 text-left dark:bg-slate-800"><tr><th className="p-3">Visitor</th><th>Mobile</th><th>Purpose</th><th>Member</th><th>Entry</th><th>Exit</th><th>Remarks</th><th></th></tr></thead>
              <tbody>{rows.map((row) => <tr key={row.id} className="border-t border-slate-100 dark:border-slate-800"><td className="p-3">{row.visitor_name}</td><td>{row.phone}</td><td>{row.purpose}</td><td>{row.member_id}</td><td>{row.entry_time?.slice(0, 16)}</td><td>{row.exit_time?.slice(0, 16)}</td><td>{row.remarks}</td><td><button onClick={() => remove(row.id)} className="text-rose-600"><Trash2 size={16} /></button></td></tr>)}</tbody>
            </table>
          </div>
        </Card>
      </div>
    </>
  )
}
