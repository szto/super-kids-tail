from pathlib import Path

from litestar import Litestar, get, post
from litestar.contrib.htmx.request import HTMXRequest
from litestar.contrib.htmx.response import HTMXTemplate
from litestar.template.config import TemplateConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.response import Template


@get("/")
async def index() -> Template:
    return Template(template_name="index.html", context={"name": "The Code is Good!"})


@get("/books/{book_id:int}")
async def get_book(book_id: int) -> dict[str, int]:
    return {"book_id": book_id}

@post("/submit")
async def submit(request: HTMXRequest) -> HTMXTemplate:
    print(request.htmx.current_url)
    return HTMXTemplate(template_name="partials/response.html", context={"name": "Effected"}, push_url="/")


template_config = TemplateConfig(
        directory=Path(__file__).parent / "templates",
        engine=JinjaTemplateEngine,
    )


app = Litestar(
    route_handlers=[index, get_book, submit],
    request_class=HTMXRequest,
    template_config=template_config,
    debug=True,
)