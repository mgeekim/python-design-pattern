from __future__ import annotations

from abc import ABC, abstractmethod


class Creator(ABC):
    """
    Creator 클래스는 Product 클래스의 객체를 반환하는 팩토리 메서드를 선언합니다.
    Creator의 하위 클래스들은 보통 이 메서드의 구현을 제공합니다.
    """

    @abstractmethod
    def factory_method(self):
        """
        Creator는 팩토리 메서드의 기본 구현을 제공할 수도 있습니다.
        """
        pass

    def some_operation(self) -> str:
        """
        또한, 이름에도 불구하고 Creator의 주요 책임은 제품을 생성하는 것이 아닙니다.
        보통은 팩토리 메서드에 의해 반환된 Product 객체에 의존하는 핵심 비즈니스 로직을 포함합니다.
        서브클래스는 팩토리 메서드를 재정의하고 이를 통해 다른 유형의 제품을 반환함으로써 이 비즈니스 로직을 간접적으로 변경할 수 있습니다.
        """

        # 팩토리 메서드를 호출하여 Product 객체를 생성합니다.
        product = self.factory_method()

        # 이제 제품을 사용합니다.
        result = f"Creator: 동일한 생성자 코드가 방금 {product.operation()}을 사용했습니다."

        return result


"""
구체적인 Creator들은 결과적으로 생성되는 제품의 유형을 변경하기 위해 팩토리 메서드를 재정의합니다.
"""


class ConcreteCreator1(Creator):
    """
    실제로 구체적인 제품이 반환되는 메서드이지만 여전히 추상 제품 유형을 사용하는 것에 유의합니다.
    이렇게 함으로써 Creator는 구체적인 제품 클래스와 독립적으로 유지될 수 있습니다.
    """

    def factory_method(self) -> Product:
        return ConcreteProduct1()


class ConcreteCreator2(Creator):
    def factory_method(self) -> Product:
        return ConcreteProduct2()


class Product(ABC):
    """
    Product 인터페이스는 모든 구체적인 제품이 구현해야 할 작업을 선언합니다.
    """

    @abstractmethod
    def operation(self) -> str:
        pass


"""
구체적인 제품은 Product 인터페이스의 여러 구현을 제공합니다.
"""


class ConcreteProduct1(Product):
    def operation(self) -> str:
        return "{ConcreteProduct1의 결과}"


class ConcreteProduct2(Product):
    def operation(self) -> str:
        return "{ConcreteProduct2의 결과}"


def client_code(creator: Creator) -> None:
    """
    클라이언트 코드는 구체적인 생성자의 인스턴스와 함께 작동하지만 그 인터페이스를 통해입니다.
    클라이언트가 생성자를 기본 인터페이스를 통해 계속 사용하는 한, 어떤 생성자의 하위 클래스든 전달할 수 있습니다.
    """

    print(f"Client: 생성자의 클래스를 알지 못하지만 작동합니다.\n"
          f"{creator.some_operation()}", end="")


if __name__ == "__main__":
    print("앱: ConcreteCreator1으로 실행됨.")
    client_code(ConcreteCreator1())
    print("\n")

    print("앱: ConcreteCreator2으로 실행됨.")
    client_code(ConcreteCreator2())
