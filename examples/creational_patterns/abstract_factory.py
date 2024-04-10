from __future__ import annotations

from abc import ABC, abstractmethod


class AbstractFactory(ABC):
    """
    Abstract Factory 인터페이스는 서로 다른 추상 제품을 반환하는 일련의 메서드를 선언합니다.
    이러한 제품들은 하나의 패밀리를 형성하며, 일반적으로 서로 협력할 수 있습니다.
    제품 패밀리는 여러 가지 변형을 가질 수 있지만, 한 변형의 제품들은 다른 변형의 제품들과 호환되지 않습니다.
    """

    @abstractmethod
    def create_product_a(self) -> AbstractProductA:
        pass

    @abstractmethod
    def create_product_b(self) -> AbstractProductB:
        pass


class ConcreteFactory1(AbstractFactory):
    """
    Concrete Factory는 단일 변형에 속하는 제품 패밀리를 생성합니다.
    공장은 결과 제품이 호환되도록 보장합니다.
    Concrete Factory의 메서드 서명은 추상 제품을 반환하지만, 메서드 내에서는 구체적인 제품이 인스턴스화됩니다.
    """

    def create_product_a(self) -> AbstractProductA:
        return ConcreteProductA1()

    def create_product_b(self) -> AbstractProductB:
        return ConcreteProductB1()


class ConcreteFactory2(AbstractFactory):
    """
    각 Concrete Factory에는 해당 제품 변형이 있습니다.
    """

    def create_product_a(self) -> AbstractProductA:
        return ConcreteProductA2()

    def create_product_b(self) -> AbstractProductB:
        return ConcreteProductB2()


class AbstractProductA(ABC):
    """
    제품 패밀리의 각 고유한 제품은 기본 인터페이스를 가져야 합니다.
    모든 제품의 변형은 이 인터페이스를 구현해야 합니다.
    """

    @abstractmethod
    def useful_function_a(self) -> str:
        pass


class ConcreteProductA1(AbstractProductA):
    def useful_function_a(self) -> str:
        return "Product A1의 결과입니다."


class ConcreteProductA2(AbstractProductA):
    def useful_function_a(self) -> str:
        return "Product A2의 결과입니다."


class AbstractProductB(ABC):
    """
    여기에 다른 제품의 기본 인터페이스가 있습니다.
    모든 제품은 서로 상호 작용할 수 있지만, 올바른 상호 작용은 동일한 구체적 변형의 제품 간에만 가능합니다.
    """

    @abstractmethod
    def useful_function_b(self) -> None:
        pass

    @abstractmethod
    def another_useful_function_b(self, collaborator: AbstractProductA) -> None:
        pass


class ConcreteProductB1(AbstractProductB):
    def useful_function_b(self) -> str:
        return "Product B1의 결과입니다."

    def another_useful_function_b(self, collaborator: AbstractProductA) -> str:
        result = collaborator.useful_function_a()
        return f"B1가 A1과 상호 작용하고 있습니다: {result}"


class ConcreteProductB2(AbstractProductB):
    def useful_function_b(self) -> str:
        return "Product B2의 결과입니다."

    def another_useful_function_b(self, collaborator: AbstractProductA) -> str:
        result = collaborator.useful_function_a()
        return f"B2가 A2와 상호 작용하고 있습니다: {result}"


def client_code(factory: AbstractFactory) -> None:
    """
    클라이언트 코드는 추상 유형인 AbstractFactory 및 AbstractProduct를 통해서만 팩토리와 제품과 상호 작용합니다.
    이를 통해 클라이언트 코드에 어떤 팩토리나 제품 하위 클래스를 전달해도 문제가 없습니다.
    """
    product_a = factory.create_product_a()
    product_b = factory.create_product_b()

    print(f"{product_b.useful_function_b()}")
    print(f"{product_b.another_useful_function_b(product_a)}", end="")


if __name__ == "__main__":
    """
    클라이언트 코드는 모든 구체적 팩토리 클래스와 함께 작동할 수 있습니다.
    """
    print("첫 번째 팩토리 타입과 함께 클라이언트 코드를 테스트 중:")
    client_code(ConcreteFactory1())

    print("\n")

    print("두 번째 팩토리 타입과 함께 동일한 클라이언트 코드를 테스트 중:")
    client_code(ConcreteFactory2())
