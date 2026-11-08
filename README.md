# Job Radar — free GitHub Pages edition

Standalone personal job dashboard. Not connected to VEEBIO or SHOBA.

## Deploy

1. Create a **public** GitHub repository named `job-radar`. Do not upload private records or secrets. GitHub Pages on GitHub Free supports public repositories.
2. Upload the contents of this ZIP to the repository root, including the `.github/workflows/` directory. **Do not upload the ZIP as a single file**.
3. Commit files to `main`.
4. In repository Settings → Pages → Build and deployment, choose **GitHub Actions** as Source.
5. In Actions, open **Publish Job Radar website**, then click **Run workflow** if a run has not already started.
6. After the run succeeds, use the published Pages URL shown in the job or Settings → Pages. Expected pattern: `https://<username>.github.io/job-radar/` (confirm actual URL).
7. On iPhone, open the live URL in Safari; use Share → Add to Home Screen if desired.

## Privacy

Application status and manually entered job details are saved only in this browser using localStorage. They are not uploaded to GitHub. Do not upload your resume, screenshots, private applications, passwords, or browser exports to the public repository. Use **Export CSV** regularly as a backup; CSV can contain sensitive application data.

## Instagram

Paste an Instagram post URL or employer application link into Sources & imports, optionally select a screenshot to preview, and manually confirm job title, employer, location, and deadline. Screenshot OCR and automatic Instagram channel reading are NOT supported. Screenshot is not uploaded or retained.

## Public source collection

The collector is **manual-only** initially. Before running it, check source robots.txt, site terms, and permission for automated collection. The source was not accessible from the preparation environment, so permission and parser accuracy are unverified. Once approved, use Actions → Collect public job listings → Run workflow. If it succeeds and commits new jobs.json, the Pages publishing workflow republishes the website. The collector may require adjustment if site markup changes. Do not turn on scheduled scraping before validation.

## Limitations

Starter listings are not verified active opportunities. Application eligibility and deadlines must be checked with employers. No login or cross-device synchronization, email notifications, OCR, or guaranteed daily collection. This is a public website, not a private dashboard; only local browser data is private to your device.
