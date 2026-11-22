VALID_STATUSES = {"pending", "resolved"}


class Customer:
    """Représente un client et sa demande de support."""

    def __init__(
        self,
        id: int,
        name: str,
        email: str,
        message: str,
        status: str = "pending",
    ) -> None:
        """Initialise un objet Customer en validant ses attributs."""
        if not name or not name.strip():
            raise ValueError("Le nom du client ne peut pas être vide.")
        if not email or "@" not in email:
            raise ValueError(f"Adresse email invalide : {email}")
        if status not in VALID_STATUSES:
            raise ValueError(f"Statut invalide : {status}")

        self.id = id
        self.name = name.strip()
        self.email = email.strip()
        self.message = message
        self.status = status

    def to_dict(self) -> dict[str, int | str]:
        """Convertit l'instance Customer en dictionnaire sérialisable."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "message": self.message,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict[str, int | str]) -> "Customer":
        """Reconstruit une instance Customer à partir d'un dictionnaire."""
        return cls(
            id=int(data["id"]),
            name=str(data["name"]),
            email=str(data["email"]),
            message=str(data["message"]),
            status=str(data.get("status", "pending")),
        )

    def __repr__(self) -> str:
        """Retourne une représentation textuelle concise pour le débogage."""
        return f"Customer(id={self.id}, name='{self.name}', status='{self.status}')"