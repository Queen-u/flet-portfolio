import flet as ft
import flet_video as fv


class Portfolio:
    def __init__(self):
        self.current_page = 0
        self.sidebar_open = True
        self.dark_mode = True

        self.pages = [
            "Home", "About", "Skills", "Timeline", "GitHub",
            "Projects", "Impact", "MATLAB", "Blog",
            "Gallery", "Reflection", "Contact"
        ]

    # ---------------- THEME ----------------
    def set_theme(self):
        if self.dark_mode:
            self.bg     = "#0A1628"
            self.panel  = "#111F35"
            self.panel2 = "#172540"
            self.accent = "#06B6D4"
            self.purple = "#A78BFA"
            self.text   = "#F1F5F9"
            self.muted  = "#64748B"
            self.green  = "#10B981"
            self.yellow = "#F59E0B"
            self.red    = "#EF4444"
        else:
            self.bg     = "#F0F4F8"
            self.panel  = "#FFFFFF"
            self.panel2 = "#E8EEF5"
            self.accent = "#0891B2"
            self.purple = "#7C3AED"
            self.text   = "#0F172A"
            self.muted  = "#64748B"
            self.green  = "#059669"
            self.yellow = "#D97706"
            self.red    = "#DC2626"

    # ---------------- MAIN ----------------
    def main(self, page: ft.Page):
        page.title = "Elizabeth Nuugonya Portfolio"
        page.window.width = 1200
        page.window.height = 800
        page.padding = 0

        self.page_ref = page
        self.set_theme()
        page.bgcolor = self.bg

        self.theme_btn = ft.IconButton(
            icon=ft.Icons.LIGHT_MODE,
            on_click=self.toggle_theme,
            icon_color=self.accent,
            icon_size=20,
            tooltip="Switch to light mode",
        )

        self.content = ft.Container(
            expand=True,
            animate_opacity=ft.Animation(250, ft.AnimationCurve.EASE_IN_OUT),
        )

        self.content_stack = ft.Stack(
            [self.content, ft.Container(content=self.theme_btn, right=16, top=12)],
            expand=True,
        )

        self.sidebar = self.build_sidebar(page)
        self.main_row = ft.Row([self.sidebar, self.content_stack], expand=True)

        page.add(self.main_row)
        self.navigate(0, page)

    def toggle_theme(self, e):
        page = self.page_ref
        self.dark_mode = not self.dark_mode
        self.set_theme()
        page.bgcolor = self.bg
        self.theme_btn.icon = ft.Icons.LIGHT_MODE if self.dark_mode else ft.Icons.DARK_MODE
        self.theme_btn.icon_color = self.accent
        self.theme_btn.tooltip = "Switch to light mode" if self.dark_mode else "Switch to dark mode"
        self.navigate(self.current_page, page)

    # ---------------- SIDEBAR ----------------
    def build_sidebar(self, page):

        def toggle(e):
            self.sidebar_open = not self.sidebar_open
            self.sidebar = self.build_sidebar(page)
            self.main_row.controls[0] = self.sidebar
            page.update()

        nav_icons = [
            ft.Icons.HOME_ROUNDED,
            ft.Icons.PERSON_ROUNDED,
            ft.Icons.BOLT,
            ft.Icons.CALENDAR_MONTH,
            ft.Icons.HUB,
            ft.Icons.FOLDER_SPECIAL,
            ft.Icons.BAR_CHART,
            ft.Icons.CALCULATE,
            ft.Icons.ARTICLE,
            ft.Icons.PHOTO_LIBRARY,
            ft.Icons.PSYCHOLOGY,
            ft.Icons.CONTACT_MAIL,
        ]

        items = []
        for i, name in enumerate(self.pages):
            active = i == self.current_page
            items.append(
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Icon(nav_icons[i], size=18, color=self.accent if active else self.muted),
                            width=32,
                            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                        ),
                        ft.Text(
                            name, size=13,
                            color=self.text if active else self.muted,
                            weight="w600" if active else "normal",
                            visible=self.sidebar_open,
                        ),
                    ], spacing=4),
                    padding=ft.Padding(left=8, top=10, right=8, bottom=10),
                    border_radius=10,
                    bgcolor=self.accent + "18" if active else None,
                    border=ft.Border(left=ft.BorderSide(3, self.accent)) if active else ft.Border(left=ft.BorderSide(3, "#00000000")),
                    animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                    on_click=lambda e, idx=i: self.navigate(idx, page),
                )
            )

        avatar_section = ft.Column([
            ft.Container(
                content=ft.CircleAvatar(radius=38, foreground_image_src="IMG_1230.JPG"),
                padding=3,
                border_radius=50,
                bgcolor=self.accent + "40",
            ),
            ft.Text("Elizabeth Nuugonya", size=14, weight="bold", color=self.text, text_align="center"),
            ft.Text("ECE Student · UNAM", size=11, color=self.muted, text_align="center"),
            ft.Container(height=4),
            ft.Container(height=1, bgcolor=self.accent + "30"),
        ], horizontal_alignment="center", spacing=6)

        avatar_wrapper = ft.Container(
            content=avatar_section,
            opacity=1.0 if self.sidebar_open else 0.0,
            animate_opacity=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            height=148 if self.sidebar_open else 0,
            animate=ft.Animation(250, ft.AnimationCurve.EASE_IN_OUT),
        )

        return ft.Container(
            width=230 if self.sidebar_open else 60,
            animate=ft.Animation(250, ft.AnimationCurve.EASE_IN_OUT),
            padding=ft.Padding(left=10, top=10, right=10, bottom=10),
            bgcolor=self.panel,
            shadow=ft.BoxShadow(blur_radius=20, color="#00000060", offset=ft.Offset(4, 0)),
            content=ft.Column([
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.MENU_ROUNDED,
                        on_click=toggle,
                        icon_color=self.accent,
                        icon_size=20,
                    ),
                ], alignment=ft.MainAxisAlignment.END),
                avatar_wrapper,
                ft.Container(height=6),
                *items,
            ], scroll=ft.ScrollMode.AUTO, spacing=2)
        )

    # ---------------- NAVIGATION ----------------
    def navigate(self, index, page):
        self.current_page = index

        builders = [
            self.home, self.about, self.skills, self.timeline,
            self.github, self.projects, self.impact, self.matlab,
            self.blog, self.gallery, self.reflection, self.contact
        ]

        self.content.opacity = 0
        page.update()

        self.content.content = ft.Container(
            content=builders[index](),
            padding=30,
            expand=True,
            bgcolor=self.bg,
        )

        self.sidebar = self.build_sidebar(page)
        self.main_row.controls[0] = self.sidebar

        self.content.opacity = 1
        page.update()

    # ---------------- HELPERS ----------------
    def scrollable(self, *controls):
        return ft.Column(list(controls), scroll=ft.ScrollMode.AUTO, expand=True, spacing=16)

    def section_title(self, title, subtitle=None):
        return ft.Column([
            ft.Row([
                ft.Container(width=4, height=28, bgcolor=self.accent, border_radius=2),
                ft.Text(title, size=26, weight="bold", color=self.text),
            ], spacing=10),
            ft.Text(subtitle, size=13, color=self.muted) if subtitle else ft.Container(height=0),
        ], spacing=4)

    def pcard(self, *children, padding=20, accent_border=False, accent_color=None):
        color = accent_color or self.accent
        return ft.Container(
            padding=padding,
            bgcolor=self.panel2,
            border_radius=14,
            shadow=ft.BoxShadow(blur_radius=16, color="#00000040", offset=ft.Offset(0, 4)),
            border=ft.Border(left=ft.BorderSide(3, color)) if accent_border else None,
            content=ft.Column(list(children), spacing=10),
        )

    def tag(self, label, color=None):
        return ft.Container(
            content=ft.Text(label, size=11, color=self.text, weight="w500"),
            padding=ft.Padding(left=10, top=4, right=10, bottom=4),
            bgcolor=(color or "#1D4ED8") + "CC",
            border_radius=20,
        )

    def bullet(self, text, color=None):
        return ft.Row([
            ft.Container(width=6, height=6, bgcolor=color or self.accent, border_radius=3),
            ft.Text(text, color=self.muted, size=13, expand=True),
        ], spacing=10)

    def divider(self):
        return ft.Container(height=1, bgcolor=self.accent + "20")

    # ---------------- HOME ----------------
    def home(self):
        def stat(value, label, icon, color=None):
            c = color or self.accent
            return ft.Container(
                expand=True,
                padding=20,
                border_radius=14,
                bgcolor=self.panel2,
                shadow=ft.BoxShadow(blur_radius=16, color="#00000040", offset=ft.Offset(0, 4)),
                content=ft.Column([
                    ft.Container(
                        content=ft.Icon(icon, color=c, size=22),
                        width=44, height=44,
                        bgcolor=c + "20",
                        border_radius=12,
                        alignment=ft.Alignment(0, 0),
                    ),
                    ft.Text(value, size=30, weight="bold", color=c),
                    ft.Text(label, size=12, color=self.muted),
                ], spacing=6)
            )

        return ft.Column([
            ft.Container(
                padding=40,
                border_radius=20,
                bgcolor=self.panel2,
                shadow=ft.BoxShadow(blur_radius=30, color="#00000050", offset=ft.Offset(0, 6)),
                content=ft.Column([
                    ft.Container(
                        content=ft.CircleAvatar(radius=60, foreground_image_src="IMG_1230.JPG"),
                        padding=4,
                        border_radius=70,
                        bgcolor=self.accent + "50",
                    ),
                    ft.Text("Elizabeth Nuugonya", size=38, weight="bold", color=self.text, text_align="center"),
                    ft.Text("Electronics & Computer Engineering Student", size=17, color=self.muted, text_align="center"),
                    ft.Container(
                        content=ft.Text("University of Namibia  ·  Student ID: 225066963", size=12, color=self.accent, text_align="center"),
                        padding=ft.Padding(left=16, top=6, right=16, bottom=6),
                        bgcolor=self.accent + "15",
                        border_radius=20,
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            ),

            ft.Row([
                stat("2",  "GitHub Projects",        ft.Icons.CODE,            self.accent),
                stat("8",  "MATLAB Certifications",  ft.Icons.VERIFIED,        self.accent),
                stat("15", "Team Members",            ft.Icons.GROUPS,          self.purple),
                stat("6+", "Pull Requests Merged",   ft.Icons.MERGE_TYPE,      self.yellow),
            ], spacing=14),

            ft.Container(
                padding=24,
                border_radius=14,
                bgcolor=self.panel2,
                shadow=ft.BoxShadow(blur_radius=16, color="#00000040", offset=ft.Offset(0, 4)),
                border=ft.Border(left=ft.BorderSide(3, self.accent)),
                content=ft.Text(
                    "Welcome to my professional engineering portfolio. I'm an Electronics & Computer Engineering student "
                    "at the University of Namibia, passionate about machine learning, mobile development, and embedded "
                    "systems. This portfolio showcases my academic journey, technical projects, and certifications.",
                    color=self.muted,
                    size=14,
                )
            ),

        ], scroll=ft.ScrollMode.AUTO, expand=True, spacing=16)

    # ---------------- ABOUT ----------------
    def about(self):
        def info_row(label, value, url=None):
            val = (ft.TextButton(value, url=url, style=ft.ButtonStyle(color=self.accent))
                   if url else ft.Text(value, color=self.text, size=13))
            return ft.Row([
                ft.Text(label, color=self.muted, size=12, weight="bold", width=120),
                val,
            ])

        return self.scrollable(
            self.section_title("About Me", "Electronics & Computer Engineering · UNAM"),

            self.pcard(
                info_row("Name",       "Elizabeth Nuugonya"),
                self.divider(),
                info_row("Student ID", "225066963"),
                self.divider(),
                info_row("Institution","University of Namibia (UNAM)"),
                self.divider(),
                info_row("Programme",  "Electronics & Computer Engineering"),
                self.divider(),
                info_row("GitHub",     "github.com/Queen-u", "https://github.com/Queen-u"),
                accent_border=True,
            ),

            self.pcard(
                ft.Text("Who I Am", size=15, weight="bold", color=self.accent),
                ft.Text(
                    "I am an Electronics & Computer Engineering student at the University of Namibia, driven by a "
                    "passion for building technology that solves real-world problems. My academic journey has taken "
                    "me from circuit theory and signal processing to machine learning, mobile applications, and "
                    "full-stack web development.",
                    color=self.muted, size=13,
                ),
            ),

            self.pcard(
                ft.Text("Technical Interests", size=15, weight="bold", color=self.accent),
                self.bullet("Machine Learning & Computer Vision"),
                self.bullet("Mobile & Full-Stack Development"),
                self.bullet("Embedded Systems & Signal Processing"),
                self.bullet("Data Analysis with Python & MATLAB"),
            ),

            self.pcard(
                ft.Text("My Approach", size=15, weight="bold", color=self.accent),
                ft.Text(
                    "I believe great engineering combines technical depth with clear communication and teamwork. "
                    "Through projects like the Namibian Currency Detector and CorroCheck 2.0, I have practised "
                    "collaborative software development using Git workflows, pull request reviews, and agile "
                    "practices. I am committed to writing clean, maintainable code and continuously expanding my skillset.",
                    color=self.muted, size=13,
                ),
            ),
        )

    # ---------------- SKILLS ----------------
    def skills(self):
        def category_header(label, color):
            return ft.Container(
                content=ft.Row([
                    ft.Container(width=3, height=14, bgcolor=color, border_radius=2),
                    ft.Text(label, size=12, weight="bold", color=color),
                ], spacing=8),
                padding=ft.Padding(left=0, top=8, right=0, bottom=2),
            )

        def skill_bar(name, pct, color):
            return ft.Container(
                padding=14, bgcolor=self.panel2, border_radius=12,
                shadow=ft.BoxShadow(blur_radius=10, color="#00000030", offset=ft.Offset(0, 2)),
                content=ft.Column([
                    ft.Row([
                        ft.Text(name, color=self.text, size=13, expand=True),
                        ft.Container(
                            content=ft.Text(f"{pct}%", size=11, color=self.bg, weight="bold"),
                            padding=ft.Padding(left=8, top=2, right=8, bottom=2),
                            bgcolor=color,
                            border_radius=10,
                        ),
                    ]),
                    ft.Stack([
                        ft.Container(height=8, bgcolor="#1E3A5F", border_radius=4),
                        ft.Container(width=pct * 4, height=8, bgcolor=color, border_radius=4),
                    ])
                ], spacing=8)
            )

        return self.scrollable(
            self.section_title("Skills & Technologies"),

            category_header("Programming Languages", self.accent),
            skill_bar("Python",       90, self.accent),
            skill_bar("MATLAB",       85, self.accent),
            skill_bar("JavaScript",   80, self.accent),
            skill_bar("HTML / CSS",   80, self.accent),

            category_header("Frameworks & Libraries", self.purple),
            skill_bar("React / React Native", 75, self.purple),
            skill_bar("FastAPI",              70, self.purple),
            skill_bar("Node.js",              65, self.purple),
            skill_bar("Flet",                 75, self.purple),

            category_header("Tools & Platforms", self.purple),
            skill_bar("Git & GitHub",     85, self.purple),
            skill_bar("Firebase",         70, self.purple),
            skill_bar("YOLOv8 / ML",     65, self.purple),
            skill_bar("Jupyter Notebook", 80, self.purple),
            skill_bar("VS Code",          90, self.purple),
        )

    # ---------------- TIMELINE ----------------
    def timeline(self):
        def entry(week, task, tools, challenge, solution, is_last=False):
            dot = ft.Container(
                width=12, height=12,
                bgcolor=self.accent,
                border_radius=6,
            )
            line = ft.Container(width=2, expand=True, bgcolor=self.accent + "30") if not is_last else ft.Container()

            left_col = ft.Column([dot, line], spacing=0, horizontal_alignment="center")

            right_col = ft.Container(
                padding=ft.Padding(left=16, top=0, right=0, bottom=20),
                content=ft.Container(
                    padding=16,
                    bgcolor=self.panel2,
                    border_radius=12,
                    shadow=ft.BoxShadow(blur_radius=12, color="#00000035", offset=ft.Offset(0, 3)),
                    content=ft.Column([
                        ft.Text(week, size=13, weight="bold", color=self.accent),
                        ft.Row([ft.Icon(ft.Icons.TASK_ALT,       size=13, color=self.muted), ft.Text(task,                color=self.text, size=12, expand=True)], spacing=6),
                        ft.Row([ft.Icon(ft.Icons.BUILD,           size=13, color=self.muted), ft.Text(f"Tools: {tools}",  color=self.muted, size=11, expand=True)], spacing=6),
                        ft.Row([ft.Icon(ft.Icons.WARNING_ROUNDED, size=13, color=self.yellow), ft.Text(challenge,         color=self.muted, size=11, expand=True)], spacing=6),
                        ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE,    size=13, color=self.green),  ft.Text(solution,          color=self.muted, size=11, expand=True)], spacing=6),
                    ], spacing=6)
                )
            )

            return ft.Row([left_col, right_col], spacing=0, vertical_alignment=ft.CrossAxisAlignment.START)

        def project_label(text):
            return ft.Container(
                content=ft.Text(text, size=12, weight="bold", color=self.accent),
                padding=ft.Padding(left=12, top=4, right=12, bottom=4),
                bgcolor=self.accent + "18",
                border_radius=20,
            )

        return self.scrollable(
            self.section_title("Project Timeline"),

            project_label("CorroCheck 2.0 — Group Project (Group 7)"),

            entry("Week 1 — Team Formation & Planning",
                  "Formed Group 7 (15 members), defined project scope for a mobile corrosion inspection app",
                  "Figma, GitHub, Google Docs",
                  "Aligning 15 team members on requirements and individual roles",
                  "Held a kick-off meeting; created shared repo with branch protection rules from day one"),

            entry("Week 2 — UI/UX Design & Architecture",
                  "Created Figma prototypes for the inspection workflow and designed the Firestore database schema",
                  "Figma, Firebase, Draw.io",
                  "Designing an intuitive interface for non-technical field personnel",
                  "Ran usability walkthroughs on wireframes before coding began"),

            entry("Week 3 — Authentication & Backend Setup",
                  "Implemented Firebase Auth and set up Firestore collections for inspection records",
                  "Firebase, Node.js, React Native",
                  "Structuring Firestore for fast queries across large inspection datasets",
                  "Adopted a flat document model with indexed fields over deeply nested structures"),

            entry("Week 4 — Core Inspection Workflow",
                  "Built image capture, corrosion classification UI, and severity rating (Low / Medium / High)",
                  "React Native, Expo Camera, Firebase Storage",
                  "Large image uploads failing on slow mobile connections",
                  "Added client-side compression before upload with a visible progress indicator"),

            entry("Week 5 — ML Classifier Integration",
                  "Integrated corrosion-type classifier via modelService.js adapter pattern",
                  "Node.js, TensorFlow, modelService.js",
                  "Making the ML service swappable without breaking the app",
                  "Adapter pattern: classifyImage() interface hides model internals for easy future swaps"),

            entry("Week 6 — GPS Tagging & Report Generation",
                  "Added GPS coordinate tagging and automated PDF report generation",
                  "Expo Location, Firebase, React Native",
                  "GPS accuracy unreliable on indoor test devices",
                  "Added manual coordinate override and displayed accuracy radius to users"),

            project_label("Namibian Currency Detector"),

            entry("Week 7 — Dataset Collection & YOLOv8 Training",
                  "Labelled images of all Namibian dollar denominations; trained a YOLOv8 detection model",
                  "Python, YOLOv8, Jupyter Notebook, Roboflow",
                  "Limited labelled data for rare denominations caused poor accuracy",
                  "Applied data augmentation and oversampled rare classes in Roboflow"),

            entry("Week 8 — FastAPI Backend",
                  "Built /predict/ REST endpoint returning bounding boxes and NAD values",
                  "Python, FastAPI, Uvicorn",
                  "Overlapping detection boxes caused double-counting of notes",
                  "Implemented IoU-based deduplication before returning results"),

            entry("Week 9 — React Frontend",
                  "Built interactive web UI: image upload, live webcam, bounding box visualisation",
                  "React, Vite, CSS, Canvas API",
                  "Bounding box overlays misaligned on variable display sizes",
                  "Used canvas rendering with dynamic scaling to match displayed image dimensions"),

            entry("Week 10 — Integration & Confidence Tuning",
                  "Connected React to FastAPI; added adjustable confidence threshold slider",
                  "React, FastAPI, CORS",
                  "CORS errors blocked all frontend-to-backend requests in development",
                  "Configured FastAPI CORSMiddleware with explicit allowed origins",
                  is_last=True),
        )

    # ---------------- GITHUB ----------------
    def github(self):
        def commit_card(repo, message, detail):
            return ft.Container(
                padding=14, bgcolor=self.panel2, border_radius=10,
                border=ft.Border(left=ft.BorderSide(2, self.accent + "60")),
                shadow=ft.BoxShadow(blur_radius=8, color="#00000030", offset=ft.Offset(0, 2)),
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.COMMIT, color=self.accent, size=16),
                        width=32, height=32,
                        bgcolor=self.accent + "18",
                        border_radius=8,
                        alignment=ft.Alignment(0, 0),
                    ),
                    ft.Column([
                        ft.Text(repo, size=10, color=self.muted),
                        ft.Text(message, color=self.text, size=12, weight="bold"),
                        ft.Text(detail, color=self.muted, size=11),
                    ], spacing=2, expand=True)
                ], spacing=12)
            )

        def repo_card(name, lang, desc, url):
            return ft.Container(
                padding=18, bgcolor=self.panel2, border_radius=14,
                shadow=ft.BoxShadow(blur_radius=16, color="#00000040", offset=ft.Offset(0, 4)),
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Icon(ft.Icons.FOLDER_COPY_ROUNDED, color=self.accent, size=18),
                            width=36, height=36,
                            bgcolor=self.accent + "18",
                            border_radius=10,
                            alignment=ft.Alignment(0, 0),
                        ),
                        ft.Column([
                            ft.Text(name, size=14, weight="bold", color=self.text),
                            ft.Text(lang, size=11, color=self.muted),
                        ], spacing=2, expand=True),
                    ], spacing=12),
                    ft.Text(desc, color=self.muted, size=12),
                    ft.TextButton("View on GitHub →", url=url, style=ft.ButtonStyle(color=self.accent)),
                ], spacing=10)
            )

        return self.scrollable(
            self.section_title("GitHub Activity", "github.com/Queen-u"),

            ft.Row([
                ft.Container(
                    expand=True, padding=16, border_radius=12, bgcolor=self.panel2,
                    shadow=ft.BoxShadow(blur_radius=12, color="#00000035", offset=ft.Offset(0, 3)),
                    content=ft.Column([
                        ft.Text("2", size=26, weight="bold", color=self.accent),
                        ft.Text("Public Repos", color=self.muted, size=11),
                    ], horizontal_alignment="center")
                ),
                ft.Container(
                    expand=True, padding=16, border_radius=12, bgcolor=self.panel2,
                    shadow=ft.BoxShadow(blur_radius=12, color="#00000035", offset=ft.Offset(0, 3)),
                    content=ft.Column([
                        ft.Icon(ft.Icons.VERIFIED, color=self.yellow, size=26),
                        ft.Text("Pull Shark", size=13, weight="bold", color=self.yellow),
                        ft.Text("GitHub Achievement", color=self.muted, size=11),
                    ], horizontal_alignment="center", spacing=4)
                ),
                ft.Container(
                    expand=True, padding=16, border_radius=12, bgcolor=self.panel2,
                    shadow=ft.BoxShadow(blur_radius=12, color="#00000035", offset=ft.Offset(0, 3)),
                    content=ft.Column([
                        ft.TextButton("github.com/Queen-u", url="https://github.com/Queen-u", style=ft.ButtonStyle(color=self.accent)),
                        ft.Text("GitHub Profile", color=self.muted, size=11),
                    ], horizontal_alignment="center", spacing=4)
                ),
            ], spacing=14),

            ft.Text("Repositories", size=13, color=self.muted, weight="bold"),
            repo_card("namibian-currency-detector", "Jupyter Notebook · Python",
                      "ML web app detecting Namibian banknote denominations via YOLOv8 and calculating total NAD value.",
                      "https://github.com/Queen-u/namibian-currency-detector"),
            repo_card("Corrocheck2.0", "JavaScript · React Native",
                      "Cross-platform mobile corrosion inspection app — classifies types, tags GPS, generates field reports.",
                      "https://github.com/Queen-u/Corrocheck2.0"),

            ft.Text("Recent Commits", size=13, color=self.muted, weight="bold"),
            commit_card("Corrocheck2.0",             "Add branch protection rules and PR review workflow",    "Enforced mandatory code reviews before merging to main"),
            commit_card("namibian-currency-detector", "Implement IoU deduplication for bounding boxes",       "Prevents double-counting of overlapping detections"),
            commit_card("namibian-currency-detector", "Add confidence threshold slider to frontend",          "Lets users control detection sensitivity in real time"),
            commit_card("Corrocheck2.0",             "Integrate GPS tagging with accuracy radius display",    "Shows field personnel the precision of captured coordinates"),
            commit_card("Corrocheck2.0",             "Build modular ML adapter in modelService.js",           "Designed for future model replacement without breaking the app"),
            commit_card("namibian-currency-detector", "Configure FastAPI CORS for local dev and production",  "Fixed cross-origin errors blocking frontend requests"),
        )

    # ---------------- PROJECTS ----------------
    def projects(self):
        def pr_card(number, title, status, tech):
            colors = {"Merged": self.green, "Open": self.yellow, "Closed": self.red}
            c = colors.get(status, self.muted)
            return ft.Container(
                padding=14, bgcolor=self.panel2, border_radius=10,
                shadow=ft.BoxShadow(blur_radius=8, color="#00000030", offset=ft.Offset(0, 2)),
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.MERGE_TYPE, color=c, size=16),
                        width=32, height=32,
                        bgcolor=c + "20",
                        border_radius=8,
                        alignment=ft.Alignment(0, 0),
                    ),
                    ft.Column([
                        ft.Row([
                            ft.Text(f"PR #{number}", color=self.muted, size=10),
                            ft.Container(
                                content=ft.Text(status, size=9, color=self.text, weight="bold"),
                                padding=ft.Padding(left=8, top=2, right=8, bottom=2),
                                bgcolor=c, border_radius=10,
                            )
                        ], spacing=8),
                        ft.Text(title, color=self.text, size=12, weight="bold"),
                        ft.Text(tech, color=self.muted, size=11),
                    ], spacing=3, expand=True)
                ], spacing=12)
            )

        def project_card(icon, title, desc, tags, url, color):
            return ft.Container(
                padding=0, bgcolor=self.panel2, border_radius=14,
                shadow=ft.BoxShadow(blur_radius=20, color="#00000045", offset=ft.Offset(0, 5)),
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                content=ft.Column([
                    ft.Container(
                        padding=ft.Padding(left=20, top=16, right=20, bottom=16),
                        gradient=ft.LinearGradient(
                            begin=ft.Alignment(-1, 0),
                            end=ft.Alignment(1, 0),
                            colors=[color + "30", color + "08"],
                        ),
                        content=ft.Row([
                            ft.Container(
                                content=ft.Icon(icon, color=color, size=22),
                                width=44, height=44,
                                bgcolor=color + "25",
                                border_radius=12,
                                alignment=ft.Alignment(0, 0),
                            ),
                            ft.Text(title, size=17, weight="bold", color=self.text, expand=True),
                        ], spacing=12),
                    ),
                    ft.Container(
                        padding=ft.Padding(left=20, top=0, right=20, bottom=20),
                        content=ft.Column([
                            ft.Text(desc, color=self.muted, size=13),
                            ft.Row([self.tag(t, color) for t in tags], wrap=True, spacing=6),
                            ft.TextButton("View on GitHub →", url=url, style=ft.ButtonStyle(color=color)),
                        ], spacing=12)
                    ),
                ], spacing=0)
            )

        return self.scrollable(
            self.section_title("Projects", "Engineering builds and applications"),

            project_card(
                ft.Icons.CURRENCY_EXCHANGE,
                "Namibian Currency Detector",
                "A full-stack ML web app that detects Namibian banknote denominations from uploaded images or live webcam. "
                "Uses a trained YOLOv8 model via FastAPI with IoU deduplication to prevent double-counting. "
                "The React/Vite frontend supports an adjustable confidence threshold and displays the total NAD value.",
                ["YOLOv8", "FastAPI", "React", "Python", "Vite"],
                "https://github.com/Queen-u/namibian-currency-detector",
                self.accent,
            ),

            project_card(
                ft.Icons.BUILD_CIRCLE,
                "CorroCheck 2.0",
                "Cross-platform mobile app developed by Group 7 (15 students) for corrosion inspection. "
                "Field personnel photograph metallic structures, classify corrosion type (uniform, galvanic, pitting, crevice), "
                "assign severity (Low/Medium/High), and generate GPS-tagged PDF reports stored in Firebase.",
                ["React Native", "Node.js", "Firebase", "Expo", "Figma"],
                "https://github.com/Queen-u/Corrocheck2.0",
                self.purple,
            ),

            ft.Text("Pull Requests", size=13, color=self.muted, weight="bold"),
            pr_card(1, "Initial Firebase Auth & Firestore setup",              "Merged", "Firebase, Node.js"),
            pr_card(2, "Image upload with compression and progress indicator", "Merged", "React Native, Expo"),
            pr_card(3, "ML corrosion classifier adapter (modelService.js)",   "Merged", "Node.js, TensorFlow"),
            pr_card(4, "GPS tagging with accuracy radius overlay",             "Merged", "Expo Location"),
            pr_card(5, "YOLOv8 /predict/ endpoint with IoU deduplication",   "Merged", "FastAPI, Python"),
            pr_card(6, "Confidence threshold slider and webcam detection",    "Merged", "React, Vite"),
        )

    # ---------------- IMPACT ----------------
    def impact(self):
        def impact_card(icon, title, rows, color):
            return ft.Container(
                padding=0, bgcolor=self.panel2, border_radius=14,
                shadow=ft.BoxShadow(blur_radius=20, color="#00000045", offset=ft.Offset(0, 5)),
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                content=ft.Column([
                    ft.Container(
                        padding=ft.Padding(left=20, top=14, right=20, bottom=14),
                        gradient=ft.LinearGradient(
                            begin=ft.Alignment(-1, 0), end=ft.Alignment(1, 0),
                            colors=[color + "28", color + "06"],
                        ),
                        content=ft.Row([
                            ft.Container(
                                content=ft.Icon(icon, color=color, size=20),
                                width=40, height=40, bgcolor=color + "25", border_radius=10,
                                alignment=ft.Alignment(0, 0),
                            ),
                            ft.Text(title, size=16, weight="bold", color=self.text),
                        ], spacing=12),
                    ),
                    ft.Container(
                        padding=ft.Padding(left=20, top=4, right=20, bottom=20),
                        content=ft.Column([
                            ft.Row([
                                ft.Text(label, size=11, weight="bold", color=label_color, width=90),
                                ft.Text(value, color=self.muted, size=12, expand=True),
                            ])
                            for label, value, label_color in rows
                        ], spacing=10)
                    ),
                ], spacing=0)
            )

        def metric(value, label, color):
            return ft.Container(
                expand=True, padding=16, border_radius=12, bgcolor=self.panel2,
                shadow=ft.BoxShadow(blur_radius=12, color="#00000035", offset=ft.Offset(0, 3)),
                content=ft.Column([
                    ft.Text(value, size=28, weight="bold", color=color),
                    ft.Text(label, color=self.muted, size=11, text_align="center"),
                ], horizontal_alignment="center", spacing=4)
            )

        return self.scrollable(
            self.section_title("Engineering Impact"),

            impact_card(ft.Icons.CURRENCY_EXCHANGE, "Namibian Currency Detector", [
                ("Problem",  "No affordable automated tool to identify and total Namibian banknote denominations from images.",                                        self.red),
                ("My Role",  "Trained YOLOv8 on a custom NAD dataset, built the FastAPI backend with IoU deduplication, connected to React frontend.",               self.accent),
                ("Outcome",  "Functional web app with real-time NAD detection and confidence tuning — practical for banking, retail, and accessibility.",             self.accent),
                ("Lesson",   "Data augmentation is essential with scarce labels. Clean API contracts between ML backend and frontend simplify integration.",          self.yellow),
            ], self.accent),

            impact_card(ft.Icons.BUILD_CIRCLE, "CorroCheck 2.0", [
                ("Problem",  "Corrosion inspections relied on manual paperwork — inconsistent records, data loss, slow reporting.",                                    self.red),
                ("My Role",  "Built React Native UI and Firebase integration; implemented the ML adapter; upheld PR reviews across a 15-person team.",               self.accent),
                ("Outcome",  "Cross-platform mobile app that standardises inspection data and generates GPS-tagged PDF reports instantly.",                           self.accent),
                ("Lesson",   "Adapter pattern for ML dramatically reduces maintenance cost. Branch protection from day one pays dividends in large teams.",           self.yellow),
            ], self.purple),

            ft.Row([
                metric("8",  "MATLAB Certs",   self.accent),
                metric("15", "Team Members",   self.purple),
                metric("6+", "PRs Merged",     self.accent),
                metric("2",  "Full Projects",  self.yellow),
            ], spacing=14),
        )

    # ---------------- MATLAB ----------------
    def matlab(self):
        certs = [
            ("MATLAB Onramp",                             "Foundational MATLAB syntax, scripts, and the MATLAB Desktop environment."),
            ("Simulink Onramp",                           "Introduction to model-based design and simulation with Simulink."),
            ("Vectors and Matrices",                      "Creating, indexing, and operating on vectors and matrices in MATLAB."),
            ("Make and Manipulate Matrices",              "Advanced matrix operations, reshaping, and linear algebra applications."),
            ("How MATLAB Graphics Work",                  "Understanding the MATLAB graphics object hierarchy and plot customisation."),
            ("MATLAB Desktop Tools & Troubleshooting",    "Debugging tools, the variable editor, and effective script troubleshooting."),
            ("Simulink Fundamentals",                     "Building, simulating, and analysing dynamic systems in Simulink."),
            ("Explore Data and MATLAB Courses",           "Data exploration, visualisation, and analysis techniques using MATLAB."),
        ]

        cert_cards = []
        for i, (name, desc) in enumerate(certs, 1):
            cert_cards.append(
                ft.Container(
                    padding=14, bgcolor=self.panel2, border_radius=12,
                    shadow=ft.BoxShadow(blur_radius=10, color="#00000030", offset=ft.Offset(0, 2)),
                    content=ft.Row([
                        ft.Container(
                            content=ft.Text(str(i), color=self.bg, weight="bold", size=13),
                            width=34, height=34,
                            bgcolor=self.accent,
                            border_radius=17,
                            alignment=ft.Alignment(0, 0),
                        ),
                        ft.Column([
                            ft.Text(name, color=self.text, weight="bold", size=13),
                            ft.Text(desc, color=self.muted, size=11),
                        ], spacing=3, expand=True)
                    ], spacing=14)
                )
            )

        return self.scrollable(
            self.section_title("MATLAB Certifications", "Issued by MathWorks · MATLAB Academy"),

            ft.Container(
                padding=16, border_radius=14, bgcolor=self.panel2,
                shadow=ft.BoxShadow(blur_radius=16, color="#00000040", offset=ft.Offset(0, 4)),
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.VERIFIED, color=self.accent, size=26),
                        width=48, height=48, bgcolor=self.accent + "20", border_radius=12,
                        alignment=ft.Alignment(0, 0),
                    ),
                    ft.Column([
                        ft.Text("8 / 8 Certifications Completed", size=16, weight="bold", color=self.text),
                        ft.Text("All MathWorks MATLAB Academy courses completed", color=self.muted, size=12),
                    ], spacing=4, expand=True),
                ], spacing=14)
            ),

            *cert_cards,
        )

    # ---------------- BLOG ----------------
    def blog(self):
        def post(title, body, tags, color=None):
            c = color or self.accent
            return ft.Container(
                padding=0, bgcolor=self.panel2, border_radius=14,
                shadow=ft.BoxShadow(blur_radius=16, color="#00000040", offset=ft.Offset(0, 4)),
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                content=ft.Column([
                    ft.Container(
                        height=4,
                        gradient=ft.LinearGradient(
                            begin=ft.Alignment(-1, 0), end=ft.Alignment(1, 0),
                            colors=[c, c + "40"],
                        ),
                    ),
                    ft.Container(
                        padding=20,
                        content=ft.Column([
                            ft.Text(title, size=14, weight="bold", color=self.text),
                            ft.Text(body, color=self.muted, size=12),
                            ft.Row([self.tag(t, c) for t in tags], wrap=True, spacing=6),
                        ], spacing=10)
                    ),
                ], spacing=0)
            )

        return self.scrollable(
            self.section_title("Technical Blog", "Engineering insights from building real projects"),

            ft.Container(
                padding=0,
                border_radius=16,
                bgcolor=self.panel2,
                shadow=ft.BoxShadow(blur_radius=20, color="#00000045", offset=ft.Offset(0, 5)),
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                content=ft.Column([
                    ft.Container(
                        padding=ft.Padding(left=20, top=16, right=20, bottom=12),
                        content=ft.Row([
                            ft.Container(
                                content=ft.Icon(ft.Icons.VIDEOCAM_ROUNDED, color=self.purple, size=20),
                                width=36, height=36,
                                bgcolor=self.purple + "20",
                                border_radius=10,
                                alignment=ft.Alignment(0, 0),
                            ),
                            ft.Column([
                                ft.Text("Video: My Contributions to CorroCheck 2.0", size=15, weight="bold", color=self.text),
                                ft.Text("Elizabeth describes her role in Group 7's mobile inspection app", size=12, color=self.muted),
                            ], spacing=2, expand=True),
                        ], spacing=12),
                    ),
                    fv.Video(
                        playlist=[fv.VideoMedia(resource="/queen.mp4")],
                        height=280,
                        expand=True,
                        autoplay=False,
                        fill_color=ft.Colors.BLACK,
                        controls=fv.AdaptiveVideoControls(),
                    ),
                ], spacing=0),
            ),

            post(
                "Object Detection with YOLOv8: Training on Custom Namibian Currency Data",
                "YOLOv8 is one of the fastest object detection models available, but performance depends heavily on data quality. "
                "Building the Namibian Currency Detector taught me that data augmentation — flipping, rotating, and brightness-shifting "
                "labelled images — is as important as model architecture. I used Roboflow to augment the dataset, dramatically improving "
                "accuracy for rare denominations. Key lesson: a well-labelled small dataset beats a large noisy one every time.",
                ["YOLOv8", "Computer Vision", "Python", "Roboflow"],
                self.accent,
            ),
            post(
                "Building Cross-Platform Mobile Apps with React Native and Firebase",
                "React Native with Expo lets you write one codebase for iOS and Android — a huge advantage for student projects. "
                "For CorroCheck 2.0, Firebase handled authentication, file storage, and real-time data. The biggest challenge was "
                "Firestore document structure for fast queries. We found a flat model with explicit indexes far outperforms deeply "
                "nested structures for large inspection record sets.",
                ["React Native", "Firebase", "Expo", "Mobile Dev"],
                self.purple,
            ),
            post(
                "Why Modular Design Matters: The Adapter Pattern in CorroCheck",
                "When building CorroCheck 2.0, our team knew the corrosion ML model would eventually be replaced. Instead of "
                "hardcoding inference calls, we wrapped the model in a single adapter (modelService.js) exposing a classifyImage() "
                "interface. Swapping models now requires changing one file. This was my first exposure to design patterns in a "
                "production-like codebase, and the payoff was immediate.",
                ["Design Patterns", "Node.js", "Software Architecture"],
                self.purple,
            ),
            post(
                "MATLAB for Engineers: From Matrices to Simulink",
                "After completing all 8 MathWorks certifications, MATLAB is clearly not just a calculator — it is a complete "
                "engineering environment. The progression from scripting (MATLAB Onramp) to model-based simulation (Simulink "
                "Fundamentals) mirrors the shift from algorithm design to system-level thinking that electronics engineering demands. "
                "Simulink block diagrams map almost directly onto control systems theory from lectures.",
                ["MATLAB", "Simulink", "Signal Processing", "Engineering"],
                self.yellow,
            ),
        )

    # ---------------- GALLERY ----------------
    def gallery(self):
        def project_panel(title, subtitle, bullets, color):
            return ft.Container(
                expand=True, bgcolor=self.panel2, border_radius=14,
                shadow=ft.BoxShadow(blur_radius=16, color="#00000040", offset=ft.Offset(0, 4)),
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                content=ft.Column([
                    ft.Container(
                        height=120,
                        gradient=ft.LinearGradient(
                            begin=ft.Alignment(0, -1), end=ft.Alignment(0, 1),
                            colors=[color + "35", color + "08"],
                        ),
                        content=ft.Column([
                            ft.Icon(ft.Icons.PHOTO_CAMERA, color=color, size=34),
                            ft.Text(title, color=color, weight="bold", text_align="center", size=12),
                        ], horizontal_alignment="center", alignment=ft.MainAxisAlignment.CENTER),
                        alignment=ft.Alignment(0, 0),
                    ),
                    ft.Container(
                        padding=16,
                        content=ft.Column([
                            ft.Text(subtitle, color=self.muted, size=12),
                            ft.Column([
                                ft.Row([
                                    ft.Container(width=6, height=6, bgcolor=color, border_radius=3),
                                    ft.Text(b, color=self.muted, size=12, expand=True),
                                ], spacing=8)
                                for b in bullets
                            ], spacing=6)
                        ], spacing=8)
                    ),
                ], spacing=0)
            )

        cert_names = [
            "MATLAB\nOnramp", "Simulink\nOnramp", "Vectors &\nMatrices", "MATLAB\nGraphics",
            "Make &\nMatrices", "Desktop\nTools", "Simulink\nFund.", "Explore\nData",
        ]

        return self.scrollable(
            self.section_title("Project Gallery", "Visual overview of projects and certifications"),

            ft.Row([
                project_panel(
                    "Namibian Currency Detector",
                    "Web interface — image upload & live webcam",
                    ["Bounding box overlay on detected notes", "Real-time NAD denomination labels",
                     "Confidence threshold slider", "Automatic total value display"],
                    self.accent,
                ),
                project_panel(
                    "CorroCheck 2.0",
                    "Cross-platform mobile inspection app",
                    ["Camera capture with corrosion type overlay", "GPS-tagged inspection records",
                     "Severity rating: Low / Medium / High", "PDF report generation"],
                    self.purple,
                ),
            ], spacing=16),

            ft.Container(
                padding=20, bgcolor=self.panel2, border_radius=14,
                shadow=ft.BoxShadow(blur_radius=16, color="#00000040", offset=ft.Offset(0, 4)),
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.VERIFIED, color=self.accent, size=18),
                        ft.Text("MATLAB Certifications (8 / 8)", size=15, weight="bold", color=self.text),
                    ], spacing=8),
                    ft.Text("Certificates stored in /certificates · Issued by MathWorks", color=self.muted, size=11),
                    ft.Row([
                        ft.Container(
                            content=ft.Text(n, size=10, color=self.text, text_align="center"),
                            padding=10, border_radius=8,
                            bgcolor=self.accent + "15",
                            border=ft.Border(
                                ft.BorderSide(1, self.accent + "40"), ft.BorderSide(1, self.accent + "40"),
                                ft.BorderSide(1, self.accent + "40"), ft.BorderSide(1, self.accent + "40"),
                            ),
                            expand=True,
                        ) for n in cert_names[:4]
                    ], spacing=8),
                    ft.Row([
                        ft.Container(
                            content=ft.Text(n, size=10, color=self.text, text_align="center"),
                            padding=10, border_radius=8,
                            bgcolor=self.accent + "15",
                            border=ft.Border(
                                ft.BorderSide(1, self.accent + "40"), ft.BorderSide(1, self.accent + "40"),
                                ft.BorderSide(1, self.accent + "40"), ft.BorderSide(1, self.accent + "40"),
                            ),
                            expand=True,
                        ) for n in cert_names[4:]
                    ], spacing=8),
                ], spacing=12)
            ),
        )

    # ---------------- REFLECTION ----------------
    def reflection(self):
        def challenge_card(challenge, solution):
            return ft.Container(
                padding=0, bgcolor=self.panel2, border_radius=12,
                shadow=ft.BoxShadow(blur_radius=10, color="#00000030", offset=ft.Offset(0, 2)),
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                content=ft.Column([
                    ft.Container(
                        padding=12,
                        bgcolor=self.yellow + "12",
                        content=ft.Row([
                            ft.Icon(ft.Icons.WARNING_ROUNDED, color=self.yellow, size=15),
                            ft.Text(challenge, color=self.text, size=12, weight="bold", expand=True),
                        ], spacing=8),
                    ),
                    ft.Container(
                        padding=12,
                        content=ft.Row([
                            ft.Icon(ft.Icons.CHECK_CIRCLE, color=self.green, size=15),
                            ft.Text(solution, color=self.muted, size=12, expand=True),
                        ], spacing=8),
                    ),
                ], spacing=0)
            )

        return self.scrollable(
            self.section_title("Reflection & Growth"),

            self.pcard(
                ft.Text("Skills Developed", size=15, weight="bold", color=self.accent),
                self.bullet("Machine learning model training and deployment with YOLOv8 and FastAPI"),
                self.bullet("Cross-platform mobile development with React Native, Expo, and Firebase"),
                self.bullet("Collaborative Git workflows: feature branches, pull requests, and code reviews"),
                self.bullet("Software design patterns — adapter pattern for modular ML services"),
                self.bullet("MATLAB simulation and data analysis across 8 MathWorks-certified courses"),
            ),

            ft.Text("Challenges & Solutions", size=13, color=self.muted, weight="bold"),
            challenge_card("Insufficient labelled training data for rare Namibian denominations",
                           "Applied data augmentation (flip, rotate, brightness) and oversampled rare classes in Roboflow"),
            challenge_card("Coordinating 15 team members on a shared codebase",
                           "Enforced branch protection with mandatory PR reviews; weekly standups kept all contributors aligned"),
            challenge_card("GPS inaccuracy on indoor test devices",
                           "Added manual coordinate override and displayed accuracy radius so users judge data precision"),
            challenge_card("CORS errors blocking React frontend from reaching FastAPI",
                           "Configured CORSMiddleware with explicit allowed origins for both dev and production"),

            self.pcard(
                ft.Text("Future Improvements", size=15, weight="bold", color=self.accent),
                self.bullet("Expand currency detector to cover all SADC member-state currencies"),
                self.bullet("Add offline mode to CorroCheck for inspectors without connectivity"),
                self.bullet("Retrain corrosion classifier on a larger, more diverse image dataset"),
                self.bullet("Deploy currency detector API to a cloud platform such as Railway or Render"),
            ),

            self.pcard(
                ft.Text("What I Would Do Differently", size=15, weight="bold", color=self.accent),
                ft.Text(
                    "Starting with a clear data collection strategy before model training would have saved significant time "
                    "on the Currency Detector. For CorroCheck, establishing coding standards and linting in Week 1 rather "
                    "than retrofitting them midway would have helped. Both experiences reinforced that good planning and "
                    "architectural decisions made early have compounding benefits throughout the development lifecycle.",
                    color=self.muted, size=13,
                ),
                accent_border=True,
            ),
        )

    # ---------------- CONTACT ----------------
    def contact(self):
        def contact_row(icon, label, value, url=None, color=None):
            c = color or self.accent
            val = (ft.TextButton(value, url=url, style=ft.ButtonStyle(color=c))
                   if url else ft.Text(value, color=self.text, size=13))
            return ft.Container(
                padding=14, bgcolor=self.panel2, border_radius=12,
                shadow=ft.BoxShadow(blur_radius=8, color="#00000030", offset=ft.Offset(0, 2)),
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(icon, color=c, size=18),
                        width=40, height=40,
                        bgcolor=c + "18",
                        border_radius=10,
                        alignment=ft.Alignment(0, 0),
                    ),
                    ft.Column([
                        ft.Text(label, color=self.muted, size=10),
                        val,
                    ], spacing=2, expand=True)
                ], spacing=14)
            )

        return self.scrollable(
            self.section_title("Contact", "Let's connect — reach out via any of the channels below"),

            contact_row(ft.Icons.PERSON,  "Full Name",   "Elizabeth Nuugonya"),
            contact_row(ft.Icons.BADGE,   "Student ID",  "225066963"),
            contact_row(ft.Icons.SCHOOL,  "Institution", "University of Namibia (UNAM)"),
            contact_row(ft.Icons.CODE,    "GitHub",      "github.com/Queen-u",                "https://github.com/Queen-u",                       self.accent),
            contact_row(ft.Icons.EMAIL,   "Email",       "elizabeth@example.com",             "mailto:elizabeth@example.com",                     self.accent),
            contact_row(ft.Icons.WORK,    "LinkedIn",    "linkedin.com/in/elizabeth-nuugonya","https://linkedin.com/in/elizabeth-nuugonya",        self.purple),

            ft.Container(
                padding=20, bgcolor=self.panel2, border_radius=14,
                shadow=ft.BoxShadow(blur_radius=16, color="#00000040", offset=ft.Offset(0, 4)),
                content=ft.Column([
                    ft.Text("Open To", size=15, weight="bold", color=self.accent),
                    ft.Row([
                        self.tag("Internships",             self.accent),
                        self.tag("Research Collaborations", self.purple),
                        self.tag("Open Source",             self.accent),
                        self.tag("Graduate Opportunities",  self.yellow),
                    ], wrap=True, spacing=8),
                ], spacing=12)
            ),
        )


if __name__ == "__main__":
    ft.app(target=Portfolio().main, view=ft.AppView.WEB_BROWSER, port=8550, assets_dir=".")