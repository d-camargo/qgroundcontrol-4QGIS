# Processing algorithms reference

The QGC4QGIS plugin integrates directly into the **QGIS Processing Toolbox** under the `QGC4QGIS` provider. This allows automating photogrammetric flight planning, photo center generation, DEM downloads, and multi-format mission exports within QGIS Graphical Modeler, Python scripts (`pyqgis`), and batch processing pipelines.

---

## Provider overview

- **Provider ID**: `qgc4qgis`
- **Provider Name**: `QGC4QGIS`
- **Algorithm Group**: `Flight Planning` (`planejamento_voo`)

Below is the complete reference for all 7 algorithms registered by the `qgc4qgis` provider.

---

## 1. Generate flight grid

- **Full Algorithm ID**: `qgc4qgis:gerar_grade_voo`
- **Display Name**: Generate flight grid
- **Group**: Flight Planning (`planejamento_voo`)

### Description

Generates photogrammetric flight grid lines from a polygon layer, camera settings, altitude or GSD, overlaps, grid angle, turnaround distance, and entry corner.

### Inputs and Outputs

| Parameter (GUI) | Identifier | Direction | Description |
| :--- | :--- | :--- | :--- |
| Polygon layer | `INPUT` | Input | Vector polygon layer defining the survey area boundary. |
| Camera | `CAMERA` | Input | Selected camera spec preset from database (or manual spec). |
| Flight altitude (m) | `ALTITUDE` | Input | Flight height in meters above takeoff/ground (default: 100.0 m). |
| GSD (cm/px) - if > 0, overrides/calculates altitude | `GSD` | Input | Ground Sample Distance in cm/px. If > 0, automatically calculates and overrides altitude. |
| Side overlap (%) | `OVERLAP_SIDE` | Input | Sidelap percentage between adjacent flight lines (0–99%, default: 70.0%). |
| Frontal overlap (%) | `OVERLAP_FRONTAL` | Input | Frontal overlap percentage along flight lines (0–99%, default: 70.0%). |
| Grid angle (degrees) | `ANGLE` | Input | Flight line orientation angle in degrees (-180° to 180°, default: 0.0°). |
| Turnaround distance (m) | `TURNAROUND` | Input | Extra line extension distance in meters outside the polygon for turning maneuvers. |
| Entry point | `ENTRY_LOCATION` | Input | Grid starting corner (`Top-Left`, `Top-Right`, `Bottom-Left`, `Bottom-Right`). |
| Cross grid (Refly 90°) | `REFLY` | Input | Enables a secondary perpendicular (90°) grid pass for double-grid surveys. |
| Manual camera: Sensor width (mm) | `SENSOR_WIDTH` | Input | Sensor width in mm (optional, used when `CAMERA` is set to manual camera). |
| Manual camera: Sensor height (mm) | `SENSOR_HEIGHT` | Input | Sensor height in mm (optional, used when `CAMERA` is set to manual camera). |
| Manual camera: Image width (px) | `IMAGE_WIDTH` | Input | Image width in pixels (optional, used when `CAMERA` is set to manual camera). |
| Manual camera: Image height (px) | `IMAGE_HEIGHT` | Input | Image height in pixels (optional, used when `CAMERA` is set to manual camera). |
| Manual camera: Focal length (mm) | `FOCAL_LENGTH` | Input | Lens focal length in mm (optional, used when `CAMERA` is set to manual camera). |
| Flight grid (Lines) | `OUTPUT` | Output | Destination line vector layer for generated flight transects. |

---

## 2. Generate photo centers and footprints

- **Full Algorithm ID**: `qgc4qgis:gerar_centros_foto`
- **Display Name**: Generate photo centers and footprints
- **Group**: Flight Planning (`planejamento_voo`)

### Description

Generates point layers of photo center positions and footprint polygons, oriented by the flight transects' azimuth. Accepts polygon coverage layers or line grid layers.

### Inputs and Outputs

| Parameter (GUI) | Identifier | Direction | Description |
| :--- | :--- | :--- | :--- |
| Input layer (Polygons or Lines) | `INPUT` | Input | Polygon area layer or line flight grid layer. |
| Camera | `CAMERA` | Input | Selected camera spec preset from database (or manual spec). |
| Flight altitude (m) | `ALTITUDE` | Input | Flight altitude in meters (default: 100.0 m). |
| GSD (cm/px) - if > 0, overrides/calculates altitude | `GSD` | Input | Ground Sample Distance in cm/px (overrides altitude if > 0). |
| Side overlap (%) | `OVERLAP_SIDE` | Input | Sidelap percentage between adjacent flight lines (default: 70.0%). |
| Frontal overlap (%) | `OVERLAP_FRONTAL` | Input | Frontal overlap percentage along flight lines (default: 70.0%). |
| Grid angle (degrees) | `ANGLE` | Input | Flight line orientation angle in degrees (default: 0.0°). |
| Turnaround distance (m) | `TURNAROUND` | Input | Turnaround extension distance in meters. |
| Entry point | `ENTRY_LOCATION` | Input | Grid starting corner (`Top-Left`, `Top-Right`, `Bottom-Left`, `Bottom-Right`). |
| Cross grid (Refly 90°) | `REFLY` | Input | Enables a secondary perpendicular (90°) grid pass. |
| Manual camera: Sensor width (mm) | `SENSOR_WIDTH` | Input | Manual sensor width in mm (optional). |
| Manual camera: Sensor height (mm) | `SENSOR_HEIGHT` | Input | Manual sensor height in mm (optional). |
| Manual camera: Image width (px) | `IMAGE_WIDTH` | Input | Manual image width in pixels (optional). |
| Manual camera: Image height (px) | `IMAGE_HEIGHT` | Input | Manual image height in pixels (optional). |
| Manual camera: Focal length (mm) | `FOCAL_LENGTH` | Input | Manual lens focal length in mm (optional). |
| Photo centers (Points) | `OUTPUT_CENTERS` | Output | Output point vector layer of calculated camera exposure points. |
| Photo footprints (Polygons) | `OUTPUT_FOOTPRINTS` | Output | Output polygon vector layer of photo ground coverage footprints. |

---

## 3. Export QGC plan (.plan)

- **Full Algorithm ID**: `qgc4qgis:exportar_plano_qgc`
- **Display Name**: Export QGC plan (.plan)
- **Group**: Flight Planning (`planejamento_voo`)

### Description

Exports a complete mission plan in native QGroundControl format (`.plan`) from coverage polygons or flight grid lines, with optional DEM elevation raster support for terrain following.

### Inputs and Outputs

| Parameter (GUI) | Identifier | Direction | Description |
| :--- | :--- | :--- | :--- |
| Input layer (Polygons or Lines) | `INPUT` | Input | Polygon area layer or line grid layer. |
| Camera | `CAMERA` | Input | Selected camera specification preset or manual profile. |
| Flight altitude (m) | `ALTITUDE` | Input | Flight height in meters (default: 100.0 m). |
| GSD (cm/px) - if > 0, overrides/calculates altitude | `GSD` | Input | Target GSD in cm/px (overrides flight altitude if > 0). |
| Side overlap (%) | `OVERLAP_SIDE` | Input | Sidelap percentage between flight lines (default: 70.0%). |
| Frontal overlap (%) | `OVERLAP_FRONTAL` | Input | Frontal overlap percentage along flight lines (default: 70.0%). |
| Grid angle (degrees) | `ANGLE` | Input | Flight line angle in degrees (default: 0.0°). |
| Turnaround distance (m) | `TURNAROUND` | Input | Turnaround extension distance in meters. |
| Entry point | `ENTRY_LOCATION` | Input | Mission entry corner (`Top-Left`, `Top-Right`, `Bottom-Left`, `Bottom-Right`). |
| Cross grid (Refly 90°) | `REFLY` | Input | Option to generate double-grid pass (90° cross grid). |
| Manual camera: Sensor width (mm) | `SENSOR_WIDTH` | Input | Manual sensor width in mm (optional). |
| Manual camera: Sensor height (mm) | `SENSOR_HEIGHT` | Input | Manual sensor height in mm (optional). |
| Manual camera: Image width (px) | `IMAGE_WIDTH` | Input | Manual image width in pixels (optional). |
| Manual camera: Image height (px) | `IMAGE_HEIGHT` | Input | Manual image height in pixels (optional). |
| Manual camera: Focal length (mm) | `FOCAL_LENGTH` | Input | Manual lens focal length in mm (optional). |
| Cruise speed (m/s) | `CRUISE_SPEED` | Input | Desired cruise flight speed in m/s (default: 15.0 m/s). |
| Hover speed (m/s) | `HOVER_SPEED` | Input | Vehicle hover speed in m/s (default: 5.0 m/s). |
| Firmware Type | `FIRMWARE_TYPE` | Input | Target autopilot firmware (`PX4 (12)` or `ArduPilot (3)`). |
| Vehicle Type | `VEHICLE_TYPE` | Input | Target vehicle type (`Multirotor (2)`, `Fixed Wing (1)`, `VTOL (19)`). |
| Elevation layer (DEM) — if set, exports in above-terrain mode | `ELEVATION_LAYER` | Input | Optional DEM raster layer for terrain-following mode export. |
| Terrain tolerance (m) | `TOLERANCE` | Input | Elevation tolerance in meters for terrain sampling (default: 10.0 m). |
| Output file (.plan) | `OUTPUT` | Output | Output file path for generated `.plan` file. |

---

## 4. Export Litchi mission (.csv)

- **Full Algorithm ID**: `qgc4qgis:exportar_litchi_csv`
- **Display Name**: Export Litchi mission (.csv)
- **Group**: Flight Planning (`planejamento_voo`)

### Description

Exports a flight mission in Litchi CSV format (`.csv`) from coverage polygons or flight grid lines. Supports terrain relative calculation when an elevation layer is provided.

### Inputs and Outputs

| Parameter (GUI) | Identifier | Direction | Description |
| :--- | :--- | :--- | :--- |
| Input layer (Polygons or Lines) | `INPUT` | Input | Polygon area layer or line grid layer. |
| Camera | `CAMERA` | Input | Selected camera specification preset or manual profile. |
| Flight altitude (m) | `ALTITUDE` | Input | Flight height in meters (default: 100.0 m). |
| GSD (cm/px) - if > 0, overrides/calculates altitude | `GSD` | Input | Target GSD in cm/px (overrides flight altitude if > 0). |
| Side overlap (%) | `OVERLAP_SIDE` | Input | Sidelap percentage between flight lines (default: 70.0%). |
| Frontal overlap (%) | `OVERLAP_FRONTAL` | Input | Frontal overlap percentage along flight lines (default: 70.0%). |
| Grid angle (degrees) | `ANGLE` | Input | Flight line angle in degrees (default: 0.0°). |
| Turnaround distance (m) | `TURNAROUND` | Input | Turnaround extension distance in meters. |
| Entry point | `ENTRY_LOCATION` | Input | Mission entry corner (`Top-Left`, `Top-Right`, `Bottom-Left`, `Bottom-Right`). |
| Cross grid (Refly 90°) | `REFLY` | Input | Option to generate double-grid pass (90° cross grid). |
| Manual camera: Sensor width (mm) | `SENSOR_WIDTH` | Input | Manual sensor width in mm (optional). |
| Manual camera: Sensor height (mm) | `SENSOR_HEIGHT` | Input | Manual sensor height in mm (optional). |
| Manual camera: Image width (px) | `IMAGE_WIDTH` | Input | Manual image width in pixels (optional). |
| Manual camera: Image height (px) | `IMAGE_HEIGHT` | Input | Manual image height in pixels (optional). |
| Manual camera: Focal length (mm) | `FOCAL_LENGTH` | Input | Manual lens focal length in mm (optional). |
| Trigger mode | `TRIGGER_MODE` | Input | Photo trigger mechanism (`By distance`, `By time`, `By photo`). |
| Speed (m/s) | `SPEED` | Input | Flight speed along waypoints in m/s (default: 5.0 m/s). |
| Gimbal angle (degrees) | `GIMBAL_PITCH` | Input | Gimbal pitch angle in degrees (-90° to 20°, default: -90.0°). |
| Wait at waypoint (s) | `WAYPOINT_WAIT` | Input | Pause duration in seconds at each waypoint (default: 0.0 s). |
| Elevation layer (DEM) — if set, exports in above-terrain mode | `ELEVATION_LAYER` | Input | Optional DEM raster layer for terrain relative height calculation. |
| Terrain tolerance (m) | `TOLERANCE` | Input | Elevation tolerance in meters for terrain sampling (default: 10.0 m). |
| Takeoff point (optional — default: first waypoint) | `PONTO_DECOLAGEM` | Input | Custom reference point coordinates for relative altitude calculations (optional). |
| Output file (.csv) | `OUTPUT` | Output | Output file path for generated Litchi `.csv` mission spreadsheet. |

---

## 5. Export Litchi Mission Hub mission (.kml)

- **Full Algorithm ID**: `qgc4qgis:exportar_litchi_kml`
- **Display Name**: Export Litchi Mission Hub mission (.kml)
- **Group**: Flight Planning (`planejamento_voo`)

### Description

Exports a flight mission in Litchi Mission Hub KML format (`.kml`) from coverage polygons or flight grid lines for web import at flylitchi.com/hub.

### Inputs and Outputs

| Parameter (GUI) | Identifier | Direction | Description |
| :--- | :--- | :--- | :--- |
| Input layer (Polygons or Lines) | `INPUT` | Input | Polygon area layer or line grid layer. |
| Camera | `CAMERA` | Input | Selected camera specification preset or manual profile. |
| Flight altitude (m) | `ALTITUDE` | Input | Flight height in meters (default: 100.0 m). |
| GSD (cm/px) - if > 0, overrides/calculates altitude | `GSD` | Input | Target GSD in cm/px (overrides flight altitude if > 0). |
| Side overlap (%) | `OVERLAP_SIDE` | Input | Sidelap percentage between flight lines (default: 70.0%). |
| Frontal overlap (%) | `OVERLAP_FRONTAL` | Input | Frontal overlap percentage along flight lines (default: 70.0%). |
| Grid angle (degrees) | `ANGLE` | Input | Flight line angle in degrees (default: 0.0°). |
| Turnaround distance (m) | `TURNAROUND` | Input | Turnaround extension distance in meters. |
| Entry point | `ENTRY_LOCATION` | Input | Mission entry corner (`Top-Left`, `Top-Right`, `Bottom-Left`, `Bottom-Right`). |
| Cross grid (Refly 90°) | `REFLY` | Input | Option to generate double-grid pass (90° cross grid). |
| Manual camera: Sensor width (mm) | `SENSOR_WIDTH` | Input | Manual sensor width in mm (optional). |
| Manual camera: Sensor height (mm) | `SENSOR_HEIGHT` | Input | Manual sensor height in mm (optional). |
| Manual camera: Image width (px) | `IMAGE_WIDTH` | Input | Manual image width in pixels (optional). |
| Manual camera: Image height (px) | `IMAGE_HEIGHT` | Input | Manual image height in pixels (optional). |
| Manual camera: Focal length (mm) | `FOCAL_LENGTH` | Input | Manual lens focal length in mm (optional). |
| Trigger mode | `TRIGGER_MODE` | Input | Photo trigger mechanism (`By distance`, `By time`, `By photo`, default: `By photo`). |
| Speed (m/s) | `SPEED` | Input | Flight speed along waypoints in m/s (default: 5.0 m/s). |
| Elevation layer (DEM) — if set, exports in above-terrain mode | `ELEVATION_LAYER` | Input | Optional DEM raster layer for terrain relative height calculation. |
| Terrain tolerance (m) | `TOLERANCE` | Input | Elevation tolerance in meters for terrain sampling (default: 10.0 m). |
| Takeoff point (optional — default: first waypoint) | `PONTO_DECOLAGEM` | Input | Custom reference point coordinates for relative altitude calculations (optional). |
| Output file (.kml) | `OUTPUT` | Output | Output file path for generated Litchi Mission Hub `.kml` file. |

---

## 6. Export DJI Fly mission (.kmz)

- **Full Algorithm ID**: `qgc4qgis:exportar_dji_kmz`
- **Display Name**: Export DJI Fly mission (.kmz)
- **Group**: Flight Planning (`planejamento_voo`)

### Description

Exports a flight mission in DJI WPML format (`.kmz`) containing `template.kml` and `waylines.wpml` for execution in DJI Fly app and compatible controllers.

### Inputs and Outputs

| Parameter (GUI) | Identifier | Direction | Description |
| :--- | :--- | :--- | :--- |
| Input layer (Polygons or Lines) | `INPUT` | Input | Polygon area layer or line grid layer. |
| Camera | `CAMERA` | Input | Selected camera specification preset or manual profile. |
| Flight altitude (m) | `ALTITUDE` | Input | Flight height in meters (default: 100.0 m). |
| GSD (cm/px) - if > 0, overrides/calculates altitude | `GSD` | Input | Target GSD in cm/px (overrides flight altitude if > 0). |
| Side overlap (%) | `OVERLAP_SIDE` | Input | Sidelap percentage between flight lines (default: 70.0%). |
| Frontal overlap (%) | `OVERLAP_FRONTAL` | Input | Frontal overlap percentage along flight lines (default: 70.0%). |
| Grid angle (degrees) | `ANGLE` | Input | Flight line angle in degrees (default: 0.0°). |
| Turnaround distance (m) | `TURNAROUND` | Input | Turnaround extension distance in meters. |
| Entry point | `ENTRY_LOCATION` | Input | Mission entry corner (`Top-Left`, `Top-Right`, `Bottom-Left`, `Bottom-Right`). |
| Cross grid (Refly 90°) | `REFLY` | Input | Option to generate double-grid pass (90° cross grid). |
| Manual camera: Sensor width (mm) | `SENSOR_WIDTH` | Input | Manual sensor width in mm (optional). |
| Manual camera: Sensor height (mm) | `SENSOR_HEIGHT` | Input | Manual sensor height in mm (optional). |
| Manual camera: Image width (px) | `IMAGE_WIDTH` | Input | Manual image width in pixels (optional). |
| Manual camera: Image height (px) | `IMAGE_HEIGHT` | Input | Manual image height in pixels (optional). |
| Manual camera: Focal length (mm) | `FOCAL_LENGTH` | Input | Manual lens focal length in mm (optional). |
| Trigger mode | `TRIGGER_MODE` | Input | Photo trigger mechanism (`By distance`, `By time`, `By photo`, default: `By photo`). |
| Speed (m/s) | `SPEED` | Input | Flight speed along waypoints in m/s (default: 5.0 m/s). |
| Gimbal angle (degrees) | `GIMBAL_PITCH` | Input | Gimbal pitch angle in degrees (-90° to 20°, default: -90.0°). |
| Wait at waypoint (s) | `WAYPOINT_WAIT` | Input | Pause duration in seconds at each waypoint (default: 0.0 s). |
| Action on finish | `FINISH_ACTION` | Input | Post-mission action (`Return to home (goHome)`, `No action (noAction)`, `Auto land (autoLand)`, `Go to first waypoint (gotoFirstWaypoint)`). |
| Action on RC signal lost | `RC_LOST_ACTION` | Input | Action if RC signal is lost (`Return (goBack)`, `Land (landing)`, `Hover (hover)`). |
| Transitional speed (m/s) | `TRANSITIONAL_SPEED` | Input | Aircraft transit speed between home and mission start in m/s (default: 5.0 m/s). |
| KMZ (ZIP) file layout | `ZIP_LAYOUT` | Input | Archive internal structure (`wpmz/ subfolder (DJI default)` or `At file root`). |
| Elevation layer (DEM) — if set, exports in above-terrain mode | `ELEVATION_LAYER` | Input | Optional DEM raster layer for terrain-following relative altitude conversion. |
| Terrain tolerance (m) | `TOLERANCE` | Input | Elevation tolerance in meters for terrain sampling (default: 10.0 m). |
| Takeoff point (optional — default: first waypoint) | `PONTO_DECOLAGEM` | Input | Custom reference point coordinates for relative altitude calculations (optional). |
| Output file (.kmz) | `OUTPUT` | Output | Output file path for generated DJI WPML `.kmz` mission package. |

---

## 7. Download Copernicus DEM for area

- **Full Algorithm ID**: `qgc4qgis:baixar_dem_copernicus`
- **Display Name**: Download Copernicus DEM for area
- **Group**: Flight Planning (`planejamento_voo`)

### Description

Downloads the Copernicus DEM GLO-30 (~30m global resolution) digital elevation raster for the extent of the input vector polygon layer, with a configurable safety margin in meters.

### Inputs and Outputs

| Parameter (GUI) | Identifier | Direction | Description |
| :--- | :--- | :--- | :--- |
| Polygon layer | `INPUT` | Input | Vector polygon layer defining the geographical region of interest. |
| Safety margin (m) | `MARGEM` | Input | Extra buffer radius in meters expanded around the area bounding box (default: 250.0 m). |
| Output DEM | `OUTPUT` | Output | Destination raster layer path for the downloaded GeoTIFF DEM tile. |
