# Terrain and elevation data

QGC4QGIS provides automatic terrain elevation data (DEM/DTM) retrieval directly from web services. This allows photogrammetric flight planning with terrain following (*Terrain Following*) without needing to pre-load local raster files.

---

## Data source and QGroundControl consistency

- **Data source**: Copernicus DEM GLO-30 (~30-meter global spatial resolution / 1 arc-second).
- **Service endpoint**: Auterion REST web service (`terrain-ce.suite.auterion.com/api/v1/carpet`).
- **Consistency with QGroundControl**: Copernicus DEM via Auterion is the exact same elevation provider and API used natively by QGroundControl (as defined in `ElevationMapProvider.h`). Terrain heights sampled in exported `.plan` files match what QGC queries and recalculates internally.

---

## How to use elevation data in QGIS

You can download elevation data for your mission area using two interfaces in QGIS:

### 1. Dock Widget

1. Open the **QGC4QGIS** dock panel.
2. In the **Terrain** section, click **Download area DEM…**.
3. The plugin calculates the bounding box of your mission area (including the safety margin), downloads the Copernicus DEM GeoTIFF, and automatically loads it as a raster layer in your QGIS project.

### 2. Processing Toolbox

- Use the algorithm `qgc4qgis:baixar_dem_copernicus` (`Download Copernicus DEM`).
- Parameters:
  - **Coverage area / Extent**: Vector layer polygon or custom geographic bounding box.
  - **Margin (meters)**: Extra buffer radius around the area.
  - **Output GeoTIFF**: File path where the downloaded raster tile will be saved.

---

## Safety margin parameter

The **Margin** parameter expands the requested bounding box around the mission area.

### Why margin matters

- **Turnaround areas**: Maneuver turns and acceleration/deceleration zones (*turnarounds*) extend beyond the survey polygon perimeter.
- **Takeoff and approach**: Ensures elevation data coverage for the takeoff location and initial approach path to the first waypoint.

---

## API limits and constraints

- **Spatial resolution**: Nominal ~30 meters (1 arc-second).
- **Network requirement**: Active internet connection required during tile download.
- **Tile request ceiling**: The server limits single requests to a maximum of **256 tiles**, corresponding to a bounding box of approximately **$18 \times 18\text{ km}$**. Requests exceeding this size are rejected by the server.

---

## Mandatory copyright attribution

!!! important "Mandatory Attribution"
    Per the provider's terms of use, using Copernicus DEM GLO-30 data requires
    displaying the following copyright attribution:
    **© Airbus Defence and Space GmbH**

---

## Altitude reference (EGM2008 Geoid)

!!! note "Orthometric Altitude Convention"
    Heights provided by the Copernicus DEM are **orthometric** (referenced to the **EGM2008** geoid model — height above mean sea level). This follows the exact same convention used by QGroundControl. **Do not confuse orthometric heights with ellipsoidal heights** obtained directly from raw GNSS/GPS receivers without applying a geoid model.

---

## NumPy compatibility

Downloading DEM data **does not require NumPy** and operates using standard Python and native GDAL bindings.

- **Lazy GDAL import**: GDAL bindings are only imported when writing the raster file.
- **No `osgeo.gdal_array` dependency**: The plugin avoids importing `osgeo.gdal_array` (which links against binary NumPy extensions).
- **QGIS 4 & NumPy 2.x ready**: No plugin path loads NumPy during loading or DEM retrieval. This prevents binary interface crashes in environments with NumPy 2.x (such as QGIS 4), even when system GDAL bindings were compiled against NumPy 1.x.

---

## Known issues and troubleshooting

### 1. "A module that was compiled using NumPy 1.x…" log warning

If the warning *"A module that was compiled using NumPy 1.x..."* appears in the QGIS **Log Messages** panel while the DEM downloads and loads normally, it indicates another component in the environment imported a legacy NumPy 1.x extension. The DEM download operation completes successfully.

### 2. "A module that was compiled using NumPy 1.x…" dialog during installation

If a modal dialog with this error appears when installing the plugin (common in Flatpak QGIS setups):

- **Root cause**: A secondary `numpy` 2.x package installed via `pip` in `/var/data/python/...` shadows runtime binaries.
- **Fix**: Remove the user-installed `pip` package under `/var/data/python/...` in Flatpak so QGIS reverts to its paired runtime binaries. Do not downgrade system NumPy.
