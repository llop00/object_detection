## Apartado 2: Pasos necesarios para entrenar un modelo de detección con categorías no existentes en los modelos preentrenados

### Pasos a seguir.

1. **Recolección de datos**: recolectar imágenes etiquetadas de las nuevas categorías de objetos a detectar.
  - ¿Dispongo de un dataset para las nuevas categorías necesarias?
    - **Sí**
      - Procede con la siguiente etapa de desarrollo.
    - **No**
      - **Decisión:** Buscar un dataset existente vs. Recolectar y anotar datos propios mediante herramientas con soporte para YOLO como https://github.com/HumanSignal/labelImg.

    Cualquier de los datasets seleccionados deberá seguir el siguiente formato YOLO:
    
    ```
    class x_center y_center width height
    ```

2. **Preprocesamiento de datos**: realizar preprocesamiento necesario, como redimensionamiento (640x640 para YOLOv9) y normalización de las imágenes, en caso de ser significativamente diferentes a las de entrenamiento. También se puede considerar aplicar técnicas de data augmentation en el caso de no contar con datos suficientes o probar si mejoran el desempeño del modelo.

3. **Configuración del entrenamiento**: la elección del YOLO facilita el entrenamiento, siendo posible el uso de librerías que directamente implementan el proceso de finetuning. https://docs.ultralytics.com/es/modes/train/

4. **Monitorización del entrenamiento**: conviene monitorizar el desempeño del modelo. Para ello pueden utilizarse herramientas como tensorboard https://docs.ultralytics.com/es/integrations/tensorboard/

5. **Evaluación**: evaluar el rendimiento del modelo en un conjunto de datos de prueba y realizar ajustes si es necesario. La métrica de evaluación habitual es AP (Average precision) para diferentes IoU (Intersection over Union).

### Descripción de posibles problemas que puedan surgir y medidas para reducir el riesgo.

- **Sobreajuste**: a la hora de reentrenar el modelo para nuevas categorías, lo más habitual es seguir un proceso de fine-tuning, en lugar de entrenar de 0 el modelo. Es necesario decidir, que porcentaje de la red vamos a entrenar, pudiendo esto afectar a la capacidad de generalización del modelo sobre las clases ya entrenadas.

- **Datos insuficientes o sesgados**: incluir una amplia variedad de ejemplos en el conjunto de datos para las diferentes clases que se pretendan incluir, que comprendan la naturaleza de situaciones en las que se observaran durante la inferencia. La capacidad de generalización puede además probarse sobre un conjunto de test que comprenda situaciones nunca antes vistas.

- **Desbalanceo en los datos**: al recurrir a técnicas de fine-tuning, podemos caer en un problema de desbalanceo de clases, al estar trabajando sobre un subconjunto presumiblemente menor que el utilizado durante el entrenamiento para el resto de clases. En el caso de ser imposible recopilar más muestras, podría recurrirse a técnicas de data augmentation.


### Estimación de cantidad de datos necesarios y resultados esperados

El dataset COCO cuenta con 200k imágenes etiquetadas para 80 categorías, por lo que se recomienda al menos unos cientos de imágenes anotadas por categoría que se quiera añadir.

En referencia a los problemas comentados en el apartado anterior, deberá probarse la capacidad de generalización del modelo con los datos disponibles, y observar sesgos o la influencia en el desbalanceo de los datos.

Por ejemplo, a la hora de entrenar el modelo para reconocer una nueva categoría "bache de carretera". Podemos centrarnos en recolectar muestras de un país y evaluar su rendimiento. Si en el futuro trasladamos el mismo servicio de reconocimiento a otro país, debemos cerciorarnos de la capacidad de generalización del modelo sobre nuevas carreteras, y si debemos construir el dataset con más imágenes de forma equilibrada.

### Enumeración y pequeña descripción (2-3 frases) de técnicas que se pueden utilizar para:

#### Mejorar el desempeño

- Data Augmentation: realizar transformaciones sobre las imágenes como rotaciones, cambios de escala, ajustes de brillo o contrastes, y añadirlas al conjunto de entrenamiento. Esto ayuda al modelo a aprender características robustas que son invariantes a las diferentes situaciones que pueda encontrarse durante la inferencia.

- Fine-tuning: entrenar las últimas capas del modelo preentrenado con el nuevo conjunto de datos para mejorar la precisión para las nuevas clases manteniendo el conocimiento adquirido durante el entrenamiento original. El número de capas del modelo a entrenar puede considerarse un hiperparámetro.

- Regularización: técnicas como la regularización L1/L2 y Dropout previenen el sobreajuste al añadir una penalización a los pesos de gran magnitud y desactivar aleatoriamente ciertas neuronas durante el entrenamiento, respectivamente. Implica modificar la arquitectura del modelo original.

- Optimización de hiperparámetros: una gran parte de los esfuerzos debe ir dedicada al ajuste de los hiperparámetros utilizados para finetunear el modelo, como la tasa de aprendizaje, el batch size o el número de epochs.

- Ensemble Learning: combinar las predicciones de múltiples modelos puede mejorar la precisión y robustez del sistema de detección. https://docs.ultralytics.com/es/yolov5/tutorials/model_ensembling/.

- Attention-Maps: se tratan de algoritmos que buscan mejorar la interpretabilidad del modelo mostrando mapas de calor de las zonas de la imagen que han sido más determinantes para que el modelo realice una predicción. Una sugerencia de herramienta es Grad-CAM https://github.com/pooya-mohammadi/yolov5-gradcam

#### Métricas del modelo en tiempo de entrenamiento

- Loss: seguimiento del valor de la función de perdida utilizada por el modelo para las epochs durante las que se realiza el entrenamiento. Puede ayudarnos a rastrear tanto la estabilidad del entrenamiento como divergencias con los datos de test.

- MAP: Mean Average Precision, se calcula con la precisión y el recall para cada clase a diferentes umbrales de confianza. Luego, se calcula la precisión promedio (AP) para cada clase al calcular el área bajo la curva precision-recall. Finalmente, el mAP es el promedio de estos valores de AP para todas las clases.

  - mAP@.5: MAP con un IoU de al menos 0.5 

  - mAP@.5:.95 MAP medio en intervalos de 0.05 desde 0.5 hasta 0.95

#### Métricas del modelo en tiempo de inferencia

- Tiempo de Inferencia: el tiempo que tarda el modelo en procesar una imagen y realizar predicciones.

- FPS (Frames Per Second): en el caso de utilizar el modelo para predicciones sobre vídeo, debe medirse el número de imágenes (frames) que el modelo puede procesar por segundo. 

- Consumo de recursos: evaluar el uso de memoria y la carga computacional del modelo durante la inferencia. Pueden realizarse pruebas de estrés, observando la capacidad máxima de peticiones y su tiempo de respuesta. Desplegando en edge sobre dispositivos con menores recursos como móviles o dispositivos especializados como NVIDIA Jetson, debe comprobarse de forma especialmente crítica la fluidez del modelo.