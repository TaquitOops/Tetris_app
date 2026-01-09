# Tetris Game
Un juego de Tetris completo con sistema de autenticación, preguntas de cultura general y ranking global.

# Características
- Autenticación: Sistema de login y registro con Supabase Auth
- Juego de Tetris: Con controles táctiles para dispositivos móviles
- Preguntas de Trivia: Al llegar a Game Over, responde preguntas de cultura general para continuar
- Sistema de Niveles: El juego se vuelve más difícil con cada nivel
- Ranking: Tabla de clasificación con las mejores partidas del jugador
- Puntajes Persistentes: Los puntajes se guardan en la base de datos

# Cómo Jugar

1. Registro/Login: Crea una cuenta o inicia sesión con tu correo y contraseña
2. Menú Principal:
   -  JUGAR: Comienza una nueva partida
   -  TOP GLOBAL: Ve los mejores puntajes
   -  SALIR: Cierra sesión
3. Controles del Juego:
   - ⬅️: Mover pieza a la izquierda
   - ➡️: Mover pieza a la derecha
   - ⬇️: Mover pieza hacia abajo
   - 🔄 ROTAR: Rotar la pieza
   - ⬇️⬇️ DROP: Dejar caer la pieza rápidamente
4. Game Over: Cuando pierdas, responde una pregunta de cultura general:
   -  Respuesta correcta: Continúas jugando con la mitad del puntaje
   -  Respuesta incorrecta: Pierdes el puntaje y vuelves al menú

# Instalación
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python main.py
```
# Tecnologías Utilizadas

- Python 3: Lenguaje de programación
- Flet: Framework para crear aplicaciones multiplataforma
- Supabase: Backend as a Service para autenticación y base de datos
- PostgreSQL: Base de datos relacional
  
# Estructura de la Base de Datos

- profiles: Perfiles de usuario con nombres de usuario
- scores: Puntajes de los jugadores con niveles alcanzados
- questions: Preguntas de cultura general para el modo trivia

# Para Dispositivos Móviles

Esta aplicación está diseñada para funcionar en dispositivos móviles gracias a:
- Botones táctiles para todos los controles
- Interfaz responsive
- Flet permite compilar a APK para Android o IPA para iOS
