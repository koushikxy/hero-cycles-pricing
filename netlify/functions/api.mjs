import parts from './parts.json' with { type: 'json' }

const json = (body, status = 200) => new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } })

export default async req => {
  const path = new URL(req.url).pathname
  if (path.endsWith('/parts')) {
    const catalog = {}
    for (const [id, p] of Object.entries(parts)) (catalog[p.component] ??= {})[id] = p.name
    return json(catalog)
  }
  if (path.endsWith('/calculate') && req.method === 'POST') {
    const { date, parts: ids = [] } = await req.json()
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date || '')) return json({ detail: 'Pick a valid date.' }, 400)
    if (ids.includes('tubeless_tyre') && ids.includes('tube')) return json({ detail: "Conflict: Cannot select both 'Tubeless Tyre' and 'Tube' in one cycle." }, 400)
    const items = []
    for (const id of ids) {
      const p = parts[id]
      if (!p) return json({ detail: `Unknown part: '${id}'.` }, 400)
      const hit = p.prices.find(([, from, until]) => date >= from && (!until || date < until))
      if (!hit) return json({ detail: `No price for '${p.name}' on ${date}.` }, 400)
      items.push({ name: p.name, component: p.component, price: hit[0] })
    }
    return json({ total: items.reduce((s, i) => s + i.price, 0), items })
  }
  return json({ detail: 'Not found' }, 404)
}

export const config = { path: '/api/*' }
