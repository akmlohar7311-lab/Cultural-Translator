# Group 18 Cultural Translator — Deploy on Render

This project is a Flask server application, not a static HTML website.

## Before publishing
- Rotate/revoke any Gemini API key previously shown in screenshots, chat, or a public repository.
- **Never upload `.env` or your API key to GitHub.** The `.gitignore` protects local accidental Git commits, but confirm before uploading.
- Use a newly created Gemini API key with appropriate quota/billing controls.

## Deploy on Render (manual setup)
1. Extract the ZIP and open the `Group18_Render_Deploy` folder.
2. On GitHub, create an empty repository (private is fine, if connected to Render).
3. Use **Add file → Upload files** and upload the contents *inside* `Group18_Render_Deploy` (not the outer folder or ZIP). Keep `app.py`, `requirements.txt`, and `render.yaml` at the repo root; keep `index.html` inside `templates/`.
4. Open https://dashboard.render.com/ and choose **New → Web Service**, then connect the repository.
5. Configure: Language **Python 3**; Build **`pip install -r requirements.txt`**; Start **`gunicorn app:app --workers 1 --threads 4 --timeout 120 --bind 0.0.0.0:$PORT`**; choose Free if available and appropriate.
6. In **Environment**, add `GEMINI_API_KEY` = your **new private key** and `GEMINI_MODEL` = `gemini-3.5-flash-lite`.
7. Choose **Create Web Service**. When the deploy says **Live**, open the service URL ending in `.onrender.com`.
8. Submit a sample such as `Break a leg!` (English -> Marathi). Verify both translated outputs and the cultural note.

Alternative: use **New → Blueprint** with `render.yaml`; Render will prompt you for the `GEMINI_API_KEY` value. 

## Local Windows testing
From the folder containing `app.py`:
```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
# create .env locally with GEMINI_API_KEY=... (do not commit it)
.\.venv\Scripts\python.exe app.py
```
Open http://127.0.0.1:5000

## Important considerations
- The Render Free web service spins down after inactivity; its first request may be slow. The free plan is suited to demonstrations, not guaranteed uptime.
- Public visitors can send requests to the Gemini API through your site, potentially using your quota or causing charges. For a classroom demo, share the URL only as needed and monitor API quota/billing.
- Translation history is held in browser-session storage; it is not a server database.
- Translation content is sent to Google Gemini. Avoid entering personal or confidential information.
- If your model is inaccessible, check your account's available model identifiers and update `GEMINI_MODEL` in Render's Environment settings.
