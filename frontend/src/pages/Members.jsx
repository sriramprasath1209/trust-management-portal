import { Printer, QrCode, Save, Trash2 } from 'lucide-react'
import { QRCodeCanvas } from 'qrcode.react'
import { useEffect, useState } from 'react'
import { api } from '../api/client'
import { Button, Card, Field, PageHeader, inputClass, textareaClass } from '../components/ui'

const blank = { name: '', father_name: '', mother_name: '', gender: 'Female', dob: '', age: '', aadhaar_no: '', pan_no: '', blood_group: 'O+', allergies: '', medical_conditions: '', disability: '', medications: '', phone: '', emergency_name: '', emergency_phone: '', relationship: '', plot_number: '', street: '', area: '', village: '', taluk: '', district: '', state: '', pincode: '', room_number: '', guardian: '', admission_date: new Date().toISOString().slice(0, 10), education: '', occupation: '', current_status: 'Active', notes: '' }

export default function Members() {
  const [members, setMembers] = useState([])
  const [form, setForm] = useState(blank)
  const [selected, setSelected] = useState(null)
  const [q, setQ] = useState('')

  useEffect(() => { load() }, [])
  async function load() {
    const { data } = await api.get('/members', { params: { q } })
    setMembers(data)
  }
  async function save() {
    const payload = cleanPayload(form, ['age'])
    if (selected) await api.put(`/members/${selected}`, payload)
    else await api.post('/members', payload)
    setForm(blank); setSelected(null); await load()
  }
  async function remove(id) {
    await api.delete(`/members/${id}`)
    await load()
  }

  return (
    <>
      <PageHeader title="Member Details" subtitle="Manage personal, government, medical, contact, address, trust, and document information." />
      <div className="grid gap-4 2xl:grid-cols-[1fr_520px]">
        <Card>
          <div className="mb-4 flex gap-2">
            <input className={inputClass} placeholder="Search members" value={q} onChange={(e) => setQ(e.target.value)} />
            <Button onClick={load}>Search</Button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full min-w-[900px] text-sm">
              <thead className="bg-slate-50 text-left dark:bg-slate-800">
                <tr><th className="p-3">Photo</th><th>Member ID</th><th>Name</th><th>Age</th><th>Blood</th><th>Room</th><th>Emergency</th><th>Admission</th><th>Actions</th></tr>
              </thead>
              <tbody>
                {members.map((m) => (
                  <tr key={m.member_id} className="border-t border-slate-100 dark:border-slate-800">
                    <td className="p-3"><div className="h-9 w-9 rounded bg-blue-100" /></td><td>{m.member_id}</td><td>{m.name}</td><td>{m.age}</td><td>{m.blood_group}</td><td>{m.room_number}</td><td>{m.emergency_phone}</td><td>{m.admission_date}</td>
                    <td className="flex gap-2 py-3">
                      <button onClick={() => { setSelected(m.member_id); setForm({ ...blank, ...m }) }} className="text-primary">Edit</button>
                      <button onClick={() => window.print()} className="text-slate-600"><Printer size={16} /></button>
                      <button onClick={() => remove(m.member_id)} className="text-rose-600"><Trash2 size={16} /></button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
        <Card>
          <h3 className="mb-4 font-semibold">{selected ? `Update ${selected}` : 'New Member'}</h3>
          <Section title="Personal Details" fields={['name', 'father_name', 'mother_name', 'gender', 'dob', 'age']} form={form} setForm={setForm} />
          <Section title="Government Details" fields={['aadhaar_no', 'pan_no']} form={form} setForm={setForm} />
          <Section title="Medical Information" fields={['blood_group', 'allergies', 'medical_conditions', 'disability', 'medications']} form={form} setForm={setForm} />
          <Section title="Contact Details" fields={['phone', 'emergency_name', 'emergency_phone', 'relationship']} form={form} setForm={setForm} />
          <Section title="Address" fields={['plot_number', 'street', 'area', 'village', 'taluk', 'district', 'state', 'pincode']} form={form} setForm={setForm} />
          <Section title="Trust Information" fields={['admission_date', 'room_number', 'guardian', 'education', 'occupation', 'current_status']} form={form} setForm={setForm} />
          <Field label="Documents"><input className={inputClass} type="file" multiple /></Field>
          <Field label="Notes"><textarea className={textareaClass} value={form.notes || ''} onChange={(e) => setForm({ ...form, notes: e.target.value })} /></Field>
          {selected && <div className="my-4 rounded border border-slate-200 p-3"><QrCode size={18} className="mb-2" /><QRCodeCanvas value={`${window.location.origin}/members/${selected}`} size={96} /></div>}
          <div className="mt-4 flex flex-wrap gap-2">
            <Button onClick={save}><Save size={16} className="mr-2 inline" />Save</Button>
            <Button onClick={save} variant="secondary">Update</Button>
            <Button onClick={() => { setForm(blank); setSelected(null) }} variant="secondary">Reset</Button>
            <Button onClick={() => window.print()} variant="secondary">Print ID Card</Button>
          </div>
        </Card>
      </div>
    </>
  )
}

function Section({ title, fields, form, setForm }) {
  return (
    <div className="mb-4">
      <h4 className="mb-2 text-sm font-bold text-primary">{title}</h4>
      <div className="grid gap-3 sm:grid-cols-2">
        {fields.map((field) => (
          <Field key={field} label={field.replaceAll('_', ' ')}>
            <input className={inputClass} type={field.includes('date') || field === 'dob' ? 'date' : 'text'} value={form[field] || ''} onChange={(e) => setForm({ ...form, [field]: e.target.value })} />
          </Field>
        ))}
      </div>
    </div>
  )
}

function cleanPayload(payload, numericFields = []) {
  return Object.fromEntries(
    Object.entries(payload).map(([key, value]) => {
      if (value === '' || value === null) return [key, null]
      if (numericFields.includes(key)) return [key, Number(value)]
      return [key, value]
    })
  )
}
