"""Firebase Functions entry point for the Flask application."""

from firebase_functions import https_fn

from app import create_app


app = create_app()


@https_fn.on_request()
def jigsaw_functions(req: https_fn.Request) -> https_fn.Response:
    with app.request_context(req.environ):
        return app.full_dispatch_request()
