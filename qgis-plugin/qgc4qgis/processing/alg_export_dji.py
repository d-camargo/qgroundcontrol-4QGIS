"""Processing algorithm to export a DJI Fly mission (.kmz) file."""

from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsGeometry,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterLayer,
)

from qgc4qgis.core.cameracalc import CameraCalc
from qgc4qgis.core.cameras import CUSTOM_CAMERA_NAME, CameraSpec, load_cameras
from qgc4qgis.core.geo import AEQDProjection
from qgc4qgis.core.missionitems import DistanceMode
from qgc4qgis.core.route import route_from_transects
from qgc4qgis.core.survey import generate_survey_transects
from qgc4qgis.core.terrain import adjust_terrain_flight_path
from qgc4qgis.core.wpml import save_kmz
from qgc4qgis.processing.alg_survey_grid import extract_polygons


class ExportDjiAlgorithm(QgsProcessingAlgorithm):
    """QGIS Processing Algorithm to export DJI Fly mission (.kmz) files."""

    INPUT = "INPUT"
    CAMERA = "CAMERA"
    ALTITUDE = "ALTITUDE"
    GSD = "GSD"
    OVERLAP_SIDE = "OVERLAP_SIDE"
    OVERLAP_FRONTAL = "OVERLAP_FRONTAL"
    ANGLE = "ANGLE"
    TURNAROUND = "TURNAROUND"
    ENTRY_LOCATION = "ENTRY_LOCATION"
    REFLY = "REFLY"
    SENSOR_WIDTH = "SENSOR_WIDTH"
    SENSOR_HEIGHT = "SENSOR_HEIGHT"
    IMAGE_WIDTH = "IMAGE_WIDTH"
    IMAGE_HEIGHT = "IMAGE_HEIGHT"
    FOCAL_LENGTH = "FOCAL_LENGTH"
    TRIGGER_MODE = "TRIGGER_MODE"
    SPEED = "SPEED"
    GIMBAL_PITCH = "GIMBAL_PITCH"
    WAYPOINT_WAIT = "WAYPOINT_WAIT"
    FINISH_ACTION = "FINISH_ACTION"
    RC_LOST_ACTION = "RC_LOST_ACTION"
    TRANSITIONAL_SPEED = "TRANSITIONAL_SPEED"
    ZIP_LAYOUT = "ZIP_LAYOUT"
    ELEVATION_LAYER = "ELEVATION_LAYER"
    TOLERANCE = "TOLERANCE"
    OUTPUT = "OUTPUT"

    def name(self) -> str:
        """Return unique algorithm name."""
        return "exportar_dji_kmz"

    def displayName(self) -> str:
        """Return localized human-readable algorithm name."""
        return "Exportar missão DJI Fly (.kmz)"

    def group(self) -> str:
        """Return localized group name."""
        return "Planejamento de Voo"

    def groupId(self) -> str:
        """Return unique group identifier."""
        return "planejamento_voo"

    def createInstance(self) -> "ExportDjiAlgorithm":
        """Create new instance of algorithm."""
        return ExportDjiAlgorithm()

    def shortHelpString(self) -> str:
        """Return short help text for algorithm GUI."""
        return (
            "Exporta uma missão de voo no formato DJI WPML (.kmz) "
            "a partir de polígonos de cobertura ou linhas de grade de voo."
        )

    def initAlgorithm(self, config=None) -> None:
        """Define algorithm parameters and outputs."""
        cameras = load_cameras()
        camera_names = [c.canonicalName for c in cameras]

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                "Camada de entrada (Polígonos ou Linhas)",
                [QgsProcessing.TypeVectorPolygon, QgsProcessing.TypeVectorLine],
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.CAMERA,
                "Câmera",
                options=camera_names,
                defaultValue=0,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.ALTITUDE,
                "Altura de voo (m)",
                QgsProcessingParameterNumber.Double,
                defaultValue=100.0,
                minValue=0.0,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.GSD,
                "GSD (cm/px) - se > 0 sobrescreve/calcula altura",
                QgsProcessingParameterNumber.Double,
                defaultValue=0.0,
                minValue=0.0,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.OVERLAP_SIDE,
                "Sobreposição lateral (%)",
                QgsProcessingParameterNumber.Double,
                defaultValue=70.0,
                minValue=0.0,
                maxValue=99.0,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.OVERLAP_FRONTAL,
                "Sobreposição frontal (%)",
                QgsProcessingParameterNumber.Double,
                defaultValue=70.0,
                minValue=0.0,
                maxValue=99.0,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.ANGLE,
                "Ângulo da grade (graus)",
                QgsProcessingParameterNumber.Double,
                defaultValue=0.0,
                minValue=-180.0,
                maxValue=180.0,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.TURNAROUND,
                "Distância de turnaround (m)",
                QgsProcessingParameterNumber.Double,
                defaultValue=0.0,
                minValue=0.0,
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.ENTRY_LOCATION,
                "Ponto de entrada",
                options=["Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right"],
                defaultValue=0,
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.REFLY,
                "Grade cruzada (Refly 90°)",
                defaultValue=False,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.SENSOR_WIDTH,
                "Câmera manual: Largura do sensor (mm)",
                QgsProcessingParameterNumber.Double,
                defaultValue=35.9,
                minValue=0.0,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.SENSOR_HEIGHT,
                "Câmera manual: Altura do sensor (mm)",
                QgsProcessingParameterNumber.Double,
                defaultValue=24.0,
                minValue=0.0,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.IMAGE_WIDTH,
                "Câmera manual: Largura da imagem (px)",
                QgsProcessingParameterNumber.Integer,
                defaultValue=7952,
                minValue=0,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.IMAGE_HEIGHT,
                "Câmera manual: Altura da imagem (px)",
                QgsProcessingParameterNumber.Integer,
                defaultValue=5304,
                minValue=0,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.FOCAL_LENGTH,
                "Câmera manual: Distância focal (mm)",
                QgsProcessingParameterNumber.Double,
                defaultValue=35.0,
                minValue=0.0,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.TRIGGER_MODE,
                "Modo de disparo",
                options=["Por distância", "Por tempo", "Por foto"],
                defaultValue=2,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.SPEED,
                "Velocidade (m/s)",
                QgsProcessingParameterNumber.Double,
                defaultValue=5.0,
                minValue=0.1,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.GIMBAL_PITCH,
                "Ângulo de gimbal (graus)",
                QgsProcessingParameterNumber.Double,
                defaultValue=-90.0,
                minValue=-90.0,
                maxValue=20.0,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.WAYPOINT_WAIT,
                "Espera no waypoint (s)",
                QgsProcessingParameterNumber.Double,
                defaultValue=0.0,
                minValue=0.0,
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.FINISH_ACTION,
                "Ação ao terminar",
                options=[
                    "Retornar ao início (goHome)",
                    "Nenhuma ação (noAction)",
                    "Pouso automático (autoLand)",
                    "Ir para primeiro waypoint (gotoFirstWaypoint)",
                ],
                defaultValue=0,
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.RC_LOST_ACTION,
                "Ação em perda de rádio",
                options=["Retornar (goBack)", "Pousar (landing)", "Pairar (hover)"],
                defaultValue=0,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.TRANSITIONAL_SPEED,
                "Velocidade de transição (m/s)",
                QgsProcessingParameterNumber.Double,
                defaultValue=5.0,
                minValue=0.1,
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.ZIP_LAYOUT,
                "Layout do arquivo KMZ (ZIP)",
                options=["Subpasta wpmz/ (padrão DJI)", "Na raiz do arquivo"],
                defaultValue=0,
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.ELEVATION_LAYER,
                "Camada de elevação (DEM) — se definida, exporta em modo acima do terreno",
                optional=True,
                defaultValue=None,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.TOLERANCE,
                "Tolerância do terreno (m)",
                QgsProcessingParameterNumber.Double,
                defaultValue=10.0,
                minValue=0.1,
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT,
                "Arquivo de destino (.kmz)",
                fileFilter="DJI KMZ (*.kmz)",
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """Execute DJI Fly KMZ export algorithm logic."""
        source = self.parameterAsSource(parameters, self.INPUT, context)
        if source is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))

        output_file = self.parameterAsFileOutput(parameters, self.OUTPUT, context)
        if not output_file:
            raise QgsProcessingException("Caminho do arquivo de saída não especificado.")

        camera_idx = self.parameterAsEnum(parameters, self.CAMERA, context)
        cameras = load_cameras()
        if 0 <= camera_idx < len(cameras):
            spec = cameras[camera_idx]
        else:
            spec = cameras[0]

        if spec.canonicalName == CUSTOM_CAMERA_NAME:
            sensor_w = self.parameterAsDouble(parameters, self.SENSOR_WIDTH, context)
            sensor_h = self.parameterAsDouble(parameters, self.SENSOR_HEIGHT, context)
            img_w = self.parameterAsInt(parameters, self.IMAGE_WIDTH, context)
            img_h = self.parameterAsInt(parameters, self.IMAGE_HEIGHT, context)
            focal_l = self.parameterAsDouble(parameters, self.FOCAL_LENGTH, context)
            spec = CameraSpec(
                canonicalName=CUSTOM_CAMERA_NAME,
                sensorWidth=sensor_w,
                sensorHeight=sensor_h,
                imageWidth=img_w,
                imageHeight=img_h,
                focalLength=focal_l,
            )

        altitude = self.parameterAsDouble(parameters, self.ALTITUDE, context)
        gsd = self.parameterAsDouble(parameters, self.GSD, context)
        side_overlap = self.parameterAsDouble(parameters, self.OVERLAP_SIDE, context)
        frontal_overlap = self.parameterAsDouble(parameters, self.OVERLAP_FRONTAL, context)
        grid_angle = self.parameterAsDouble(parameters, self.ANGLE, context)
        turnaround = self.parameterAsDouble(parameters, self.TURNAROUND, context)
        entry_loc = self.parameterAsEnum(parameters, self.ENTRY_LOCATION, context)
        refly = self.parameterAsBool(parameters, self.REFLY, context)

        trigger_mode_idx = self.parameterAsEnum(parameters, self.TRIGGER_MODE, context)
        trigger_mode_map = {0: "POR_DISTANCIA", 1: "POR_TEMPO", 2: "POR_FOTO"}
        trigger_mode_str = trigger_mode_map.get(trigger_mode_idx, "POR_DISTANCIA")

        speed = self.parameterAsDouble(parameters, self.SPEED, context)
        gimbal_pitch = self.parameterAsDouble(parameters, self.GIMBAL_PITCH, context)
        waypoint_wait = self.parameterAsDouble(parameters, self.WAYPOINT_WAIT, context)

        finish_idx = self.parameterAsEnum(parameters, self.FINISH_ACTION, context)
        finish_action_map = {0: "goHome", 1: "noAction", 2: "autoLand", 3: "gotoFirstWaypoint"}
        finish_action_str = finish_action_map.get(finish_idx, "goHome")

        rc_idx = self.parameterAsEnum(parameters, self.RC_LOST_ACTION, context)
        rc_action_map = {0: "goBack", 1: "landing", 2: "hover"}
        rc_action_str = rc_action_map.get(rc_idx, "goBack")

        transitional_speed = self.parameterAsDouble(parameters, self.TRANSITIONAL_SPEED, context)
        zip_layout_idx = self.parameterAsEnum(parameters, self.ZIP_LAYOUT, context)
        in_wpmz_dir = zip_layout_idx == 0

        elevation_layer = self.parameterAsRasterLayer(parameters, self.ELEVATION_LAYER, context)
        terrain_mode = elevation_layer is not None and elevation_layer.isValid()
        tolerance = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        distance_mode = DistanceMode.CALC_ABOVE_TERRAIN if terrain_mode else DistanceMode.RELATIVE

        value_set_is_distance = gsd <= 0.0
        calc = CameraCalc(
            spec=spec,
            value_set_is_distance=value_set_is_distance,
            distance_to_surface=altitude,
            image_density=gsd,
            frontal_overlap=frontal_overlap,
            side_overlap=side_overlap,
        )

        if not calc.recalculate():
            raise QgsProcessingException("Falha ao calcular os parâmetros da câmera/voo.")

        crs_wgs84 = QgsCoordinateReferenceSystem("EPSG:4326")
        source_crs = source.sourceCrs()
        need_transform = source_crs != crs_wgs84
        if need_transform:
            to_wgs84 = QgsCoordinateTransform(source_crs, crs_wgs84, context.transformContext())

        all_transects = []

        feature_count = source.featureCount()
        total_steps = feature_count if feature_count > 0 else 100
        step = 0

        for feature in source.getFeatures():
            if feedback.isCanceled():
                break

            geom = feature.geometry()
            if geom.isEmpty() or geom.isNull():
                continue

            geom_wgs84 = QgsGeometry(geom)
            if need_transform:
                geom_wgs84.transform(to_wgs84)

            is_polygon = QgsGeometry.type(geom_wgs84) == 2  # Polygon geometry type

            if is_polygon:
                polygons = extract_polygons(geom_wgs84)
                for polygon_pts in polygons:
                    if len(polygon_pts) < 3:
                        continue

                    ref_lat, ref_lon = polygon_pts[0]
                    proj = AEQDProjection(ref_lat, ref_lon)
                    planar_pts = [proj.forward(lat, lon) for lat, lon in polygon_pts]

                    transects = generate_survey_transects(
                        polygon_points=planar_pts,
                        grid_angle=grid_angle,
                        grid_spacing=calc.adjusted_footprint_side,
                        entry_location=entry_loc,
                        turnaround_distance=turnaround,
                        refly_90_degrees=refly,
                    )

                    geo_transects = [[proj.inverse(x, y) for x, y in tr] for tr in transects]

                    if terrain_mode:
                        adjusted_transects = [
                            adjust_terrain_flight_path(
                                tr,
                                raster_layer=elevation_layer,
                                target_altitude=calc.distance_to_surface,
                                step_distance=tolerance,
                                tolerance=tolerance,
                                transform_context=context.transformContext(),
                            )
                            for tr in geo_transects
                        ]
                        geo_transects = [
                            [(p.lat, p.lon, p.altitude) for p in tr] for tr in adjusted_transects
                        ]

                    all_transects.extend(geo_transects)
            else:
                # LineString geometry fallback
                if geom_wgs84.isMultipart():
                    lines = geom_wgs84.asMultiPolyline()
                else:
                    lines = [geom_wgs84.asPolyline()]

                for line in lines:
                    if not line:
                        continue
                    line_pts = [(pt.y(), pt.x()) for pt in line]
                    if terrain_mode:
                        adjusted = adjust_terrain_flight_path(
                            line_pts,
                            raster_layer=elevation_layer,
                            target_altitude=calc.distance_to_surface,
                            step_distance=tolerance,
                            tolerance=tolerance,
                            transform_context=context.transformContext(),
                        )
                        line_pts = [(p.lat, p.lon, p.altitude) for p in adjusted]
                    all_transects.append(line_pts)

            step += 1
            feedback.setProgress(int(100.0 * step / total_steps))

        if trigger_mode_str == "POR_TEMPO":
            trig_dist = calc.trigger_distance / speed if speed > 0 else calc.trigger_distance
        else:
            trig_dist = calc.trigger_distance

        route = route_from_transects(
            all_transects,
            altitude=calc.distance_to_surface,
            trigger_distance=trig_dist,
            trigger_mode=trigger_mode_str,
            distance_mode=distance_mode,
            flight_speed=speed,
            gimbal_pitch=gimbal_pitch,
        )

        if waypoint_wait > 0.0:
            for wp in route.waypoints:
                wp.wait_time = waypoint_wait

        try:
            warnings = save_kmz(
                filepath=output_file,
                route=route,
                in_wpmz_dir=in_wpmz_dir,
                finish_action=finish_action_str,
                exit_on_rc_lost="executeLostAction",
                execute_rc_lost_action=rc_action_str,
                global_transitional_speed=transitional_speed,
                auto_flight_speed=speed,
                default_execute_height=calc.distance_to_surface,
                default_waypoint_speed=speed,
                default_gimbal_pitch=gimbal_pitch,
                trigger_mode=trigger_mode_str,
                trigger_distance=trig_dist,
                gimbal_pitch=gimbal_pitch,
                distance_mode=distance_mode,
            )
        except ValueError as e:
            raise QgsProcessingException(str(e)) from e

        for warning in warnings:
            feedback.pushWarning(warning)

        return {self.OUTPUT: output_file}
