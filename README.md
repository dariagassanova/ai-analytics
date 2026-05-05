# Cluster Analytics Dashboard

Upload a cluster CSV and instantly see:
- Monthly creation dynamics
- Closure rate (Merged vs NoDuplicates) by month
- Closure split by score band
- Unresolved backlog breakdown

## Deploy to Streamlit Community Cloud (free, ~5 mins)

1. **Create a GitHub repo** (public or private)
   - Go to github.com → New repository
   - Name it e.g. `cluster-dashboard`

2. **Add these two files to the repo**
   - `app.py`
   - `requirements.txt`

3. **Deploy on Streamlit**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click **New app**
   - Select your repo, branch `main`, file `app.py`
   - Click **Deploy** — live in ~2 minutes

4. **Share the link**
   - Your app will be at `https://yourname-cluster-dashboard-app-xxxx.streamlit.app`
   - Share with anyone — no login required to view

## Expected CSV columns

| Column | Description |
|--------|-------------|
| `cluster_id` | Unique cluster identifier |
| `current_cluster_status` | e.g. SuspectedDuplicates, Merged, NoDuplicates |
| `createcluster` | Timestamp of cluster creation |
| `terminatingevent` | Timestamp of closure (if resolved) |
| `wk_score_2dp` | Similarity score 0–1 |

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
