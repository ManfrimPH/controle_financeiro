class BotError(Exception):
    """Base for all bot errors. Safe to show user_message to users."""
    user_message: str = "Erro inesperado. Tente novamente."

    def __init__(self, message: str = "", user_message: str = ""):
        super().__init__(message or user_message or self.user_message)
        if user_message:
            self.user_message = user_message


class DatabaseConnectionError(BotError):
    user_message = "Erro de conexão com o banco. Tente novamente mais tarde."


class DatabaseIntegrityError(BotError):
    user_message = "Dados inválidos. Verifique os valores e tente novamente."


class ValidationError(BotError):
    user_message = "Formato inválido. Verifique os dados informados."


class ConversationTimeoutError(BotError):
    user_message = "Tempo limite excedido. Comece novamente com /add ou /del."


class EntryNotFoundError(BotError):
    user_message = "Registro não encontrado."
