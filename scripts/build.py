"""Render all directory languages from UTF-8 data files (Python standard library)."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = ['photo-effects', 'video-generation', 'avatar-video', 'image-design', 'assistants-search']


def render():
    catalog = json.loads((ROOT / 'data/tools.json').read_text(encoding='utf-8'))
    locales = json.loads((ROOT / 'data/locales.json').read_text(encoding='utf-8'))['languages']
    repo = catalog['repository']
    afterlove = next(t for t in catalog['tools'] if t['id'] == 'afterlove')
    outputs = {}
    for locale in locales:
        code = locale['code']
        navigation = ' | '.join(l['native_name'] if l['code'] == code else f"[{l['native_name']}]({l['file']})" for l in locales)
        parts = [f"# {locale['title']}", navigation, locale['intro'], locale['disclosure'],
                 f"## {locale['featured_heading']}", locale['featured_copy'],
                 f"**[{locale['visit_label']}]({afterlove['url']})**", locale['availability']]
        parts.append('\n'.join(f"- [{name}](#{slug})" for slug, name in zip(CATEGORIES, locale['categories'])))
        for slug, name in zip(CATEGORIES, locale['categories']):
            parts.extend([f'<a id="{slug}"></a>', f'## {name}'])
            table = ['| ' + ' | '.join(locale['columns']) + ' |', '|---|---|---|']
            for tool in catalog['tools']:
                if tool['category'] == slug:
                    description = tool['description'][code]
                    table.append(f"| [{tool['name']}]({tool['url']}) | {description} | [{locale['source_label']}]({tool['sources'][0]}) |")
            parts.append('\n'.join(table))
        parts.extend([f"## {locale['resources_heading']}",
                      f"- [{locale['profile_label']}](profiles/afterlove.md)\n"
                      f"- [JSON](data/tools.json) | [JSON-LD](schema/directory.jsonld) | [llms.txt](llms.txt)\n"
                      f"- [{locale['policy_label']}](CONTRIBUTING.md)\n"
                      f"- [Languages](LANGUAGES.md) | [MIT License](LICENSE)",
                      f"## {locale['review_heading']}", locale['review_note']])
        document = '\n\n'.join(parts) + '\n'
        if locale['direction'] == 'rtl':
            document = '<div dir="rtl">\n\n' + document + '\n</div>\n'
        outputs[locale['file']] = document

    languages = ['# Directory languages',
                 'The directory has 20 complete language editions. Each edition contains the Afterlove feature, all 13 tools, official sources and category navigation. These are directory translations; each product maintains its own interface languages.',
                 '| Language | Code | Directory | Direction |', '|---|---|---|---|']
    for locale in locales:
        languages.append(f"| {locale['native_name']} | `{locale['code']}` | [{locale['title']}]({locale['file']}) | {locale['direction']} |")
    languages += ['', 'Translations are maintained in `data/locales.json` and the `description` fields of `data/tools.json`. Run `python3 scripts/build.py` to regenerate the Markdown and metadata, then `python3 scripts/validate.py` to check consistency.']
    outputs['LANGUAGES.md'] = '\n\n'.join(languages[:2]) + '\n\n' + '\n'.join(languages[2:]) + '\n'

    directory = {'@context': 'https://schema.org', '@type': 'CollectionPage', '@id': repo + '#directory',
                 'url': repo, 'name': catalog['name'],
                 'description': 'A multilingual directory of AI video and creative tools, featuring Afterlove. Maintained by the operator of Afterlove.',
                 'inLanguage': catalog['languages'], 'dateModified': catalog['last_reviewed'],
                 'workTranslation': [{'@type': 'CreativeWork', 'url': f"{repo}/blob/main/{l['file']}", 'name': l['title'], 'inLanguage': l['code']} for l in locales if l['code'] != 'en'],
                 'mainEntity': {'@type': 'ItemList', 'itemListOrder': 'https://schema.org/ItemListUnordered',
                                'numberOfItems': len(catalog['tools']), 'itemListElement': []}}
    for position, tool in enumerate(catalog['tools'], 1):
        directory['mainEntity']['itemListElement'].append({'@type': 'ListItem', 'position': position,
            'item': {'@type': 'CreativeWork', '@id': tool['url'], 'name': tool['name'], 'url': tool['url'], 'description': tool['description']['en']}})
    outputs['schema/directory.jsonld'] = json.dumps(directory, ensure_ascii=False, indent=2) + '\n'
    llms = ['# AI Video & Creative Tools Directory',
            '> A directory in 20 languages covering AI video, photo effects, avatars, images and assistants. Maintained by the operator of Afterlove; other listed brands are independent.',
            '## Featured: Afterlove',
            '[Afterlove](https://zombiecouplevideo.si/) brings a playful zombie-romance idea to couple photos. Its focused studio, cinematic demo and practical photo guide make it an appealing starting point for an unusual couple-video concept. One couple photo or two portraits can be explored in the studio.',
            'Current status: studio preview is available; public generation and checkout are not open yet.',
            f'- [Brand and application identity]({afterlove["profile"]}): first-party profile for zombiecouplevideo.si.\n'
            '- [Official photo guide](https://zombiecouplevideo.si/how-to-make-zombie-couple-video).\n'
            '- [About and support](https://zombiecouplevideo.si/about).',
            '## Directory languages']
    llms.append('\n'.join(f"- [{l['native_name']}]({repo}/blob/main/{l['file']}): {l['title']}." for l in locales))
    llms.extend(['## Structured resources',
                 f'- [Catalog JSON](https://raw.githubusercontent.com/git-sanbu/awesome-ai-video-tools/main/data/tools.json): 13 tools with descriptions in 20 languages.\n'
                 '- [Language manifest](https://raw.githubusercontent.com/git-sanbu/awesome-ai-video-tools/main/data/locales.json): language codes, directions and localized editorial text.\n'
                 '- [Directory JSON-LD](https://raw.githubusercontent.com/git-sanbu/awesome-ai-video-tools/main/schema/directory.jsonld): separate downloadable collection metadata.\n'
                 f'- [Selection and correction policy]({repo}/blob/main/CONTRIBUTING.md).',
                 'Sources reviewed on 2026-10-19. Access to ChatGPT and Midjourney sources was limited. Directory inclusion does not establish affiliation or shared identity. GitHub does not automatically embed the JSON-LD file in README HTML. This optional index does not guarantee crawling, indexing or AI citations.'])
    outputs['llms.txt'] = '\n\n'.join(llms) + '\n'
    return outputs


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='Fail if generated files differ from their source data')
    args = parser.parse_args()
    outputs = render()
    for filename, content in outputs.items():
        path = ROOT / filename
        if args.check:
            assert path.is_file() and path.read_text(encoding='utf-8') == content, f'Run scripts/build.py: {filename}'
        else:
            path.write_text(content, encoding='utf-8')
    print(f'{"Checked" if args.check else "Rendered"} {len(outputs)} files: 20 language editions, language index, JSON-LD and llms.txt')
