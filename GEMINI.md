# GEMINI.md — qgroundcontrol-4QGIS

> **Este arquivo (`GEMINI.md`) é a fonte única das regras deste repo.**
> `CLAUDE.md` e `AGENTS.md` são symlinks relativos para cá. **Edite sempre o
> `GEMINI.md`** — o `agy` (Antigravity) não segue symlink e só lê arquivo real,
> e o Edit do Claude Code recusa escrever através de symlink. Medido em
> 2026-08-10.

> Este repo é FORK de `mavlink/qgroundcontrol`: as docs de agente do UPSTREAM
> vivem em `AGENTS.upstream.md` (renomeadas na C47, 2026-08-28 — os nomes
> `CLAUDE.md`/`AGENTS.md` da raiz pertencem às regras DO PROJETO, igual aos
> demais repos da VPS). Conflito de merge nesses caminhos num pull do upstream é
> manutenção conhecida e aceita: conflito VISÍVEL é preferível a três CLIs
> lendo regras diferentes em silêncio.

## O que é

Fork do QGroundControl (upstream `mavlink/qgroundcontrol`) mantido pelo Diego
(@d-camargo), com o plugin QGIS `qgc4qgis/` em subpasta (metadata.txt próprio).

## Regras de trabalho

- Desenvolvimento pelo fluxo Hermes: `/plan` → `/run` → `/review` → `/push`
  (motor `planexec.py`). Agente não commita direto.
- Código C++/QML do QGroundControl: siga `AGENTS.upstream.md` (style, Fact
  System, CI, preflight).
- O plugin `qgc4qgis/` é código Python/QGIS: mesmo padrão dos outros plugins —
  o review só aprova com testes verdes (e, onde aplicável, Qt5 E Qt6).
- Sincronizar/rebasar com o upstream só por decisão explícita do Diego.
