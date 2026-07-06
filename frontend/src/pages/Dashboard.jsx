import { Baby, CalendarCheck, Cake, UserCheck, UserX, Users, UsersRound } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Bar, BarChart, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { api } from '../api/client'
import { Card, PageHeader } from '../components/ui'

const statIcons = [Users, UserCheck, UserX, UsersRound, Users, Baby, Cake]
const colors = ['#2563EB', '#16A34A', '#DC2626', '#0891B2', '#7C3AED', '#EA580C', '#DB2777']

export default function Dashboard() {
  const [stats, setStats] = useState(null)

  useEffect(() => {
    api.get('/dashboard/stats').then(({ data }) => setStats(data))
  }, [])

  const cards = stats
    ? [
        ['Total Members', stats.total_members],
        ['Present Today', stats.present_today],
        ['Absent Today', stats.absent_today],
        ['Visitors Today', stats.visitors_today],
        ['Staff Count', stats.staff_count],
        ['New Members', stats.new_members],
        ['Upcoming Birthdays', stats.upcoming_birthdays]
      ]
    : []
  const attendance = Object.entries(stats?.attendance_summary || {}).map(([name, value]) => ({ name, value }))
  const blood = Object.entries(stats?.blood_group_distribution || {}).map(([name, value]) => ({ name, value }))

  return (
    <>
      <PageHeader title="Dashboard" subtitle="Operational summary for residents, staff, visitors, and attendance." />
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {cards.map(([label, value], index) => {
          const Icon = statIcons[index]
          return (
            <Card key={label}>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-500 dark:text-slate-400">{label}</p>
                  <p className="mt-2 text-3xl font-bold text-slate-950 dark:text-white">{value}</p>
                </div>
                <div className="grid h-12 w-12 place-items-center rounded bg-blue-50 text-primary dark:bg-blue-950">
                  <Icon />
                </div>
              </div>
            </Card>
          )
        })}
      </div>
      <div className="mt-5 grid gap-4 xl:grid-cols-3">
        <ChartCard title="Attendance Summary">
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={attendance}>
              <XAxis dataKey="name" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="value" fill="#2563EB" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
        <ChartCard title="Monthly Admissions">
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={stats?.monthly_admissions || []}>
              <XAxis dataKey="month" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="count" fill="#0891B2" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
        <ChartCard title="Blood Group Distribution">
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie data={blood} dataKey="value" nameKey="name" outerRadius={90} label>
                {blood.map((_, index) => <Cell key={index} fill={colors[index % colors.length]} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>
    </>
  )
}

function ChartCard({ title, children }) {
  return (
    <Card>
      <h3 className="mb-4 font-semibold text-slate-950 dark:text-white">{title}</h3>
      {children}
    </Card>
  )
}
