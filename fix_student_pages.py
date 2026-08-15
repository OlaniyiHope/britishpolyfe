from pathlib import Path
import re

base = Path(r"c:\Users\User\Desktop\edu\student")

style = '''
        body {
            margin: 0;
            background: #edf4ff;
            padding: 0;
        }

        .student-shell {
            display: flex;
            min-height: 100vh;
            width: 100%;
            background: #edf4ff;
        }

        .sidebar {
            width: 260px;
            background: linear-gradient(180deg, #0a1e3c 0%, #123d76 100%);
            color: #ffffff;
            padding: 22px 16px 18px;
            flex-shrink: 0;
            box-shadow: 8px 0 30px rgba(10, 30, 60, 0.14);
        }

        .sidebar .brand {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 1.4rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            padding-bottom: 18px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.14);
        }

        .sidebar .brand span {
            color: #a9c7ff;
        }

        .sidebar .nav-section {
            margin-top: 22px;
        }

        .sidebar .nav-label {
            font-size: 0.65rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: rgba(255, 255, 255, 0.55);
            padding: 0 12px 8px;
            font-weight: 700;
        }

        .sidebar .nav-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 11px 12px;
            margin-bottom: 8px;
            border-radius: 12px;
            color: rgba(255, 255, 255, 0.75);
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9rem;
            transition: 0.15s ease;
        }

        .sidebar .nav-item:hover,
        .sidebar .nav-item.active {
            background: rgba(255, 255, 255, 0.12);
            color: #ffffff;
        }

        .sidebar .nav-item .icon {
            width: 30px;
            text-align: center;
            font-size: 0.95rem;
            color: #cfe0ff;
        }

        .sidebar .nav-item .badge {
            margin-left: auto;
            background: #1a5cff;
            color: #fff;
            border-radius: 999px;
            padding: 3px 8px;
            font-size: 0.6rem;
            font-weight: 700;
        }

        .content-panel {
            flex: 1;
            padding: 24px;
            background: #f3f8ff;
        }

        .content-panel > * {
            width: 100%;
        }
'''

sidebar_html = '''
<div class="student-shell">
    <aside class="sidebar">
        <div class="brand">British Poly <span>Student</span></div>

        <div class="nav-section">
            <div class="nav-label">Overview</div>
            <a class="nav-item active" href="#"><span class="icon"><i class="fa-solid fa-grid-2"></i></span>Dashboard <span class="badge">Live</span></a>
            <a class="nav-item" href="#"><span class="icon"><i class="fa-solid fa-clipboard-list"></i></span>Courses</a>
            <a class="nav-item" href="#"><span class="icon"><i class="fa-solid fa-wallet"></i></span>Fees</a>
            <a class="nav-item" href="#"><span class="icon"><i class="fa-solid fa-calendar-days"></i></span>Timetable</a>
        </div>

        <div class="nav-section">
            <div class="nav-label">Academic</div>
            <a class="nav-item" href="#"><span class="icon"><i class="fa-solid fa-book-open"></i></span>Results</a>
            <a class="nav-item" href="#"><span class="icon"><i class="fa-solid fa-file-lines"></i></span>Registration</a>
            <a class="nav-item" href="#"><span class="icon"><i class="fa-solid fa-chalkboard-user"></i></span>Class Info</a>
            <a class="nav-item" href="#"><span class="icon"><i class="fa-solid fa-briefcase"></i></span>Placement</a>
        </div>

        <div class="nav-section">
            <div class="nav-label">Support</div>
            <a class="nav-item" href="#"><span class="icon"><i class="fa-solid fa-bell"></i></span>Notice Board</a>
            <a class="nav-item" href="#"><span class="icon"><i class="fa-solid fa-circle-user"></i></span>Profile</a>
        </div>
    </aside>
    <main class="content-panel">
'''
close_html = '''
    </main>
</div>
'''

for p in sorted(base.glob("*.html")):
    text = p.read_text(encoding="utf-8", errors="ignore")
    if "<aside" not in text.lower() and 'class="sidebar"' not in text.lower():
        if "</head>" in text:
            text = text.replace("</head>", "<style>" + style + "</style>\n</head>", 1)
        elif "</style>" in text:
            text = text.replace("</style>", style + "\n</style>", 1)
        else:
            text = "<style>" + style + "</style>\n" + text

        if "<body>" in text:
            text = text.replace("<body>", "<body>\n" + sidebar_html, 1)
        else:
            text = text.replace("<html>", "<html>\n<body>\n" + sidebar_html, 1)

        if "</body>" in text:
            text = text.replace("</body>", close_html + "\n</body>", 1)
        else:
            text += close_html

        p.write_text(text, encoding="utf-8")

    match = re.search(r"<title>(.*?)</title>", p.read_text(encoding="utf-8", errors="ignore"), re.I | re.S)
    if match:
        title = match.group(1).strip()
        title = title.replace("·", "-").replace("&", " and ")
        title = re.sub(r"[\\/:*?\"<>|]+", "", title)
        title = re.sub(r"\s+", " ", title).strip()
        safe_name = title + ".html"
        if safe_name != p.name:
            target = p.with_name(safe_name)
            counter = 1
            while target.exists() and target != p:
                target = p.with_name(f"{title} ({counter}).html")
                counter += 1
            if target != p:
                p.rename(target)
