# Sira Quran Academy — Android build repo

This repo builds a real native Android app (via Capacitor) from the same
`www/index.html` web app, with working daily reminder notifications that
fire even when the app is fully closed. GitHub builds and signs it for
you — nothing needs installing on your phone or computer except a
browser.

## One-time setup (do this once)

### 1. Upload these files to your empty GitHub repo

Go to your repo on github.com → **Add file → Upload files**, then drag
this whole folder's contents in (or use GitHub Desktop / `git push` from
a computer if you have one later — either works). Keep the folder
structure exactly as given: `www/`, `.github/workflows/`, `scripts/`,
`package.json`, `capacitor.config.json`, `.gitignore`.

Do **not** upload your keystore file itself. It never goes in the repo.

### 2. Turn your keystore into one line of text (base64)

You need to do this on any computer (your friend's PC, or a phone with
Termux) that has your `.keystore`/`.jks` file.

On a computer (Mac/Linux terminal, or Git Bash on Windows):
```
base64 -w0 your-keystore-file.jks > keystore_base64.txt
```
On Windows PowerShell:
```
[Convert]::ToBase64String([IO.File]::ReadAllBytes("your-keystore-file.jks")) | Out-File keystore_base64.txt
```
Open `keystore_base64.txt` and copy its entire contents (it will be one
long line of random-looking text). Never paste this — or your keystore
password — into a chat with anyone, including me.

### 3. Add 4 secrets to the GitHub repo

In your repo: **Settings → Secrets and variables → Actions → New
repository secret**. Add these four, one at a time:

| Secret name | Value |
|---|---|
| `KEYSTORE_BASE64` | the long text from step 2 |
| `KEYSTORE_PASSWORD` | your keystore's password |
| `KEY_ALIAS` | your key's alias |
| `KEY_PASSWORD` | your key's password (often the same as the keystore password) |

These stay encrypted inside GitHub and are never shown again, even to
you — so keep `keystore_base64.txt` somewhere safe in case you need it
again later.

## Every time you want a new build

1. Go to the repo's **Actions** tab → **Build signed Android app bundle**
   → **Run workflow**.
2. It asks for a `versionCode` (must be a plain whole number **higher**
   than whatever you last uploaded to Play Console — check your Play
   Console dashboard if unsure) and a `versionName` (anything readable,
   e.g. `1.1.0`).
3. Click **Run workflow**. It takes a few minutes — GitHub is installing
   Capacitor, building the native Android project, and signing it with
   your key.
4. When it finishes (green check), click into that run → under
   **Artifacts** at the bottom, download `sira-quran-academy-release`.
   Unzip it — inside is `app-release.aab`.
5. In Play Console, go to your app → **Production** (or a testing
   track) → **Create new release** → upload that `.aab`.

Because this uses the exact same package name (`academy.quran.sira`)
and the exact same signing key as your current PWA-Builder app, Play
Console will treat this as an **update** to the same app — not a new
one. Your closed-testing progress is not affected.

## What changed for the reminder feature

Inside the app, when it detects it's running as this native Android
build, it now schedules the daily reminder using the phone's own
notification scheduler (`@capacitor/local-notifications`) instead of
relying on the browser's Notification API. That's what makes the
reminder fire reliably even when the app isn't open. When the same
`index.html` runs as a plain PWA in a regular browser, it automatically
falls back to the old behavior — nothing breaks for web users.

One small trade-off: the native reminder text is a fixed encouraging
message rather than one that mentions your exact streak number, since
the phone schedules it in advance rather than computing it the moment
it fires. Say the word if you'd like me to make that smarter later
(e.g. rescheduling it fresh each time the app is opened).
