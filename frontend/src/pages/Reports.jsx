import { Download } from 'lucide-react'
import { useState } from 'react'
import { api } from '../api/client'
import { Button, Card, Field, PageHeader, inputClass } from '../components/ui'

const reports = ['attendance', 'members', 'visitors', 'staff', 'blood-group', 'birthday-list', 'admission']
const exports = ['json', 'pdf', 'excel', 'csv']

export default function Reports() {
  const [type, setType] = useState('attendance')
  const [format, setFormat] = useState('json')
  const [result, setResult] = useState(null)
  async function generate() {
    try {
      const response = await api.get(`/reports/${type}`, {
        params: { export: format },
        responseType: 'blob',
      })
      const contentType = response.headers['content-type'] || 'application/octet-stream'
      const blob = new Blob([response.data], { type: contentType })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      const extension = format === 'json' ? 'json' : format === 'csv' ? 'csv' : format === 'excel' ? 'xls' : 'pdf'
      link.download = `${type}.${extension}`
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
      setResult({ message: `${format.toUpperCase()} report downloaded`, file: link.download })
    } catch (error) {
      setResult({ error: 'Unable to generate report' })
    }
  }
  return (
    <>
      <PageHeader title="Reports" subtitle="Generate attendance, members, visitors, staff, blood group, birthday, and admission reports." />
      <Card>
        <div className="grid gap-3 md:grid-cols-[1fr_1fr_auto]">
          <Field label="Report">
            <select className={inputClass} value={type} onChange={(e) => setType(e.target.value)}>{reports.map((item) => <option key={item}>{item}</option>)}</select>
          </Field>
          <Field label="Export">
            <select className={inputClass} value={format} onChange={(e) => setFormat(e.target.value)}>{exports.map((item) => <option key={item}>{item}</option>)}</select>
          </Field>
          <Button onClick={generate} className="self-end"><Download size={16} className="mr-2 inline" />Generate</Button>
        </div>
      </Card>
      {result && <Card className="mt-4"><pre className="max-h-[520px] overflow-auto text-xs">{JSON.stringify(result, null, 2)}</pre></Card>}
    </>
  )
}
