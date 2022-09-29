from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return password_context.hash(password)

def verify(hashed_password, simple_password):
    return password_context.verify(simple_password, hashed_password)