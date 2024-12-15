from litestar import Litestar, get


@get("/")
async def index() -> str:
    return "test"


app = Litestar([index])
