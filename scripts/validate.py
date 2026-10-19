"""Check the public catalog, references and entity semantics without network calls."""
import json
import re
from pathlib import Path
from urllib.parse import urlparse
from build import render

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / 'data/tools.json').read_text(encoding='utf-8'))
directory = json.loads((ROOT / 'schema/directory.jsonld').read_text(encoding='utf-8'))
locales = json.loads((ROOT / 'data/locales.json').read_text(encoding='utf-8'))['languages']
languages = [l['code'] for l in locales]
assert len(languages) == len(set(languages)) == 20
assert set(catalog['languages']) == set(directory['inLanguage']) == set(languages)
assert {x['inLanguage'] for x in directory['workTranslation']} == set(languages) - {'en'}
assert len({l['file'] for l in locales}) == len(locales)
tools = catalog['tools']
assert len({t['id'] for t in tools}) == len(tools)
assert len({t['url'] for t in tools}) == len(tools)
assert directory['mainEntity']['numberOfItems'] == len(tools)
assert 'sameAs' not in json.dumps(directory), 'A directory must not merge separate tool identities'
assert {x['item']['url'] for x in directory['mainEntity']['itemListElement']} == {t['url'] for t in tools}
for tool in tools:
    assert tool['sources']
    for url in [tool['url'], *tool['sources']]:
        parsed = urlparse(url)
        assert parsed.scheme == 'https' and parsed.hostname
    assert re.fullmatch(r'\d{4}-\d{2}-\d{2}', tool['last_reviewed'])
    assert tool['source_check']['result'] in ['retrieved', 'access_limited']
    assert set(tool['description']) == set(languages)
    for locale in locales:
        lang, filename = locale['code'], locale['file']
        readme = (ROOT / filename).read_text(encoding='utf-8')
        assert tool['url'] in readme
        assert tool['description'][lang] in readme
        assert len(tool['description'][lang].strip()) > 5
        assert locale['featured_copy'] in readme
        assert locale['availability'] in readme
        assert len(locale['categories']) == 5
        assert readme.count('<a id=') == 5
        if locale['direction'] == 'rtl':
            assert readme.startswith('<div dir="rtl">')
        for alternate in locales:
            if alternate['code'] != lang:
                assert f"]({alternate['file']})" in readme
afterlove = next(t for t in tools if t['id'] == 'afterlove')
assert afterlove['relationship'] == 'maintainer_operated'
assert all(t['relationship'] == 'independent_external_listing' for t in tools if t['id'] != 'afterlove')
assert not afterlove['availability']['generation_enabled']
profile = (ROOT / 'profiles/afterlove.md').read_text(encoding='utf-8')
assert '## Brand identity' in profile and '## Application identity' in profile
assert afterlove['url'] in profile
for file in ROOT.rglob('*.md'):
    body = file.read_text(encoding='utf-8')
    assert '\ufffd' not in body, f'Invalid replacement character in {file}'
    for target in re.findall(r'\]\(([^\s)]+)\)', body):
        if urlparse(target).scheme or target.startswith('#'):
            continue
        assert (file.parent / target.split('#')[0]).is_file(), (file, target)
for filename, content in render().items():
    assert (ROOT / filename).read_text(encoding='utf-8') == content, f'Stale generated file: {filename}'
print(f'PASS: {len(tools)} tools, {len(locales)} full languages, {len(tools) * len(locales)} descriptions, navigation, RTL, metadata and identity anchors')
