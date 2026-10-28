# GD2027 conference website

24th International Conference on Gas Discharges and their Applications

**12–17 September 2027 · University of Liverpool · United Kingdom**

英文会议官网，包含首页、会议主题、重要日期、投稿与下载、会场信息。采用 HTML / CSS / 少量 JavaScript，支持手机浏览，无第三方运行依赖，可以托管到 GitHub Pages。

## 文件结构

```text
gd2027/
├── index.html                   首页
├── scientific-topics.html       会议主题
├── key-dates.html               重要日期
├── submissions.html             投稿与下载
├── venue.html                   会场信息
├── documents/                   所有会议文件集中放这里
│   ├── gd2027-call-for-abstracts.docx  原始征稿通知（内容未改动）
│   ├── gd2027-conference.ics     日历文件（自动生成）
│   ├── templates/               后续摘要和全文模板
│   └── programme/               后续日程和会议手册
├── assets/                      图片、样式、手机菜单脚本
├── figure/                      用户提供的校园照片，供首页顶部使用
├── content/conference.json      日期、联系人、下载路径等基础信息
└── scripts/build_site.py        生成静态页面的脚本
```

## 在本机预览

在这个仓库目录打开终端，运行：

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

然后浏览器打开 http://127.0.0.1:8000/ 。也可以直接打开 `index.html` 查看（所有页面与图片都使用相对路径）。

## 修改会议资料

1. 编辑 `content/conference.json`：会议日期、联系人、截止日期和下载文件路径均在这里。
2. `null` 表示尚未公布，网站会自动显示待定或待发布。
3. 新文件先放入 `documents/` 对应子文件夹，再在配置中填写路径。例如：

```json
"abstract_deadline": "15 February 2027",
"abstract_template": "documents/templates/gd2027-abstract-template.docx"
```

以上日期只是说明填写方式，并非实际截止日期。

4. 运行以下命令，重新生成五个页面和日历文件：

```bash
python3 scripts/build_site.py
```

5. 提交配置、文档和重新生成的网页。标题、介绍、版块内容在 `scripts/build_site.py` 中修改；样式在 `assets/css/style.css` 中修改。生成脚本会覆盖根目录的五个 HTML 文件。

## 发布到 GitHub Pages

本项目无需安装 npm，也不需要构建服务器。

1. 将所有文件推送到本仓库的 `main` 分支。
2. 打开仓库 **Settings → Pages**。
3. Source 选择 **Deploy from a branch**。
4. Branch 选择 **main**，目录选择 **/ (root)**，点击 **Save**。
5. 等待 GitHub 完成发布，网站地址为 https://xueyongshef.github.io/gd2027/ 。

`.nojekyll` 告诉 GitHub Pages 直接发布这些静态文件。以后推送到 `main`，GitHub Pages 会自动更新网站。

## 内容来源与待补充信息

会议基本资料依据用户提供的 `Call for abstract GD2027.docx`，日期为 **2027 年 9 月 12–17 日**。文稿中的 **24th** 届次原样保留。摘要截止日期、全文截止日期、注册安排、提交方式、模板、具体房间、交通住宿和详细日程尚待确认，网站未编造这些信息。

首页直接展示征稿通知的会议介绍、研究范围、投稿要求、截止日期、模板状态和联系方式，并保留原始 Word 文件下载。模板尚未提供，因此将原稿中的链接占位符显示为待发布状态。

## 图片来源

首页顶部校园照片使用用户提供的 `figure/University-of-Liverpool-Image-Gallery-2.jpg.webp`，图片文件未改动。

`assets/images/liverpool-waterfront.jpg`：**Liverpool skyline from the Mersey Ferry - 2012-05-27.JPG**，作者 **Rept0n1x**，经 Wikimedia Commons 获取，**CC BY-SA 3.0**。

- 来源：https://commons.wikimedia.org/wiki/File:Liverpool_skyline_from_the_Mersey_Ferry_-_2012-05-27.JPG
- 许可：https://creativecommons.org/licenses/by-sa/3.0/
- 网站通过 CSS 裁切和叠加色层以适应版面；图片文件为原始下载文件。署名和许可链接保留在每页页脚。
