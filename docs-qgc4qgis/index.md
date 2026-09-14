# QGC4QGIS

**QGC4QGIS** brings QGroundControl's photogrammetric flight planning into QGIS:
starting from an area-of-interest polygon, it generates the **flight grid**
(transects with side and front overlap), the **photo centers**, the **mission
statistics**, and exports the native QGroundControl **`.plan`** file — in
addition to Litchi (`.csv`/`.kml`) and DJI WPML (`.kmz`) exports.

The plugin also ships the Processing algorithms (`QGC4QGIS` provider, *Flight
Planning* group) and automatic download of the Copernicus DEM — the same
elevation source QGroundControl uses natively (Auterion), so the terrain
sampled in the exported `.plan` matches what QGC recalculates.

!!! info "Compatibility"
    QGIS **3.34 → 4.x** (`qgisMinimumVersion=3.34`, `qgisMaximumVersion=4.99`)
    and **Qt5 and Qt6** (`supportsQt6=True`).

QGC4QGIS is published in the official QGIS plugin repository, at
[plugins.qgis.org](https://plugins.qgis.org/plugins/qgc4qgis/), with the
**QGIS 4 Ready** badge.

<div class="grid cards" markdown>

- **[Installation](installation.md)**

    ---

    Install from the official QGIS plugin repository, from the release zip,
    or by copy/symlink — and the plugin's requirements.

- **[Flight planning panel](workflow.md)**

    ---

    The five-step workflow in the dock: polygon, camera, altitude/GSD, grid,
    and export.

- **[Exports](exports.md)**

    ---

    QGroundControl's `.plan`, Litchi `.csv`/`.kml`, and DJI Fly WPML `.kmz`,
    and what each one supports for terrain.

- **[Terrain and elevation](elevation.md)**

    ---

    The Copernicus GLO-30 DEM via Auterion, and flight following the
    terrain.

- **[Processing algorithms](algorithms.md)**

    ---

    The provider's 7 algorithms, for the Graphical Modeler, `pyqgis`, and
    batch processing.

- **[Changelog](changelog.md)**

    ---

    What changed in each version (current: 0.7.1).

</div>

QGC4QGIS is free software under **GPL-3.0**. The code lives at
[github.com/d-camargo/qgroundcontrol-4QGIS](https://github.com/d-camargo/qgroundcontrol-4QGIS).
