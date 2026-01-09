/*
  # Crear estructura de base de datos para Tetris

  ## Descripción
  Este script crea todas las tablas necesarias para el juego de Tetris con sistema de autenticación,
  puntajes, niveles y preguntas de cultura general.

  ## 1. Nuevas Tablas
  
  ### `profiles`
  - `id` (uuid, FK a auth.users)
  - `username` (text, único) - Nombre de usuario
  - `created_at` (timestamp) - Fecha de creación
  
  ### `scores`
  - `id` (uuid, PK) - ID único del puntaje
  - `user_id` (uuid, FK a auth.users) - ID del usuario
  - `score` (integer) - Puntaje obtenido
  - `level` (integer) - Nivel alcanzado
  - `created_at` (timestamp) - Fecha del puntaje
  
  ### `questions`
  - `id` (uuid, PK) - ID único de la pregunta
  - `question` (text) - Texto de la pregunta
  - `option_a` (text) - Opción A
  - `option_b` (text) - Opción B
  - `option_c` (text) - Opción C
  - `option_d` (text) - Opción D
  - `correct_answer` (text) - Respuesta correcta (A, B, C o D)
  - `created_at` (timestamp) - Fecha de creación

  ## 2. Seguridad
  
  - Se habilita RLS en todas las tablas
  - Los usuarios pueden leer y actualizar su propio perfil
  - Los usuarios pueden insertar y leer sus propios puntajes
  - Los usuarios pueden leer el top global de puntajes
  - Todos los usuarios autenticados pueden leer las preguntas

  ## 3. Índices
  
  - Índice en scores.user_id para consultas rápidas de puntajes por usuario
  - Índice en scores.score para ordenamiento rápido del leaderboard

  ## 4. Datos Iniciales
  
  - Se insertan 20 preguntas de cultura general en español
*/

-- Crear tabla de perfiles
CREATE TABLE IF NOT EXISTS profiles (
  id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  username text UNIQUE NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Crear tabla de puntajes
CREATE TABLE IF NOT EXISTS scores (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL,
  score integer NOT NULL DEFAULT 0,
  level integer NOT NULL DEFAULT 1,
  created_at timestamptz DEFAULT now(),

  CONSTRAINT scores_user_id_fkey
    FOREIGN KEY (user_id)
    REFERENCES profiles(id)
    ON DELETE CASCADE
);

-- Crear tabla de preguntas
CREATE TABLE IF NOT EXISTS questions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  question text NOT NULL,
  option_a text NOT NULL,
  option_b text NOT NULL,
  option_c text NOT NULL,
  option_d text NOT NULL,
  correct_answer text NOT NULL CHECK (correct_answer IN ('A', 'B', 'C', 'D')),
  created_at timestamptz DEFAULT now()
);

-- Habilitar RLS en todas las tablas
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE questions ENABLE ROW LEVEL SECURITY;

-- Políticas para profiles
CREATE POLICY "Users can read all profiles"
  ON profiles FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Users can insert own profile"
  ON profiles FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  TO authenticated
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

-- Políticas para scores
CREATE POLICY "Users can read all scores for leaderboard"
  ON scores FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Users can insert own scores"
  ON scores FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

-- Políticas para questions
CREATE POLICY "Authenticated users can read questions"
  ON questions FOR SELECT
  TO authenticated
  USING (true);

-- Crear índices para mejor rendimiento
CREATE INDEX IF NOT EXISTS idx_scores_user_id ON scores(user_id);
CREATE INDEX IF NOT EXISTS idx_scores_score ON scores(score DESC);
CREATE INDEX IF NOT EXISTS idx_scores_level ON scores(level DESC);
CREATE INDEX IF NOT EXISTS idx_scores_leaderboard
ON scores(score DESC, level DESC);


-- Insertar preguntas de cultura general
INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_answer)
VALUES
  ('¿Cuál es la capital de Francia?', 'Londres', 'Berlín', 'París', 'Madrid', 'C'),
  ('¿En qué año llegó el hombre a la Luna?', '1965', '1969', '1972', '1980', 'B'),
  ('¿Quién pintó la Mona Lisa?', 'Picasso', 'Van Gogh', 'Da Vinci', 'Dalí', 'C'),
  ('¿Cuál es el océano más grande del mundo?', 'Atlántico', 'Índico', 'Ártico', 'Pacífico', 'D'),
  ('¿Cuántos continentes hay en el mundo?', '5', '6', '7', '8', 'C'),
  ('¿Quién escribió Don Quijote de la Mancha?', 'García Lorca', 'Cervantes', 'Lope de Vega', 'Góngora', 'B'),
  ('¿Cuál es el planeta más grande del sistema solar?', 'Saturno', 'Júpiter', 'Neptuno', 'Urano', 'B'),
  ('¿En qué país se encuentra la Torre Eiffel?', 'Italia', 'España', 'Francia', 'Alemania', 'C'),
  ('¿Cuál es el metal más abundante en la corteza terrestre?', 'Hierro', 'Cobre', 'Aluminio', 'Oro', 'C'),
  ('¿Quién fue el primer presidente de Estados Unidos?', 'Jefferson', 'Washington', 'Lincoln', 'Adams', 'B'),
  ('¿Cuál es el río más largo del mundo?', 'Nilo', 'Amazonas', 'Yangtsé', 'Misisipi', 'B'),
  ('¿En qué año comenzó la Segunda Guerra Mundial?', '1935', '1939', '1941', '1945', 'B'),
  ('¿Cuál es el país más grande del mundo?', 'Canadá', 'China', 'Rusia', 'Estados Unidos', 'C'),
  ('¿Quién desarrolló la teoría de la relatividad?', 'Newton', 'Einstein', 'Hawking', 'Galileo', 'B'),
  ('¿Cuál es el hueso más largo del cuerpo humano?', 'Húmero', 'Tibia', 'Fémur', 'Radio', 'C'),
  ('¿En qué año se descubrió América?', '1482', '1492', '1502', '1512', 'B'),
  ('¿Cuál es la montaña más alta del mundo?', 'K2', 'Everest', 'Kilimanjaro', 'Aconcagua', 'B'),
  ('¿Quién inventó la bombilla eléctrica?', 'Tesla', 'Edison', 'Bell', 'Marconi', 'B'),
  ('¿Cuál es el animal terrestre más rápido?', 'León', 'Guepardo', 'Tigre', 'Leopardo', 'B'),
  ('¿En qué país se originaron los Juegos Olímpicos?', 'Roma', 'Egipto', 'Grecia', 'Turquía', 'C')
ON CONFLICT DO NOTHING;
