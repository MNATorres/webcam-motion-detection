# Webcam Motion Detection

![Motion Detection Banner](https://img.shields.io/badge/OpenCV-Motion%20Detection-blue?style=for-the-badge&logo=opencv)

Detecta y registra intervalos de movimiento usando tu webcam, OpenCV y pandas. Guarda los resultados en un archivo CSV.

---

## 🚀 Requisitos

- Python 3.8+
- [OpenCV](https://pypi.org/project/opencv-python/)
- [pandas](https://pypi.org/project/pandas/)

Instala dependencias con:

```bash
pip install opencv-python pandas
```

---

## 🖥️ Uso rápido

1. Clona este repositorio o descarga los archivos.
2. Ejecuta el script principal:

```bash
python capture.py
```

3. Se abrirán varias ventanas mostrando el video y el procesamiento.
4. Presiona `q` para finalizar la grabación.
5. Consulta los intervalos de movimiento detectados en el archivo `Times.csv`.

---

## 📂 ¿Qué hace el script?

- Inicia la webcam y analiza el video en tiempo real.
- Detecta cambios significativos entre frames (movimiento).
- Marca los momentos de inicio y fin de cada movimiento.
- Guarda los intervalos en un archivo CSV para su análisis posterior.

---

## 📝 Ejemplo de salida (`Times.csv`)

| Start                | End                  |
|----------------------|---------------------|
| 2025-08-22 18:02:23  | 2025-08-22 18:03:10 |
| 2025-08-22 18:04:01  | 2025-08-22 18:04:15 |

---

## 🎨 Créditos y recursos

- Basado en tutoriales de OpenCV y pandas.
- Autor: MNATorres

---

## 💡 Notas

- Puedes ajustar la sensibilidad cambiando el valor de área mínima en el script (`cv2.contourArea(contour) < 1000`).
- El script funciona en Windows, Linux y MacOS.

---

¡Contribuciones y sugerencias son bienvenidas!
