from qgis.core import (
    QgsGeometry,
    QgsPointXY
)


def convert_point(entity):

    point = entity.dxf.location

    qgis_point = QgsPointXY(
        point.x,
        point.y
    )

    return QgsGeometry.fromPointXY(
        qgis_point
    )


def convert_line(entity):

    start = entity.dxf.start
    end = entity.dxf.end

    points = [
        QgsPointXY(
            start.x,
            start.y
        ),
        QgsPointXY(
            end.x,
            end.y
        )
    ]

    return QgsGeometry.fromPolylineXY(
        points
    )


def convert_lwpolyline(entity):

    points = []

    for point in entity.get_points():

        x = point[0]
        y = point[1]

        points.append(
            QgsPointXY(x, y)
        )

    if len(points) < 2:
        return None

    # Closed LWPOLYLINE becomes a polygon
    if entity.closed:

        if len(points) < 3:
            return None

        if points[0] != points[-1]:

            points.append(
                points[0]
            )

        return QgsGeometry.fromPolygonXY(
            [points]
        )

    # Open LWPOLYLINE becomes a line
    return QgsGeometry.fromPolylineXY(
        points
    )


def convert_solid(entity):

    points = []

    # DXF SOLID has up to four corner points
    for attribute in [
        "vtx0",
        "vtx1",
        "vtx2",
        "vtx3"
    ]:

        if hasattr(entity.dxf, attribute):

            point = getattr(
                entity.dxf,
                attribute
            )

            points.append(
                QgsPointXY(
                    point.x,
                    point.y
                )
            )

    # Remove duplicate points
    unique_points = []

    for point in points:

        if point not in unique_points:

            unique_points.append(point)

    points = unique_points

    # A polygon requires at least 3 points
    if len(points) < 3:

        return None

    # Close the polygon
    if points[0] != points[-1]:

        points.append(
            points[0]
        )

    return QgsGeometry.fromPolygonXY(
        [points]
    )
