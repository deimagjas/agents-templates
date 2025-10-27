# Agent: a2t

Documentación para el agente `a2t` incluido en este repositorio.

## Descripción

El agente `a2t` es una plantilla ligera para ejecutar un agente que interactúa con servicios en la nube. Este README describe cómo lanzar el agente y las variables de entorno obligatorias para su correcto funcionamiento.

## Requisitos

- Tener instalado el ADK (Agent Development Kit) y estar familiarizado con su comando `adk run`.
- Acceso a las credenciales necesarias para usar el servicio de Bedrock (u otro servicio configurado internamente por el agente).

## Variables de entorno obligatorias

Antes de lanzar el agente, exporta las siguientes variables de entorno en tu shell:

- `AWS_REGION_NAME` — Región de AWS que debe usar el agente (por ejemplo `us-east-1`).
- `AWS_BEARER_TOKEN_BEDROCK` — Token de autorización (Bearer token) para acceder al servicio Bedrock.

Ejemplo (zsh):

```zsh
export AWS_REGION_NAME=us-east-1
export AWS_BEARER_TOKEN_BEDROCK="<tu_bearer_token_aqui>"
```

Nota: Mantén `AWS_BEARER_TOKEN_BEDROCK` seguro y no lo comprometas en repositorios públicos.

## Cómo lanzar el agente

Para iniciar el agente usa el siguiente comando desde la raíz del proyecto:

```zsh
# En desarrollo (usar ADK)
adk run a2t

# También puedes ejecutar cualquier agente por su nombre:
adk run <nombre_del_agente>

# Lanzar la interfaz web de desarrollo (si está disponible)
adk web
```

Para ejecutar el agente fuera del ADK (por ejemplo en un entorno de producción o para pruebas fuera del flujo de desarrollo) puedes ejecutar directamente el script del ejemplo. Por ejemplo:

```zsh
# Ejecutar el agente de ejemplo con 'uv'
uv run python  adk_example/agent.py
```

Este conjunto de comandos permite lanzar el agente en modo desarrollo usando las herramientas del ADK (`adk run`, `adk web`) o ejecutar el ejemplo directamente cuando se desea correrlo sin el ADK.

## Ejemplo de flujo rápido

1. Configura las variables de entorno (ver sección anterior).
2. Ejecuta `adk run a2t`.
3. Observa los logs en la terminal y prueba las funcionalidades expuestas por el agente según cómo esté implementado en `a2t/agent.py`.

## Buenas prácticas y notas

- No incluyas tokens ni credenciales en el código ni en commits.
- Usa un gestor de secretos o variables de entorno en entornos de producción (AWS Secrets Manager, Vault, etc.).
- Si necesitas cambiar la configuración (por ejemplo, otro servicio o parámetros), revisa y modifica `a2t/agent.py`.

## Contacto y contribuciones

Si encuentras errores o quieres mejorar la plantilla, abre un issue o PR en este repositorio con una descripción clara del cambio.
