# QGC4QGIS

O **QGC4QGIS** traz o planejamento fotogramétrico do QGroundControl para
dentro do QGIS: a partir de um polígono de área de interesse, gera a **grade
de voo** (transectos com sobreposição lateral e frontal), os **centros de
foto**, as **estatísticas da missão** e exporta o arquivo **`.plan`** nativo
do QGroundControl — além de Litchi (`.csv`/`.kml`) e DJI WPML (`.kmz`).

O plugin também traz os algoritmos do Processing (provider `QGC4QGIS`, grupo
*Flight Planning*) e o download automático do DEM Copernicus — a mesma fonte
de elevação que o QGroundControl usa nativamente (Auterion), então o terreno
amostrado no `.plan` bate com o que o QGC recalcula.

!!! info "Compatibilidade"
    QGIS **3.34 → 4.x** (`qgisMinimumVersion=3.34`, `qgisMaximumVersion=4.99`)
    e **Qt5 e Qt6** (`supportsQt6=True`).

O QGC4QGIS está publicado no repositório oficial de plugins do QGIS, em
[plugins.qgis.org](https://plugins.qgis.org/plugins/qgc4qgis/), com o selo
**QGIS 4 Ready**.

<div class="grid cards" markdown>

- **[Instalação](installation.md)**

    ---

    Instalar pelo repositório oficial de plugins do QGIS, pelo zip da release
    ou por cópia/symlink — e os requisitos do plugin.

- **[Painel de planejamento de voo](workflow.md)**

    ---

    O fluxo de cinco passos no dock: polígono, câmera, altitude/GSD, grade e
    exportação.

- **[Exportações](exports.md)**

    ---

    O `.plan` do QGroundControl, Litchi `.csv`/`.kml` e WPML `.kmz` do DJI
    Fly, e o que cada um suporta de terreno.

- **[Terreno e elevação](elevation.md)**

    ---

    O DEM Copernicus GLO-30 via Auterion, e o voo acompanhando o terreno.

- **[Algoritmos do Processing](algorithms.md)**

    ---

    Os 7 algoritmos do provider, para o modelador gráfico, `pyqgis` e
    processamento em lote.

- **[Histórico de alterações](changelog.md)**

    ---

    O que mudou em cada versão (atual: 0.7.1).

</div>

O QGC4QGIS é software livre sob **GPL-3.0**. O código vive em
[github.com/d-camargo/qgroundcontrol-4QGIS](https://github.com/d-camargo/qgroundcontrol-4QGIS).
