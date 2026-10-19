import { test } from 'node:test'
import assert from 'node:assert/strict'
import { handle } from '../netlify/functions/api.mjs'

const memoryStore = () => {
  const data = new Map()
  return {
    get: async key => (data.has(key) ? JSON.parse(data.get(key)) : null),
    setJSON: async (key, value) => void data.set(key, JSON.stringify(value)),
  }
}

const call = async (store, path, body) => {
  const res = await handle(new Request(`http://x/api${path}`, body
    ? { method: 'POST', body: JSON.stringify(body), headers: { 'Content-Type': 'application/json' } }
    : {}), store)
  return { status: res.status, data: await res.json() }
}

test('prices match the Python engine', async () => {
  const s = memoryStore()
  assert.equal((await call(s, '/calculate', { date: '2026-12-15', parts: ['steel_frame', 'v_brakes'] })).data.total, 2200)
  assert.equal((await call(s, '/calculate', { date: '2026-08-01', parts: ['steel_frame'] })).data.total, 1300)
})

test('bad requests are rejected', async () => {
  const s = memoryStore()
  assert.equal((await call(s, '/calculate', { date: '2026-10-01', parts: ['tube', 'tubeless_tyre'] })).status, 400)
  assert.equal((await call(s, '/calculate', { date: '2025-12-31', parts: ['steel_frame'] })).status, 400)
  assert.equal((await call(s, '/calculate', { date: '2026-10-01', parts: ['nope'] })).status, 400)
  assert.equal((await call(s, '/prices', { part_id: 'steel_frame', price: 0, valid_from: '2026-05-01' })).status, 400)
})

test('a new price splits the current window', async () => {
  const s = memoryStore()
  await call(s, '/prices', { part_id: 'steel_frame', price: 1250, valid_from: '2026-05-01' })
  const total = async date => (await call(s, '/calculate', { date, parts: ['steel_frame'] })).data.total
  assert.deepEqual([await total('2026-04-30'), await total('2026-05-01'), await total('2026-08-01')], [1200, 1250, 1300])
})

test('saved quotes keep their prices', async () => {
  const s = memoryStore()
  const { data } = await call(s, '/quotes', { date: '2026-10-01', parts: ['steel_frame', 'v_brakes'] })
  await call(s, '/prices', { part_id: 'steel_frame', price: 5000, valid_from: '2026-09-01' })
  const saved = (await call(s, `/quotes/${data.id}`)).data
  assert.equal(saved.total, 2200)
  assert.equal((await call(s, '/quotes')).data[0].id, data.id)
  assert.equal((await call(s, '/quotes/99')).status, 404)
})
