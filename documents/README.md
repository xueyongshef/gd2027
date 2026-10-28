# 会议文件

所有会议文档集中存放在本文件夹，便于后续维护和下载。

- `gd2027-call-for-abstracts.docx`：用户提供的原始 Call for Abstracts，内容未改动。
- `gd2027-conference.ics`：由网站脚本生成的会议日历，覆盖 2027 年 9 月 12–17 日。
- `templates/`：后续放摘要模板、全文模板。
- `programme/`：后续放会议日程、会议手册。

需要在网站显示的新下载文件，还应在 `content/conference.json` 中填写相对路径，再运行 `python3 scripts/build_site.py`。

这个文件夹中的资料会随会议网站一起公开发布。
