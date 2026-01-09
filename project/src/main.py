import flet as ft
import os
import random
import asyncio
from supabase_client import supabase
from tetris_game import TetrisGame, BOARD_WIDTH, BOARD_HEIGHT, CELL_SIZE


class TetrisApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Tetris Game"
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 20

        self.user = None
        self.username = ""
        self.game = None
        self.game_loop_running = False
        self.current_question = None

        self.show_login()

    def show_login(self):
        self.page.clean()

        email_field = ft.TextField(label="Correo", width=300, autofocus=True)
        password_field = ft.TextField(label="Contraseña", password=True, width=300)
        error_text = ft.Text("", color=ft.Colors.RED)
        
        def login_click(e):
            try:
                response = supabase.auth.sign_in_with_password({
                    "email": email_field.value,
                    "password": password_field.value
                })

                if response.user is None:
                    error_text.value = "Credenciales incorrectas"
                    self.page.update()
                    return

                self.user = response.user

                profile = (
                    supabase
                    .table("profiles")
                    .select("username")
                    .eq("id", self.user.id)
                    .single()
                    .execute()
                )

                self.username = profile.data["username"]
                self.show_menu()

            except Exception as ex:
                error_text.value = f"Error: {str(ex)}"
                self.page.update()

        def go_to_register(e):
            self.show_register()

        self.page.add(
            ft.Column(
                [
                    ft.Text("TETRIS GAME", size=40, weight=ft.FontWeight.BOLD),
                    ft.Text("Inicia Sesión", size=24),
                    email_field,
                    password_field,
                    error_text,
                    ft.ElevatedButton("Iniciar Sesión", on_click=login_click, width=300),
                    ft.TextButton("¿No tienes cuenta? Regístrate", on_click=go_to_register),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    def show_register(self):
        self.page.clean()

        username_field = ft.TextField(label="Usuario", width=300)
        email_field = ft.TextField(label="Correo", width=300, autofocus=True)
        password_field = ft.TextField(label="Contraseña", password=True, width=300)
        error_text = ft.Text("", color=ft.Colors.RED)
        success_text = ft.Text("", color=ft.Colors.GREEN)
        
        def register_click(e):
            try:
                response = supabase.auth.sign_up({
                    "email": email_field.value,
                    "password": password_field.value
                })

                if response.user is None:
                    error_text.value = "Error al crear usuario"
                    self.page.update()
                    return

                supabase.table("profiles").insert({
                    "id": response.user.id,
                    "username": username_field.value
                }).execute()

                success_text.value = "Registro exitoso. Inicia sesión."
                error_text.value = ""
                self.page.update()

            except Exception as ex:
                error_text.value = f"Error: {str(ex)}"
                self.page.update()

        def go_to_login(e):
            self.show_login()

        self.page.add(
            ft.Column(
                [
                    ft.Text(" TETRIS GAME", size=40, weight=ft.FontWeight.BOLD),
                    ft.Text("Registro", size=24),
                    username_field,
                    email_field,
                    password_field,
                    error_text,
                    success_text,
                    ft.ElevatedButton("Registrarse", on_click=register_click, width=300),
                    ft.TextButton("¿Ya tienes cuenta? Inicia Sesión", on_click=go_to_login),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    def show_menu(self):
        self.page.clean()

        def play_click(e):
            self.start_game()

        def leaderboard_click(e):
            self.show_leaderboard()

        def logout_click(e):
            supabase.auth.sign_out()
            self.user = None
            self.username = ""
            self.show_login()

        self.page.add(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(f"Usuario: {self.username}", size=16),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    ft.Text(" TETRIS GAME", size=50, weight=ft.FontWeight.BOLD),
                    ft.Container(height=20),
                    ft.ElevatedButton(
                        " JUGAR",
                        on_click=play_click,
                        width=300,
                        height=60,
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.GREEN_700,
                        ),
                    ),
                    ft.ElevatedButton(
                        " PARTIDAS",
                        on_click=leaderboard_click,
                        width=300,
                        height=60,
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLUE_700,
                        ),
                    ),
                    ft.ElevatedButton(
                        " SALIR",
                        on_click=logout_click,
                        width=300,
                        height=60,
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.RED_700,
                        ),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    def show_leaderboard(self):
        self.page.clean()

        try:
            response = (
                supabase
                .table("scores")
                .select("score, level, created_at")
                .eq("user_id", self.user.id)
                .order("score", desc=True)
                .limit(10)
                .execute()
            )

            leaderboard_items = []

            if not response.data:
                leaderboard_items.append(
                    ft.Text("Aún no tienes partidas guardadas", size=18)
                )
            else:
                for idx, record in enumerate(response.data, 1):
                    leaderboard_items.append(
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Text(f"{idx}.", size=18, weight=ft.FontWeight.BOLD, width=40),
                                    ft.Text(f"{record['score']} pts", size=18, width=120),
                                    ft.Text(f"Nivel {record['level']}", size=16),
                                ],
                            ),
                            padding=10,
                            border=ft.border.all(1, ft.Colors.BLUE_700),
                            border_radius=10,
                        )
                    )

        except Exception as ex:
            leaderboard_items = [
                ft.Text(f"Error al cargar partidas: {str(ex)}", color=ft.Colors.RED)
            ]

        def back_click(e):
            self.show_menu()

        self.page.add(
            ft.Column(
                [
                    ft.Text("MIS MEJORES PARTIDAS", size=36, weight=ft.FontWeight.BOLD),
                    ft.Container(height=20),
                    ft.Column(leaderboard_items, scroll=ft.ScrollMode.AUTO, height=400),
                    ft.Container(height=20),
                    ft.ElevatedButton("Volver al Menú", on_click=back_click, width=300),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )


    def start_game(self):
        self.game = TetrisGame()
        self.game_loop_running = True
        self.page.clean()

        board_container = ft.Container(
            width=BOARD_WIDTH * CELL_SIZE,
            height=BOARD_HEIGHT * CELL_SIZE,
            bgcolor=ft.Colors.BLACK,
            border=ft.border.all(2, ft.Colors.WHITE),
            content=ft.Stack(
                [],
                width=BOARD_WIDTH * CELL_SIZE,
                height=BOARD_HEIGHT * CELL_SIZE,
            ),
        )

        score_text = ft.Text(f"Puntuación: {self.game.score}", size=20, weight=ft.FontWeight.BOLD)
        level_text = ft.Text(f"Nivel: {self.game.level}", size=20)
        username_text = ft.Text(f"Usuario: {self.username}", size=16)
        
        def update_board():
            cells = []

            # Dibujar tablero fijo
            for y in range(BOARD_HEIGHT):
                for x in range(BOARD_WIDTH):
                    if self.game.board[y][x]:
                        cells.append(
                            ft.Container(
                                left=x * CELL_SIZE,
                                top=y * CELL_SIZE,
                                width=CELL_SIZE - 1,
                                height=CELL_SIZE - 1,
                                bgcolor=self.game.board[y][x],
                                border_radius=2,
                            )
                        )

            # Dibujar pieza actual
            if self.game.current_piece:
                for x, y in self.game.current_piece.get_cells():
                    if y >= 0:
                        cells.append(
                            ft.Container(
                                left=x * CELL_SIZE,
                                top=y * CELL_SIZE,
                                width=CELL_SIZE - 1,
                                height=CELL_SIZE - 1,
                                bgcolor=self.game.current_piece.color,
                                border_radius=2,
                            )
                        )

            board_container.content = ft.Stack(cells)
            score_text.value = f"Puntuación: {self.game.score}"
            level_text.value = f"Nivel: {self.game.level}"
            self.page.update()

        def move_left(e):
            if self.game and not self.game.game_over:
                self.game.move_piece(-1, 0)
                update_board()

        def move_right(e):
            if self.game and not self.game.game_over:
                self.game.move_piece(1, 0)
                update_board()

        def rotate(e):
            if self.game and not self.game.game_over:
                self.game.rotate_piece()
                update_board()

        def move_down(e):
            if self.game and not self.game.game_over:
                self.game.move_piece(0, 1)
                update_board()

        def hard_drop(e):
            if self.game and not self.game.game_over:
                self.game.hard_drop()
                update_board()

        def pause_game(e):
            self.game_loop_running = False
            self.show_menu()

        async def game_loop():
            while self.game_loop_running and not self.game.game_over:
                await asyncio.sleep(max(0.6 - self.game.level * 0.08, 0.08))
                if self.game and not self.game.game_over:
                    self.game.drop_piece()
                    update_board()

            if self.game.game_over:
                self.game_loop_running = False
                self.show_trivia_question()

        update_board()

        self.page.add(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=score_text,
                                expand=True,
                            ),
                            username_text,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    level_text,
                    ft.Container(height=10),
                    board_container,
                    ft.Container(height=20),
                    ft.Row(
                        [
                            ft.ElevatedButton("⬅️", on_click=move_left, width=80, height=60),
                            ft.ElevatedButton("⬇️", on_click=move_down, width=80, height=60),
                            ft.ElevatedButton("➡️", on_click=move_right, width=80, height=60),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton("ROTAR", on_click=rotate, width=120, height=60),
                            ft.ElevatedButton("DROP", on_click=hard_drop, width=120, height=60),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.ElevatedButton("MENU", on_click=pause_game, width=250),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

        self.page.run_task(game_loop)
    
    async def continue_after_correct(self):
        await asyncio.sleep(2)
        self.start_game()

    async def continue_after_wrong(self):
        await asyncio.sleep(2)
        self.show_game_over(True)

    def show_trivia_question(self):
        self.page.clean()

        try:
            response = supabase.table("questions").select("*").execute()
            questions = response.data

            if questions:
                self.current_question = random.choice(questions)
            else:
                self.show_game_over(True)
                return

        except Exception as ex:
            self.show_game_over(False)
            return

        question_text = ft.Text(
            self.current_question["question"],
            size=24,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        result_text = ft.Text("", size=18, text_align=ft.TextAlign.CENTER)
        
        def check_answer(answer):
            def handler(e):
                if answer == self.current_question["correct_answer"]:
                    result_text.value = "¡Correcto! Puedes seguir jugando"
                    result_text.color = ft.Colors.GREEN
                    self.page.update()

                    self.game.reduce_score()
                    self.game.reset_board()

                    
                    self.page.run_task(self.continue_after_correct)

                else:
                    result_text.value = "Incorrecto. Juego Terminado"
                    result_text.color = ft.Colors.RED
                    self.page.update()

                    self.page.run_task(self.continue_after_wrong)

            return handler

        self.page.add(
            ft.Column(
                [
                    ft.Text("GAME OVER", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.RED),
                    ft.Text(f"Puntuación: {self.game.score}", size=24),
                    ft.Container(height=20),
                    ft.Text("Responde correctamente para continuar:", size=20),
                    ft.Container(height=10),
                    question_text,
                    ft.Container(height=20),
                    ft.ElevatedButton(
                        f"A) {self.current_question['option_a']}",
                        on_click=check_answer('A'),
                        width=400,
                    ),
                    ft.ElevatedButton(
                        f"B) {self.current_question['option_b']}",
                        on_click=check_answer('B'),
                        width=400,
                    ),
                    ft.ElevatedButton(
                        f"C) {self.current_question['option_c']}",
                        on_click=check_answer('C'),
                        width=400,
                    ),
                    ft.ElevatedButton(
                        f"D) {self.current_question['option_d']}",
                        on_click=check_answer('D'),
                        width=400,
                    ),
                    ft.Container(height=20),
                    result_text,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    def show_game_over(self, save_score=False):
        self.page.clean()

        final_score = self.game.score if self.game else 0
        final_level = self.game.level if self.game else 1

        if not save_score:
            final_score = 0

        if save_score and final_score > 0:
            try:
                supabase.table("scores").insert({
                    "user_id": self.user.id,
                    "score": final_score,
                    "level": final_level
                }).execute()
            except Exception as ex:
                print(f"Error saving score: {ex}")

        def menu_click(e):
            self.show_menu()

        self.page.add(
            ft.Column(
                [
                    ft.Text("JUEGO TERMINADO", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.RED),
                    ft.Container(height=20),
                    ft.Text(f"Puntuación Final: {final_score}", size=30),
                    ft.Text(f"Nivel Alcanzado: {final_level}", size=24),
                    ft.Container(height=40),
                    ft.ElevatedButton("Volver al Menú", on_click=menu_click, width=300, height=60),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        
def main(page: ft.Page):
    TetrisApp(page)

ft.app(
    target=main,
    view=ft.AppView.WEB_BROWSER,
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 8080)),
)

if __name__ == "__main__":
    ft.app(target=main)
