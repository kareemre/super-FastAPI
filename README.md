# Routing 

In routes directory you will find a module named `routes_registry.py` that can be used for registering application routes.

`__init__.py` : We Register our application routes in `__all__` variable list.

Example: 

```python
from . import (
    orders,
    products,
    users,
)

__all__ = [
    "users",
    "orders",
]
```

`register_routes`: After setting application routes `register_routes` function must be called in the application request entry

```python
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
```


# Dependencies 

Here in this package resides all our application dependencies.

# Response 

Instead of relying on FastAPI response Scheme, in `routers/api_response/custom_api_response.py` custom response functionalities are defined 
adhering to FastAPI and Pydantic Json Serialization, filtering and validation rules.


# Database
The default database is PostgreSQL, with asyncpg to utilize the async feature of sqlalchemy,
And in .env file you can set your database credentials and use it in configs/database.py module. This module handles database/connection.py to  yielding a asyncsession (Assuming application used ORM is SqlAlchemy; as sqlmodels still does not have the clear functionality utilizing the async behaviour of sqlalchemy).


# Models 

This structure relies on sqlalchemy ORM. All models are defined in `models` package. Please note that every new defined model should be registered in `models/__init__.py` file in `__all__` variable list. This is necessary for creating DB tables in database/connection.py

# Repositories 

This Paragraph is from Martin Fowler's famous Book "Patterns of Enterprise Application Architecture":
> A system with a complex domain model often benefits from a layer, such as the one provided by Data Mapper, that isolates domain objects from details of the database access code. In such systems it can be worthwhile to build another layer of abstraction over the mapping layer where query construction code is concentrated. This becomes more important when there are a large number of domain classes or heavy querying. In these cases particularly, adding this layer helps minimize duplicate query logic.


# Request Life Cycle

The main entry point is app/main.py,  
Please run: 
```bash
fastapi dev app/main.py
```
            


## TODO 
- Implementing Repository pattern with strategy design pattern for database operations.

