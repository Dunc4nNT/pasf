import uuid
from collections.abc import Sequence
from typing import Annotated

from asyncpg import Connection, Record
from litestar import Controller, MediaType, Request, Response, delete, get, patch, post
from litestar.params import Parameter

from app.domain.cards import urls
from app.domain.cards.schemas import Card, CardCreate, CardUpdate


class CardController(Controller):
    """Controller for cards."""

    tags: Sequence[str] | None = ["Cards"]

    @get(operation_id="GetCard", path=urls.CARD_GET)
    async def get_card(
        self,
        request: Request,
        db_connection: Connection,
        card_id: Annotated[
            uuid.UUID, Parameter(title="Card ID", description="ID of the card to get.")
        ],
    ) -> Response[Card | str]:
        """Retrieve a card.

        Parameters
        ----------
        card_id : UUID
            ID of the card.

        Returns
        -------
        Response[Card | str]
            The card if found, else error.
        """
        selection: list[Record] = await db_connection.fetch(
            """
            SELECT id, name, front_content, back_content
            FROM cards
            WHERE id = $1;
            """,
            card_id,
        )
        # If the card we're trying to get doesn't exist, we error.
        if len(selection) == 0:
            return Response(
                "Card with id does not exist.",
                status_code=400,
                media_type=MediaType.JSON,
            )

        card: Record = selection[0]

        return Response(
            Card(id=card[0], name=card[1], front_content=card[2], back_content=card[3]),
            status_code=200,
            media_type=MediaType.JSON,
        )

    @get(operation_id="ListCards", path=urls.CARD_LIST)
    async def list_cards(
        self, request: Request, db_connection: Connection
    ) -> Response[list[Card]]:
        """Retrieve all the cards.

        Returns
        -------
        list[Card]
            List with all the cards.
        """
        selection: list[Record] = await db_connection.fetch(
            """
            SELECT id, name, front_content, back_content
            FROM cards;
            """
        )

        if len(selection) == 0:
            cards: list[Card] = []
        else:
            cards: list[Card] = [
                Card(id=card[0], name=card[1], front_content=card[2], back_content=card[3])
                for card in selection
            ]

        return Response(cards, status_code=200, media_type=MediaType.JSON)

    @post(operation_id="CreateCard", path=urls.CARD_CREATE)
    async def create_card(
        self, request: Request, db_connection: Connection, data: CardCreate
    ) -> Response[Card]:
        """Create a card.

        Parameters
        ----------
        data : CardCreate
            Json with card data.

        Returns
        -------
        Response[Card]
            The created card.
        """
        selection: list[Record] = await db_connection.fetch(
            """
            INSERT INTO cards
            VALUES ($1, $2, $3, $4)
            ON CONFLICT DO NOTHING
            RETURNING id, name, front_content, back_content;
            """,
            uuid.uuid4(),
            data.name,
            data.front_content,
            data.back_content,
        )

        card = selection[0]

        return Response(
            Card(id=card[0], name=card[1], front_content=card[2], back_content=card[3]),
            status_code=200,
            media_type=MediaType.JSON,
        )

    @patch(operation_id="UpdateCard", path=urls.CARD_UPDATE)
    async def update_card(
        self,
        request: Request,
        db_connection: Connection,
        data: CardUpdate,
        card_id: Annotated[
            uuid.UUID, Parameter(title="Card ID", description="ID of the card to update.")
        ],
    ) -> Response[Card | str]:
        """Update a card.

        Updatable data:
            name
            front_content
            back_content

        Parameters
        ----------
        data : CardUpdate
            Json with card update data.
        card_id : UUID
            ID of the card.

        Returns
        -------
        Response[Card | str]
            The updated card if succeeded, else error.
        """
        original_selection: list[Record] = await db_connection.fetch(
            """
            SELECT name, front_content, back_content
            FROM cards
            WHERE id = $1;
            """,
            card_id,
        )

        # If the card we're trying to update doesn't exist, we error.
        if len(original_selection) == 0:
            return Response(
                "Card with id does not exist.",
                status_code=400,
                media_type=MediaType.JSON,
            )

        original_card_selection: Record = original_selection[0]

        original_card: Card = Card(
            id=card_id,
            name=original_card_selection[0],
            front_content=original_card_selection[1],
            back_content=original_card_selection[2],
        )

        selection: list[Record] = await db_connection.fetch(
            """
            UPDATE cards
            SET name = $2, front_content = $3, back_content = $4
            WHERE id = $1
            RETURNING id, name, front_content, back_content;
            """,
            card_id,
            data.name if data.name is not None else original_card.name,
            data.front_content if data.front_content is not None else original_card.front_content,
            data.back_content if data.back_content is not None else original_card.back_content,
        )

        card_selection: Record = selection[0]

        return Response(
            Card(
                id=card_selection[0],
                name=card_selection[1],
                front_content=card_selection[2],
                back_content=card_selection[3],
            ),
            status_code=200,
            media_type=MediaType.JSON,
        )

    @delete(operation_id="DeleteCard", path=urls.CARD_DELETE)
    async def delete_card(
        self,
        request: Request,
        db_connection: Connection,
        card_id: Annotated[
            uuid.UUID, Parameter(title="Card ID", description="ID of the card to delete.")
        ],
    ) -> Response[None]:
        """Delete  a card.

        Parameters
        ----------
        card_id : UUID
            ID of the card.

        Returns
        -------
        Response[None]
            A success code.
        """
        await db_connection.execute(
            """
            DELETE FROM cards
            WHERE id = $1;
            """,
            card_id,
        )

        return Response(
            None,
            status_code=200,
            media_type=MediaType.JSON,
        )
