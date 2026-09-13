# Flight planning panel

Photogrammetric flight mission planning through the QGC4QGIS dock widget follows a structured **five-step** workflow.

## Five-step workflow

```text
[Step 1: Polygon] ➔ [Step 2: Camera] ➔ [Step 3: Altitude/GSD] ➔ [Step 4: Grid] ➔ [Step 5: Export]
```

1. **Coverage Polygon Selection**:
   - Select the polygon vector layer that defines the area of interest (AOI).
   - Choose the specific feature in the layer or use all features to delimit the survey perimeter.

2. **Camera Configuration**:
   - Choose a preconfigured camera model from the integrated camera library (e.g., Sony ILCE-7R, DJI cameras, etc.).
   - Alternatively, select *Custom Camera* (Manual Camera) to specify the sensor's physical properties: sensor width (mm), sensor height (mm), image width (px), image height (px), and focal length (mm).

3. **Flight Altitude or GSD Definition**:
   - Choose the main control parameter: **Flight Altitude (m)** or **GSD (cm/px)**.
   - When one of the values is changed, the plugin automatically calculates the corresponding value while keeping the camera's optical relationship.

4. **Grid and Overlap Adjustment**:
   - Set the **Side Overlap (%)** (*side overlap*) and the **Front Overlap (%)** (*front overlap*).
   - Adjust the **Grid Angle (degrees)** to orient the flight transects in the desired direction (e.g., aligned with the wind or with the largest dimension of the terrain).
   - Configure the **Turnaround Distance (m)** to extend the strips beyond the polygon, allowing the flight to stabilize before taking photos.
   - Set the **Entry Point** (*Top-Left*, *Top-Right*, *Bottom-Left*, *Bottom-Right*) and enable **Cross Grid (Refly 90°)** if you want a double orthogonal flight.

5. **Preview and Export (.plan)**:
   - Preview the transect grid, photo centers, and footprint polygons directly on the QGIS map in real time.
   - Check the calculated statistics: total area (ha), flight length (km), estimated number of photos, and flight time.
   - Click **Export QGC Plan (.plan)** to save the file ready to be imported into QGroundControl or loaded onto the drone.

## Parameter table

The table below describes all the parameters available in the plugin's dock widget and processing tools (`gerar_grade_voo`, `gerar_centros_foto`, and `exportar_plano_qgc`):

| Parameter | Identifier | Type / Unit | Default Value | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Input Layer** | `INPUT` | Vector (Polygon / Line) | *Required* | Vector layer containing the coverage area geometry or transect lines. |
| **Camera** | `CAMERA` | Enum / Text | `0` (First in the list) | Camera selected from the predefined library or manual model (*Custom Camera*). |
| **Flight Altitude** | `ALTITUDE` | Numeric (`Double`) / meters (m) | `100.0` | Relative flight altitude above the takeoff point. |
| **GSD** | `GSD` | Numeric (`Double`) / cm/px | `0.0` | Ground resolution. If > 0, it calculates and overrides the flight altitude. |
| **Side Overlap** | `OVERLAP_SIDE` | Numeric (`Double`) / percentage (%) | `70.0` | Overlap percentage between adjacent flight strips. |
| **Front Overlap** | `OVERLAP_FRONTAL` | Numeric (`Double`) / percentage (%) | `70.0` | Overlap percentage between consecutive images in the same strip. |
| **Grid Angle** | `ANGLE` | Numeric (`Double`) / degrees (°) | `0.0` | Orientation of the flight transects relative to North (-180° to 180°). |
| **Turnaround** | `TURNAROUND` | Numeric (`Double`) / meters (m) | `0.0` | Extension of lines beyond the polygon for the aircraft's turn and acceleration maneuver. |
| **Entry Point** | `ENTRY_LOCATION` | Enum (`0`: Top-Left, `1`: Top-Right, `2`: Bottom-Left, `3`: Bottom-Right) | `0` | Starting corner for the flight grid execution. |
| **Cross Grid** | `REFLY` | Boolean (`True`/`False`) | `False` | If enabled, generates a second transect grid perpendicular (90°) to the first. |
| **Sensor Width** | `SENSOR_WIDTH` | Numeric (`Double`) / mm | `35.9` | Physical width of the photographic sensor (used in Manual Camera). |
| **Sensor Height** | `SENSOR_HEIGHT` | Numeric (`Double`) / mm | `24.0` | Physical height of the photographic sensor (used in Manual Camera). |
| **Image Width** | `IMAGE_WIDTH` | Numeric (`Integer`) / pixels | `7952` | Horizontal resolution of the captured image (used in Manual Camera). |
| **Image Height** | `IMAGE_HEIGHT` | Numeric (`Integer`) / pixels | `5304` | Vertical resolution of the captured image (used in Manual Camera). |
| **Focal Length** | `FOCAL_LENGTH` | Numeric (`Double`) / mm | `35.0` | Actual focal length of the camera lens (used in Manual Camera). |
| **Cruise Speed** | `CRUISE_SPEED` | Numeric (`Double`) / m/s | `15.0` | Nominal horizontal speed of the aircraft in flight (used when exporting the `.plan`). |
| **Hover Speed** | `HOVER_SPEED` | Numeric (`Double`) / m/s | `5.0` | Horizontal deceleration/hover speed for multicopters. |
| **Firmware** | `FIRMWARE_TYPE` | Enum (`12`: PX4, `3`: ArduPilot) | `12` (PX4) | Autopilot protocol and format for mission export. |
| **Vehicle Type** | `VEHICLE_TYPE` | Enum (`2`: Multicopter, `1`: Fixed Wing, `19`: VTOL) | `2` (Multicopter) | Category of the unmanned aerial vehicle. |

## Known limitations

To maintain full compatibility with QGroundControl's original algorithm, QGC4QGIS inherits two architectural limitations from QGC's `SurveyComplexItem` library:

### Concave polygon without decomposition

- **Description**: QGC's flight transect generator treats the coverage polygon as a single continuous outer ring (*outer ring*). When processing areas with concave geometries (such as "L", "C", or "U" shapes) or polygons containing holes (*donuts*), the grid is generated by sweeping the full extent of the bounding envelope (*bounding envelope*).
- **Consequence**: The algorithm does not perform automatic decomposition of the geometry into isolated convex subpolygons. As a result, some transects may cross regions outside the polygon between two concave indentations.

### GSD calculated using sensor width only

- **Description**: The conversion equation between Flight Altitude (m) and GSD (cm/px) in QGroundControl calculates ground resolution exclusively based on the sensor's horizontal dimension (`sensorWidth`) and the image width in pixels (`imageWidth`):

$$\text{GSD} = \frac{\text{Flight Altitude (m)} \times \text{Sensor Width (mm)}}{\text{Focal Length (mm)} \times \text{Image Width (px)}} \times 100$$

$$\text{Flight Altitude (m)} = \frac{\text{GSD (cm/px)} \times \text{Focal Length (mm)} \times \text{Image Width (px)}}{\text{Sensor Width (mm)} \times 100}$$

- **Consequence**: The sensor's vertical dimension (`sensorHeight`) and the image height in pixels (`imageHeight`) do not affect the scalar GSD calculation or the resulting flight altitude; they are used only to determine the extent of the footprints and the front photo trigger distance.
