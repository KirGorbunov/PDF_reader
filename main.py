import sys
from pathlib import Path

from PyQt6.QtCore import QPointF, QRect, QPoint, Qt
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtWidgets import QFileDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMainWindow


class CustomPdfView(QPdfView):
    def __init__(self, parent):
        super().__init__(parent)
        self.refresh_view()

    def refresh_view(self):
        self.begin = QPoint()
        self.end = QPoint()
        self.drawing = False

    def paintEvent(self, event):
        super().paintEvent(event)
        qp = QPainter(self.viewport())
        qp.setPen(QColor(255, 0, 0))
        qp.drawRect(QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.drawing = True
        self.begin = event.pos()

    def mouseMoveEvent(self, event):
        if self.drawing == True:
            self.end = event.pos()
            self.viewport().repaint()

    def mouseReleaseEvent(self, event):
        self.drawing = False


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 870)
        self.setWindowTitle('PDF Reader')
        self.pdf_document = QPdfDocument(None)
        self.pdf_view = CustomPdfView(None)
        self.nav = self.pdf_view.pageNavigator()

        # Buttons:
        button_open = QPushButton("Загрузить", self)
        button_open.clicked.connect(self.open_pdf)

        button_prev_page = QPushButton("<", self)
        button_prev_page.clicked.connect(self.go_previous_page)

        button_next_page = QPushButton(">", self)
        button_next_page.clicked.connect(self.go_next_page)

        # Layouts
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        button_open_layout = QHBoxLayout()
        buttons_move_layout = QHBoxLayout()
        pdf_layout = QVBoxLayout()

        layout.addLayout(button_layout)
        layout.addLayout(pdf_layout)

        button_layout.addLayout(button_open_layout)
        button_layout.addLayout(buttons_move_layout)

        # Add widgets to layouts
        button_open_layout.addWidget(button_open)
        button_open_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        buttons_move_layout.addWidget(button_prev_page)
        buttons_move_layout.addWidget(button_next_page)
        buttons_move_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        pdf_layout.addWidget(self.pdf_view)

        window = QWidget()
        window.setLayout(layout)
        self.setCentralWidget(window)
        self.show()

    def go_next_page(self):
        self.pdf_view.refresh_view()

        if self.nav.currentPage() < self.pdf_document.pageCount() - 1:
            self.nav.jump(self.nav.currentPage() + 1, QPointF())

    def go_previous_page(self):
        self.pdf_view.refresh_view()

        if self.nav.currentPage() > 0:
            self.nav.jump(self.nav.currentPage() - 1, QPointF())

    def open_pdf(self):
        self.pdf_view.refresh_view()

        home_dir = str(Path.home())
        doc_location = QFileDialog.getOpenFileName(
            self,
            'Open File',
            home_dir,
            "PDF files (*.pdf)"
        )

        if self.nav.currentPage() > 0:
            self.nav.jump(0, QPointF())

        self.pdf_document.load(doc_location[0])
        self.pdf_view.setDocument(self.pdf_document)
        self.pdf_view.setZoomMode(QPdfView.ZoomMode.FitInView)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myApp = MainWindow()
    myApp.show()
    sys.exit(app.exec())
