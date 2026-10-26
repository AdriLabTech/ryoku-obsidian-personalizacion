// Inyecta una hoja CSS en Discord por el protocolo de depuración de Chromium (sin tocar la instalación).
// Uso: node inject.mjs <css> [puerto]   |   node inject.mjs --shot <png> [puerto]   |   node inject.mjs --dump [puerto]   (lista variables CSS de :root)
import { readFileSync, writeFileSync } from "node:fs";

const arg = process.argv[2];
const port = Number((arg === "--shot" ? process.argv[4] : process.argv[3]) || 9223);
const base = `http://127.0.0.1:${port}`;

async function target() {
  for (let i = 0; i < 120; i++) {
    try {
      const l = await (await fetch(`${base}/json`)).json();
      const t = l.find((x) => x.type === "page" && /discord\.com/.test(x.url));
      if (t) return t;
    } catch {}
    await new Promise((r) => setTimeout(r, 1000));
  }
  throw new Error("Discord no responde en el puerto de depuración");
}

function session(url) {
  const ws = new WebSocket(url);
  let id = 0;
  const pend = new Map();
  ws.onmessage = (m) => {
    const d = JSON.parse(m.data);
    if (d.id && pend.has(d.id)) { pend.get(d.id)(d); pend.delete(d.id); }
  };
  const ready = new Promise((r) => (ws.onopen = r));
  const send = (method, params = {}) => new Promise((res) => { const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
  return { ready, send, ws };
}

const t = await target();
const s = session(t.webSocketDebuggerUrl);
await s.ready;

if (arg === "--dump") {
  const r = await s.send("Runtime.evaluate", { returnByValue: true, expression: `(() => {
    const out = {}; const cs = getComputedStyle(document.documentElement);
    for (const sheet of document.styleSheets) { let rules; try { rules = sheet.cssRules } catch { continue }
      for (const rule of rules) if (rule.style) for (const p of rule.style) if (p.startsWith("--")) out[p] = cs.getPropertyValue(p).replace(/\\s+/g, " ").trim().slice(0, 80); }
    return JSON.stringify(out); })()` });
  process.stdout.write(r.result.result.value + "\n", () => process.exit(0));
}

if (arg === "--shot") {
  const r = await s.send("Page.captureScreenshot", { format: "png" });
  writeFileSync(process.argv[3], Buffer.from(r.result.data, "base64"));
  console.log("captura", process.argv[3]);
  process.exit(0);
}

const css = readFileSync(arg, "utf8");
const js = `(() => { let el = document.getElementById("ryoku-obsidian"); if (!el) { el = document.createElement("style"); el.id = "ryoku-obsidian"; document.documentElement.appendChild(el); } el.textContent = ${JSON.stringify(css)}; })()`;
await s.send("Page.enable");
await s.send("Page.addScriptToEvaluateOnNewDocument", { source: js });   // sobrevive a recargas del cliente
await s.send("Runtime.evaluate", { expression: js });
console.log("css inyectado en", t.url);
s.ws.close();
