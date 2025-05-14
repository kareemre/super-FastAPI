from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import FastAPI  

def register_routes(app: "FastAPI", prefix: str | None = None) -> None:
    """
    Register all API routes with the FastAPI application.
   
    Args:
        app (FastAPI): The FastAPI application instance.
        prefix (str | None, optional): Optional prefix for all routes. Defaults to None.
    """
    from app.routers import __all__
    import importlib
    
    for module_name in __all__:
        try:
            module = importlib.import_module(f"app.routers.{module_name}")
        
            if hasattr(module, "router"):
                if prefix:
                    app.include_router(module.router, prefix=prefix)
                else:
                    app.include_router(module.router)
        except ImportError as e:
            print(f"Error importing module {module_name}: {e}")
                