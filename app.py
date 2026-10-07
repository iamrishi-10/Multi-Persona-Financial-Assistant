from src.ui.interface import build_app

if __name__ == "__main__":
    app = build_app()
    app.launch(js="() => { document.documentElement.classList.toggle('dark') }")
