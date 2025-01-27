# Gestión de Subida de Imágenes con S3 y URLs Prefirmadas
Este proyecto implementa la funcionalidad para gestionar la subida de imágenes a un bucket de Amazon S3 mediante URLs prefirmadas, utilizando un backend desarrollado con Python y un frontend que permite a los usuarios cargar imágenes directamente al bucket sin exponer las credenciales de AWS.

## Funcionalidad
1. Generación de URLs prefirmadas:

- Se genera una URL con permisos temporales para subir archivos directamente a S3.
- Las URLs prefirmadas tienen un tiempo de expiración configurable (por defecto, 1 hora).

2. Subida segura de imágenes:

- Los usuarios pueden subir imágenes al bucket sin necesidad de tener credenciales de AWS.
- El backend valida la solicitud y entrega las URLs prefirmadas a los clientes autorizados.

3. Configuración del bucket S3:

- Políticas de seguridad configuradas para restringir el acceso y permitir solo subidas específicas desde URLs prefirmadas o referencias autorizadas.

## Tecnologías utilizadas
- Backend: Python (Boto3, FastAPI)
- Servicios en la nube: Amazon S3
- Despliegue del backend: Render Dashboard
- Base de datos: MongoDB Atlas
