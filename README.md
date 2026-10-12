# DXF2GIS

DXF2GIS is a QGIS plugin for converting supported DXF CAD geometry into GIS vector layers and exporting the results to a GeoPackage.

It is designed to provide a simple workflow for bringing basic CAD survey and engineering geometry into QGIS while retaining useful CAD information such as the original layer name and entity type.

## Features

DXF2GIS currently supports the following DXF entities:

- POINT
- LINE
- LWPOLYLINE
- SOLID

Supported geometry is converted into:

- Point layers
- Line layers
- Polygon layers

The plugin also:

- Allows the user to select the coordinate reference system (CRS) used by the DXF coordinates.
- Preserves the original CAD layer name as an attribute.
- Preserves the DXF entity type as an attribute.
- Creates a GeoPackage containing the converted GIS layers.
- Provides a DXF analysis dialog showing entity and CAD layer information.

## How It Works

The basic workflow is:

1. Open DXF2GIS from the QGIS toolbar or Plugins menu.
2. Select a DXF file.
3. Select the CRS used by the DXF coordinates.
4. DXF2GIS reads the supported entities from the DXF file.
5. The entities are converted into QGIS vector geometries.
6. The converted layers are added to the QGIS project.
7. A GeoPackage is created beside the original DXF file.

The GeoPackage is created using the following naming pattern:

```text
original_filename_DXF2GIS.gpkg
```

## Attributes

Each converted feature contains the following attributes:

| Field | Description |
|---|---|
| `id` | Sequential feature identifier |
| `layer` | Original DXF/CAD layer name |
| `ent_type` | Original DXF entity type |

For example, a LINE entity from a CAD layer named `ROAD` will retain:

```text
layer    = ROAD
ent_type = LINE
```

## Coordinate Reference System

DXF2GIS asks the user to select the coordinate reference system used by the coordinates in the DXF file.

The selected CRS is assigned to the resulting QGIS layers and GeoPackage.

The CRS selection does not currently transform the coordinate values from one CRS to another. The selected CRS should therefore correspond to the coordinate system in which the DXF coordinates were created.

For example, if the DXF coordinates are in UTM Zone 32N, the corresponding UTM Zone 32N CRS should be selected.

## GeoPackage Output

DXF2GIS uses GeoPackage as its output format.

GeoPackage is an SQLite-based spatial data format that can contain multiple GIS layers in a single file.

Depending on the geometry contained in the DXF file, the generated GeoPackage can contain:

```text
DXF_Points
DXF_Lines
DXF_Polygons
```

Only layers for which supported geometry is found are created.

## Requirements

- QGIS 3.34 or later
- Python package `ezdxf`

DXF2GIS uses `ezdxf` to read DXF files.

### Installing ezdxf

The `ezdxf` package must be available to the Python environment used by QGIS.

For QGIS installations where `ezdxf` is not already available, install a compatible version into the QGIS Python environment before using DXF2GIS.

The plugin does not download or install Python packages automatically.

## Installation

### From a ZIP file

1. Download the DXF2GIS plugin ZIP package.
2. Open QGIS.
3. Go to:

```text
Plugins → Manage and Install Plugins
```

4. Select:

```text
Install from ZIP
```

5. Select the DXF2GIS ZIP file.
6. Confirm the installation.
7. Enable DXF2GIS from the QGIS Plugin Manager.

### From Source

Clone or download the source repository:

```text
https://github.com/Akachukwu123/dxftogisconverter
```

Place the `DXF2GIS` plugin folder inside the QGIS plugins directory.

Restart QGIS and enable the plugin from the Plugin Manager.

## Supported Geometry

| DXF Entity | GIS Geometry |
|---|---|
| POINT | Point |
| LINE | Line |
| LWPOLYLINE | Line or Polygon when closed |
| SOLID | Polygon |

## Current Limitations

Version 1.0.0 focuses on basic DXF geometry conversion.

The following features are not currently included:

- DXF TEXT extraction
- Advanced DXF entity conversion
- Batch DXF processing
- Processing Toolbox integration
- Automatic CRS transformation
- Shapefile export
- GeoJSON export
- Automatic splitting of output into separate layers for every CAD layer

These features may be considered for future versions.

## Version

Current version:

```text
1.0.0
```

## Source Code

The DXF2GIS source code is publicly available on GitHub:

https://github.com/Akachukwu123/dxftogisconverter

Issues and feature requests can be submitted through the repository's issue tracker.

## License

DXF2GIS is released under the GNU General Public License version 2 or later (GPL-2.0-or-later).

See the `LICENSE` file included with the plugin for the full license text.

## Author

Akachukwu Okoro