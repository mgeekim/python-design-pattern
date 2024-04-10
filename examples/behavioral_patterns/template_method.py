from abc import ABC, abstractmethod


class AbstractClass(ABC):
    """
    추상 클래스는 일반적으로 추상 기본 작업에 대한 호출로 구성된 알고리즘의 뼈대를 정의하는 템플릿 메서드를 정의합니다.

    구체적인 하위 클래스는 이러한 작업을 구현해야 하지만 템플릿 메서드 자체는 그대로 둬야 합니다.
    """

    def template_method(self) -> None:
        """
        템플릿 메서드는 알고리즘의 뼈대를 정의합니다.
        """

        self.base_operation1()
        self.required_operations1()
        self.base_operation2()
        self.hook1()
        self.required_operations2()
        self.base_operation3()
        self.hook2()

    # 이러한 작업에는 이미 구현이 있습니다.

    def base_operation1(self) -> None:
        print("AbstractClass가 말합니다: 작업의 대부분을 수행 중입니다")

    def base_operation2(self) -> None:
        print("AbstractClass가 말합니다: 하지만 몇몇 작업을 하위 클래스에게 위임합니다")

    def base_operation3(self) -> None:
        print("AbstractClass가 말합니다: 하지만 작업의 대부분을 수행 중입니다")

    # 이러한 작업은 하위 클래스에서 구현되어야 합니다.

    @abstractmethod
    def required_operations1(self) -> None:
        pass

    @abstractmethod
    def required_operations2(self) -> None:
        pass

    # 이것들은 "훅"입니다. 하위 클래스가 오버라이드 할 수 있지만, 필수는 아닙니다.
    # 훅은 알고리즘의 중요한 위치에서 추가 확장 포인트를 제공합니다.

    def hook1(self) -> None:
        pass

    def hook2(self) -> None:
        pass


class ConcreteClass1(AbstractClass):
    """
    구체 클래스는 기본 클래스의 모든 추상 작업을 구현해야 합니다. 또한 몇몇 작업을 기본 구현으로 오버라이드 할 수 있습니다.
    """

    def required_operations1(self) -> None:
        print("ConcreteClass1이 말합니다: 작업1을 구현했습니다")

    def required_operations2(self) -> None:
        print("ConcreteClass1이 말합니다: 작업2를 구현했습니다")


class ConcreteClass2(AbstractClass):
    """
    일반적으로 구체 클래스는 기본 클래스의 작업 중 일부만 오버라이드합니다.
    """

    def required_operations1(self) -> None:
        print("ConcreteClass2가 말합니다: 작업1을 구현했습니다")

    def required_operations2(self) -> None:
        print("ConcreteClass2가 말합니다: 작업2를 구현했습니다")

    def hook1(self) -> None:
        print("ConcreteClass2가 말합니다: 훅1을 오버라이드했습니다")


def client_code(abstract_class: AbstractClass) -> None:
    """
    클라이언트 코드는 템플릿 메서드를 호출하여 알고리즘을 실행합니다. 클라이언트 코드는 작업을 수행하는 객체의 구체적인 클래스를 알 필요가 없습니다.
    대신, 그들의 기본 클래스를 통해 객체와 작업합니다.
    """

    # ...
    abstract_class.template_method()
    # ...


if __name__ == "__main__":
    print("동일한 클라이언트 코드는 다른 하위 클래스와 함께 작동할 수 있습니다:")
    client_code(ConcreteClass1())
    print("")

    print("동일한 클라이언트 코드는 다른 하위 클래스와 함께 작동할 수 있습니다:")
    client_code(ConcreteClass2())
