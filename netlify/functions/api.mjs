import seed from './parts.json' with { type: 'json' }

const json = (body, status = 200) => new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } })
const validDate = d => /^\d{4}-\d{2}-\d{2}$/.test(d || '') && !isNaN(new Date(d))
const covers = (date, [, from, until]) => from <= date && (!until || date < until)

class BadRequest extends Error {}

function calculate(parts, date, ids) {
  if (!validDate(date)) throw new BadRequest('Pick a valid date.')
  if (ids.includes('tubeless_tyre') && ids.includes('tube')) throw new BadRequest("Conflict: Cannot select both 'Tubeless Tyre' and 'Tube' in one cycle.")
  const items = ids.map(id => {
    const p = parts[id]
    if (!p) throw new BadRequest(`Unknown part: '${id}'.`)
    const hit = p.prices.find(e => covers(date, e))
    if (!hit) throw new BadRequest(`No price for '${p.name}' on ${date}.`)
    return { name: p.name, component: p.component, price: hit[0] }
  })
  return { total: items.reduce((s, i) => s + i.price, 0), items }
}

function addPrice(parts, id, price, day) {
  const p = parts[id]
  if (!p) throw new BadRequest(`Unknown part: '${id}'.`)
  if (!(price > 0)) throw new BadRequest('Price must be more than 0.')
  if (!validDate(day)) throw new BadRequest('Pick a valid date.')
  const current = p.prices.find(e => covers(day, e))
  if (current && current[1] === day) return void (current[0] = price)
  const until = current ? current[2] : p.prices.map(e => e[1]).filter(f => f > day).sort()[0] ?? null
  if (current) current[2] = day
  p.prices.push([price, day, until])
  p.prices.sort((a, b) => a[1].localeCompare(b[1]))
}

export async function handle(req, store) {
  const path = new URL(req.url).pathname.replace(/^\/api/, '')
  const parts = (await store.get('parts', { type: 'json' })) ?? structuredClone(seed)
  const quotes = (await store.get('quotes', { type: 'json' })) ?? []
  const body = req.method === 'POST' ? await req.json().catch(() => ({})) : {}

  try {
    if (path === '/parts') {
      const catalog = {}
      for (const [id, p] of Object.entries(parts)) (catalog[p.component] ??= {})[id] = p.name
      return json(catalog)
    }
    if (path === '/prices' && req.method === 'GET') {
      return json(Object.entries(parts).map(([id, p]) => ({ id, ...p })))
    }
    if (path === '/prices' && req.method === 'POST') {
      addPrice(parts, body.part_id, body.price, body.valid_from)
      await store.setJSON('parts', parts)
      return json({ ok: true })
    }
    if (path === '/calculate' && req.method === 'POST') {
      return json(calculate(parts, body.date, body.parts ?? []))
    }
    if (path === '/quotes' && req.method === 'POST') {
      const id = quotes.length + 1
      quotes.push({ id, created_at: new Date().toISOString(), quote_date: body.date, ...calculate(parts, body.date, body.parts ?? []) })
      await store.setJSON('quotes', quotes)
      return json({ id })
    }
    if (path === '/quotes') {
      return json(quotes.slice(-20).reverse().map(({ items, ...q }) => q))
    }
    const one = path.match(/^\/quotes\/(\d+)$/)
    if (one) {
      const q = quotes.find(q => q.id === Number(one[1]))
      return q ? json(q) : json({ detail: 'Quote not found.' }, 404)
    }
  } catch (e) {
    if (e instanceof BadRequest) return json({ detail: e.message }, 400)
    throw e
  }
  return json({ detail: 'Not found' }, 404)
}

export default async req => {
  const { getStore } = await import('@netlify/blobs')
  return handle(req, getStore({ name: 'hero-cycles', consistency: 'strong' }))
}

export const config = { path: '/api/*' }
