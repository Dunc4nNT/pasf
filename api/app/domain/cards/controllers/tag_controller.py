import uuid
from collections.abc import Sequence
from typing import Annotated

from asyncpg import Connection, Record
from litestar import Controller, MediaType, Request, Response, delete, get, patch, post
from litestar.params import Parameter

from app.domain.cards import urls
from app.domain.cards.schemas import Tag, TagCreate, TagUpdate
from app.errors import TagNotFoundError


class TagController(Controller):
    """Controller for card tags."""

    tags: Sequence[str] | None = ["Card Tags"]

    async def _get_tag_by_name(self, db_connection: Connection, name: str) -> Tag:
        """Get a tag from its name.

        Parameters
        ----------
        db_connection : Connection
            Asyncpg database connection.
        name : str
            Name of the tag.

        Returns
        -------
        Tag
            The tag.

        Raises
        ------
        TagNotFoundError
            If tag with name does not exist.
        """
        selection: list[Record] = await db_connection.fetch(
            """
            SELECT id, name
            FROM tags
            WHERE name = $1;
            """,
            name,
        )

        if len(selection) == 0:
            msg = "Tag with name does not exist."
            raise TagNotFoundError(msg)

        tag: Record = selection[0]

        return Tag(id=tag[0], name=tag[1])

    @get(operation_id="GetTag", path=urls.TAG_GET)
    async def get_tag(
        self,
        request: Request,
        db_connection: Connection,
        tag_id: Annotated[
            uuid.UUID, Parameter(title="Tag ID", description="ID of the tag to get.")
        ],
    ) -> Response[Tag | str]:
        """Retrieve a tag.

        Parameters
        ----------
        tag_id : UUID
            ID of the tag.

        Returns
        -------
        Response[Tag | str]
            The tag if found, else error.
        """
        selection: list[Record] = await db_connection.fetch(
            """
            SELECT id, name
            FROM tags
            WHERE id = $1;
            """,
            tag_id,
        )
        # If the tag we're trying to get doesn't exist, we error.
        if len(selection) == 0:
            return Response(
                "Tag with id does not exist.",
                status_code=400,
                media_type=MediaType.JSON,
            )

        tag: Record = selection[0]

        return Response(
            Tag(id=tag[0], name=tag[1]),
            status_code=200,
            media_type=MediaType.JSON,
        )

    @get(operation_id="ListTags", path=urls.TAG_LIST)
    async def list_tags(self, request: Request, db_connection: Connection) -> Response[list[Tag]]:
        """Retrieve all the tags.

        Returns
        -------
        list[Tag]
            List with all the tags.
        """
        selection: list[Record] = await db_connection.fetch(
            """
            SELECT id, name
            FROM tags;
            """
        )

        if len(selection) == 0:
            tags: list[Tag] = []
        else:
            tags: list[Tag] = [Tag(id=tag[0], name=tag[1]) for tag in selection]

        return Response(tags, status_code=200, media_type=MediaType.JSON)

    @post(operation_id="CreateTag", path=urls.TAG_CREATE)
    async def create_tag(
        self, request: Request, db_connection: Connection, data: TagCreate
    ) -> Response[Tag | str]:
        """Create a tag.

        Parameters
        ----------
        data : TagCreate
            Json with tag data.

        Returns
        -------
        Response[Tag | str]
            The created tag if succeeded, else error.
        """
        selection: list[Record] = await db_connection.fetch(
            """
            INSERT INTO tags
            VALUES ($1, $2)
            ON CONFLICT DO NOTHING
            RETURNING id, name;
            """,
            uuid.uuid4(),
            data.name,
        )
        # If a tag with this name already exists, we error.
        if len(selection) == 0:
            return Response(
                "Tag with name already exists.",
                status_code=400,
                media_type=MediaType.JSON,
            )

        tag: Record = selection[0]

        return Response(
            Tag(id=tag[0], name=tag[1]),
            status_code=200,
            media_type=MediaType.JSON,
        )

    @patch(operation_id="UpdateTag", path=urls.TAG_UPDATE)
    async def update_tag(
        self,
        request: Request,
        db_connection: Connection,
        data: TagUpdate,
        tag_id: Annotated[
            uuid.UUID, Parameter(title="Tag ID", description="ID of the tag to update.")
        ],
    ) -> Response[Tag | str]:
        """Update a tag.

        Updatable data:
            name

        Parameters
        ----------
        data : TagUpdate
            Json with tag update data.
        tag_id : UUID
            ID of the tag.

        Returns
        -------
        Response[Tag | str]
            The updated tag if succeeded, else error.
        """
        # If a tag with the new name already exists, we error.
        try:
            await self._get_tag_by_name(db_connection, data.name)
        except TagNotFoundError:
            pass
        else:
            return Response(
                "Tag with this name already exists, the name must be unique.",
                status_code=400,
                media_type=MediaType.JSON,
            )

        selection: list[Record] = await db_connection.fetch(
            """
            UPDATE tags
            SET name = $2
            WHERE id = $1
            RETURNING id, name;
            """,
            tag_id,
            data.name,
        )

        # If the tag we're trying to update doesn't exist, we also error.
        if len(selection) == 0:
            return Response(
                "Tag with id does not exist.",
                status_code=400,
                media_type=MediaType.JSON,
            )

        tag: Record = selection[0]

        return Response(
            Tag(id=tag[0], name=tag[1]),
            status_code=200,
            media_type=MediaType.JSON,
        )

    @delete(operation_id="DeleteTag", path=urls.TAG_DELETE)
    async def delete_card(
        self,
        request: Request,
        db_connection: Connection,
        tag_id: Annotated[
            uuid.UUID, Parameter(title="Tag ID", description="ID of the tag to delete.")
        ],
    ) -> Response[None]:
        """Delete  a tag.

        Parameters
        ----------
        tag_id : UUID
            ID of the tag.

        Returns
        -------
        Response[None]
            A success code.
        """
        await db_connection.execute(
            """
            DELETE FROM tags
            WHERE id = $1;
            """,
            tag_id,
        )

        return Response(
            None,
            status_code=200,
            media_type=MediaType.JSON,
        )
