CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS profiles (
  id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  username text UNIQUE NOT NULL,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS scores (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  score integer NOT NULL DEFAULT 0,
  level integer NOT NULL DEFAULT 1,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS questions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  question text NOT NULL,
  option_a text NOT NULL,
  option_b text NOT NULL,
  option_c text NOT NULL,
  option_d text NOT NULL,
  correct_answer char(1) NOT NULL
    CHECK (correct_answer IN ('A','B','C','D')),
  created_at timestamptz DEFAULT now()
);

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE questions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "profiles_select"
  ON profiles FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "profiles_insert"
  ON profiles FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = id);

CREATE POLICY "profiles_update"
  ON profiles FOR UPDATE
  TO authenticated
  USING (auth.uid() = id);

CREATE POLICY "scores_select"
  ON scores FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "scores_insert"
  ON scores FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "questions_select"
  ON questions FOR SELECT
  TO authenticated
  USING (true);

CREATE INDEX IF NOT EXISTS idx_scores_user_id
  ON scores(user_id);

CREATE INDEX IF NOT EXISTS idx_scores_leaderboard
  ON scores(score DESC, level DESC);

INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_answer) VALUES
('¿Cuál es la capital de Francia?', 'Londres', 'Berlín', 'París', 'Madrid', 'C'),
('¿En qué año llegó el hombre a la Luna?', '1965', '1969', '1972', '1980', 'B'),
('¿Quién pintó la Mona Lisa?', 'Picasso', 'Van Gogh', 'Da Vinci', 'Dalí', 'C'),
('¿Océano más grande del mundo?', 'Atlántico', 'Índico', 'Ártico', 'Pacífico', 'D'),
('¿Cuántos continentes hay?', '5', '6', '7', '8', 'C')
ON CONFLICT DO NOTHING;
