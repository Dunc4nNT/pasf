import uuid
from collections.abc import Sequence
from typing import Annotated

from asyncpg import Connection, Record
from litestar import Controller, MediaType, Request, Response, delete, get, patch, post
from litestar.params import Parameter

from app.domain.cards import urls
from app.domain.cards.schemas import Deck, DeckCreate, DeckUpdate
from app.errors import DeckNotFoundError


class DeckController(Controller):
    """Controller for decks."""

    tags: Sequence[str] | None = ["Decks"]

    async def _get_deck_by_name(self, db_connection: Connection, name: str) -> Deck:
        """Get a deck from its name.

        Parameters
        ----------
        db_connection : Connection
            Asyncpg database connection.
        name : str
            Name of the deck.

        Returns
        -------
        Deck
            The deck.

        Raises
        ------
        DeckNotFoundError
            If deck with name does not exist.
        """
        selection: list[Record] = await db_connection.fetch(
            """
            SELECT id, name
            FROM decks
            WHERE name = $1;
            """,
            name,
        )

        if len(selection) == 0:
            msg = "Deck with name does not exist."
            raise DeckNotFoundError(msg)

        deck = selection[0]

        return Deck(id=deck[0], name=deck[1])

    @get(operation_id="GetDeck", path=urls.DECK_GET)
    async def get_deck(
        self,
        request: Request,
        db_connection: Connection,
        deck_id: Annotated[
            uuid.UUID, Parameter(title="Deck ID", description="ID of the deck to get.")
        ],
    ) -> Response[Deck | str]:
        """Retrieve a deck.

        Parameters
        ----------
        deck_id : UUID
            ID of the deck.

        Returns
        -------
        Response[Deck | str]
            The deck if found, else error.
        """
        selection: list[Record] = await db_connection.fetch(
            """
            SELECT id, name
            FROM decks
            WHERE id = $1;
            """,
            deck_id,
        )
        # If the deck we're trying to get doesn't exist, we error.
        if len(selection) == 0:
            return Response(
                "Deck with id does not exist.",
                status_code=400,
                media_type=MediaType.JSON,
            )

        deck: Record = selection[0]

        return Response(
            Deck(id=deck[0], name=deck[1]),
            status_code=200,
            media_type=MediaType.JSON,
        )

    @get(operation_id="ListDecks", path=urls.DECK_LIST)
    async def list_decks(
        self, request: Request, db_connection: Connection
    ) -> Response[list[Deck]]:
        """Retrieve all the decks.

        Returns
        -------
        list[Deck]
            List with all the decks.
        """
        selection: list[Record] = await db_connection.fetch(
            """
            SELECT id, name
            FROM decks;
            """
        )

        if len(selection) == 0:
            decks: list[Deck] = []
        else:
            decks: list[Deck] = [Deck(id=deck[0], name=deck[1]) for deck in selection]

        return Response(decks, status_code=200, media_type=MediaType.JSON)

    @post(operation_id="CreateDeck", path=urls.DECK_CREATE)
    async def create_deck(
        self, request: Request, db_connection: Connection, data: DeckCreate
    ) -> Response[Deck | str]:
        """Create a deck.

        Parameters
        ----------
        data : DeckCreate
            Json with deck data.

        Returns
        -------
        Response[Deck | str]
            The created deck if succeeded, else error.
        """
        selection: list[Record] = await db_connection.fetch(
            """
            INSERT INTO decks
            VALUES ($1, $2)
            ON CONFLICT DO NOTHING
            RETURNING id, name;
            """,
            uuid.uuid4(),
            data.name,
        )

        # If a deck with this name already exists, we error.
        if len(selection) == 0:
            return Response(
                "Deck with name already exists.",
                status_code=400,
                media_type=MediaType.JSON,
            )

        deck: Record = selection[0]

        return Response(
            Deck(id=deck[0], name=deck[1]),
            status_code=200,
            media_type=MediaType.JSON,
        )

    @patch(operation_id="UpdateDeck", path=urls.DECK_UPDATE)
    async def update_deck(
        self,
        request: Request,
        db_connection: Connection,
        data: DeckUpdate,
        deck_id: Annotated[
            uuid.UUID, Parameter(title="Deck ID", description="ID of the deck to update.")
        ],
    ) -> Response[Deck | str]:
        """Update a deck.

        Updatable data:
            name

        Parameters
        ----------
        data : DeckUpdate
            Json with deck update data.
        deck_id : UUID
            ID of the deck.

        Returns
        -------
        Response[Deck | str]
            The updated deck if succeeded, else error.
        """
        # If a deck with the new name already exists, we error.
        try:
            await self._get_deck_by_name(db_connection, data.name)
        except DeckNotFoundError:
            pass
        else:
            return Response(
                "Deck with this name already exists, the name must be unique.",
                status_code=400,
                media_type=MediaType.JSON,
            )

        selection: list[Record] = await db_connection.fetch(
            """
            UPDATE decks
            SET name = $2
            WHERE id = $1
            RETURNING id, name;
            """,
            deck_id,
            data.name,
        )

        # If the deck we're trying to update doesn't exist, we also error.
        if len(selection) == 0:
            return Response(
                "Deck with id does not exist.",
                status_code=400,
                media_type=MediaType.JSON,
            )

        deck = selection[0]

        return Response(
            Deck(id=deck[0], name=deck[1]),
            status_code=200,
            media_type=MediaType.JSON,
        )

    @delete(operation_id="DeleteDeck", path=urls.DECK_DELETE)
    async def delete_deck(
        self,
        request: Request,
        db_connection: Connection,
        deck_id: Annotated[
            uuid.UUID, Parameter(title="Deck ID", description="ID of the deck to delete.")
        ],
    ) -> Response[None]:
        """Delete  a deck.

        Parameters
        ----------
        deck_id : UUID
            ID of the deck.

        Returns
        -------
        Response[None]
            A success code.
        """
        await db_connection.execute(
            """
            DELETE FROM decks
            WHERE id = $1;
            """,
            deck_id,
        )

        return Response(
            None,
            status_code=200,
            media_type=MediaType.JSON,
        )
