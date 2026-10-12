from qgis.PyQt.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHBoxLayout
)


class DXFAnalysisDialog(QDialog):

    def __init__(self, filename, entity_types, layer_counts, parent=None):
        super().__init__(parent)

        self.setWindowTitle("DXF2GIS - DXF Analysis")
        self.resize(500, 400)

        self.filename = filename
        self.entity_types = entity_types
        self.layer_counts = layer_counts

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout()

        title = QLabel("DXF Drawing Analysis")
        title.setStyleSheet(
            "font-size: 18px; font-weight: bold;"
        )

        file_label = QLabel(
            f"File: {self.filename}"
        )

        total_entities = sum(self.entity_types.values())

        total_label = QLabel(
            f"Total entities: {total_entities}"
        )

        self.table = QTableWidget()

        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(
            ["Entity Type", "Count"]
        )

        self.table.setRowCount(
            len(self.entity_types)
        )

        for row, (entity_type, count) in enumerate(
            self.entity_types.items()
        ):

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(entity_type)
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(str(count))
            )

        self.table.resizeColumnsToContents()

        layer_title = QLabel("CAD Layers")

        self.layer_table = QTableWidget()

        self.layer_table.setColumnCount(2)

        self.layer_table.setHorizontalHeaderLabels(
            ["Layer", "Entity Count"]
        )

        self.layer_table.setRowCount(
            len(self.layer_counts)
        )

        for row, (layer, count) in enumerate(
                self.layer_counts.items()
        ):
            self.layer_table.setItem(
                row,
                0,
                QTableWidgetItem(layer)
            )

            self.layer_table.setItem(
                row,
                1,
                QTableWidgetItem(str(count))
            )

        self.layer_table.resizeColumnsToContents()

        close_button = QPushButton("Close")

        close_button.clicked.connect(
            self.close
        )

        button_layout = QHBoxLayout()

        button_layout.addStretch()
        button_layout.addWidget(close_button)

        layout.addWidget(title)
        layout.addWidget(file_label)
        layout.addWidget(total_label)
        layout.addWidget(self.table)
        layout.addWidget(layer_title)
        layout.addWidget(self.layer_table)
        layout.addLayout(button_layout)

        self.setLayout(layout)
