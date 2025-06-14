import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QGridLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QPixmap
from a_star import AStar
from utils import get_neighbors

CELL_SIZE = 40
GRID_SIZE = 10

class GridWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        self.start = (0, 0)
        self.goal = (GRID_SIZE-1, GRID_SIZE-1)
        self.mode = 'barrier'
        self.path = []
        self.setFixedSize(CELL_SIZE*GRID_SIZE, CELL_SIZE*GRID_SIZE)
        self.setMouseTracking(True)

    def paintEvent(self, event):
        qp = QPainter(self)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                rect = (j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if hasattr(self, 'explored') and (i, j) in getattr(self, 'explored', set()):
                    qp.fillRect(*rect, QColor(255, 255, 120))
                if hasattr(self, 'open_set') and (i, j) in getattr(self, 'open_set', set()):
                    qp.fillRect(*rect, QColor(120, 255, 255))
                if (i, j) == self.start:
                    qp.fillRect(*rect, QColor(0, 200, 0))
                elif (i, j) == self.goal:
                    qp.fillRect(*rect, QColor(200, 0, 0))
                elif self.grid[i, j] == 1:
                    qp.fillRect(*rect, QColor(50, 50, 50))
                elif (i, j) in self.path:
                    qp.fillRect(*rect, QColor(0, 0, 200))
                elif not ((i, j) in getattr(self, 'explored', set()) or (i, j) in getattr(self, 'open_set', set())):
                    qp.fillRect(*rect, QColor(255, 255, 255))
                qp.drawRect(*rect)
        if getattr(self, 'no_path', False):
            qp.setPen(QColor(200,0,0))
            qp.setFont(self.font())
            qp.drawText(self.rect(), Qt.AlignCenter, 'Caminho impossível!')

    def mousePressEvent(self, event):
        x = event.y() // CELL_SIZE
        y = event.x() // CELL_SIZE
        if self.mode == 'barrier':
            if (x, y) != self.start and (x, y) != self.goal:
                self.grid[x, y] = 1 if self.grid[x, y] == 0 else 0
        elif self.mode == 'start':
            if self.grid[x, y] == 0 and (x, y) != self.goal:
                self.start = (x, y)
        elif self.mode == 'goal':
            if self.grid[x, y] == 0 and (x, y) != self.start:
                self.goal = (x, y)
        self.update()

    def clear_path(self):
        self.path = []
        self.explored = set()
        self.open_set = set()
        self.no_path = False
        self.update()

    def run_astar(self):
        self.path = []
        self.explored = set()
        self.open_set = set()
        self.no_path = False
        self.update()
        from time import sleep
        astar = AStar()
        astar.get_neighbors = lambda node: get_neighbors(node, self.grid)
        widget = self
        def step_callback(current, open_set, closed_set, came_from, grid, start, goal):
            widget.explored = set(closed_set)
            widget.open_set = set(open_set)
            path = []
            if current in came_from:
                node = current
                while node in came_from:
                    path.append(node)
                    node = came_from[node]
                path.append(start)
                path = path[::-1]
            widget.path = path
            widget.update()
            QApplication.processEvents()
            sleep(0.04)
        astar.step_callback = step_callback
        path = astar.find_path(self.start, self.goal, grid=self.grid)
        if path:
            self.path = path
            self.no_path = False
        else:
            self.path = []
            self.no_path = True
        self.explored = set(astar.closed_set)
        self.open_set = set()
        self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('A* Pathfinding Visualizer (PyQt5)')
        self.grid_widget = GridWidget()
        legend_layout = QHBoxLayout()
        legend_layout.setSpacing(18)
        legend_layout.setContentsMargins(0, 8, 0, 8)
        legend_layout.setAlignment(Qt.AlignCenter)
        legend_layout.addWidget(self._legend_label('Início', QColor(0,200,0)))
        legend_layout.addWidget(self._legend_label('Objetivo', QColor(200,0,0)))
        legend_layout.addWidget(self._legend_label('Caminho', QColor(0,0,200)))
        legend_layout.addWidget(self._legend_label('Barreira', QColor(50,50,50)))
        legend_layout.addWidget(self._legend_label('Livre', QColor(220,220,220)))
        legend_widget = QWidget()
        legend_widget.setLayout(legend_layout)
        legend_widget.setStyleSheet('''
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f8f8fa, stop:1 #e8eaf6);
            border-radius: 10px;
            padding: 8px 0px 8px 0px;
            margin-top: 10px;
            margin-bottom: 0px;
        ''')
        legend_widget.setFixedHeight(48)
        legend_container = QHBoxLayout()
        legend_container.addStretch()
        legend_container.addWidget(legend_widget)
        legend_container.addStretch()
        legend_container.setAlignment(Qt.AlignCenter)
        legend_container.setContentsMargins(0, 0, 0, 0)
        self.instructions = QLabel(
            '<b>Como usar:</b> Clique no grid para adicionar/remover barreiras.<br>'
            'Pressione <b>S</b> para modo início, <b>G</b> para modo objetivo, <b>B</b> para barreira.<br>'
            'Pressione <b>Enter</b> ou clique em "Rodar A*" para executar. <b>R</b> ou "Resetar" para reiniciar.'
        )
        self.instructions.setAlignment(Qt.AlignCenter)
        self.info = QLabel('Modo atual: barreira')
        self.info.setAlignment(Qt.AlignCenter)
        self.btn_run = QPushButton('Rodar A*')
        self.btn_run.clicked.connect(self.grid_widget.run_astar)
        self.btn_reset = QPushButton('Resetar')
        self.btn_reset.clicked.connect(self.reset_grid)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.instructions, alignment=Qt.AlignCenter)
        layout.addWidget(self.info, alignment=Qt.AlignCenter)
        layout.addWidget(self.grid_widget, alignment=Qt.AlignCenter)
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.addWidget(self.btn_run)
        btn_layout.addWidget(self.btn_reset)
        layout.addLayout(btn_layout)
        layout.addLayout(legend_container)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def _legend_label(self, text, color):
        pix = QPixmap(24, 24)
        pix.fill(Qt.white)
        painter = QPainter(pix)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor(60, 60, 60))
        painter.setBrush(color)
        painter.drawRect(3, 3, 18, 18)
        painter.end()
        label = QLabel()
        label.setPixmap(pix)
        label.setFixedWidth(30)
        label.setToolTip(text)
        label_text = QLabel(text)
        label_text.setStyleSheet('margin-left:8px; margin-right:16px; font-weight: 500; color: #222;')
        label_text.setMinimumWidth(60)
        h = QHBoxLayout()
        h.setContentsMargins(0,0,0,0)
        h.setSpacing(0)
        h.addWidget(label)
        h.addWidget(label_text)
        h.addStretch()
        w = QWidget()
        w.setLayout(h)
        w.setMinimumWidth(120)
        return w

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_S:
            self.grid_widget.mode = 'start'
            self.info.setText('Modo atual: início')
        elif event.key() == Qt.Key_G:
            self.grid_widget.mode = 'goal'
            self.info.setText('Modo atual: objetivo')
        elif event.key() == Qt.Key_B:
            self.grid_widget.mode = 'barrier'
            self.info.setText('Modo atual: barreira')
        elif event.key() == Qt.Key_R:
            self.reset_grid()
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.grid_widget.run_astar()

    def reset_grid(self):
        self.grid_widget.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        self.grid_widget.start = (0, 0)
        self.grid_widget.goal = (GRID_SIZE-1, GRID_SIZE-1)
        self.grid_widget.clear_path()
        self.info.setText('Modo atual: barreira')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
