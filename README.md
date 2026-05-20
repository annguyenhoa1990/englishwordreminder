# English Word Reminder Web App

This is a Flask web app that reminds you to learn 5 English words every day.

## Run locally

1. Install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
2. Start the app:
   ```bash
   python3 app.py --port 5001
   ```
3. Open in browser:
   - `http://127.0.0.1:5001`

## Deploy to the internet

### Option 1: Use Render (recommended)

1. Create a GitHub repository and push this project.
2. Sign in to https://render.com and create a new Web Service.
3. Connect your GitHub repo.
4. Use these settings:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Deploy and open the generated public URL.

### Option 2: Use ngrok for temporary sharing

1. Run the app locally:
   ```bash
   python3 app.py --port 5001
   ```
2. In another terminal, run:
   ```bash
   ngrok http 5001
   ```
3. Use the public URL displayed by ngrok.

## What was added for deployment

- `requirements.txt` now includes `gunicorn`
- `Procfile` to start the app on hosting services
- `runtime.txt` to fix the Python version on hosts that use it

## Notes

- This app is ready for small deployments and demos.
- For stable production, use a service like Render, Railway, or PythonAnywhere.
