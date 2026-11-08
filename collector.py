"""Public-listing collector. Run: pip install -r requirements.txt && python collector.py"""
import json, re, pathlib, datetime, urllib.parse
import requests
from bs4 import BeautifulSoup
BASE='https://internships.jobstoapply.com'
OUT=pathlib.Path(__file__).parent/'jobs.json'
HEADERS={'User-Agent':'JobRadarPersonalResearch/1.0 (public listings; respectful low-frequency checks)'}
def main():
    # Keep existing records when the source is temporarily unavailable.
    old=json.loads(OUT.read_text()) if OUT.exists() else []
    byurl={x['url']:x for x in old}
    response=requests.get(BASE+'/',headers=HEADERS,timeout=25)
    response.raise_for_status()
    soup=BeautifulSoup(response.text,'html.parser')
    links={}
    for a in soup.select('a[href]'):
        href=urllib.parse.urljoin(BASE,a['href'])
        if re.search(r'/opportunities/\d+/',href):
            links[href]=a.get_text(' ',strip=True)
    for url,title in links.items():
        if not title or title.lower() in {'apply','view','details','read more'}:continue
        item=byurl.get(url,{'id':re.search(r'/opportunities/(\d+)/',url).group(1),'source':'Jobs To Apply','url':url})
        item['title']=title
        item['last_seen']=datetime.date.today().isoformat()
        try:
            detail=requests.get(url,headers=HEADERS,timeout=20)
            detail.raise_for_status()
            doc=BeautifulSoup(detail.text,'html.parser')
            text=doc.get_text(' ',strip=True)
            org=re.search(r'(?:Organization|Employer):\s*(.{2,100}?)(?:\s*[·|]\s*|Job type:|Deadline:)',text,re.I)
            deadline=re.search(r'Deadline:\s*([A-Za-z]{3,9}\s+\d{1,2},?\s+20\d{2}|Open)',text,re.I)
            location=re.search(r'Location:\s*(.{2,60}?)(?:\s*(?:Reports to|Deadline:|Job Type:|Contract Type:|Salary:)|\s*[·|]\s*)',text,re.I)
            if org:item['company']=org.group(1).strip()
            if deadline:item['deadline']=deadline.group(1)
            if location:item['location']=location.group(1).strip()
            item['summary']=text[:900]
        except requests.RequestException as exc:
            item['fetch_warning']=str(exc)[:120]
        byurl[url]=item
    if not links:raise RuntimeError('No opportunity links detected; site structure may have changed. Existing data preserved.')
    OUT.write_text(json.dumps(sorted(byurl.values(),key=lambda x:x['id']),ensure_ascii=False,indent=2)+'\n')
    print(f'Collected {len(links)} links; {len(byurl)} stored')
if __name__=='__main__':main()
