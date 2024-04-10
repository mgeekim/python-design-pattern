from __future__ import annotations

from abc import ABC, abstractmethod


class Abstraction:
    """
    Abstraction은 두 클래스 계층의 "제어(control)" 부분의 인터페이스를 정의합니다.
    이는 Implementation 계층의 객체에 대한 참조를 유지하고, 모든 실제 작업을 이 객체에 위임합니다.
    """

    def __init__(self, implementation: Implementation) -> None:
        self.implementation = implementation

    def operation(self) -> str:
        return (f"Abstraction: 기본 작업:\n"
                f"{self.implementation.operation_implementation()}")


class ExtendedAbstraction(Abstraction):
    """
    Abstraction을 변경하지 않고 확장할 수 있습니다.
    """

    def operation(self) -> str:
        return (f"ExtendedAbstraction: 확장된 작업:\n"
                f"{self.implementation.operation_implementation()}")


class Implementation(ABC):
    """
    Implementation은 모든 구현 클래스에 대한 인터페이스를 정의합니다.
    이는 Abstraction의 인터페이스와 일치할 필요가 없습니다. 사실, 두 인터페이스는 완전히 다를 수 있습니다.
    일반적으로 Implementation 인터페이스는 기본 작업만을 제공하며, Abstraction은 이러한 기본 작업을 기반으로 더 높은 수준의 작업을 정의합니다.
    """

    @abstractmethod
    def operation_implementation(self) -> str:
        pass


"""
각 구체적인 Implementation은 특정 플랫폼에 해당하며, 해당 플랫폼의 API를 사용하여 Implementation 인터페이스를 구현합니다.
"""


class ConcreteImplementationA(Implementation):
    def operation_implementation(self) -> str:
        return "ConcreteImplementationA: 플랫폼 A에서의 결과입니다."


class ConcreteImplementationB(Implementation):
    def operation_implementation(self) -> str:
        return "ConcreteImplementationB: 플랫폼 B에서의 결과입니다."


def client_code(abstraction: Abstraction) -> None:
    """
    초기화 단계를 제외하고는, Abstraction 객체가 특정 Implementation 객체와 연결될 때,
    클라이언트 코드는 오직 Abstraction 클래스에 의존해야 합니다.
    이런 방식으로, 클라이언트 코드는 어떤 추상화-구현 조합이든지 지원할 수 있습니다.
    """

    # ...

    print(abstraction.operation(), end="")

    # ...


if __name__ == "__main__":
    """
    클라이언트 코드는 어떤 사전 구성된 추상화-구현 조합이든지 작동해야 합니다.
    """

    implementation = ConcreteImplementationA()
    abstraction = Abstraction(implementation)
    client_code(abstraction)

    print("\n")

    implementation = ConcreteImplementationB()
    abstraction = ExtendedAbstraction(implementation)
    client_code(abstraction)
