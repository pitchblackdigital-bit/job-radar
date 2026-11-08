# Job Radar automated collection — deployment notes

This package adds a collector for public Greenhouse and Lever ATS feeds, plus a GitHub Actions schedule (three runs daily, UTC; times shift relative to Toronto daylight saving). Source slugs are configurable in `sources.json` and are **candidates, not verified working integrations**. On the first run, inspect the Actions log and `feed-status.json` to identify valid sources. The workflow requires GitHub Actions permission to write repository contents (Settings > Actions > General > Workflow permissions > Read and write permissions), otherwise the collector may run but cannot commit the feed. Public repositories can use GitHub Pages and limited Actions minutes without payment, subject to platform policies and limits.

No Instagram account scraping or private channel access is implemented. Users can still manually import links/screenshots using the existing UI; screenshot OCR is not implemented. Listings are public ATS postings, **not verified for Canadian eligibility**. No salary or job validity is invented. The collector excludes internships and traineeships and uses title matching for design and technology-adjacent creative roles.

Important: The existing Job Radar UI stores personal application statuses in the browser. Data does not synchronize between devices. The collector updates `jobs.json` in the public repository; it does not transmit saved jobs or personal data.

## Publishing

Upload the entire contents of this package to the root of the existing `pitchblackdigital-bit/job-radar` repository, preserving `.github/workflows/`. Ensure GitHub Pages remains configured to publish from `main` root, or use the included Pages workflow if switching to GitHub Actions source. Do not run both publishing strategies unnecessarily. Open Actions > Refresh Job Radar public job feeds > Run workflow for the first manual test. Review the results and the published `jobs.json`. This package is locally validated but not deployed or live-tested.
