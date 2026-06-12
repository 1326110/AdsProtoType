from handlers.user import user_router
from handlers.admin import admin_router
from handlers.group import group_router
from handlers.errors import error_router


def register_all_routers(dp):
    dp.include_routers(
        user_router,
        admin_router,
        group_router,
        error_router,
    )
