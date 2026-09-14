# Installation

## Requirements

- **QGIS**: version 3.34 to 4.x (`qgisMinimumVersion=3.34`, `qgisMaximumVersion=4.99`).
- **Qt**: both Qt5 and Qt6 are supported (`supportsQt6=True`).
- **Python**: 3.9 or higher, already included in QGIS standard distributions.

## Installation methods

### Method A: QGIS Plugin Repository (recommended)

1. In QGIS, go to the **Plugins** menu → **Manage and Install Plugins...**
2. Open the **All** tab and search for **QGC4QGIS**.
3. Click **Install Plugin**.

The plugin is published at <https://plugins.qgis.org/plugins/qgc4qgis/> with
the **QGIS 4 Ready** badge.

### Method B: ZIP from the GitHub release

1. Download `qgc4qgis.<version>.zip` from
   <https://github.com/d-camargo/qgroundcontrol-4QGIS/releases/latest>.
2. In QGIS, go to the **Plugins** menu → **Manage and Install Plugins...**
3. Select the **Install from ZIP** tab.
4. Select the downloaded `.zip` file and click **Install Plugin**.

### Method C: symlink (development)

Copy or create a symbolic link of the `qgc4qgis` folder into your QGIS profile's
plugins directory:

- **Linux**:

  ```bash
  mkdir -p ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins
  ln -s /path/to/qgroundcontrol-4qgis/qgc4qgis ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/qgc4qgis
  ```

- **Windows**:

  ```text
  %APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\qgc4qgis
  ```

- **macOS**:

  ```bash
  ~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/qgc4qgis
  ```

Compressing the `qgc4qgis` folder into a `.zip` file is useful to test a ZIP
before the release, via the **Install from ZIP** tab.

## Activation

After copying or installing the file, open QGIS, go to the **Plugins** menu
→ **Manage and Install Plugins...**, find **QGC4QGIS** in the list, and
check the box to enable it.

## NumPy compatibility

!!! note "No plugin path loads NumPy"
    Downloading the DEM does not require NumPy: it operates directly via
    Python and native GDAL bindings. Since version 0.6.1 the plugin does not
    import the GDAL bindings when loaded (lazy import, only at the moment of
    writing the DEM). Starting with version 0.6.2, the plugin also does not
    enable GDAL exceptions through the path that imports `osgeo.gdal_array`
    (a binary linked against NumPy). This way, no plugin path (loading or DEM
    download) loads NumPy, ensuring conflict-free operation in environments
    with NumPy 2.x (such as QGIS 4), even when the environment's GDAL
    bindings were compiled with NumPy 1.x.

!!! warning "Diagnosis: NumPy 1.x message"
    - **"A module that was compiled using NumPy 1.x…" warning in the log
      during DEM download**: if the traceback appears in the QGIS log as a
      `WARNING` while the DEM downloads and loads normally, this is a C
      extension compiled against NumPy 1.x being imported by another
      component of the environment and printing the warning — the
      operation does not fail.
    - **"A module that was compiled using NumPy 1.x…" dialog when
      installing**: if the dialog appears when installing the plugin, the
      origin is another component of QGIS's Python — typical of QGIS in
      Flatpak with `numpy` 2.x installed via `pip` in
      `/var/data/python/...`, which shadows the runtime's NumPy and breaks
      extensions compiled against the older NumPy.
      - **Environment fix**: remove that `numpy` installed via `pip` in
        `/var/data/python/...` in the Flatpak (the runtime reverts to
        using the NumPy paired with its binaries), instead of downgrading
        NumPy.
