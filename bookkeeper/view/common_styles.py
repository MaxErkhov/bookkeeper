"""
Стили для отображения виджетов
"""

COMMON_STYLESHEET = """
    QLabel {
        font-size: 18px;
        font-weight: bold;
    }
    QTableWidget {
        gridline-color: #ddd;
        background-color: #f5f5f5; /* Default background color */
        font: 14px;
        border-radius: 5px;
    }
    QTableWidget::item {
        background-color: #ffffff;
        border: 1px solid #ddd;
        border-radius: 5px;
        color: #000000;
    }
    QTableWidget::item:selected {
        background-color: #e0e0e0;
        color: #000000;
    }
    QHeaderView::section {
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #007bff, stop: 1 #0056b3);
        color: white;
        padding: 5px;
        border: 1px solid #ddd;
        font: 14px;
        border-radius: 5px;
    }
"""
