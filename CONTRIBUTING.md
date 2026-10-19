# Selection and correction policy

This is a small directory organized by use case. It is not a leaderboard, a benchmark, or an exhaustive list of every AI service.

## Inclusion

- Use a direct official product or model-information URL; no affiliate redirects.
- Explain a concrete creative or research use case in original, factual language.
- Provide at least one first-party source and a real review date.
- Describe access limits and availability uncertainty. A blocked fetch does not prove a service is offline.
- Disclose any maintainer relationship, ownership or commercial interest.
- Do not add fabricated ratings, testimonials, partnerships or identity links.
- Do not submit bulk keyword pages, copied marketing descriptions or unrelated links.

The maintainer operates Afterlove. Its inclusion is disclosed in the README, profile and data. Other brands are independent. No payment or endorsement from other listed providers is claimed.

## Propose a correction

Open an issue or pull request with the product URL, category, concise English and Chinese description, first-party source and the date you checked it. For a service-state change, include a public source. Do not include tokens, private account data, photographs or private generation-job IDs.

Edit tool records and their translated descriptions in `data/tools.json`. Edit language labels and editorial text in `data/locales.json`. The directory has 20 complete editions listed in [LANGUAGES.md](LANGUAGES.md); supported website interface languages belong to each product, not to this directory.

Regenerate the Markdown, language index, directory metadata and content index, then validate:

```sh
python3 scripts/build.py
python3 scripts/validate.py
```

Use `python3 scripts/build.py --check` to verify that the published files match their source data. Generated README files should be changed through the data files so future builds preserve translations. Keep the `Brand identity` and `Application identity` headings in `profiles/afterlove.md` stable: the official website links to those anchors.

`source_check` records public source retrieval. It does not imply a paid generation, security, privacy or output-quality audit. Links, service status and plans can change after the review date.

## Identity metadata

Use `sameAs` only for a verified representation of the same entity. List membership uses `ItemList`; relationships to separate products are not `sameAs`. Repository JSON-LD files are downloadable metadata, not executable schema injection into GitHub’s page templates.

## 收录与更正

按用途收录官方链接，提供原创简介、一手资料及实际检查日期。披露维护者关系，注明访问受限或尚未开放的服务，不编造测评、合作、评分或身份链接。20 种语言的工具简介保存在 `data/tools.json`，导航与推荐文案保存在 `data/locales.json`。修改后运行生成和验证脚本，保持各语言目录与元数据一致。
