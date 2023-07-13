from sqlmodel import Session, select

from .models import Message, MessageCreate, MessageUpdate


def create_message(session: Session, message: MessageCreate):
    db_message = Message.from_orm(message)
    session.add(db_message)
    session.commit()
    session.refresh(db_message)
    return db_message


def read_messages(session: Session):
    return session.exec(select(Message)).all()


def read_message(session: Session, id: int):
    return session.get(Message, id)


def update_message(session: Session, id: int, update: MessageUpdate):
    message = read_message(session=session, id=id)
    if message is None:
        return None
    update_data = update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(message, key, value)
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


def delete_message(session: Session, id: int):
    message = read_message(session=session, id=id)
    if message is None:
        return None
    session.delete(message)
    session.commit()
    return message
