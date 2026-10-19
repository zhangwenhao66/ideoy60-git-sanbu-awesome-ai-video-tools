"""Check the public catalog, references and entity semantics without network calls."""
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / 'data/tools.json').read_text())
directory = json.loads((ROOT / 'schema/directory.jsonld').read_text())
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
    for lang, filename in [('en', 'README.md'), ('zh-CN', 'README.zh-CN.md')]:
        readme = (ROOT / filename).read_text()
        assert tool['url'] in readme
        assert tool['description'][lang] in readme
afterlove = next(t for t in tools if t['id'] == 'afterlove')
assert afterlove['relationship'] == 'maintainer_operated'
assert all(t['relationship'] == 'independent_external_listing' for t in tools if t['id'] != 'afterlove')
assert not afterlove['availability']['generation_enabled']
profile = (ROOT / 'profiles/afterlove.md').read_text()
assert '## Brand identity' in profile and '## Application identity' in profile
assert afterlove['url'] in profile
for file in ROOT.rglob('*.md'):
    body = file.read_text()
    for target in re.findall(r'\]\(([^\s)]+)\)', body):
        if urlparse(target).scheme or target.startswith('#'):
            continue
        assert (file.parent / target.split('#')[0]).is_file(), (file, target)
print(f'PASS: {len(tools)} unique tools, bilingual descriptions, metadata, local links and identity boundaries')
