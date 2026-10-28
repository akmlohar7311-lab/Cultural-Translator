# LinguaContext — Group 18 · Stage 2 (Dark Edition)

**Akash Lohar · Rafat Sayyed · Arshita Gupta**

This is an upgraded version of the existing Flask + Gemini student translator. It provides a dark, responsive interface and compares neutral translation with meaning-preserving cultural localization.

## What was improved

- Dark responsive visual design, mobile-friendly layout and demo example chips
- **Swap languages** control (source = Auto-detect uses a sensible target fallback)
- **Copy** buttons for both translations and the cultural explanation
- **Recent history**, saved for this browser tab only (`sessionStorage`); Restore, Copy and Clear controls
- Original / Formal / Casual tone and optional regional context
- Prompt improvements for idioms and proverbs (including the "apple a day" example), no invented literal translation
- Safe on-screen API errors and length validation (4,000 input characters)
- **One Gemini request** yields standard, localized and explanation fields as structured JSON

**Important:** Both AI translations may legitimately be identical. Browser-tab history does not send requests or make a server-side database; translation content is still sent to Gemini to generate results. Avoid private or sensitive information.

## Update your already-working VS Code project (easy)

1. **Back up** your current folder.
2. Download and extract this ZIP, then open the new folder in VS Code. Do not copy `.venv` from your previous folder; if you want, make a fresh one (instructions below).
3. **Copy your existing PRIVATE `.env` file** from your previous working project into this folder, beside `app.py`. Keep the same working API key and model name. The ZIP deliberately contains **only `.env.example`**, never your private key.
4. Open the VS Code terminal (PowerShell) in this folder.
5. Create the environment (if needed): `py -m venv .venv`
6. Install: `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`
7. Run: `.\.venv\Scripts\python.exe app.py`
8. Open `http://127.0.0.1:5000`.
9. Stop with **Ctrl+C**. Stop any older Flask server first if port 5000 is already occupied.

If the command `py` is not found, use your installed Python interpreter to create the environment. When a virtual environment exists, use `.\.venv\Scripts\python.exe` to start Flask to avoid the "Python was not found" Windows error.

## File layout

```
Group18_Dark_Cultural_Translator/
├── app.py                    # Backend, Gemini prompt and API
├── templates/index.html      # Dark UI, swap/copy/history JavaScript
├── .env.example              # Template only (never a real key)
├── .gitignore
├── requirements.txt
├── tests/test_app.py          # Offline unit tests
└── README.md
```

## Tests

From the project folder:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The offline tests mock Gemini. They do **not** prove live translation accuracy. For a real evaluation record, test with your own authorized Gemini API key and have a fluent speaker review the output.

## Presentation examples

| Input | Source → Target | Suggested tone | Check |
|---|---|---|---|
| Break a leg! | English → Marathi | Original | Wish of good luck, not a literal leg injury |
| An apple a day keeps the doctor away. | English → Marathi | Formal | General healthy habits; not advice to skip medical care |
| This exam is a piece of cake. | English → Hindi | Casual | Exam is easy, not about food |
| Thank you for your assistance. | English → Marathi | Formal | Politeness in translation |

## Notes

- If the Gemini API returns `503`, it may be temporarily busy. The official Google GenAI SDK handles retries for many transient issues already. We do not add an extra retry loop.
- API availability, billing, rate limits and output quality depend on your project and model access.
- Flask's built-in server is for **local development**, not public deployment.
- The history feature uses `sessionStorage` for the **current browser tab** with the latest **8** successful translations and can be erased by clicking **Clear history**. Closing the tab normally clears session storage, although some browsers may restore sessions.
- Do not share the `.env` file or display API keys in project screenshots. The example `.env.example` is safe to share.
