# BJS - Sistema de Procesamiento de Boletines Judiciales para extraer Remates Judiciales con ayuda de la tecnológia AI

## Descripción General

El **Boletines Judiciales System (BJS)** es una plataforma integral de automatización y análisis diseñada para la extracción, procesamiento e indexación inteligente de remates judiciales en Costa Rica. El sistema procesa boletines oficiales en formato PDF utilizando Inteligencia Artificial local (modelos LLM ejecutados en llama.cpp) y heurísticas legales avanzadas para identificar, clasificar y estructurar información crítica relacionada con subastas judiciales de vehículos y bienes inmuebles.

BJS opera como un pipeline completo de datos: ingesta de documentos, extracción de texto, análisis semántico legal, estructuración de entidades, almacenamiento en base de datos MySQL y visualización mediante una interfaz web especializada. La plataforma es capaz de detectar automáticamente publicaciones relevantes dentro de documentos complejos, interpretar lenguaje jurídico, y transformar información no estructurada en registros organizados y consultables.

El sistema permite cargar boletines de forma automática o manual desde una carpeta designada o mediante una interfaz web. Cada documento es procesado por un motor de IA local que identifica remates judiciales de vehículos y propiedades, extrae atributos clave —como marca, modelo, VIN, matrícula, plano catastrado, ubicación, juzgado, expediente, precio base y fecha de remate— y genera registros estructurados que se almacenan en una base de datos centralizada.

El sistema contempla funciones de detección de duplicados, manejo de errores de OCR, reprocesamiento de documentos, edición manual de registros, generación de exportaciones (CSV y SQL), y un módulo analítico con métricas operativas sobre actividad judicial, distribución geográfica y comportamiento de precios.

Diseñado para operar sobre infraestructura local (XAMPP, MySQL y llama), BJS prioriza independencia tecnológica, privacidad de datos y escalabilidad futura. La arquitectura permite integrar nuevas fuentes judiciales, ampliar capacidades de análisis, conectar con sistemas externos y evolucionar hacia una plataforma comercial de inteligencia de remates judiciales.

El resultado es un entorno robusto que transforma boletines legales en información accionable: un sistema que no solo registra remates, sino que los organiza, los anticipa, los analiza y los convierte en una herramienta estratégica para consulta, monitoreo y detección de oportunidades dentro del ámbito judicial e inmobiliario.

## Disclaimer legal:

Cumplimiento legal y tratamiento de datos

El sistema BJS se diseña conforme al marco jurídico costarricense en materia de acceso a la información pública y protección de datos personales (Ley N.º 8968 y normativa del Poder Judicial).

BJS no interactúa ni se conecta directamente con bases de datos institucionales, gubernamentales o judiciales, ni realiza scraping de sistemas protegidos.

El sistema procesa únicamente documentos PDF previamente descargados y almacenados localmente por el usuario, provenientes de publicaciones oficiales de acceso público (como el Boletín Judicial), y los analiza con fines de organización, indexación y consulta.

La información extraída se utiliza con finalidad informativa y de gestión documental, respetando principios de proporcionalidad, finalidad y seguridad del tratamiento de datos personales.

El responsable de la instalación y uso del sistema deberá garantizar el cumplimiento de la legislación vigente sobre protección de datos, confidencialidad y uso legítimo de la información pública.

## Características Principales

- **Procesamiento Asíncrono**: La carga de documentos PDF masivos se realiza en segundo plano, permitiendo el uso continuo de la interfaz sin bloqueos.
- **Detección Inteligente**:
  - Utiliza heurísticas específicas (frase clave "En este Despacho") para garantizar la captura de todos los remates.
  - Integra modelos de lenguaje locales (Llama.cpp / Qwen2.5) para extraer datos estructurados (marca, modelo, placa, precio base, juzgado) de texto legal no estructurado.
- **Gestión de Datos**:
  - Almacenamiento persistente en base de datos MySQL.
  - Interfaz web para visualizar, detallar y eliminar registros.
- **Extracción Robusta**: Fuerza la indexación de remates detectados incluso si la extracción de datos es parcial, asegurando que no se pierdan oportunidades importantes.

## Arquitectura del Sistema

### Backend (Python / FastAPI)
- **Framework**: FastAPI para una API RESTful de alto rendimiento.
- **Motor de I.A.**: `llama-cpp-python` para ejecutar modelos GGUF optimizados localmente.
- **Procesamiento de PDF**: `PyMuPDF` (fitz) para la extracción de texto crudo.
- **Base de Datos**: `mysql-connector` para la gestión de registros.
- **Background Tasks**: Gestión de colas de trabajo para el procesamiento pesado de documentos.

### Frontend (HTML5 / JS)
- **Diseño**: Bootstrap 5 para una interfaz responsiva y moderna.
- **Lógica**: Vanilla JavaScript para la interacción con la API (Carga de archivos, listado dinámico, modales de detalle, eliminación de registros).

## Flujo de Trabajo

1.  **Carga**: El usuario sube un PDF (Boletín Judicial) a través de la interfaz web.
2.  **Cola de Trabajo**: El servidor recibe el archivo y confirma la recepción inmediatamente, iniciando el proceso de análisis en segundo plano.
3.  **Extracción y Segmentación**:
    - El sistema extrae todo el texto del PDF.
    - Se identifican bloques de texto que inician con "En este Despacho", marcándolos como remates confirmados.
4.  **Análisis con I.A.**:
    - Cada bloque identificado es enviado al modelo LLM local.
    - El modelo intenta estructurar la información en formato JSON (Vehículo/Propiedad, Descripción, Precio, etc.).
    - Si el modelo falla en estructurar, el sistema guarda el bloque como un remate "detectado" con la información disponible, garantizando cero pérdida de datos.
5.  **Visualización**: Los resultados aparecen en tiempo real en la tabla de la interfaz web, donde el usuario puede consultar los detalles completos o eliminar registros irrelevantes.

## Requisitos del Sistema

- Python 3.10+
- MySQL Server
- Modelos GGUF (ej. Qwen2.5-3B-Instruct) en la carpeta `modelos/`
- Bibliotecas Python: `fastapi`, `uvicorn`, `mysql-connector-python`, `pymupdf`, `llama-cpp-python`

## Instalación y Uso

1.  Clonar el repositorio.
2.  Instalar dependencias: `pip install -r requirements.txt`.
3.  Configurar la base de datos en `backend/init_db.py` y `backend/main.py`.
4.  Colocar el modelo `.gguf` en la carpeta `modelos`.
5.  Iniciar el servidor: ejecutar `start_server.bat` o `uvicorn backend.main:app --reload`.
6.  Acceder a `http://localhost:8000` (o abrir `index.html` servido estáticamente).

---------------------------------------------------------------------

TO DO LIST — Sistema BJS (Boletines Judiciales System)

Objetivo: ampliar el sistema con funciones de filtrado avanzado, búsqueda inteligente, alertas y lógica de precios para seguimiento de remates judiciales.


1. FILTRADO AVANZADO EN INTERFAZ WEB

Implementar en el panel principal:

* filtro por tipo:

  * vehículo
  * propiedad
* filtro por tipo de propiedad:

  * casa
  * lote
  * terreno
  * finca
  * apartamento
* filtro por rango de precios:

  * mínimo
  * máximo
* filtro por fecha de remate:

  * hoy
  * esta semana
  * este mes
  * rango personalizado
* filtro por ubicación:

  * provincia
  * cantón
  * distrito
* filtro por juzgado
* filtro por estado:

  * pendiente
  * adjudicado
  * reprogramado
  * cancelado

Los filtros deben:

* combinarse entre sí
* guardarse en sesión del usuario
* permitir ordenamiento por:

  * precio
  * fecha
  * tipo
  * ubicación


2. BÚSQUEDA POR ATRIBUTOS

Crear motor de búsqueda estructurada y textual:

Campos buscables:

* marca
* modelo
* VIN
* placa
* matrícula
* plano catastrado
* expediente
* texto completo del remate

Funciones:

* búsqueda rápida global
* búsqueda avanzada por múltiples campos
* autocompletado
* tolerancia a errores (fuzzy search)
* indexación para velocidad (FULLTEXT MySQL o Elastic futuro)


3. SISTEMA DE ALERTA TEMPRANA (3 DÍAS ANTES)

Crear módulo automático que:

* revise base de datos diariamente
* detecte remates con fecha dentro de 3 días
* genere alertas:

Tipos:

* notificación web
* email
* dashboard de alertas

Información en alerta:

* tipo remate
* ubicación
* precio base
* fecha y hora
* link a detalle

Agregar:

* configuración de días previos (1, 3, 5, 7)
* sistema de suscripción por tipo:

  * solo vehículos
  * solo propiedades
  * zonas específicas


4. SISTEMA DE PRECIOS EN CASCADA

Objetivo:
seguir remates que no fueron adjudicados y registrar nuevos precios en remates posteriores.

Lógica:

Si un remate:

* no se adjudica
* se reprograma

entonces:

* crear nuevo registro vinculado al anterior
* guardar histórico de precios

Campos nuevos:

* id_remate_original
* intento_numero
* precio_anterior
* precio_actual
* porcentaje_reduccion
* estado_remate

Funcionalidad:

* visualizar evolución del precio
* gráfico de bajadas
* detección automática de oportunidades

Ejemplo:

Remate 1:
₡50M

Remate 2:
₡40M

Remate 3:
₡32M


5. DETECCIÓN DE OPORTUNIDADES

Sistema que identifique:

* remates con reducción significativa
* precios debajo de promedio de mercado
* remates repetidos

Mostrar en panel:

"OPORTUNIDADES"


6. DASHBOARD ANALÍTICO

Panel con:

* total remates activos
* remates por tipo
* remates próximos
* reducción promedio de precios
* zonas con más actividad judicial


7. AUTOMATIZACIÓN OPERATIVA

Agregar:

* cron de procesamiento PDF
* cron de alertas
* cron de reanálisis de remates no adjudicados


8. ESCALABILIDAD FUTURA

Preparar arquitectura para:

* múltiples fuentes judiciales
* integración con portales inmobiliarios
* valoración automática de propiedades
* API pública


RESULTADO ESPERADO

Un sistema que no solo registre remates judiciales, sino que:

* permita buscarlos profesionalmente
* anticipe eventos importantes
* detecte oportunidades reales
* siga la evolución de precios
* sirva como herramienta comercial y analítica.


*Desarrollado como una solución de automatización legal mediante I.A. local para privacidad y eficiencia.*
