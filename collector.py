"""Job Radar public ATS feed collector. No Instagram scraping or private access."""
import datetime as dt
import hashlib
import json
import pathlib
import re
import sys
from urllib.parse import urlparse
import requests

ROOT = pathlib.Path(__file__).resolve().parent
OUTPUT = ROOT / 'jobs.json'
CONFIG = ROOT / 'sources.json'
TIMEOUT = 20
HEADERS = {'User-Agent': 'JobRadar/1.0 (public ATS feed; low-frequency personal job discovery)'}
ROLE = re.compile(r'\b(ux|ui|user experience|user interface|product design(?:er)?|wordpress|web design(?:er)?|website design(?:er)?|design systems?|visual design(?:er)?|brand(?:ing)? design(?:er)?|creative director|art director|design director|design lead|design manager|design strategist|digital experience design(?:er)?|content design(?:er)?|experience design(?:er)?|interaction design(?:er)?|ux research(?:er)?|marketing design(?:er)?)\b', re.I)
EXCLUDE = re.compile(r'\b(intern(?:ship)?|trainee(?:ship)?|volunteer|unpaid|early career|new grad|graduate program)\b', re.I)

def is_relevant(title):
    return bool(ROLE.search(title or '')) and not EXCLUDE.search(title or '')

def identity(url):
    return hashlib.sha256(url.encode('utf-8')).hexdigest()[:20]

def normalize(title, company, location, url, source, kind='Job'):
    if not url.startswith('https://') or not is_relevant(title) or not canada_eligible(location):
        return None
    return {'id': identity(url), 'title': title.strip(), 'company': company.strip(),
            'location': (location or 'Location not stated').strip(), 'url': url,
            'type': kind, 'source': source, 'deadline': 'Not provided',
            'verification': 'Public ATS listing; Canadian location indicated, work eligibility not independently verified',
            'last_seen': dt.datetime.now(dt.timezone.utc).date().isoformat()}

def greenhouse(session, board):
    r = session.get(f'https://boards-api.greenhouse.io/v1/boards/{board}/jobs', timeout=TIMEOUT)
    r.raise_for_status()
    for j in r.json().get('jobs', []):
        loc = j.get('location') or {}
        yield normalize(j.get('title', ''), board.replace('-', ' ').title(), loc.get('name', ''),
                        j.get('absolute_url', ''), f'Greenhouse / {board}')

def lever(session, company):
    r = session.get(f'https://api.lever.co/v0/postings/{company}?mode=json', timeout=TIMEOUT)
    r.raise_for_status()
    for j in r.json():
        cat = j.get('categories') or {}
        yield normalize(j.get('text', ''), company.replace('-', ' ').title(), cat.get('location', ''),
                        j.get('hostedUrl', ''), f'Lever / {company}', cat.get('commitment', 'Job'))

def main():
    cfg = json.loads(CONFIG.read_text(encoding='utf-8'))
    old = json.loads(OUTPUT.read_text(encoding='utf-8')) if OUTPUT.exists() else []
    old_by_url = {j['url']: j for j in old if j.get('url') and j.get('source', '').startswith(('Greenhouse', 'Lever')) and is_relevant(j.get('title')) and canada_eligible(j.get('location'))}
    session = requests.Session()
    session.headers.update(HEADERS)
    fetched = {}
    successes = 0
    failures = []
    for platform, getter in [('greenhouse', greenhouse), ('lever', lever)]:
        for board in cfg.get(platform, []):
            if not re.fullmatch(r'[a-zA-Z0-9_-]{2,60}', board):
                failures.append(f'{platform}/{board}: invalid board identifier')
                continue
            try:
                for job in getter(session, board):
                    if job:
                        fetched[job['url']] = job
                successes += 1
            except (requests.RequestException, ValueError, KeyError, TypeError) as exc:
                failures.append(f'{platform}/{board}: {type(exc).__name__}: {str(exc)[:120]}')
    if successes == 0:
        print('No sources succeeded; preserving previous feed. ' + '; '.join(failures), file=sys.stderr)
        return 1
    # Keep recent jobs from temporarily failing feeds, but never keep unrelated starter records.
    # Old entries from successfully fetched feeds disappear when the employer removes them.
    failed_sources = {s.split(':', 1)[0] for s in failures}
    for url, old_job in old_by_url.items():
        platform, _, board = old_job['source'].partition(' / ')
        if f'{platform.lower()}/{board}' in failed_sources and url not in fetched:
            fetched[url] = old_job
    fresh = sorted(fetched.values(), key=lambda j: (j['company'], j['title']))
    OUTPUT.write_text(json.dumps(fresh, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    (ROOT / 'feed-status.json').write_text(json.dumps({
        'last_run_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'sources_successful': successes, 'jobs': len(fresh), 'warnings': failures, 'geography': 'Canada-first; Canadian location indicated, eligibility unverified'
    }, indent=2) + '\n', encoding='utf-8')
    print(f'Collected {len(fresh)} relevant roles from {successes} public ATS feeds.')
    if failures:
        print('Warnings: ' + '; '.join(failures), file=sys.stderr)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
