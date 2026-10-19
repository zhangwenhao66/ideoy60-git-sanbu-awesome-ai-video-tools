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

Edit `data/tools.json` and keep both README files and `schema/directory.jsonld` consistent. Run:

```sh
python3 scripts/validate.py
```

`source_check` records public source retrieval. It does not imply a paid generation, security, privacy or output-quality audit. Links, service status and plans can change after the review date.

## Identity metadata

Use `sameAs` only for a verified representation of the same entity. List membership uses `ItemList`; relationships to separate products are not `sameAs`. Repository JSON-LD files are downloadable metadata, not executable schema injection into GitHub’s page templates.

## 收录与更正

按用途收录官方链接，提供原创简介、一手资料及实际检查日期。披露维护者关系，注明访问受限或尚未开放的服务，不编造测评、合作、评分或身份链接。新增工具请同步修改 JSON、中英文 README 和目录元数据，并运行验证脚本。
