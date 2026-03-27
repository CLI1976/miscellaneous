from google import genai
from google.genai import types
import configparser, os

# 讀取 API Key
_cfg = configparser.ConfigParser()
_cfg.read(os.path.join(os.path.dirname(__file__), "api.ini"), encoding="utf-8")
_api_key = _cfg.get("gemini", "api_key")

client = genai.Client(api_key=_api_key)

SYSTEM_INSTRUCTION = """# Role
You are RaioAssistant, a specialized AI collaborator for clinical radiologists. Your primary goal is to refine English radiology reports and provide evidence-based diagnostic support.

# Core Functions

1. **Report Refinement (English Only):**
   - Refine the user's radiology findings and impressions to match the professional standards of English-speaking countries (US/UK/AU).
   - Findings: structured list organized by organ systems or anatomic regions.
   - Impression: focus on the most significant diagnoses. Be direct and succinct.
   - Style: use standardized medical lexicons (e.g., BI-RADS, PI-RADS, LI-RADS, Fleischner Society).

2. **Clinical D/D Support:**
   - Suggest differential diagnoses based on patient demographics and imaging findings.
   - Provide a brief justification for each D/D.
   - For every D/D, provide a direct hyperlink to Radiopaedia or RadioGraphics (specific article, not homepage).

# Language & Tone
- Radiology Reports: strictly in English.
- General Communication & Justifications: Traditional Chinese (zh-tw).
- Tone: professional, peer-to-peer, high-efficiency.

# Knowledge Base
- Radiopaedia: https://radiopaedia.org/
- RadioGraphics: https://pubs.rsna.org/journal/radiographics
- Radiology Assistant: https://radiologyassistant.nl/

# OUTPUT FORMAT — STRICT JSON ONLY
You MUST respond with ONLY a valid JSON object. No markdown, no code blocks, no extra text before or after.

JSON schema:
{
  "intro": "string — 繁體中文 opening sentence",
  "report": {
    "title": "string — e.g. Chest CT (Non-contrast and Contrast-enhanced)",
    "findings": [
      {
        "label": "string — organ system label, e.g. Lungs and Pleura",
        "items": ["string", "string"]
      }
    ],
    "impression": ["string", "string"]
  },
  "dd": [
    {
      "title": "string — e.g. 縱膈腔淋巴結腫大 (Mediastinal Lymphadenopathy)",
      "differentials": [
        {
          "name": "string — diagnosis name",
          "justification": "string — 繁體中文 brief reasoning",
          "references": [
            {"text": "string — link label", "url": "string — full URL"}
          ]
        }
      ]
    }
  ],
  "note": "string or null — optional closing remark in 繁體中文"
}"""

GEM_CONFIG = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION,
    temperature=0.5,
)

GEM_MODEL = "gemini-3-flash-preview"  # gemini-2.5-flash, gemini-3-flash-preview

# ── 顯示設定 ─────────────────────────────────────────────
FONT_FAMILY = "Microsoft JhengHei, Segoe UI, sans-serif"
FONT_SIZE   = 15  # px

# ── JSON → HTML ──────────────────────────────────────────
def json_to_html(json_str):
    import json, re
    from html import escape

    # 去掉 model 可能加的 markdown code block wrapper
    json_str = re.sub(r'^```(?:json)?\s*', '', json_str.strip())
    json_str = re.sub(r'\s*```$', '', json_str.strip())

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        return f'<div class="error"><h3>JSON 解析失敗，原始輸出：</h3><pre>{escape(json_str)}</pre></div>'

    p = []

    # Intro
    if data.get('intro'):
        p.append(f'<p class="intro">{escape(data["intro"])}</p>')

    # Report
    report = data.get('report', {})
    if report:
        p.append('<div class="report">')
        if report.get('title'):
            p.append(f'<h2>{escape(report["title"])}</h2>')

        findings = report.get('findings', [])
        if findings:
            p.append('<h3>Findings</h3>')
            for f in findings:
                p.append('<div class="finding-group">')
                p.append(f'<div class="finding-label">{escape(f.get("label",""))}</div>')
                p.append('<ul>')
                for item in f.get('items', []):
                    p.append(f'<li>{escape(item)}</li>')
                p.append('</ul></div>')

        impression = report.get('impression', [])
        if impression:
            p.append('<h3>Impression</h3><ol>')
            for item in impression:
                p.append(f'<li>{escape(item)}</li>')
            p.append('</ol>')

        p.append('</div><hr>')

    # D/D
    dd = data.get('dd', [])
    if dd:
        p.append('<div class="dd-section">')
        p.append('<h2>臨床鑑別診斷支援 (Clinical D/D Support)</h2>')
        for i, group in enumerate(dd, 1):
            p.append('<div class="dd-group">')
            p.append(f'<h3>{i}. {escape(group.get("title",""))}</h3>')
            for diff in group.get('differentials', []):
                p.append('<div class="differential">')
                p.append(f'<div class="dx-name">{escape(diff.get("name",""))}</div>')
                if diff.get('justification'):
                    p.append(f'<p class="justification">{escape(diff["justification"])}</p>')
                for ref in diff.get('references', []):
                    p.append(f'<a href="{escape(ref.get("url",""))}" class="ref-link">'
                             f'{escape(ref.get("text",""))}</a>')
                p.append('</div>')
            p.append('</div>')
        p.append('</div>')

    # Note
    if data.get('note'):
        p.append(f'<div class="note"><p>{escape(data["note"])}</p></div>')

    return '\n'.join(p)


# ── Gemini API ────────────────────────────────────────────
def ask_gem(user_input):
    response = client.models.generate_content(
        model=GEM_MODEL,
        config=GEM_CONFIG,
        contents=user_input,
    )
    return json_to_html(response.text)


# ── GUI ──────────────────────────────────────────────────
CSS = f"""
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html {{ background: #e8e8e8; }}
  body {{ font-family: {FONT_FAMILY}; font-size: {FONT_SIZE}px; line-height: 1.75;
          max-width: 880px; margin: 20px auto; padding: 24px 28px;
          background: #f5f5f5; border-radius: 8px; color: #1a1a2e; }}

  /* Intro */
  .intro {{ color: #444; margin-bottom: 16px; }}

  /* Report */
  .report h2 {{ font-size: 1.4em; color: #1a237e; border-bottom: 2px solid #3949ab;
                padding-bottom: 5px; margin: 16px 0 10px; }}
  .report h3 {{ font-size: 1.1em; color: #283593; margin: 14px 0 6px; }}
  .finding-group {{ margin-bottom: 10px; }}
  .finding-label {{ font-weight: bold; color: #1565c0; margin-bottom: 3px; }}
  .report ul, .report ol {{ padding-left: 28px; margin: 4px 0; }}
  .report li {{ margin: 3px 0; }}

  /* D/D */
  hr {{ border: none; border-top: 1px solid #c5cae9; margin: 20px 0; }}
  .dd-section h2 {{ font-size: 1.2em; color: #1a237e; border-bottom: 2px solid #3949ab;
                    padding-bottom: 5px; margin-bottom: 14px; }}
  .dd-group {{ margin-bottom: 16px; }}
  .dd-group h3 {{ font-size: 1.05em; color: #283593; margin-bottom: 8px; }}
  .differential {{ margin-left: 16px; margin-bottom: 10px;
                   border-left: 3px solid #90caf9; padding-left: 12px; }}
  .dx-name {{ font-weight: bold; color: #1565c0; }}
  .justification {{ color: #333; margin: 4px 0 5px; }}
  .ref-link {{ display: inline-block; font-size: 0.88em; color: #1976d2;
               margin-right: 10px; margin-top: 2px; }}
  .ref-link:hover {{ text-decoration: underline; }}

  /* Note */
  .note {{ margin-top: 20px; padding: 10px 14px; background: #fff8e1;
           border-left: 4px solid #f9a825; border-radius: 4px; color: #555; }}

  /* Error fallback */
  .error {{ color: #c62828; }}
  .error pre {{ background: #fce4ec; padding: 10px; border-radius: 4px;
                font-size: 0.85em; white-space: pre-wrap; }}
"""

def show_result(html_body):
    import sys, webbrowser, tempfile, os
    from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    from PyQt6.QtWebEngineCore import QWebEnginePage

    class ExternalLinkPage(QWebEnginePage):
        def acceptNavigationRequest(self, url, nav_type, is_main_frame):
            if nav_type == QWebEnginePage.NavigationType.NavigationTypeLinkClicked:
                webbrowser.open(url.toString())
                return False
            return True

    app = QApplication.instance() or QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle(f"RadioAssistant_{GEM_MODEL}")
    window.resize(920, 720)

    view = QWebEngineView()
    view.setPage(ExternalLinkPage(view))

    _signal = os.path.join(tempfile.gettempdir(), "gem_ready.txt")
    view.loadFinished.connect(lambda _: open(_signal, 'w').close())

    full_html = f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{html_body}</body></html>'
    view.setHtml(full_html)

    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(view)
    window.setLayout(layout)
    window.show()

    app.exec()


# ── Entry Point ───────────────────────────────────────────
if __name__ == "__main__":
    import sys, os, tempfile

    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        if os.path.isfile(input_path):
            with open(input_path, "r", encoding="utf-8") as f:
                user_input = f.read().strip()
        else:
            user_input = input_path
    else:
        user_input = "請解釋一下什麼是 EUS-FNA？"

    result_html = ask_gem(user_input)
    show_result(result_html)

    tmpOut = os.path.join(tempfile.gettempdir(), "gem_out.txt")
    with open(tmpOut, "w", encoding="utf-8") as f:
        f.write('{"success": true}')
