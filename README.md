# Job Radar

Standalone public job discovery and browser-local application tracker. This project is separate from all other products.

## Live website and development

- Live public GitHub Pages: https://pitchblackdigital-bit.github.io/job-radar/
- In-progress Canada-first work: branch `feature/canada-first-ai-apply`, draft PR #1. This branch is **not** the live site and is not an approved preview.
- Do not merge until the updated collector, location filters, accessibility, and mobile flows are tested.

## Public collection

`collector.py` retrieves employer-published Greenhouse and Lever job feeds listed in `sources.json`. The GitHub Actions collector is scheduled; check Actions history and `feed-status.json` to confirm actual successful refreshes. The collector filters design-related titles, excludes internships, and requires a Canadian location signal. A Canadian location mention is **not** verification of legal work eligibility or that a vacancy remains open. Failed feeds are reported; the old feed may be retained if no sources succeed.

The committed `jobs.json` can contain old US-based and starter records until a successful refresh replaces it. Do not present those as verified current Canadian opportunities. Check employer job links before publishing or applying.

## Job-alert email discovery (proposed, not deployed)

Job alerts received by a user can help **discover** potential listings. Never commit mailbox messages, Gmail IDs, personalized click-through/tracking URLs, unsubscribe links, resume details, or private data into this public repository. Extract only candidate job title, employer, location, role type, salary when stated, and the alert date into a **private review queue**. Resolve to a canonical public employer or ATS listing; confirm the vacancy is still open, location/remote eligibility is explicit, and role is relevant. Deduplicate by canonical listing URL and employer/job ID. Only approved verified public listings should be eligible for the public job feed, with source and last-checked date. Unverifiable listings stay private and unpublished.

There is **no** deployed Gmail-to-website sync or secure mailbox backend. The connected inbox used during planning is not available to public visitors and must not be accessed from client-side JavaScript. A future automated import requires user consent, restricted OAuth permissions, server-side secrets, and a secure private processing environment.

## Privacy and current limitations

The public GitHub Pages site has no account registration, private cloud resume storage, cross-device sync, working AI assistant, or automatic AI application submission. Browser-local saved information is device-specific. Do not commit personal data, credentials, API keys, or private application records. Any future AI Apply workflow must require review and explicit user authorization before submitting applications.
