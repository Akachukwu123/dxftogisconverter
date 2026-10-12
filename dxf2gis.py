import os
import ezdxf

from collections import Counter

from qgis.PyQt.QtWidgets import QAction, QFileDialog
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QVariant

from qgis.gui import QgsProjectionSelectionDialog

from qgis.core import (
    QgsVectorLayer,
    QgsFeature,
    QgsProject,
    QgsField,
    QgsWkbTypes,
    QgsVectorFileWriter
)

from .dialogs.dxf_analysis import DXFAnalysisDialog

from .converters.dxf_geometry import (
    convert_point,
    convert_line,
    convert_lwpolyline,
    convert_solid
)


class DXF2GIS:

    def __init__(self, iface):
        self.iface = iface
        self.action = None

    def initGui(self):

        self.action = QAction(
            QIcon(os.path.join(os.path.dirname(__file__), "icon.png")),
            "DXF2GIS",
            self.iface.mainWindow()
        )

        self.action.triggered.connect(self.run)

        self.iface.addToolBarIcon(self.action)

        self.iface.addPluginToMenu(
            "&DXF2GIS",
            self.action
        )

    def unload(self):

        self.iface.removeToolBarIcon(self.action)

        self.iface.removePluginMenu(
            "&DXF2GIS",
            self.action
        )

    def run(self):

        dxf_file, _ = QFileDialog.getOpenFileName(
            self.iface.mainWindow(),
            "Select DXF File",
            "",
            "DXF Files (*.dxf);;All Files (*)"
        )

        if not dxf_file:
            return

        # Ask the user to select the CRS used by the DXF coordinates
        crs_dialog = QgsProjectionSelectionDialog(
            self.iface.mainWindow()
        )

        crs_dialog.setWindowTitle(
            "Select Coordinate Reference System"
        )

        if not crs_dialog.exec():
            return

        selected_crs = crs_dialog.crs()

        if not selected_crs.isValid():

            self.iface.messageBar().pushWarning(
                "DXF2GIS",
                "A valid coordinate reference system must be selected."
            )

            return

        print(
            f"Selected CRS: "
            f"{selected_crs.authid()} - "
            f"{selected_crs.description()}"
        )

        try:

            doc = ezdxf.readfile(dxf_file)
            modelspace = doc.modelspace()

            entity_types = Counter()

            for entity in modelspace:
                entity_types[entity.dxftype()] += 1

            layer_counts = Counter()

            for entity in modelspace:
                layer_counts[entity.dxf.layer] += 1

            converted_points = []
            converted_lines = []
            converted_polygons = []
            converted_counts = Counter()

            for entity in modelspace:

                entity_type = entity.dxftype()
                geometry = None

                if entity_type == "POINT":

                    geometry = convert_point(entity)

                elif entity_type == "LINE":

                    geometry = convert_line(entity)

                elif entity_type == "LWPOLYLINE":

                    geometry = convert_lwpolyline(entity)

                elif entity_type == "SOLID":

                    geometry = convert_solid(entity)

                else:

                    continue

                if geometry is not None:

                    feature_data = {
                        "geometry": geometry,
                        "layer": entity.dxf.layer,
                        "ent_type": entity_type
                    }

                    if geometry.type() == QgsWkbTypes.PointGeometry:
                        converted_points.append(feature_data)

                    elif geometry.type() == QgsWkbTypes.LineGeometry:
                        converted_lines.append(feature_data)

                    elif geometry.type() == QgsWkbTypes.PolygonGeometry:
                        converted_polygons.append(feature_data)

                    converted_counts[entity_type] += 1

            print("Conversion results:")

            for entity_type, count in converted_counts.items():

                print(
                    f"{entity_type}: {count}"
                )

            print(
                f"Successfully converted "
                f"{len(converted_points) + len(converted_lines) + len(converted_polygons)} "
                f"geometries."
            )

            point_layer = None

            if converted_points:

                point_layer = QgsVectorLayer(
                    "Point",
                    "DXF Points",
                    "memory"
                )

                point_layer.setCrs(
                    selected_crs
                )

                point_provider = point_layer.dataProvider()

                point_provider.addAttributes([
                    QgsField(
                        "id",
                        QVariant.Int
                    ),
                    QgsField(
                        "layer",
                        QVariant.String
                    ),
                    QgsField(
                        "ent_type",
                        QVariant.String
                    )
                ])

                point_layer.updateFields()

                for index, data in enumerate(
                    converted_points,
                    start=1
                ):

                    feature = QgsFeature(
                        point_layer.fields()
                    )

                    feature.setGeometry(
                        data["geometry"]
                    )

                    feature["id"] = index
                    feature["layer"] = data["layer"]
                    feature["ent_type"] = data["ent_type"]

                    point_provider.addFeature(
                        feature
                    )

                point_layer.updateExtents()

                QgsProject.instance().addMapLayer(
                    point_layer
                )

            line_layer = None

            if converted_lines:

                line_layer = QgsVectorLayer(
                    "LineString",
                    "DXF Lines",
                    "memory"
                )

                line_layer.setCrs(
                    selected_crs
                )

                line_provider = line_layer.dataProvider()

                line_provider.addAttributes([
                    QgsField(
                        "id",
                        QVariant.Int
                    ),
                    QgsField(
                        "layer",
                        QVariant.String
                    ),
                    QgsField(
                        "ent_type",
                        QVariant.String
                    )
                ])

                line_layer.updateFields()

                for index, data in enumerate(
                    converted_lines,
                    start=1
                ):

                    feature = QgsFeature(
                        line_layer.fields()
                    )

                    feature.setGeometry(
                        data["geometry"]
                    )

                    feature["id"] = index
                    feature["layer"] = data["layer"]
                    feature["ent_type"] = data["ent_type"]

                    line_provider.addFeature(
                        feature
                    )

                line_layer.updateExtents()

                QgsProject.instance().addMapLayer(
                    line_layer
                )

            polygon_layer = None

            if converted_polygons:

                polygon_layer = QgsVectorLayer(
                    "Polygon",
                    "DXF Polygons",
                    "memory"
                )

                polygon_layer.setCrs(
                    selected_crs
                )

                polygon_provider = polygon_layer.dataProvider()

                polygon_provider.addAttributes([
                    QgsField(
                        "id",
                        QVariant.Int
                    ),
                    QgsField(
                        "layer",
                        QVariant.String
                    ),
                    QgsField(
                        "ent_type",
                        QVariant.String
                    )
                ])

                polygon_layer.updateFields()

                for index, data in enumerate(
                    converted_polygons,
                    start=1
                ):

                    feature = QgsFeature(
                        polygon_layer.fields()
                    )

                    feature.setGeometry(
                        data["geometry"]
                    )

                    feature["id"] = index
                    feature["layer"] = data["layer"]
                    feature["ent_type"] = data["ent_type"]

                    polygon_provider.addFeature(
                        feature
                    )

                polygon_layer.updateExtents()

                QgsProject.instance().addMapLayer(
                    polygon_layer
                )

            gpkg_file = (
                os.path.splitext(dxf_file)[0]
                + "_DXF2GIS.gpkg"
            )

            print(
                f"Creating GeoPackage: {gpkg_file}"
            )

            gpkg_created = False

            if point_layer:

                options = (
                    QgsVectorFileWriter.SaveVectorOptions()
                )

                options.driverName = "GPKG"
                options.layerName = "DXF_Points"

                if gpkg_created:
                    options.actionOnExistingFile = (
                        QgsVectorFileWriter.CreateOrOverwriteLayer
                    )
                else:
                    options.actionOnExistingFile = (
                        QgsVectorFileWriter.CreateOrOverwriteFile
                    )

                result = (
                    QgsVectorFileWriter.writeAsVectorFormatV3(
                        point_layer,
                        gpkg_file,
                        QgsProject.instance().transformContext(),
                        options
                    )
                )

                if result[0] != QgsVectorFileWriter.NoError:

                    raise Exception(
                        f"Failed to export DXF_Points: {result}"
                    )

                gpkg_created = True

                print(
                    "DXF_Points exported successfully."
                )

            if line_layer:

                options = (
                    QgsVectorFileWriter.SaveVectorOptions()
                )

                options.driverName = "GPKG"
                options.layerName = "DXF_Lines"

                if gpkg_created:
                    options.actionOnExistingFile = (
                        QgsVectorFileWriter.CreateOrOverwriteLayer
                    )
                else:
                    options.actionOnExistingFile = (
                        QgsVectorFileWriter.CreateOrOverwriteFile
                    )

                result = (
                    QgsVectorFileWriter.writeAsVectorFormatV3(
                        line_layer,
                        gpkg_file,
                        QgsProject.instance().transformContext(),
                        options
                    )
                )

                if result[0] != QgsVectorFileWriter.NoError:

                    raise Exception(
                        f"Failed to export DXF_Lines: {result}"
                    )

                gpkg_created = True

                print(
                    "DXF_Lines exported successfully."
                )

            if polygon_layer:

                options = (
                    QgsVectorFileWriter.SaveVectorOptions()
                )

                options.driverName = "GPKG"
                options.layerName = "DXF_Polygons"

                if gpkg_created:
                    options.actionOnExistingFile = (
                        QgsVectorFileWriter.CreateOrOverwriteLayer
                    )
                else:
                    options.actionOnExistingFile = (
                        QgsVectorFileWriter.CreateOrOverwriteFile
                    )

                result = (
                    QgsVectorFileWriter.writeAsVectorFormatV3(
                        polygon_layer,
                        gpkg_file,
                        QgsProject.instance().transformContext(),
                        options
                    )
                )

                if result[0] != QgsVectorFileWriter.NoError:

                    raise Exception(
                        f"Failed to export DXF_Polygons: {result}"
                    )

                gpkg_created = True

                print(
                    "DXF_Polygons exported successfully."
                )

            if gpkg_created:

                self.iface.messageBar().pushSuccess(
                    "DXF2GIS",
                    f"GeoPackage created: {gpkg_file}"
                )

                print(
                    f"GeoPackage created successfully:"
                    f"\n{gpkg_file}"
                )

                print(
                    f"GeoPackage CRS: "
                    f"{selected_crs.authid()} - "
                    f"{selected_crs.description()}"
                )

            dialog = DXFAnalysisDialog(
                dxf_file,
                entity_types,
                layer_counts,
                self.iface.mainWindow()
            )

            dialog.exec()

        except Exception as e:

            self.iface.messageBar().pushCritical(
                "DXF2GIS",
                f"Failed to process DXF: {str(e)}"
            )

            print(
                f"DXF2GIS ERROR: {str(e)}"
            )
