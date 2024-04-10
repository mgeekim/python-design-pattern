from threading import Lock, Thread


class SingletonMeta(type):
    """
    이것은 스레드 안전한 Singleton의 구현입니다.
    """

    _instances = {}

    _lock: Lock = Lock()
    """
    이제 싱글톤에 대한 첫 번째 액세스 동안 스레드를 동기화하는 데 사용될 잠금 객체가 있습니다.
    """

    def __call__(cls, *args, **kwargs):
        """
        `__init__` 인수 값의 변경 사항이 반환된 인스턴스에 영향을 미치지 않습니다.
        """
        # 이제 프로그램이 실행된 직후라고 가정해 봅시다. 아직 Singleton 인스턴스가 없으므로
        # 여러 스레드가 이전 조건문을 거치고 거의 동시에 이 지점에 도달할 수 있습니다.
        # 잠금을 획득한 첫 번째 스레드는 여기서 진행하고 나머지는 여기에서 기다릴 것입니다.
        with cls._lock:
            # 잠금을 획득한 첫 번째 스레드는 이 조건에 도달하여 안으로 들어가고 Singleton 인스턴스를 생성합니다.
            # 잠금 블록을 빠져 나온 후 잠금 해제를 기다리던 스레드가 이 섹션으로 들어갈 수 있습니다.
            # 그러나 싱글톤 필드가 이미 초기화되었으므로 스레드는 새 객체를 생성하지 않습니다.
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    value: str = None
    """
    우리는 싱글톤이 실제로 작동하는지 증명하기 위해 이 속성을 사용할 것입니다.
    """

    def __init__(self, value: str) -> None:
        self.value = value

    def some_business_logic(self):
        """
        마지막으로, 모든 싱글톤은 해당 인스턴스에서 실행할 수 있는 비즈니스 로직을 정의해야 합니다.
        """


def test_singleton(value: str) -> None:
    singleton = Singleton(value)
    print(singleton.value)


if __name__ == "__main__":
    # 클라이언트 코드.

    print("동일한 값이 표시되면 싱글톤이 재사용되었습니다 (만세!)\n"
          "다른 값이 표시되면 2개의 싱글톤이 생성되었습니다 (윽!)\n\n"
          "결과:\n")

    process1 = Thread(target=test_singleton, args=("FOO",))
    process2 = Thread(target=test_singleton, args=("BAR",))
    process1.start()
    process2.start()
