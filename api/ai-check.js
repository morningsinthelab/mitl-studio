// Free AI visibility check: lead capture -> email via Resend.
// Env: RESEND_API_KEY (required to send), LEAD_FROM (required: a sender on a Resend-verified domain,
// e.g. "MiTL Studio <leads@your-verified-domain>"), LEAD_TO (optional, defaults to keith@mitl.studio).
const BOOK = '<a href="https://ro.am/keith">book a call with Keith</a>';
const NOT_READY = 'Our AI visibility check form isn\u2019t switched on yet. Please ' + BOOK + ' and we\u2019ll run it for you.';

function esc(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function readBody(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  if (typeof req.body === 'string') {
    try { return JSON.parse(req.body); } catch (_) {
      return Object.fromEntries(new URLSearchParams(req.body));
    }
  }
  return {};
}

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ ok: false, error: 'Use POST.' });
  }

  const body = readBody(req);
  const brand = String(body.brand || '').trim().slice(0, 200);
  const email = String(body.email || '').trim().slice(0, 254);
  const source = String(body.source || '').trim().slice(0, 40);
  const honeypot = String(body.company_url || '').trim();
  const elapsed = Number(body.elapsed_ms);

  // Honeypot / too-fast submit: pretend success so bots learn nothing.
  if (honeypot || (Number.isFinite(elapsed) && elapsed < 1500)) {
    return res.status(200).json({ ok: true, message: 'Thanks. Your AI visibility check is on its way.' });
  }

  if (brand.length < 2) return res.status(400).json({ ok: false, error: 'Add your brand name or website.' });
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
    return res.status(400).json({ ok: false, error: 'Add a valid email so we can send your results.' });
  }

  const key = process.env.RESEND_API_KEY;
  const from = process.env.LEAD_FROM;
  const to = (process.env.LEAD_TO || 'keith@mitl.studio').split(',').map((s) => s.trim()).filter(Boolean);
  if (!key || !from) {
    console.warn('ai-check: not configured', { hasKey: !!key, hasFrom: !!from });
    return res.status(503).json({ ok: false, error: NOT_READY });
  }

  const isTest = /^test\b/i.test(brand);
  const subject = (isTest ? '[TEST] ' : '') + 'AI visibility check request: ' + brand;
  const when = new Date().toISOString();
  const text = [
    'New free AI visibility check request from mitl.studio',
    '',
    'Brand / website: ' + brand,
    'Email: ' + email,
    'Form: ' + (source || 'unknown'),
    'Submitted: ' + when,
    'Page: ' + (req.headers.referer || 'unknown'),
  ].join('\n');
  const html = '<p><b>New free AI visibility check request from mitl.studio</b></p><table>' +
    [['Brand / website', brand], ['Email', email], ['Form', source || 'unknown'], ['Submitted', when], ['Page', req.headers.referer || 'unknown']]
      .map(([k, v]) => '<tr><td style="padding:2px 12px 2px 0;color:#666">' + esc(k) + '</td><td>' + esc(v) + '</td></tr>').join('') +
    '</table>';

  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: 'Bearer ' + key, 'Content-Type': 'application/json' },
      body: JSON.stringify({ from, to, reply_to: email, subject, text, html }),
    });
    if (!r.ok) {
      console.error('ai-check: resend error', r.status, await r.text().catch(() => ''));
      return res.status(502).json({ ok: false, error: 'We couldn\u2019t send that just now. Please try again, or ' + BOOK + '.' });
    }
    return res.status(200).json({ ok: true, message: 'Thanks. We\u2019ll email your AI visibility check to ' + email + '.' });
  } catch (e) {
    console.error('ai-check: send failed', e && e.message);
    return res.status(502).json({ ok: false, error: 'We couldn\u2019t send that just now. Please try again, or ' + BOOK + '.' });
  }
};
