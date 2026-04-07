import sys, os
import urllib.request
import importlib.util
from urllib.parse import urlparse, parse_qs

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget,
    QVBoxLayout, QToolBar, QAction, QPushButton, QHBoxLayout,
    QSplashScreen, QMessageBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtCore import QUrl, Qt, QPoint
from PyQt5.QtGui import QPixmap

HOMEPAGE = "http://google.com"
TWIG_VERSION = "1.2"

class TwigPage(QWebEnginePage):
    def acceptNavigationRequest(self, url, nav_type, is_main_frame):
        url_str = url.toString()

        # Allow all other URLs
        return super().acceptNavigationRequest(url, nav_type, is_main_frame)

    def _get_main_window(self):
        """
        Walk up from QWebEngineView → BrowserTab → Twig.
        Assumes structure:
          Twig (QMainWindow)
            └─ BrowserTab (QWidget)
                └─ QWebEngineView
        """
        view = self.view()
        if view is None:
            return None
        tab = view.parent()
        if tab is None:
            return None
        main_window = tab.parent
        if isinstance(main_window, QMainWindow):
            return main_window
        return None


class BrowserTab(QWidget):
    def __init__(self, url=HOMEPAGE, parent=None):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout(self)

        self.browser = QWebEngineView()
        self.page = TwigPage(self.browser)
        self.browser.setPage(self.page)

        self.browser.setUrl(QUrl(url))
        self.layout.addWidget(self.browser)

        self.browser.titleChanged.connect(self.update_tab_title)
        self.browser.loadFinished.connect(self.handle_load_result)

    def update_tab_title(self, title):
        index = self.parent.tabs.indexOf(self)
        if title.strip() == "":
            title = "Untitled"
        elif self.browser.url().toString() == HOMEPAGE:
            title = "Home"
        self.parent.tabs.setTabText(index, title)

    def handle_load_result(self, success):
        if not success:
            index = self.parent.tabs.indexOf(self)
            self.parent.tabs.setTabText(index, "⚠️ Failed")


class TitleBar(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setFixedHeight(40)
        self.setStyleSheet("background-color: #03c2fc;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.addStretch()

        self.min_btn = QPushButton("—")
        self.max_btn = QPushButton("O")
        self.close_btn = QPushButton("X")

        for btn in [self.min_btn, self.max_btn, self.close_btn]:
            btn.setFixedSize(32, 32)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1e1e1e;
                    color: #f0f0f0;
                    border: none;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #1e1e1e;
                }
            """)

        self.min_btn.clicked.connect(self.parent.showMinimized)
        self.max_btn.clicked.connect(self.toggle_max_restore)
        self.close_btn.clicked.connect(self.parent.close)

        layout.addWidget(self.min_btn)
        layout.addWidget(self.max_btn)
        layout.addWidget(self.close_btn)

        self.drag_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.parent.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self.drag_pos and event.buttons() == Qt.LeftButton:
            self.parent.move(event.globalPos() - self.drag_pos)

    def toggle_max_restore(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()


class Twig(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Twig")
        self.resize(1024, 768)
        self.setWindowFlags(Qt.FramelessWindowHint)

        profile = QWebEngineProfile.defaultProfile()
        original_agent = profile.httpUserAgent()

        profile.setCachePath(os.path.join(os.getenv("APPDATA") or "", "TwigCache"))
        profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)
        
        profile = QWebEngineProfile.defaultProfile()
        original_ua = profile.httpUserAgent()
        profile.setHttpUserAgent(f"{original_ua} Twig/{TWIG_VERSION}")
        

        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
                color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #333;
            }
            QTabBar::tab {
                background: #1e1e1e;
                color: #f0f0f0;
                padding: 8px;
                border-radius: 6px;
                margin: 2px;
            }
            QTabBar::tab:selected {
                background: #2e2e2e;
            }
            QToolBar {
                background-color: #1a1a1a;
                spacing: 6px;
            }
            QToolButton {
                background-color: #1e1e1e;
                color: #f0f0f0;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 6px 12px;
            }
            QToolButton:hover {
                background-color: #1e1e1e;
            }
        """)

        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)

        self.title_bar = TitleBar(self)
        central_layout.addWidget(self.title_bar)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        central_layout.addWidget(self.tabs)

        self.toolbar = QToolBar("Twig Controls")
        central_layout.addWidget(self.toolbar)

        self.setCentralWidget(central_widget)

        back_action = QAction("←", self)
        back_action.triggered.connect(self.go_back)
        self.toolbar.addAction(back_action)

        forward_action = QAction("→", self)
        forward_action.triggered.connect(self.go_forward)
        self.toolbar.addAction(forward_action)

        reload_action = QAction("⟳", self)
        reload_action.triggered.connect(self.reload_page)
        self.toolbar.addAction(reload_action)

        new_tab_action = QAction("+", self)
        new_tab_action.triggered.connect(lambda: self.add_tab())
        self.toolbar.addAction(new_tab_action)

        self.add_tab(HOMEPAGE)

    def add_tab(self, url=None):
        if not isinstance(url, str):
            url = HOMEPAGE
        tab = BrowserTab(url, parent=self)
        index = self.tabs.addTab(tab, "Loading...")
        self.tabs.setCurrentIndex(index)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def current_browser(self):
        current_tab = self.tabs.currentWidget()
        if hasattr(current_tab, "browser") and isinstance(current_tab.browser, QWebEngineView):
            return current_tab.browser
        return None

    def go_back(self):
        browser = self.current_browser()
        if browser:
            browser.back()

    def go_forward(self):
        browser = self.current_browser()
        if browser:
            browser.forward()

    def reload_page(self):
        browser = self.current_browser()
        if browser:
            browser.reload()

    def open_devtools(self):
        browser = self.current_browser()
        if browser:
            devtools = QWebEngineView()
            browser.page().setDevToolsPage(devtools)
            devtools.show()
            
    def get_version(self):
        return float(TWIG_VERSION)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.processEvents()

    window = Twig()
    window.show()

    sys.exit(app.exec_())