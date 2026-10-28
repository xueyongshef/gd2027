#!/usr/bin/env python3
"""Generate a dependency-free, GitHub Pages-ready conference website."""

from datetime import date, datetime, timedelta, timezone
from html import escape
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'content/conference.json').read_text(encoding='utf-8'))


def e(value):
    return escape(str(value), quote=True)


def icon(name, cls=''):
    paths = {
        'calendar': '<rect x="3" y="5" width="18" height="16" rx="1"/><path d="M3 10h18M7 3v5m10-5v5M7 14h3m4 0h3m-10 3h3"/>',
        'pin': '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
        'globe': '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18M5 6.5h14M5 17.5h14"/>',
        'file': '<path d="M5 2h9l5 5v15H5Z"/><path d="M14 2v6h5M8 12h8M8 16h8"/>',
        'menu': '<path d="M3 6h18M3 12h18M3 18h18"/>',
    }
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>'


ARROW = '<span class="arrow" aria-hidden="true">↗</span>'
FORWARD = '<span class="arrow" aria-hidden="true">→</span>'
LOGO = '<svg class="brand-symbol" viewBox="0 0 48 48" fill="none" aria-hidden="true"><ellipse cx="24" cy="24" rx="22" ry="8.5" transform="rotate(-45 24 24)" stroke="currentColor" stroke-width="1.3"/><ellipse cx="24" cy="24" rx="22" ry="8.5" transform="rotate(45 24 24)" stroke="currentColor" stroke-width="1.3"/><circle cx="24" cy="24" r="3" fill="currentColor"/></svg>'
NAV = [('index.html', 'Home'), ('scientific-topics.html', 'Scientific topics'), ('key-dates.html', 'Key dates'), ('submissions.html', 'Abstracts & downloads'), ('venue.html', 'Venue')]
TOPICS = [
    ('Gas discharges & plasmas', 'Gas discharges from low to high pressure, spanning thermal and non-thermal plasmas.'),
    ('Pulsed-power technology', 'Gas discharges and their applications in pulsed-power technology.'),
    ('Light sources', 'Gas discharges and plasma applications in light sources.'),
    ('Switchgear', 'Gas discharges and their applications in switchgear.'),
    ('Environmental technologies', 'Plasma and gas-discharge applications in environmental technologies.'),
    ('Medical applications', 'Gas discharges and plasmas for medical applications.'),
]


def header(active):
    links = ''
    for url, label in NAV:
        current = ' aria-current="page"' if url == active else ''
        links += f'<a href="{url}"{current}>{label}</a>'
    return f'''<a class="skip-link" href="#main">Skip to main content</a>
<div class="utility"><div class="wrap"><p>{e(DATA['university'])} <span class="place">&nbsp; / &nbsp; {e(DATA['country'])}</span></p><p>{e(DATA['dates'])}</p></div></div>
<header class="site-header"><div class="wrap header-inner">
  <a class="brand" href="index.html" aria-label="GD2027 home">{LOGO}<div><div class="brand-word">GD<span>2027</span></div><span class="brand-tag">GAS DISCHARGES & APPLICATIONS</span></div></a>
  <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu {icon('menu')}</button>
  <nav class="site-nav" id="site-nav" aria-label="Main navigation">{links}</nav>
</div></header>'''


def footer():
    return f'''<section class="contact-strip" aria-labelledby="contact-heading"><div class="wrap"><div><h2 id="contact-heading">Let’s stay connected.</h2><p>For conference enquiries, please contact the organising team.</p></div><a href="mailto:{e(DATA['email'])}">{e(DATA['email'])} {ARROW}</a></div></section>
<footer class="site-footer"><div class="wrap">
  <div class="footer-main"><div><div class="footer-title">GD2027</div><p>{e(DATA['edition'])} {e(DATA['title'])}<br>{e(DATA['dates'])} · {e(DATA['city'])}, {e(DATA['country'])}</p></div><nav class="footer-links" aria-label="Footer navigation"><a href="submissions.html">Abstracts & downloads</a><a href="key-dates.html">Key dates</a><a href="venue.html">Venue</a></nav></div>
  <div class="footer-bottom"><p>Hosted by the {e(DATA['department'])}, {e(DATA['university'])}.</p><p>Waterfront photograph: <a href="https://commons.wikimedia.org/wiki/File:Liverpool_skyline_from_the_Mersey_Ferry_-_2012-05-27.JPG" target="_blank" rel="noopener noreferrer">Rept0n1x / Wikimedia Commons</a> · <a href="https://creativecommons.org/licenses/by-sa/3.0/" target="_blank" rel="noopener noreferrer">CC BY-SA 3.0</a></p></div>
</div></footer>'''


def page(filename, title, description, main):
    structured = {
        '@context': 'https://schema.org', '@type': 'Event',
        'name': f"{DATA['edition']} {DATA['title']} ({DATA['short_name']})",
        'startDate': DATA['start_date'], 'endDate': DATA['end_date'],
        'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode',
        'location': {'@type': 'Place', 'name': DATA['university'], 'address': {'@type': 'PostalAddress', 'addressLocality': DATA['city'], 'addressCountry': 'GB'}},
        'organizer': {'@type': 'Organization', 'name': f"{DATA['department']}, {DATA['university']}", 'email': DATA['email']},
        'description': f"{DATA['title']}. {DATA['dates']}, {DATA['city']}, {DATA['country']}.",
    }
    structured_json = json.dumps(structured, ensure_ascii=False).replace('<', '\\u003c')
    style_version = hashlib.sha256((ROOT / 'assets/css/style.css').read_bytes()).hexdigest()[:10]
    return f'''<!doctype html>
<html lang="en-GB"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} | GD2027 · Liverpool</title><meta name="description" content="{e(description)}">
<meta name="theme-color" content="#112e3b"><meta property="og:title" content="{e(title)} | GD2027"><meta property="og:description" content="{e(description)}"><meta property="og:type" content="website">
<link rel="icon" href="assets/images/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/css/style.css?v={style_version}"><script src="assets/js/main.js" defer></script>
<script type="application/ld+json">{structured_json}</script>
<noscript><style>@media(max-width:800px){{.site-header{{position:static}}.header-inner{{flex-wrap:wrap;padding-block:18px}}.menu-toggle{{display:none}}.site-nav{{display:flex;position:static;flex-direction:row;flex-wrap:wrap;box-shadow:none;padding:0;border:0}}.site-nav a{{padding:8px 10px}}}}</style></noscript>
</head><body>{header(filename)}<main id="main">{main}</main>{footer()}</body></html>
'''


def page_heading(label, heading, intro):
    return f'''<section class="page-heading"><div class="wrap"><div class="breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span>{e(label)}</div><span class="eyebrow">{e(label)}</span><h1>{heading}</h1><p class="intro">{intro}</p></div></section>'''


def deadline(key):
    return e(DATA.get(key) or 'To be confirmed')


def status(key):
    value = DATA.get(key)
    return f'<span class="status{" confirmed" if value else ""}">{e(value or "To be confirmed")}</span>'


def topic_keywords():
    return ''.join(f'<li>{e(name)}</li>' for name, _ in TOPICS)


def local_guide():
    links = ''.join(
        f'<li><a href="{e(attraction["url"])}" target="_blank" rel="noopener noreferrer"><span><strong>{e(attraction["title"])}</strong><small>{e(attraction["description"])}</small></span>{ARROW}</a></li>'
        for attraction in DATA['local_attractions']
    )
    return f'''<aside class="abstract-note local-guide" aria-labelledby="local-guide-heading"><span class="eyebrow">Get to know your hosts</span><h3 id="local-guide-heading">Our department<br>& Liverpool.</h3><p>Meet our host department and discover places to explore during your visit to Liverpool.</p><a class="button" href="{e(DATA['department_about_url'])}" target="_blank" rel="noopener noreferrer">About our department {ARROW}</a><a class="text-link guide-research" href="{e(DATA['department_research_url'])}" target="_blank" rel="noopener noreferrer">Explore our research {ARROW}</a><div class="guide-city"><h4>Explore Liverpool</h4><ul class="guide-links" aria-label="Liverpool visitor attractions">{links}</ul></div></aside>'''


def home():
    templates = ''.join([
        download_row('abstract_template', 'Abstract template', 'The conference abstract format'),
        download_row('full_paper_template', 'Full paper template', 'The conference paper format'),
    ])
    return f'''<section class="hero" aria-labelledby="hero-heading">
  <img class="hero-image" src="figure/University-of-Liverpool-Image-Gallery-2.jpg.webp" alt="Red-brick University of Liverpool campus buildings overlooking a green courtyard" fetchpriority="high" width="2200" height="1366">
  <div class="wrap"><span class="eyebrow">{e(DATA['edition'])} International Conference · GD2027</span><h1 id="hero-heading">Advancing gas<br>discharge <em>science.</em></h1>
  <p class="hero-title">{e(DATA['title'])}</p>
  <div class="hero-meta"><span>{icon('calendar')}{e(DATA['dates'])}</span><span>{icon('pin')}{e(DATA['city'])}, {e(DATA['country'])}</span></div>
  <div class="hero-actions"><a class="button" href="#call-for-abstracts">Call for abstracts <span class="arrow" aria-hidden="true">↓</span></a><a class="text-link" href="{e(DATA['call_for_abstracts'])}" download>Download conference notice {ARROW}</a></div>
  <div class="hero-keywords"><span class="eyebrow">Scientific keywords</span><ul aria-label="Scientific keywords">{topic_keywords()}</ul></div></div>
</section>
<section class="facts" aria-label="Conference at a glance"><div class="wrap">
  <div class="fact">{icon('calendar')}<div><span class="label">Save the date</span><strong>{e(DATA['dates'])}</strong></div></div>
  <div class="fact">{icon('pin')}<div><span class="label">Our host</span><strong>{e(DATA['university'])}</strong></div></div>
  <div class="fact">{icon('globe')}<div><span class="label">An international meeting</span><strong>Gas discharges & their applications</strong></div></div>
</div></section>
<section class="section home-cfp" id="call-for-abstracts" aria-labelledby="cfp-heading"><div class="wrap welcome-grid">
  <article class="welcome-copy"><span class="eyebrow red">Welcome to GD2027</span><h2 id="cfp-heading">Call for Abstracts</h2>
  <div class="body-copy"><p>We are pleased to invite you to participate in the {e(DATA['edition'])} {e(DATA['title'])} ({e(DATA['short_name'])}), which will be held in {e(DATA['city'])}, {e(DATA['country'])}, {e(DATA['dates'])}.</p>
  <p>The conference will be hosted by the {e(DATA['department'])} at the {e(DATA['university'])}.</p>
  <p>The conference will bring together researchers and practitioners working on gas discharges and their applications. Topics span low- to high-pressure plasmas and thermal to non-thermal plasmas, with applications including pulsed-power technology, light sources, switchgear, environmental technologies and medicine.</p>
  <h3 class="cfp-subheading">Abstract submissions</h3><p>We welcome abstracts on gas discharges and their applications. Submissions should follow the conference abstract template, which will be available below once published.</p>
  <dl class="cfp-deadlines"><div><dt>Abstract submission deadline</dt><dd>{deadline('abstract_deadline')}</dd></div><div><dt>Full paper submission deadline</dt><dd>{deadline('full_paper_deadline')}</dd></div><div><dt>Registration deadline</dt><dd>{e(DATA.get('registration_deadline') or 'To be announced in due course.')}</dd></div></dl>
  <h3 class="cfp-subheading">Submission Templates</h3><div class="download-list">{templates}</div>
  <h3 class="cfp-subheading">Contact</h3><p>If you have any queries, please contact <a href="mailto:{e(DATA['email'])}">{e(DATA['email'])}</a>.</p></div>
  </article>
  {local_guide()}
</div></section>
<section class="city-band" aria-labelledby="city-heading"><img class="city-image" src="assets/images/liverpool-waterfront.jpg" alt="The Liverpool skyline across the River Mersey" loading="lazy" width="4320" height="2430"><div class="city-copy"><span class="eyebrow">Liverpool · United Kingdom</span><h2 id="city-heading">See you in Liverpool.</h2><p>Join us at the {e(DATA['university'])} for an international meeting of researchers and practitioners in gas discharges and their applications.</p><a class="text-link" href="venue.html">Discover the venue {FORWARD}</a></div></section>'''


def scientific_topics():
    heading = page_heading('Scientific topics', 'From fundamental science<br>to practical applications.', 'GD2027 explores gas discharges across pressure regimes, from thermal to non-thermal plasmas, and the technologies they make possible.')
    details = ''.join(f'<article class="topic-detail"><span class="topic-number">{i:02d}</span><div><h2>{name}</h2><p>{description}</p></div></article>' for i, (name, description) in enumerate(TOPICS, 1))
    return heading + f'''<section class="page-content"><div class="wrap"><div class="topic-details">{details}</div><p class="bottom-note">These areas reflect the conference call for abstracts. Detailed programme information will be announced in due course.</p><a class="button" href="submissions.html">Abstract information {ARROW}</a></div></section>'''


def key_dates():
    heading = page_heading('Key dates', 'Your dates for GD2027.', 'Keep track of the conference and submission milestones. Dates that have not yet been announced are clearly marked below.')
    milestones = [
        ('Abstract submission', 'Deadline for conference abstracts.', status('abstract_deadline')),
        ('Full paper submission', 'Deadline for full conference papers.', status('full_paper_deadline')),
        ('Registration', 'Registration deadline to be announced in due course.', status('registration_deadline')),
        ('GD2027 conference', f"{e(DATA['university'])}, {e(DATA['city'])}, {e(DATA['country'])}.", f'<span class="status confirmed">{e(DATA["dates"])}</span>'),
    ]
    rows = ''.join(f'<li class="date-item"><span class="date-index">{i:02d}</span><div><h2>{title}</h2><p>{description}</p></div>{badge}</li>' for i, (title, description, badge) in enumerate(milestones, 1))
    return heading + f'''<section class="page-content"><div class="wrap content-grid"><div><ol class="date-list">{rows}</ol><div class="info-note">Submission and registration deadlines will be updated here when confirmed by the organisers.</div></div><aside class="detail-panel"><span class="eyebrow red">Save the date</span><h2>Meet us<br>in Liverpool.</h2><div class="detail-row"><span class="label">Conference dates</span>{e(DATA['dates'])}</div><div class="detail-row"><span class="label">Location</span>{e(DATA['university'])}<br>{e(DATA['city'])}, {e(DATA['country'])}</div><a class="button light" href="documents/gd2027-conference.ics" download>Add to calendar {ARROW}</a></aside></div></section>'''


def download_row(key, title, explanation):
    path = DATA.get(key)
    if path:
        resolved = ROOT / path
        if not resolved.is_file() or not resolved.resolve().is_relative_to((ROOT / 'documents').resolve()):
            raise ValueError(f'Download must exist inside documents/: {path}')
        size = max(1, round(resolved.stat().st_size / 1024))
        kind = resolved.suffix.lstrip('.').upper()
        description = f'{e(explanation)} · {kind} · {size} KB'
        action = f'<a class="text-link" href="{e(path)}" download aria-label="Download {e(title)}">Download <span class="arrow" aria-hidden="true">↓</span></a>'
    else:
        description = e(explanation)
        action = '<span class="status">To be published</span>'
    return f'<div class="download-row"><div class="download-icon">{icon("file", "file-icon")}<div><h3>{e(title)}</h3><p>{description}</p></div></div>{action}</div>'


def submissions():
    heading = page_heading('Abstracts & downloads', 'Share your research.', 'We welcome abstracts on gas discharges and their applications. Read the call for abstracts and find conference documents below.')
    downloads = ''.join([
        download_row('call_for_abstracts', 'Call for abstracts', 'Conference invitation and overview'),
        download_row('abstract_template', 'Abstract template', 'The conference abstract format'),
        download_row('full_paper_template', 'Full paper template', 'The conference paper format'),
    ])
    return heading + f'''<section class="page-content"><div class="wrap content-grid"><div><h2>Conference documents</h2><p>Submissions should follow the conference abstract template. The abstract and full paper templates will be made available here once published.</p><div class="download-list">{downloads}</div>
  <div class="steps"><h2>Preparing your submission</h2><div class="step"><span class="step-number">1</span><div><h3>Read the call for abstracts</h3><p>Download the conference notice for the scientific scope, dates and contact details.</p></div></div><div class="step"><span class="step-number">2</span><div><h3>Use the conference template</h3><p>Prepare your abstract using the official template when it becomes available.</p></div></div><div class="step"><span class="step-number">3</span><div><h3>Check the submission instructions</h3><p>The submission method and final deadlines will be published here when confirmed.</p></div></div></div>
  </div><aside><div class="detail-panel"><span class="eyebrow red">Submission milestones</span><h3>Plan your contribution.</h3><div class="detail-row"><span class="label">Abstract deadline</span>{deadline('abstract_deadline')}</div><div class="detail-row"><span class="label">Full paper deadline</span>{deadline('full_paper_deadline')}</div><div class="detail-row"><span class="label">Registration deadline</span>{e(DATA.get('registration_deadline') or 'To be announced')}</div><a class="button light" href="key-dates.html">All key dates {FORWARD}</a></div><div class="info-note">Questions about the conference?<br><a href="mailto:{e(DATA['email'])}">Contact the organising team</a>.</div></aside>
</div></section>'''


def venue():
    heading = page_heading('Venue', 'Liverpool.<br>A place to connect.', f"GD2027 will be hosted by the {e(DATA['department'])} at the {e(DATA['university'])}, {e(DATA['city'])}, {e(DATA['country'])}.")
    return heading + f'''<section class="page-content"><div class="wrap"><figure class="venue-photo"><img src="assets/images/liverpool-waterfront.jpg" alt="Liverpool waterfront, including the Royal Liver Building, viewed from the Mersey" width="4320" height="2430"><figcaption>Liverpool waterfront. Photograph by <a href="https://commons.wikimedia.org/wiki/File:Liverpool_skyline_from_the_Mersey_Ferry_-_2012-05-27.JPG" target="_blank" rel="noopener noreferrer">Rept0n1x / Wikimedia Commons</a>, <a href="https://creativecommons.org/licenses/by-sa/3.0/" target="_blank" rel="noopener noreferrer">CC BY-SA 3.0</a>.</figcaption></figure>
  <div class="content-grid"><div class="venue-copy"><span class="eyebrow red">Our host</span><h2>{e(DATA['university'])}</h2><p>We look forward to welcoming researchers and practitioners to {e(DATA['city'])} for the {e(DATA['edition'])} {e(DATA['title'])}.</p><p>The conference will take place from {e(DATA['dates'])} and will be hosted by the {e(DATA['department'])}.</p><h3>Planning your visit</h3><p>Detailed information about conference rooms, travel and accommodation will be published here as arrangements are confirmed.</p><a class="button light" href="{e(DATA['map_url'])}" target="_blank" rel="noopener noreferrer">View the university on Google Maps {ARROW}</a></div>
  <aside class="detail-panel"><span class="eyebrow red">At a glance</span><div class="detail-row"><span class="label">When</span>{e(DATA['dates'])}</div><div class="detail-row"><span class="label">Host institution</span>{e(DATA['university'])}</div><div class="detail-row"><span class="label">Host department</span>{e(DATA['department'])}</div><div class="detail-row"><span class="label">City</span>{e(DATA['city'])}, {e(DATA['country'])}</div><div class="detail-row"><span class="label">Enquiries</span><a href="mailto:{e(DATA['email'])}">{e(DATA['email'])}</a></div></aside></div>
</div></section>'''


def calendar():
    start = date.fromisoformat(DATA['start_date'])
    end_exclusive = date.fromisoformat(DATA['end_date']) + timedelta(days=1)
    def ics_escape(value):
        return str(value).replace('\\', '\\\\').replace('\n', '\\n').replace(',', '\\,').replace(';', '\\;')
    lines = [
        'BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//GD2027//Conference//EN', 'CALSCALE:GREGORIAN',
        'BEGIN:VEVENT', 'UID:gd2027-conference@xueyongshef.github.io',
        'DTSTAMP:' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'),
        'DTSTART;VALUE=DATE:' + start.strftime('%Y%m%d'), 'DTEND;VALUE=DATE:' + end_exclusive.strftime('%Y%m%d'),
        'SUMMARY:' + ics_escape(DATA['short_name'] + ' — ' + DATA['title']),
        'LOCATION:' + ics_escape(f"{DATA['university']}, {DATA['city']}, {DATA['country']}"),
        'DESCRIPTION:' + ics_escape(f"{DATA['edition']} {DATA['title']}. Hosted by the {DATA['department']}. Conference enquiries: {DATA['email']}. Detailed programme to be announced."),
        'END:VEVENT', 'END:VCALENDAR',
    ]
    folded = []
    for line in lines:
        current = ''
        for char in line:
            if len((current + char).encode('utf-8')) > 73:
                folded.append(current)
                current = ' '
            current += char
        folded.append(current)
    (ROOT / 'documents/gd2027-conference.ics').write_bytes(('\r\n'.join(folded) + '\r\n').encode('utf-8'))


def main():
    pages = [
        ('index.html', 'Gas Discharges and their Applications', 'GD2027: the 24th International Conference on Gas Discharges and their Applications, 12–17 September 2027, University of Liverpool, United Kingdom.', home()),
        ('scientific-topics.html', 'Scientific topics', 'Explore the scientific scope of GD2027: gas discharges, thermal and non-thermal plasmas, pulsed power, light sources, switchgear, environmental and medical applications.', scientific_topics()),
        ('key-dates.html', 'Key dates', 'Conference dates and submission milestones for GD2027, Liverpool, 12–17 September 2027. Abstract, full paper and registration deadlines will be confirmed.', key_dates()),
        ('submissions.html', 'Abstracts & downloads', 'Download the GD2027 call for abstracts and find the latest information on abstract and full paper templates, deadlines and submissions.', submissions()),
        ('venue.html', 'Venue', 'GD2027 at the University of Liverpool, hosted by the Department of Electrical Engineering and Electronics, 12–17 September 2027.', venue()),
    ]
    for filename, title, description, content in pages:
        (ROOT / filename).write_text(page(filename, title, description, content), encoding='utf-8')
    calendar()
    # A clean deployment folder excludes source scripts, Git metadata and notes.
    if '--publish-dir' in sys.argv:
        dest = ROOT / '_site'
        dest.mkdir(exist_ok=True)
        for filename, *_ in pages:
            shutil.copy2(ROOT / filename, dest / filename)
        for folder in ['assets', 'documents', 'figure']:
            shutil.copytree(ROOT / folder, dest / folder, dirs_exist_ok=True, ignore=shutil.ignore_patterns('README.md', '.gitkeep'))
        (dest / '.nojekyll').touch()
    print(f'Built {len(pages)} pages and the conference calendar.')


if __name__ == '__main__':
    main()
