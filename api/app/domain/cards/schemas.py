from uuid import UUID

from pydantic import BaseModel


class Deck(BaseModel):
    """Represents a deck."""

    id: UUID
    name: str


class DeckCreate(BaseModel):
    """Data in the decks/create endpoint."""

    name: str


class DeckUpdate(BaseModel):
    """Data in the decks/update endpoint."""

    name: str


class Card(BaseModel):
    """Represents a card."""

    id: UUID
    name: str
    front_content: str
    back_content: str


class CardCreate(BaseModel):
    """Data in the cards/create endpoint."""

    name: str | None = None
    front_content: str | None = None
    back_content: str | None = None


class CardUpdate(BaseModel):
    """Data in the cards/update endpoint."""

    name: str | None = None
    front_content: str | None = None
    back_content: str | None = None


class Tag(BaseModel):
    """Represents a tag."""

    id: UUID
    name: str


class TagCreate(BaseModel):
    """Data in the tags/create endpoint."""

    name: str


class TagUpdate(BaseModel):
    """Data in the tags/update endpoint."""

    name: str
