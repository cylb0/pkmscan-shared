from ..domain import CardIdentity

def get_s3_img_key(
    card: CardIdentity,
    folder: str,
    extension: str = "png",
) -> str:
    return f"{folder}/{card.expansion}/{card.lang.value}/{card.id}.{extension}"
