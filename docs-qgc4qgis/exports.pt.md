# Opções de exportação de missão

Além do formato nativo `.plan` do QGroundControl, o QGC4QGIS permite exportar planos de voo fotogramétricos para os aplicativos **Litchi** (formatos `.csv` e `.kml`) e **DJI Fly** (formato WPML `.kmz`).

## Visão geral dos formatos suportados

| Formato | Extensão do Arquivo | Aplicativos Alvo | Suporte ao Modo Terreno | Principais Características e Restrições |
| :--- | :--- | :--- | :--- | :--- |
| **Plano QGroundControl** | `.plan` | QGroundControl, PX4, ArduPilot | Acompanhamento de relevo nativo | Estrutura completa de missão com disparos de câmera e parâmetros de telemetria. |
| **Pacote WPML** | `.kmz` | DJI Fly, Litchi Hub 2 | Convertido para altitude relativa à decolagem | Formato WPML oficial da DJI contendo `template.kml` e `waylines.wpml`. |
| **Missão Litchi** | `.csv` | Litchi (Hub Clássico e Hub 2), Litchi Mobile | Altitude relativa | Tabela CSV padrão D8 contendo coordenadas, altitude, proa e inclinação do gimbal. |
| **KML Litchi** | `.kml` | Hub Clássico do Litchi | Altitude relativa | Marcas de posição KML com coordenadas e altitudes; requer configuração de ação de foto na importação. |

---

## Exportação nativa do QGroundControl (`.plan`)

O formato nativo `.plan` exporta a definição completa da missão para o QGroundControl:

- Contém itens complexos de levantamento (*SurveyComplexItem*), transectos, curvas de manobra (*turnaround*), velocidades, especificações de câmera e destino de firmware de piloto automático (PX4 ou ArduPilot).
- Preserva os parâmetros originais de acompanhamento de terreno quando utilizado o DEM Copernicus ou rasters locais de elevação.
- Pronto para ser carregado diretamente no QGroundControl em computadores ou dispositivos móveis.

---

## Exportação WPML (`.kmz`) para DJI Fly e Litchi Hub 2

O formato WPML `.kmz` é o formato oficial da DJI para execução de missões por waypoints em aeronaves DJI mais recentes.

### Conversão do modo terreno

- Missões com acompanhamento de terreno são convertidas em altitudes relativas ao ponto de decolagem (parâmetro `PONTO_DECOLAGEM`, cujo padrão é a elevação do primeiro waypoint).
- Isso permite que aeronaves com suporte a WPML sigam o perfil do relevo mesmo operando com comandos de altura relativa.

!!! warning "Aviso: Altura relativa $\le 0$"
    O plugin emite um aviso caso qualquer altura relativa calculada seja $\le 0$ metros em relação ao ponto de decolagem.

### Carga no DJI Fly

1. No aplicativo **DJI Fly** (ou no controle DJI RC / RC 2 / RC Pro), crie e salve uma missão de teste com **1 waypoint** para que o aplicativo gere sua estrutura de arquivos e um identificador único de pasta (GUID).
2. Localize a pasta do GUID criada no armazenamento do dispositivo:
   - **Android**: `Android/data/dji.go.v5/files/waypoint`
   - **iOS / Armazenamento do Controle**: `Files/DJI Fly/wayline_mission/`
3. Renomeie o arquivo `.kmz` exportado com o mesmo nome GUID da pasta.
4. Substitua o arquivo `.kmz` original localizado dentro da pasta GUID do dispositivo pelo arquivo renomeado gerado pelo QGC4QGIS.

!!! warning "Não re-editar no DJI Fly"
    Não edite ou salve a missão importada dentro do aplicativo DJI Fly! Se a missão for salva no DJI Fly, o aplicativo reescreverá a estrutura do WPML, podendo corromper ou remover gatilhos de fotos e ações customizadas nos waypoints.

### Carga no Litchi Hub 2

- O mesmo arquivo WPML `.kmz` exportado para o DJI Fly pode ser importado diretamente no [Litchi Hub 2](https://hub.flylitchi.com) como arquivo de missão.
- O Hub 2 detecta os componentes `template.kml` e `waylines.wpml` dentro do arquivo comprimido.

!!! warning "Diálogo de importação no Hub 2"
    O Hub 2 possui dois diálogos de importação distintos. O diálogo de área/overlay (`.kml`, `.kmz`, `.geojson`, `.json`) serve apenas para desenhar camadas visuais no mapa e **não cria waypoints de voo**. Para carregar a rota de voo, utilize sempre o diálogo de importação de missão (**Mission → Import**).

---

## Exportação Litchi (`.csv`)

O formato `.csv` exporta rotas de voo formatadas para o Litchi (especificação D8).

### Ajustes manuais globais exigidos no Litchi Hub

Ao importar uma missão `.csv` no Litchi Mission Hub ([flylitchi.com/hub](https://flylitchi.com/hub) ou [hub.flylitchi.com](https://hub.flylitchi.com)), três parâmetros globais devem ser configurados manualmente no painel antes de salvar:

1. **Heading Mode** (Modo de Direção): Selecione **"Custom (WP)"** para que o aplicativo utilize a coluna `heading(deg)` gravada no CSV (o azimute calculado para cada faixa de voo).
2. **Finish Action** (Ação ao Finalizar): Defina o comportamento desejado ao término da missão (ex.: *Return to Home (RTH)*, *None* ou *Land*).
3. **Path Mode** (Modo de Trajetória): Selecione **"Straight Lines"** — o CSV é gerado com `curvesize=0` e não define curvas.

!!! warning "Aviso de modo de disparo e ação de foto"
    Na exportação para `.csv`, se o modo de disparo de foto selecionado não gerar ações explícitas de foto por waypoint (por exemplo, ao utilizar disparos por distância ou tempo sem amostragem de waypoints), o Litchi não executará ações de foto por waypoint. Para garantir a amostragem de waypoints com ações de foto, gere a missão com **Modo de disparo = "Por foto"**.

---

## Exportação KML Litchi (`.kml`) para o Hub Clássico

O formato `.kml` é projetado especificamente para o Hub Clássico do Litchi ([flylitchi.com/hub](https://flylitchi.com/hub)).

### Passos de carga

1. Acesse o [Hub Clássico do Litchi](https://flylitchi.com/hub).
2. Clique em **Mission → Import** e selecione o arquivo `.kml`.
3. **Marque a opção "Add take photo action"** e **deixe "Placemarks as POI" desmarcado**.
4. Esta configuração adiciona automaticamente uma ação *Take Photo* em **todos** os waypoints e força o modo de trajetória para linhas retas (*Straight Lines*).

### Requisito do modo de disparo

- O uso do formato `.kml` exige que a missão seja gerada com **Modo de disparo = "Por foto"**. Caso contrário, os vértices do KML representarão apenas as pontas de início e fim de cada transecto.
- Definir **Modo de disparo = "Por foto"** também assegura a amostragem adequada de waypoints na exportação `.csv`.

### Parâmetros ausentes no KML

Como os arquivos KML contêm apenas coordenadas geográficas e altitudes, os parâmetros não posicionais não são importados e devem ser ajustados manualmente no Mission Hub:

| Parâmetro Ausente no KML | Comportamento Padrão no Hub Clássico | Onde Ajustar no Mission Hub |
| :--- | :--- | :--- |
| **Proa (Heading)** | Direção para o próximo waypoint (ou Norte) | Painel de Configurações da Missão (`Heading Mode`) |
| **Gimbal Pitch** | $0^\circ$ (horizontal) | Propriedades do Waypoint / Ações |
| **Velocidade (Speed)** | Velocidade padrão global da missão | Painel de Configurações da Missão (`Speed`) |
| **Modo de Trajetória (Curvo/Reto)** | *Straight Lines* (forçado por *Take Photo*) | Painel de Configurações da Missão (`Path Mode`) |
| **Pontos de Interesse (POI)** | Não importados (manter "Placemarks as POI" desmarcado) | Adicionar manualmente no mapa |
| **Modo de Altitude Explícito** | Relativo ao solo no ponto de decolagem (*Relative*) | Propriedades individuais do waypoint |

### Comportamentos silenciosos e limites do importador KML no Hub Clássico

- **Ajustes Silenciosos de Altitude**: O importador KML do Hub Clássico converte silenciosamente **altura 0 m para 30 m** e trunca altitudes fora do intervalo `[-200, 500]` metros. O plugin exibe avisos antes da exportação quando essas condições ocorrem.
- **Teto de Waypoints**: O importador KML do Hub Clássico suporta até **10.000** waypoints (waypoints excedentes além de 10.000 somem silenciosamente sem avisos de erro).
- **Incompatibilidade com `.kmz`**: O **Hub Clássico não suporta arquivos `.kmz`**. Não importe arquivos `waylines.wpml` no Hub Clássico, pois coordenadas WPML não possuem definições de altitude e farão com que todas as alturas da missão assumam 30 m.

---

## Limitações e comportamentos dos aplicativos

### Limites de waypoints

- **Litchi**: Limite máximo de **99 waypoints** por missão. O QGC4QGIS alerta o usuário quando uma missão excede 99 waypoints.
- **DJI Fly**: A DJI não publica um limite rígido oficial, mas o valor aceito pela comunidade é de **200 waypoints**. O QGC4QGIS emite um aviso quando uma missão excede 200 waypoints.

### Matriz comparativa dos Hubs

| Interface | URL | Formatos de Missão Suportados | Nota |
| :--- | :--- | :--- | :--- |
| **Hub Clássico** | [flylitchi.com/hub](https://flylitchi.com/hub) | `.csv`, `.kml`, `.wpml` | Requer opção "Add take photo action" para KML. |
| **Hub 2** | [hub.flylitchi.com](https://hub.flylitchi.com) | `.csv`, `.kmz` (WPML) | Utilizar diálogo de importação de missão, não de área/overlay. |
