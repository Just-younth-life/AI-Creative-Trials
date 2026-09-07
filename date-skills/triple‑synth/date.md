<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Triple Synth — Role Separation × Multi-AI Synthesis</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');
    :root {
      --bg: #f8f8f6;
      --card: #fff;
      --text: #1a1a1a;
      --muted: #71717a;
      --line: #e4e4e7;
      --accent: #18181b;
      --propose: #1d4ed8;
      --proposeBg: #eff6ff;
      --proposeLine: #93c5fd;
      --critic: #b45309;
      --criticBg: #fffbeb;
      --criticLine: #fbbf24;
      --judge: #047857;
      --judgeBg: #ecfdf5;
      --judgeLine: #34d399;
      --synth: #7c3aed;
      --synthBg: #f5f3ff;
      --synthLine: #a78bfa;
      --dialectic: #be123c;
      --dialecticBg: #fff1f2;
      --dialecticLine: #fb7185;
      --radius: 8px;
      --shadow: 0 1px 3px rgba(0,0,0,.06), 0 1px 2px rgba(0,0,0,.04);
    }
    * { box-sizing: border-box; margin: 0; }
    body {
      font-family: 'IBM Plex Sans', system-ui, sans-serif;
      background: var(--bg); color: var(--text);
      line-height: 1.6; -webkit-font-smoothing: antialiased;
    }

    .wrap { max-width: 1280px; margin: 0 auto; padding: 0 16px 40px; }

    /* Sticky header */
    .top-bar {
      position: sticky; top: 0; z-index: 100;
      background: rgba(248,248,246,.92);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid var(--line);
      padding: 10px 16px;
      margin: 0 -16px 16px;
    }
    .top-bar-inner {
      max-width: 1280px; margin: 0 auto;
      display: flex; align-items: center; justify-content: space-between;
      flex-wrap: wrap; gap: 8px;
    }
    .hLeft { display: flex; align-items: baseline; gap: 10px; }
    .hLeft h1 { font-size: 16px; font-weight: 700; letter-spacing: -.02em; }
    .hLeft .sub { font-size: 11px; color: var(--muted); font-weight: 500; }
    .hRight { display: flex; gap: 6px; align-items: center; flex-wrap: wrap; }
    .pill {
      font-family: 'IBM Plex Mono', monospace;
      font-size: 10px; color: var(--muted);
      border: 1px solid var(--line); background: var(--card);
      padding: 3px 8px; border-radius: 999px;
    }

    /* Sections */
    .section { margin-bottom: 14px; }

    /* Card */
    .card {
      background: var(--card); border: 1px solid var(--line);
      border-radius: var(--radius); padding: 12px;
      box-shadow: var(--shadow);
    }

    /* Input */
    label { display: block; font-size: 12px; font-weight: 600; color: var(--muted); margin-bottom: 3px; }
    textarea, input {
      width: 100%; border: 1px solid var(--line); border-radius: 6px;
      padding: 8px 10px; font: inherit; font-size: 13px;
      background: #fafafa; transition: border-color .15s; resize: vertical;
    }
    textarea:focus, input:focus { outline: none; border-color: var(--accent); background: #fff; }
    .mono { font-family: 'IBM Plex Mono', monospace; font-size: 12px; }

    /* Grids */
    .grid3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
    @media (max-width: 980px) { .grid3 { grid-template-columns: 1fr; } }

    /* Role cards */
    .role-card { border-width: 2px; position: relative; padding-top: 26px; }
    .role-card .role-badge {
      position: absolute; top: -1px; right: 10px;
      font-size: 9px; font-weight: 700; letter-spacing: .06em;
      padding: 2px 8px; border-radius: 0 0 5px 5px; color: #fff;
    }
    .role-propose { border-color: var(--proposeLine); }
    .role-propose .role-badge { background: var(--propose); }
    .role-critic { border-color: var(--criticLine); }
    .role-critic .role-badge { background: var(--critic); }
    .role-judge { border-color: var(--judgeLine); }
    .role-judge .role-badge { background: var(--judge); }
    .role-none { border-color: var(--line); }
    .role-none .role-badge { display: none; }
    .role-none.role-card { padding-top: 12px; }

    .role-label {
      font-size: 12px; font-weight: 700; margin-bottom: 6px;
      display: flex; align-items: center; gap: 5px;
    }
    .role-label .dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
    .role-propose .dot { background: var(--propose); }
    .role-critic .dot { background: var(--critic); }
    .role-judge .dot { background: var(--judge); }

    /* Buttons */
    .btns { display: flex; gap: 6px; flex-wrap: wrap; }
    button {
      font-family: inherit;
      border: 0; border-radius: 6px;
      padding: 7px 12px; font-size: 11px; font-weight: 700;
      cursor: pointer; color: #fff;
      transition: transform .1s, opacity .15s;
      letter-spacing: .01em; white-space: nowrap;
    }
    button:active { transform: translateY(1px); }
    button:hover { opacity: .88; }
    .btn-dark { background: var(--accent); }
    .btn-synth { background: var(--synth); }
    .btn-dialectic { background: var(--dialectic); }
    .btn-muted { background: #a1a1aa; }
    .btn-red { background: #dc2626; }
    .btn-sm { padding: 5px 10px; font-size: 10px; }

    /* Output */
    .output-synth { border: 2px solid var(--synthLine); background: var(--synthBg); }
    .output-dialectic { border: 2px solid var(--dialecticLine); background: var(--dialecticBg); }

    /* Role select */
    .role-select { display: flex; gap: 0; border: 1px solid var(--line); border-radius: 6px; overflow: hidden; }
    .role-select button {
      flex: 1; border-radius: 0; padding: 5px 6px; font-size: 11px;
      background: #f4f4f5; color: var(--text); font-weight: 600;
      border-right: 1px solid var(--line);
    }
    .role-select button:last-child { border-right: 0; }
    .role-select button.active-propose { background: var(--proposeBg); color: var(--propose); }
    .role-select button.active-critic { background: var(--criticBg); color: var(--critic); }
    .role-select button.active-judge { background: var(--judgeBg); color: var(--judge); }
    .role-select button.active-none { background: #e4e4e7; color: var(--text); }

    /* Helpers */
    .flex-between { display: flex; align-items: center; justify-content: space-between; gap: 8px; flex-wrap: wrap; }
    .hint { font-size: 10px; color: var(--muted); margin-top: 4px; }
    .mb6 { margin-bottom: 6px; }
    .mb8 { margin-bottom: 8px; }
    .gap-row { display: flex; gap: 10px; flex-wrap: wrap; align-items: flex-end; }
    .gap-row > div { flex: 1; min-width: 200px; }

    /* Toast */
    .toast {
      position: fixed; right: 16px; bottom: 16px;
      background: rgba(24,24,27,.92); color: #fff;
      padding: 7px 12px; border-radius: 6px;
      font-size: 11px; font-weight: 500;
      opacity: 0; transform: translateY(6px);
      transition: .2s ease; pointer-events: none; z-index: 200;
    }
    .toast.show { opacity: 1; transform: translateY(0); }
  </style>
</head>
<body>

  <!-- Sticky top bar -->
  <div class="top-bar">
    <div class="top-bar-inner">
      <div class="hLeft">
        <h1>Triple Synth</h1>
        <span class="sub">Role Separation × Multi-AI Synthesis</span>
        <span class="pill" id="sessionPill"></span>
      </div>
      <div class="hRight">
        <button class="btn-dark btn-sm" onclick="newSession()">New</button>
        <button class="btn-red btn-sm" onclick="resetAll()">Reset All</button>
      </div>
    </div>
  </div>

  <div class="wrap">

    <!-- Input -->
    <div class="section">
      <div class="card">
        <div class="gap-row mb8">
          <div style="flex:2;">
            <label>Topic / Question</label>
            <input id="topic" placeholder="The topic you want 3 AIs to address" />
          </div>
          <div style="flex:1;">
            <label>Source (optional)</label>
            <input id="source" placeholder="Guidelines, paper summaries, etc." />
          </div>
        </div>

        <label class="mb6">Role Assignment</label>
        <div class="grid3 mb8">
          <div>
            <label style="font-weight:700; color:var(--text); font-size:12px;">ChatGPT</label>
            <div class="role-select" data-model="gpt">
              <button onclick="setRole('gpt','none',this)">None</button>
              <button onclick="setRole('gpt','propose',this)" class="active-propose">Proposer</button>
              <button onclick="setRole('gpt','critic',this)">Critic</button>
              <button onclick="setRole('gpt','judge',this)">Judge</button>
            </div>
          </div>
          <div>
            <label style="font-weight:700; color:var(--text); font-size:12px;">Claude</label>
            <div class="role-select" data-model="claude">
              <button onclick="setRole('claude','none',this)">None</button>
              <button onclick="setRole('claude','propose',this)">Proposer</button>
              <button onclick="setRole('claude','critic',this)" class="active-critic">Critic</button>
              <button onclick="setRole('claude','judge',this)">Judge</button>
            </div>
          </div>
          <div>
            <label style="font-weight:700; color:var(--text); font-size:12px;">Gemini</label>
            <div class="role-select" data-model="gemini">
              <button onclick="setRole('gemini','none',this)">None</button>
              <button onclick="setRole('gemini','propose',this)">Proposer</button>
              <button onclick="setRole('gemini','critic',this)">Critic</button>
              <button onclick="setRole('gemini','judge',this)" class="active-judge">Judge</button>
            </div>
          </div>
        </div>

        <div class="btns">
          <button class="btn-dark" onclick="genPrompt('gpt')">ChatGPT Prompt</button>
          <button class="btn-dark" onclick="genPrompt('claude')">Claude Prompt</button>
          <button class="btn-dark" onclick="genPrompt('gemini')">Gemini Prompt</button>
        </div>
        <div class="hint">Each button generates a model-optimized prompt with role instructions → copy & paste into each AI</div>
      </div>
    </div>

    <!-- Responses -->
    <div class="section">
      <div class="grid3">
        <div class="card role-card role-propose">
          <span class="role-badge" id="badgeGpt">PROPOSE</span>
          <div class="role-label"><span class="dot"></span><span id="labelGpt">ChatGPT (Proposer)</span></div>
          <textarea id="ansGpt" rows="7" placeholder="Paste response here"></textarea>
        </div>
        <div class="card role-card role-critic">
          <span class="role-badge" id="badgeClaude">CRITIC</span>
          <div class="role-label"><span class="dot"></span><span id="labelClaude">Claude (Critic)</span></div>
          <textarea id="ansClaude" rows="7" placeholder="Paste response here"></textarea>
        </div>
        <div class="card role-card role-judge">
          <span class="role-badge" id="badgeGemini">JUDGE</span>
          <div class="role-label"><span class="dot"></span><span id="labelGemini">Gemini (Judge)</span></div>
          <textarea id="ansGemini" rows="7" placeholder="Paste response here"></textarea>
        </div>
      </div>
    </div>

    <!-- Synthesis + Dialectic -->
    <div class="section">
      <div class="card">
        <div class="flex-between mb8">
          <div class="btns">
            <button class="btn-synth" onclick="genSynthesis()">Synthesize</button>
            <button class="btn-dialectic" onclick="genDialectic()">Dialectic</button>
          </div>
          <div class="btns">
            <button class="btn-muted btn-sm" onclick="copyOutput()">Copy</button>
            <button class="btn-muted btn-sm" onclick="clearOutput()">Clear</button>
          </div>
        </div>
        <textarea id="output" class="mono output-synth" rows="8" placeholder="Generated prompt will appear here"></textarea>
        <div class="hint">Synthesize = produce a final answer (when converging) · Dialectic = find holes (when another round is needed) → paste into any AI's new chat</div>
      </div>
    </div>

  </div>

  <div id="toast" class="toast"></div>

<script>
const $ = id => document.getElementById(id);

// --- Roles ---
const roles = { gpt: 'propose', claude: 'critic', gemini: 'judge' };
const modelNames = { gpt: 'ChatGPT', claude: 'Claude', gemini: 'Gemini' };
const roleNames = { propose: 'Proposer', critic: 'Critic', judge: 'Judge', none: '' };
const roleClasses = { propose: 'role-propose', critic: 'role-critic', judge: 'role-judge', none: 'role-none' };
const badgeText = { propose: 'PROPOSE', critic: 'CRITIC', judge: 'JUDGE', none: '' };
const activeClass = { propose: 'active-propose', critic: 'active-critic', judge: 'active-judge', none: 'active-none' };

function setRole(model, role, btn) {
  roles[model] = role;
  btn.parentElement.querySelectorAll('button').forEach(b => b.className = '');
  btn.className = activeClass[role];
  updateCards();
}

function updateCards() {
  const map = { gpt: 'Gpt', claude: 'Claude', gemini: 'Gemini' };
  for (const [model, role] of Object.entries(roles)) {
    const s = map[model];
    const card = $('ans' + s).closest('.role-card');
    card.className = `card role-card ${roleClasses[role]}`;
    $('badge' + s).textContent = badgeText[role];
    const dot = card.querySelector('.dot');
    if (role === 'none') {
      $('label' + s).textContent = modelNames[model];
      dot.style.display = 'none';
    } else {
      $('label' + s).textContent = `${modelNames[model]} (${roleNames[role]})`;
      dot.style.display = '';
    }
  }
}

// --- Session ---
function makeId() {
  const d = new Date();
  const p = n => String(n).padStart(2, '0');
  return `${d.getFullYear()}${p(d.getMonth()+1)}${p(d.getDate())}-${p(d.getHours())}${p(d.getMinutes())}${p(d.getSeconds())}-${Math.random().toString(36).slice(2,5).toUpperCase()}`;
}
function nowIso() {
  const d = new Date();
  const p = n => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth()+1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}`;
}

let sessionId = makeId();
$('sessionPill').textContent = sessionId;

function newSession() {
  sessionId = makeId();
  $('sessionPill').textContent = sessionId;
  toast('New session');
}
function resetAll() {
  ['topic','source','ansGpt','ansClaude','ansGemini','output'].forEach(id => $(id).value = '');
  newSession();
  toast('Reset');
}

// --- Toast ---
function toast(msg) {
  const t = $('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 1200);
}

// --- Copy ---
async function copyText(text) {
  if (!text) { toast('Nothing to copy'); return; }
  $('output').value = text;
  try {
    await navigator.clipboard.writeText(text);
    toast('Copied');
  } catch {
    try {
      $('output').focus(); $('output').select();
      document.execCommand('copy');
      toast('Copied');
    } catch { toast('Auto-copy failed'); }
  }
}
function copyOutput() { copyText($('output').value); }
function clearOutput() { $('output').value = ''; toast('Cleared'); }
function norm(v) { return (v || '').trim() || 'N/A'; }

// --- Prompt Generation (per-model format) ---
const roleInstructions = {
  propose: {
    core: 'Act as the Proposer. Present the single best hypothesis for the topic, provide 3 supporting reasons, and state 1 falsifiable prediction.',
    constraint: 'Mark uncertain points as "unverified." Do not fill gaps with speculation.'
  },
  critic: {
    core: 'Act as the Critic. Identify up to 5 weaknesses, counterexamples, or blind spots. Propose 1 alternative hypothesis if possible, and list what additional information is needed to decide.',
    constraint: 'Mark uncertain points as "unverified." Do not fill gaps with speculation. Do not agree easily.'
  },
  judge: {
    core: 'Act as the Judge. Organize: (a) points of agreement, (b) points of contention, (c) the most defensible conclusion at this stage, (d) open questions and next verification steps.',
    constraint: 'Mark uncertain points as "unverified." Do not fill gaps with speculation. Do not decide by majority vote.'
  }
};

function genPrompt(model) {
  const topic = norm($('topic').value);
  const source = norm($('source').value);
  const role = roles[model];
  let prompt;

  // Role-free prompt
  if (role === 'none') {
    if (model === 'claude') {
      prompt = `<session>${sessionId}</session>

<source>
${source}
</source>

<instructions>
Constraints:
Mark uncertain points as "unverified." Do not fill gaps with speculation.
If Source is provided, mark claims beyond Source as "unverified" and prefer deletion.
</instructions>

<topic>
${topic}
</topic>

<output_format>
Conclusion (1–3 sentences) → Evidence (bullet list, max 5) → Limitations
</output_format>`;
    } else if (model === 'gpt') {
      prompt = `# Session: ${sessionId}

## Topic
${topic}

## Constraints
- Mark uncertain points as "unverified." Do not fill gaps with speculation.
- If Source is provided, mark claims beyond Source as "unverified" and prefer deletion.
- Source: ${source}

## Output Format (strict)
1. **Conclusion** (1–3 sentences)
2. **Evidence** (max 5, bullet list)
3. **Limitations**`;
    } else {
      prompt = `[Session] ${sessionId}

[Background]
Source: ${source}

Topic:
${topic}

[Instructions]
Constraints:
Mark uncertain points as "unverified." Do not fill gaps with speculation.
If Source is provided, mark claims beyond Source as "unverified" and prefer deletion.

Output format:
Conclusion (1–3 sentences) → Evidence (bullet list, max 5) → Limitations`;
    }
    copyText(prompt);
    return;
  }

  // Role-assigned prompt
  const ri = roleInstructions[role];

  if (model === 'claude') {
    prompt = `<session>${sessionId}</session>

<source>
${source}
</source>

<instructions>
Your role: ${roleNames[role]}
${ri.core}

Constraints:
${ri.constraint}
If Source is provided, mark claims beyond Source as "unverified" and prefer deletion.
</instructions>

<topic>
${topic}
</topic>

<output_format>
Conclusion (1–3 sentences) → Evidence (bullet list, max 5) → Likely counterarguments (2) → Limitations
</output_format>`;
  } else if (model === 'gpt') {
    prompt = `# Session: ${sessionId}

## Your role: ${roleNames[role]}

${ri.core}

## Constraints
- ${ri.constraint}
- If Source is provided, mark claims beyond Source as "unverified" and prefer deletion
- Source: ${source}

## Topic
${topic}

## Output Format (strict)
1. **Conclusion** (1–3 sentences)
2. **Evidence** (max 5, bullet list)
3. **Likely counterarguments** (2)
4. **Limitations**`;
  } else {
    prompt = `[Session] ${sessionId}

[Background]
Source: ${source}

Topic:
${topic}

[Instructions]
Your role: ${roleNames[role]}

${ri.core}

Constraints:
${ri.constraint}
If Source is provided, mark claims beyond Source as "unverified" and prefer deletion.

Output format:
Conclusion (1–3 sentences) → Evidence (bullet list, max 5) → Likely counterarguments (2) → Limitations`;
  }
  copyText(prompt);
}

// --- Synthesis ---
function genSynthesis() {
  const topic = norm($('topic').value);
  const source = norm($('source').value);
  $('output').className = 'mono output-synth';

  const parts = [];
  for (const [model, role] of Object.entries(roles)) {
    const fieldMap = { gpt: 'ansGpt', claude: 'ansClaude', gemini: 'ansGemini' };
    const label = role === 'none' ? modelNames[model] : `${modelNames[model]} (${roleNames[role]})`;
    parts.push(`[${label}]\n${norm($(fieldMap[model]).value)}`);
  }

  const anyRoles = Object.values(roles).some(r => r !== 'none');
  const roleNote = anyRoles ? '\nThe 3 outputs below were generated under different assigned roles.' : '';

  const prompt =
`[Session] ${sessionId}
[Generated] ${nowIso()}

[SYNTHESIS]
Goal: Integrate 3 outputs into a single final answer.
Source: ${source}
${roleNote}
Judge by quality of evidence, not majority vote. Resolve contradictions and handle unverified claims.

Rules:
- If Source exists: mark claims beyond Source as "unverified" and prefer deletion
- If no Source: evaluate by Logic / Ops / Risk and keep it minimal
- Forbidden: majority vote, listing agreements, verbose commentary

Topic: ${topic}

${parts.join('\n\n')}

[Output]
- Integrated final answer (finished product only)
- Clearly state: agreements, disputes, provisional conclusion, open questions
- If unverified claims remain, mark them as "unverified"`;

  copyText(prompt);
}

// --- Dialectic ---
function genDialectic(targetModel) {
  targetModel = targetModel || 'gpt';
  const source = norm($('source').value);
  const goal = norm($('topic').value);
  $('output').className = 'mono output-dialectic';

  const order = ['gpt', 'claude', 'gemini'];
  const sorted = [targetModel, ...order.filter(m => m !== targetModel)];
  const fieldMap = { gpt: 'ansGpt', claude: 'ansClaude', gemini: 'ansGemini' };

  const blocks = sorted.map((model, i) => {
    const role = roles[model];
    const roleLabel = role === 'none' ? '' : ` (${roleNames[role]})`;
    const label = `AI${i} = ${modelNames[model]}${roleLabel}:`;
    return `${label}\n${norm($(fieldMap[model]).value)}`;
  });

  const prompt =
`[Session] ${sessionId}
[Generated] ${nowIso()}

[DIALECTIC CRITIQUE]
Goal: ${goal}
Source: ${source}

${blocks.join('\n\n')}

If Source exists: mark claims beyond Source as "unverified" and delete
If no Source: evaluate by Logic, Ops (practicality), Risk

Priority rules:
- Forbidden: agreement, compromise, commentary, majority vote
- STOP if: agreement inflation / goal drift / Source drift → output reset statement only
- Prefer deletion over addition. Always ask: "Is this addition truly necessary?"
- Reject changes that increase user burden

Hole categories:
- [Logic] Logical contradiction or misalignment with the goal
- [Risk] Legal, safety, ethical issues, hallucination
- [Scope] Over- or under-scoping
- [Ops] Practicality and usability

Output:
1. Holes (one line per AI0/AI1/AI2; "none" if none found)
2. Blind spots (important angles all 3 missed; "none" if none)
3. Items to delete (if any)
4. Verdict: "No change needed" / "Minor revision" / "Major revision needed"
5. Revised version (only if major revision; finished product only)`;

  copyText(prompt);
}
</script>
</body>
</html>
