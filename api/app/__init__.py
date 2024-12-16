from litestar import Litestar, MediaType, Response, get


@get("/")
async def index() -> str:
    return "test"


@get("/health-check", media_type=MediaType.TEXT)
async def health_check() -> Response[str]:
    return Response(content="definitely healthy", status_code=200)


app = Litestar([index, health_check])
