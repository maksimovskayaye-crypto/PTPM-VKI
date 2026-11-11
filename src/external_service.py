from abc import ABC, abstractmethod


class IExternalService(ABC):

    @abstractmethod
    def send_result(self, result: str) -> bool:
        pass


class EmailService(IExternalService):

    def send_result(self, result: str) -> bool:
        print(f"[EMAIL] Отправка результата: {result}")
        return True